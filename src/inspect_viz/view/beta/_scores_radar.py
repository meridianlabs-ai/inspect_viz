from typing import Any, Literal, cast

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
from inspect_viz.mark import title as title_mark
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


def scores_radar_by_task_df(
    data: pd.DataFrame,
    invert: list[str] | None = None,
    models: list[str] | None = None,
    tasks: list[str] | None = None,
    normalization: Literal["percentile", "min_max", "absolute"] = "absolute",
    domain: tuple[float, float] | None = None,
) -> pd.DataFrame:
    """
    Creates a dataframe for a radar chart showing headline metrics across multiple models and tasks.

    This is useful for comparing the headline metrics of multiple models across multiple tasks.

    Args:
        data: Evals data table containing model scores. It assumes one row per model for each task.
        invert: Optional list of metrics to invert (where lower scores are better). These should
                match the values in the "score_headline_metric" column.
        models: Optional list of models to include. If None, all models will be included. These
                should match the values in the "model" column. We expect the same set of models
                for all tasks.
        tasks: Optional list of tasks to include. If None, all tasks will be included. These
               should match the values in the "task_name" column.
        normalization: The normalization method to use for the headline metrics. Can be "percentile",
                       "min_max", or "absolute". Defaults to "absolute" (no normalization).
        domain: Optional min-max domain to use for the normalization. Only used if normalization is
                "min_max". Otherwise, the domain is inferred from the data. Defaults to None.
    """
    if models:
        data = data[data["model"].isin(models)]

    if tasks:
        data = data[data["task_name"].isin(tasks)]

    metric_cols = [
        "score_headline_name",
        "score_headline_metric",
        "score_headline_value",
    ]
    required_columns = ["model", "task_id", "task_name"] + metric_cols
    check_required_columns(data, required_columns)

    data = filter_columns(data, required_columns)

    # check for multiple rows per model and task_name and throw exception if found
    model_counts = data.groupby(["model", "task_name"]).size()
    duplicate_models = model_counts[model_counts > 1]
    if not duplicate_models.empty:
        raise ValueError(
            f"Duplicate model scores found for task: {duplicate_models.index.tolist()}. "
            "Each task should have one score per model."
        )

    # check for tasks with multiple unique score_headline_metric values
    task_metric_counts = data.groupby("task_name")["score_headline_metric"].nunique()
    duplicate_task_metrics = task_metric_counts[task_metric_counts > 1]
    if not duplicate_task_metrics.empty:
        raise ValueError(
            f"Tasks with multiple unique score_headline_metric values: {duplicate_task_metrics.index.tolist()}. "
            "Expected exactly one unique score_headline_metric per task."
        )

    # check if all tasks have the same model set
    models_per_task = data.groupby("task_name")["model"].apply(frozenset)
    if models_per_task.nunique() != 1:
        raise ValueError(
            f"Tasks have different model sets: {models_per_task}. "
            "Each task should have the same set of models. "
            "Use `models` parameter to specify the models to include."
        )

    # calculate angles for radar chart coordinates
    angles_closed = compute_closed_angles(num_axes=data["task_name"].nunique())

    # calculate normlaized scores for each task across all models
    normalized_values: dict[str, pd.Series] = {}
    for task_name in data["task_name"].unique():
        task_data = data[data["task_name"] == task_name]
        # score_headline_metric has the same value for all rows of a task
        metric_name = str(task_data["score_headline_metric"].iloc[0])
        values = invert_values_if_needed(
            task_data["score_headline_value"], metric_name, invert, domain
        )
        normalized_values[task_name] = normalize_values(
            values, task_data["model"], normalization, domain
        )

    all_rows = []
    for model in data["model"].unique():
        model_data = data[data["model"] == model]

        model_row = create_empty_radar_chart_row()

        for task_name in model_data["task_name"].unique():
            task_data = model_data[model_data["task_name"] == task_name]

            metric_name = task_data["score_headline_metric"].item()
            scorer_name = task_data["score_headline_name"].item()
            value_raw = float(task_data["score_headline_value"].item())
            value_scaled = normalized_values[task_name].loc[model]

            task_id = task_data["task_id"].item()
            log_url = task_data["log"].item() if "log" in model_data.columns else ""

            model_row["task_id"].append(task_id)
            model_row["task_name"].append(task_name)
            model_row["model"].append(model)
            model_row["log"].append(log_url)
            model_row["metric"].append(metric_name)
            model_row["scorer"].append(scorer_name)
            model_row["value"].append(value_raw)
            model_row["value_scaled"].append(value_scaled)

        # append first value to the end to close the polygon lines
        for key in model_row.keys():
            model_row[key] = append_first_value_to_list(model_row[key])

        model_row["x"] = np.array(model_row["value_scaled"]) * np.cos(angles_closed)
        model_row["y"] = np.array(model_row["value_scaled"]) * np.sin(angles_closed)

        all_rows.append(pd.DataFrame(model_row))

    if not all_rows:
        raise ValueError("No valid task data found after processing.")

    return pd.concat(all_rows, ignore_index=True)


def scores_radar_by_metric_df(
    data: pd.DataFrame,
    scorer: str,
    metrics: list[str] | None = None,
    invert: list[str] | None = None,
    normalization: Literal["percentile", "min_max", "absolute"] = "absolute",
    domain: tuple[float, float] | None = None,
) -> pd.DataFrame:
    """
    Creates a dataframe for a radar chart showing multiple models across multiple metrics in a single task.

    This is useful for tasks with multiple metrics, where each metric is a separate axis on the radar chart.

    Args:
        data: Evals data table containing model scores. It assumes one row per model.
        scorer: The name of the scorer to use for identifying metric columns.
        metrics: Optional list of specific metrics to plot. If None, all metrics
                 starting with 'score_{scorer}_' from the data will be used.
        invert: Optional list of metrics to invert (where lower scores are better).
        normalization: The normalization method to use for the metric values. Can be "percentile",
                       "min_max", or "absolute". Defaults to "absolute" (no normalization).
        domain: Optional min-max domain to use for the normalization. Only used if normalization is
                "min_max". Otherwise, the domain is inferred from the data. Defaults to None.
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

    required_columns = ["model", "task_id", "task_name"] + metric_cols
    check_required_columns(data, required_columns)

    data = filter_columns(data, required_columns)

    # check for multiple tasks and throw exception if found
    if data["task_name"].nunique() != 1:
        raise ValueError(
            f"Expected exactly one task, but found: {data['task_name'].unique().tolist()}"
        )

    # check for multiple rows per model and throw exception if found
    model_counts = data.groupby("model").size()
    duplicate_models = model_counts[model_counts > 1]
    if not duplicate_models.empty:
        raise ValueError(
            f"Multiple rows found for models: {duplicate_models.index.tolist()}. "
            f"Expected exactly one row per model."
        )

    # calculate angles for radar chart coordinates
    num_axes = len(metrics)
    angles_closed = compute_closed_angles(num_axes)

    # calculate normalized scores for each metric across all models
    normalized_values: dict[str, pd.Series] = {}
    for metric_name, metric_col in zip(metrics, metric_cols, strict=True):
        values = invert_values_if_needed(data[metric_col], metric_name, invert, domain)
        normalized_values[metric_name] = normalize_values(
            values, data["model"], normalization, domain
        )

    all_rows = []
    for model in data["model"].unique():
        model_data = data[data["model"] == model]
        values_raw = model_data[metric_cols].values[0].astype(float).tolist()
        values_scaled = [normalized_values[metric].loc[model] for metric in metrics]

        # get task_id and log for this model
        task_id = model_data["task_id"].item()
        task_name = model_data["task_name"].item()
        log_url = model_data["log"].item() if "log" in model_data.columns else ""

        model_row = create_empty_radar_chart_row()
        model_row["task_id"] = [task_id] * (num_axes + 1)
        model_row["task_name"] = [task_name] * (num_axes + 1)
        model_row["model"] = [model] * (num_axes + 1)
        model_row["log"] = [log_url] * (num_axes + 1)
        model_row["metric"] = append_first_value_to_list(metrics)
        model_row["scorer"] = [scorer] * (num_axes + 1)
        model_row["value"] = append_first_value_to_list(values_raw)
        model_row["value_scaled"] = append_first_value_to_list(values_scaled)
        model_row["x"] = np.array(model_row["value_scaled"]) * np.cos(angles_closed)
        model_row["y"] = np.array(model_row["value_scaled"]) * np.sin(angles_closed)

        all_rows.append(pd.DataFrame(model_row))

    if not all_rows:
        raise ValueError("No valid model data found after processing.")

    return pd.concat(all_rows, ignore_index=True)


def scores_radar_by_metric(
    data: Data,
    label: str = "metric",
    **kwargs: Any,
) -> Component:
    """
    Creates a radar chart showing scores for multiple models across multiple metrics in a single task.

    This is useful for tasks with multiple metrics, where each metric is a separate axis on the radar chart.

    Args:
        data: A `Data` object prepared using the `scores_radar_by_metric_df` function.
        label: Name of field holding the axes labels (defaults to "metric").
        **kwargs: Additional arguments for the `scores_radar_by_task` function.
    """
    return scores_radar_by_task(data, label=label, **kwargs)


def scores_radar_by_task(
    data: Data,
    model: str = "model_display_name",
    label: str = "task_display_name",
    title: str | Title | None = None,
    width: float = 400,
    channels: dict[str, str] | None = None,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    label_styles: LabelStyles | None = None,
    **attributes: Unpack[PlotAttributes],
) -> Component:
    """
    Creates a radar chart showing scores for multiple models across multiple tasks.

    Args:
        data: A `Data` object prepared using the `scores_radar_by_task_df` function.
        model: Name of field holding the model (defaults to "model_display_name").
        label: Name of field holding the axes labels (defaults to "task_display_name");
               use "metric" to plot against metrics.
        title: Title for plot (`str` or mark created with the `title()` function).
        width: The outer width of the plot in pixels, including margins. Defaults to 400.
               Height is automatically set to match width to maintain square aspect ratio.
        channels: Channels for the tooltips. Defaults are "Model", "Score", "Scaled Score",
                  "Metric", "Scorer", and "Task". Values in the dictionary should correspond
                  to column names in the data.
        legend: Options for the legend. Pass None to disable the legend.
        label_styles: Label styling options. It accepts `line_width` and `text_overflow`. Defaults to None.
        **attributes: Additional `PlotAttributes`. Use `margin` to set custom margin (defaults to max(60, width * 0.12)).
    """
    if "model_display_name" not in data.columns:
        model = "model"

    if "task_display_name" not in data.columns:
        task_name = "task_name"

        if label == "task_display_name":
            label = "task_name"
    else:
        task_name = "task_display_name"

    required_columns = [
        model,
        task_name,
        "task_id",
        "log",
        "scorer",
        "metric",
        "value",
        "value_scaled",
        "x",
        "y",
    ]
    if label not in required_columns:
        required_columns.append(label)
    check_required_columns(data, required_columns)

    # use margin from attributes or calculate default
    margin_attr = attributes.get("margin")
    plot_margin = int(margin_attr) if margin_attr else max(60, int(width * 0.12))

    # wrap label text if any metric name is longer than 10 characters
    if not label_styles and any(
        len(metric) > 10 for metric in data.column_unique(label)
    ):
        label_styles = LabelStyles(line_width=8)

    axes_labels = data.column_unique(label)
    axes = axes_coordinates(num_axes=len(axes_labels))
    grid_circles = grid_circles_coordinates()
    labels = labels_coordinates(labels=axes_labels, width=width, margin=plot_margin)

    model_selection = Selection.single()

    default_channels = {
        "Model": model,
        "Score": "value",
        "Scaled Score": "value_scaled",
        "Metric": "metric",
        "Scorer": "scorer",
        "Task": task_name,
    }
    channels = default_channels | (channels or {})
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
            filter_by=Selection.single(empty=True, include=model_selection),
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
                text=label["label"],
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
    default_attributes: PlotAttributes = {
        "margin": plot_margin,
        "x_axis": False,
        "y_axis": False,
    }
    attributes = default_attributes | attributes

    return plot(
        elements,
        title=title_mark(title=title, margin_top=45) if title else None,
        width=width,
        height=width,
        legend=plot_legend,
        **attributes,
    )


def compute_angles(num_axes: int, endpoint: bool = True) -> NDArray[np.floating[Any]]:
    """Computes the angles by number of axes."""
    return np.linspace(0, 2 * np.pi, num_axes, endpoint=endpoint)


def compute_closed_angles(num_axes: int) -> NDArray[np.floating[Any]]:
    """Computes angles and closes the polygon."""
    angles = compute_angles(num_axes, endpoint=False)
    return np.append(angles, angles[0])


def labels_coordinates(
    labels: list[str], width: float = 400, margin: float = 0
) -> list[dict[str, Any]]:
    """Computes coordinates for labels to be used in a radar chart.

    Args:
        labels: List of values for label text.
        width: Chart width in pixels, used to calculate radius.
        margin: Margin in pixels (defaults to 0) to subtract from width.
    """
    angles = compute_angles(len(labels), endpoint=False)

    # 15px offset regardless of chart size
    chart_radius_px = (width - 2 * margin) / 2
    label_offset_px = 15

    # convert to coordinate space: boundary circle is at radius 1.0
    label_radius = 1.0 + (label_offset_px / chart_radius_px)

    labels_coordinates: list[dict[str, Any]] = []
    for label, angle in zip(labels, angles, strict=True):
        angle_deg = np.degrees(angle) % 360

        # determine frame_anchor based on quadrant
        if 280 <= angle_deg or angle_deg < 80:  # right side
            frame_anchor = "left"
        elif 80 <= angle_deg < 100:  # top
            frame_anchor = "bottom"
        elif 100 <= angle_deg < 260:  # left side
            frame_anchor = "right"
        else:  # 260 <= angle_deg < 280, bottom
            frame_anchor = "top"

        labels_coordinates.append(
            {
                "label": [label],
                "x": [float(label_radius * np.cos(angle))],
                "y": [float(label_radius * np.sin(angle))],
                "frame_anchor": frame_anchor,
            }
        )

    return labels_coordinates


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


def create_empty_radar_chart_row() -> dict[str, list[str | float]]:
    return {
        "task_id": [],
        "task_name": [],
        "model": [],
        "log": [],
        "metric": [],
        "scorer": [],
        "value": [],
        "value_scaled": [],
        "x": [],
        "y": [],
    }


def check_required_columns(
    data: pd.DataFrame | Data, required_columns: list[str]
) -> None:
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Required columns not found in data: {missing_columns}")


def append_first_value_to_list(values: list[Any]) -> list[Any]:
    if values:
        return values + [values[0]]
    return values


def filter_columns(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Filters data to keep only required columns plus 'log' if present."""
    columns_to_keep = columns.copy()
    if "log" in data.columns:
        columns_to_keep.append("log")
    return data[columns_to_keep]


def invert_values_if_needed(
    values: pd.Series,
    metric_name: str,
    invert: list[str] | None,
    domain: tuple[float, float] | None = None,
) -> pd.Series:
    """Inverts values for metrics where lower is better."""
    if invert and metric_name in invert:
        if domain is not None:
            max_val = domain[1]
        else:
            max_val = values.astype(float).max()
        return max_val - values.astype(float)
    return values.astype(float)


def normalize_values(
    values: pd.Series,
    index: pd.Series | pd.Index | None = None,
    normalization: Literal["percentile", "min_max", "absolute"] = "absolute",
    domain: tuple[float, float] | None = None,
) -> pd.Series:
    """
    Computes normalized values for a series of values.

    Args:
        values: Series of values to normalize.
        index: Index of the values to use for the normalized values. If None, the index of the values is used.
        normalization: The normalization method to use. Can be "percentile", "min_max", or "absolute". Defaults to "absolute".
                       * "percentile": Computes the percentile rank of the values.
                       * "min_max": Computes the normalized values between 0 and 1 using the domain.
                       * "absolute": Returns the values as is without normalization.
        domain: The domain to use for the normalization. Only used if normalization is "min_max". Otherwise, the domain is
                inferred from the values. Defaults to None.
    """
    if index is None:
        index = values.index

    if normalization == "percentile":
        normalized = values.rank(method="average", pct=True)
    elif normalization == "min_max":
        if domain is None:
            domain = (values.astype(float).min(), values.astype(float).max())
        min_val = domain[0]
        max_val = domain[1]
        # handle edge case where all values are the same
        if max_val == min_val:
            # if all models have the same score, give them all 0.5
            normalized = pd.Series([0.5] * len(values), index=index)
        else:
            normalized = (values.astype(float) - min_val) / (max_val - min_val)
    elif normalization == "absolute":
        normalized = values.astype(float)
    return pd.Series(normalized.values, index=index)
