from typing import Any, cast

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from typing_extensions import TypedDict, Unpack

from inspect_viz._core import Param
from inspect_viz._core.component import Component
from inspect_viz._core.data import Data
from inspect_viz._core.selection import Selection
from inspect_viz._util.channels import resolve_log_viewer_channel
from inspect_viz._util.notgiven import NOT_GIVEN, NotGiven
from inspect_viz.mark import circle, line, text
from inspect_viz.mark._title import Title
from inspect_viz.mark._types import TextOverflow, TextStyles
from inspect_viz.plot import plot
from inspect_viz.plot._attributes import PlotAttributes
from inspect_viz.plot._legend import Legend
from inspect_viz.plot._legend import legend as create_legend


class LabelStyles(TypedDict, total=False):
    """Label styling options. It's a subset of `TextStyles`."""

    line_width: float | Param
    """The line width in ems (e.g., 10 for about 20 characters); defaults to infinity, disabling wrapping and clipping. If **text_overflow** is null, lines will be wrapped at the specified length. If a line is split at a soft hyphen (\xad), a hyphen (-) will be displayed at the end of the line. If **text_overflow** is not null, lines will be clipped according to the given strategy."""
    text_overflow: TextOverflow | Param
    """Text overflow behavior."""


def scores_radar_df(
    data: pd.DataFrame,
    scorer: str,
    metrics: list[str] | None = None,
    invert: list[str] | None = None,
) -> pd.DataFrame:
    """
    Creates a dataframe for a radar chart showing multiple models.

    Args:
        data: Evals data table containing model scores. It assumes one row per model,
              if multiple task ids are present, the first row will be used.
        scorer: The name of the scorer to use for identifying metric columns.
        metrics: Optional list of specific metrics to plot. If None, all metrics
                 starting with 'score_{scorer}_' will be used.
        invert: Optional list of metrics to invert (where lower scores are better).
    """
    if metrics:
        metric_cols = [f"score_{scorer}_{metric}" for metric in metrics]
    else:
        metric_cols = [
            col for col in data.columns if col.startswith(f"score_{scorer}_")
        ]
        if not metric_cols:
            raise ValueError(
                f"No metric columns found starting with 'score_{scorer}_'."
            )
        metrics = [col.replace(f"score_{scorer}_", "") for col in metric_cols]

    required_columns = ["model", "task_id"] + metric_cols
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Required columns not found in data: {missing_columns}")

    # check for multiple rows per model and throw exception if found
    model_counts = data.groupby("model").size()
    duplicate_models = model_counts[model_counts > 1]
    if not duplicate_models.empty:
        raise ValueError(
            f"Multiple rows found for models: {duplicate_models.index.tolist()}. "
            f"Expected exactly one row per model."
        )

    columns_to_keep = required_columns
    if "log" in data.columns:
        columns_to_keep.append("log")

    data = data[columns_to_keep]

    # calculate angles for radar chart coordinates
    num_axes = len(metrics)
    angles = compute_angles(num_axes, endpoint=False)
    # close polygon angles by repeating first point
    angles_closed = np.append(angles, angles[0])

    # calculate percentile ranks for each metric across all models
    metric_percentile_ranks = {}
    for metric_name, metric_col in zip(metrics, metric_cols, strict=True):
        # handle metrics where lower is better
        if invert and metric_name in invert:
            max_val = data[metric_col].astype(float).max()
            values = max_val - data[metric_col].astype(float)
        else:
            values = data[metric_col].astype(float)

        metric_percentile_ranks[metric_name] = values.rank(method="average", pct=True)

    all_rows = []
    for i, model in enumerate(data["model"].tolist()):
        model_data = data[data["model"] == model]
        values_raw = model_data[metric_cols].values[0].astype(float).tolist()
        values_scaled = [metric_percentile_ranks[metric].iloc[i] for metric in metrics]

        # close polygon values by repeating first point
        values_scaled_closed = values_scaled + [values_scaled[0]]

        # get task_id and log for this model
        task_id_value = model_data["task_id"].item()
        log_value = model_data["log"].item() if "log" in model_data.columns else ""

        model_rows = pd.DataFrame(
            {
                "task_id": [task_id_value] * (num_axes + 1),
                "model": [model] * (num_axes + 1),
                "log": [log_value] * (num_axes + 1),
                "metric": metrics + [metrics[0]],
                "value": values_raw + [values_raw[0]],
                # polygon coordinates
                "x": np.array(values_scaled_closed) * np.cos(angles_closed),
                "y": np.array(values_scaled_closed) * np.sin(angles_closed),
            }
        )

        all_rows.append(model_rows)

    if not all_rows:
        raise ValueError("No valid model data found after processing.")

    return pd.concat(all_rows, ignore_index=True)


def compute_angles(num_axes: int, endpoint: bool = True) -> NDArray[np.floating[Any]]:
    """Computes the angles by number of axes."""
    return np.linspace(0, 2 * np.pi, num_axes, endpoint=endpoint)


def labels_coordinates(
    metrics: list[str], width: float = 400, margin: float = 0
) -> list[dict[str, Any]]:
    """Computes coordinates for labels to be used in a radar chart.

    Args:
        metrics: List of metric names for label text.
        width: Chart width in pixels, used to calculate radius.
        margin: Margin in pixels (defaults to 0) to substract from width.

    Returns:
        List of dictionaries, each containing text mark arguments for one label.
    """
    angles = compute_angles(len(metrics), endpoint=False)

    # 15px offset regardless of chart size
    chart_radius_px = (width - 2 * margin) / 2
    label_offset_px = 15

    # convert to coordinate space: boundary circle is at radius 1.0
    label_radius = 1.0 + (label_offset_px / chart_radius_px)

    labels = []
    for metric, angle in zip(metrics, angles, strict=True):
        angle_deg = np.degrees(angle) % 360

        # determine frame_anchor based on quadrant
        if 315 <= angle_deg or angle_deg < 45:  # right side
            frame_anchor = "left"
        elif 45 <= angle_deg < 135:  # top
            frame_anchor = "bottom"
        elif 135 <= angle_deg < 225:  # left side
            frame_anchor = "right"
        else:  # 225 <= angle_deg < 315, bottom
            frame_anchor = "top"

        labels.append(
            {
                "metric": [metric],
                "x": [float(label_radius * np.cos(angle))],
                "y": [float(label_radius * np.sin(angle))],
                "frame_anchor": frame_anchor,
            }
        )

    return labels


def axes_coordinates(num_axes: int) -> dict[str, list[float]]:
    """Computes coordinates for axes to be used in a radar chart."""
    angles = compute_angles(num_axes, endpoint=False)
    return {
        "x": (np.tile([0, 1], num_axes) * np.repeat(np.cos(angles), 2)).tolist(),
        "y": (np.tile([0, 1], num_axes) * np.repeat(np.sin(angles), 2)).tolist(),
    }


def grid_circles_coordinates() -> list[dict[str, list[float]]]:
    """Computes coordinates for grid circles to be used in a radar chart."""
    radii = [0.2, 0.4, 0.6, 0.8, 1.0]
    circle_angles = compute_angles(100)
    return [
        {
            "x": (radius * np.cos(circle_angles)).tolist(),
            "y": (radius * np.sin(circle_angles)).tolist(),
        }
        for radius in radii
    ]


def scores_radar(
    data: Data,
    model: str = "model_display_name",
    title: str | Title | None = None,
    width: float = 400,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    label_styles: LabelStyles | None = None,
    **attributes: Unpack[PlotAttributes],
) -> Component:
    """
    Creates a radar chart showing scores for multiple models across multiple metrics.

    Args:
        data: A `Data` object prepared using the `scores_radar_df` function.
        model: Name of field holding the model (defaults to "model_display_name").
        title: Title for plot (`str` or mark created with the `title()` function)
        width: The outer width of the plot in pixels, including margins. Defaults to 400.
               Height is automatically set to match width to maintain square aspect ratio.
        legend: Options for the legend. Pass None to disable the legend.
        label_styles: Label styling options. It accepts `line_width` and `text_overflow`.
        **attributes: Additional `PlotAttributes`.
                      Use `margin` to set custom margin (defaults to max(30, width * 0.12)).
    """
    if "model_display_name" not in data.columns:
        model = "model"

    required_columns = [model, "task_id", "log", "metric", "value", "x", "y"]
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Required columns not found in data: {missing_columns}")

    # use margin from attributes or calculate default
    margin_attr = attributes.get("margin")
    plot_margin = int(margin_attr) if margin_attr else max(60, int(width * 0.12))

    # wrap label text if any metric name is longer than 10 characters
    if not label_styles and any(
        len(metric) > 10 for metric in data.column_unique("metric")
    ):
        label_styles = LabelStyles(line_width=8)

    metrics = data.column_unique("metric")
    axes = axes_coordinates(num_axes=len(metrics))
    grid_circles = grid_circles_coordinates()
    labels = labels_coordinates(metrics=metrics, width=width, margin=plot_margin)

    model_selection = Selection.single()

    channels = {
        "Model": model,
        "Metric": "metric",
        "Score": "value",
    }
    resolve_log_viewer_channel(data, channels)

    grid_circle_color = "#e0e0e0"
    boundary_circle_color = "#999"
    axes_color = "#ddd"

    elements = [
        # grid circles (all but last (boundary))
        *[
            line(
                x=data["x"],
                y=data["y"],
                stroke=grid_circle_color,
            )
            for data in grid_circles[:-1]
        ],
        # boundary circle
        line(
            x=grid_circles[-1]["x"],
            y=grid_circles[-1]["y"],
            stroke=boundary_circle_color,
        ),
        # axes spokes
        line(
            x=axes["x"],
            y=axes["y"],
            stroke=axes_color,
        ),
        # filled polygon area
        line(
            data,
            x="x",
            y="y",
            fill=model,
            fill_opacity=0.1,
            curve="linear-closed",
            filter_by=model_selection,
        ),
        # polygon outlines
        line(
            data,
            x="x",
            y="y",
            stroke=model,
            filter_by=model_selection,
            tip=True,
            channels=channels,
        ),
        line(
            data,
            x="x",
            y="y",
            stroke=model,
            stroke_opacity=0.4,
            tip=False,
        ),
        # polygon vertex markers
        circle(
            data,
            x="x",
            y="y",
            r=4,
            fill=model,
            stroke="white",
            filter_by=model_selection,
            tip=False,
        ),
        # axis labels
        *[
            text(
                x=label["x"],
                y=label["y"],
                text=label["metric"],
                frame_anchor=label["frame_anchor"],
                styles=cast(TextStyles, label_styles) if label_styles else None,
            )
            for label in labels
        ],
    ]

    plot_legend = (
        create_legend("color", target=model_selection)
        if isinstance(legend, NotGiven)
        else legend
    )

    # resolve default attributes
    defaults: PlotAttributes = {
        "margin": plot_margin,
        "x_axis": False,
        "y_axis": False,
    }
    attributes = defaults | attributes

    return plot(
        elements,
        title=title,
        width=width,
        height=width,
        legend=plot_legend,
        **attributes,
    )
