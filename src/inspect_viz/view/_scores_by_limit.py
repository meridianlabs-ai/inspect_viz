import json
from typing import Literal

import numpy as np
import pandas as pd
from typing_extensions import Unpack

from inspect_viz._core.component import Component
from inspect_viz._core.data import Data
from inspect_viz._core.selection import Selection
from inspect_viz._util.channels import resolve_log_viewer_channel
from inspect_viz._util.inspect import value_to_float
from inspect_viz._util.notgiven import NOT_GIVEN, NotGiven
from inspect_viz._util.stats import z_score
from inspect_viz.interactor._interactors import highlight, nearest_x
from inspect_viz.mark import area_y, line
from inspect_viz.mark._mark import Marks
from inspect_viz.mark._title import Title
from inspect_viz.mark._util import flatten_marks
from inspect_viz.plot import plot
from inspect_viz.plot._attributes import PlotAttributes
from inspect_viz.plot._legend import Legend
from inspect_viz.plot._legend import legend as create_legend
from inspect_viz.transform._sql import sql


def scores_by_limit_df(
    df: pd.DataFrame,
    score: str,
    limit: Literal["total_tokens", "total_time", "working_time"] = "total_tokens",
    scale: Literal["log", "linear", "auto"] = "auto",
    steps: int = 100,
) -> pd.DataFrame:
    """Prepares a dataframe for plotting success rate as a function of a resource limit (time, tokens).

    Args:
       df: A dataframe containing sample summaries and eval information.
       score: Name of field containing the score (0 = fail, 1 = success).
       limit: The resource limit to use (one of 'total_tokens', 'total_time', 'working_time'). Defaults to 'total_tokens'.
       scale: The scale type for the limit access. If 'auto', will use log scale if the range is 2 or more orders of magnitude (defaults to 'auto').
       steps: The number of points to use when sampling the limit range (defaults to 100).
    """
    # validate general columns
    required_columns = ["model", "task_id", score]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in data.")

    # validate limit column
    if limit == "total_tokens":
        if "model_usage" not in df.columns:
            raise ValueError(
                "Column 'model_usage' is required to compute 'total_tokens'."
            )
    else:
        if limit not in df.columns:
            raise ValueError(f"Required column '{limit}' not found in data.")

    # omit rows with missing data
    df.dropna(
        subset=[
            "model",
            "model_usage",
            "total_time",
            "working_time",
            score,
            "sample_id",
        ],
        inplace=True,
    )

    # compute the total tokens
    if limit == "total_tokens":
        df["total_tokens"] = df.apply(
            lambda x: json.loads(x["model_usage"])
            .get(x["model"], {})
            .get("total_tokens", {})
            if pd.notnull(x["model_usage"])
            else None,
            axis=1,
        )

    # coerce the score to a float
    to_float = value_to_float()
    df[score] = df[score].apply(to_float)

    # determine the bin resolution for the the resource given the range
    # (if there are 2 or more orders of magnitude, use log spacing)
    max_tokens = df[limit].max()
    min_tokens = df[limit].min()
    if scale == "log" or (scale == "auto" and max_tokens / min_tokens >= 100):
        limits = np.logspace(np.log10(min_tokens), np.log10(max_tokens), steps)
    else:
        limits = np.linspace(min_tokens, max_tokens, steps)

    # Prepare the new data structure to represent the success
    # rate at a given limit (for each model)
    data_dict: dict[str, list[str | float | int]] = {
        limit: [],
        "model": [],
        "success_rate": [],
        "standard_error": [],
        "other_termination_rate": [],
        "count": [],
    }

    # Add log column support if it exists
    has_log_column = "log" in df.columns
    if has_log_column:
        data_dict["log"] = []
        # Get the first log value for each model
        log_by_model = df.groupby("model")["log"].first().to_dict()

    # For each limit, compute the success rate and standard error
    for current_limit in limits:
        df_limit = df.copy()
        df_limit["other_termination_condition"] = (df_limit[limit] < current_limit) & (
            df_limit[score] == 0
        )
        df_limit.loc[df_limit[limit] > current_limit, score] = 0

        by_task = df_limit.groupby(["model", "task_id"]).agg(
            success_rate=(score, "mean"),
            other_termination_rate=("other_termination_condition", "mean"),
        )

        # For standard error, go back to the original samples
        by_model_stats = df_limit.groupby(["model"]).agg(
            success_rate=(score, "mean"),
            standard_error=(score, "sem"),  # From individual samples
            count=(score, "count"),
        )

        # Combine with task-level other_termination_rate
        by_model = (
            by_task.groupby(["model"])
            .agg(
                other_termination_rate=("other_termination_rate", "mean"),
            )
            .join(by_model_stats)
            .reset_index()
        )

        for _, row in by_model.iterrows():
            data_dict[limit].append(current_limit)
            data_dict["model"].append(row["model"])
            data_dict["success_rate"].append(row["success_rate"])
            data_dict["standard_error"].append(row["standard_error"])
            data_dict["other_termination_rate"].append(row["other_termination_rate"])
            data_dict["count"].append(row["count"])
            if has_log_column:
                data_dict["log"].append(log_by_model[row["model"]])

    return pd.DataFrame(data_dict)


def scores_by_limit(
    data: Data,
    model: str = "model_display_name",
    success: str = "success_rate",
    stderr: str | None = "standard_error",
    facet: str | None = None,
    other_termination_rate: str | bool = False,
    limit: str | None = None,
    limit_label: str | NotGiven = NOT_GIVEN,
    scale: Literal["log", "linear", "auto"] = "auto",
    title: str | Title | None = None,
    marks: Marks | None = None,
    height: float | None = None,
    width: float | None = None,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    ci: float = 0.95,
    **attributes: Unpack[PlotAttributes],
) -> Component:
    """Visualizes success rate as a function of a resource limit (time, tokens).

    Model success rate is plotted as a function of the time, tokens, or other resource limit.

    Args:
       data: A dataframe prepared using the `prepare_limit_dataframe` function.
       limit: Name of field for x axis (by default, will detect limit type using the columns present in the data frame).
       success: Name of field containing the success rate (defaults to "success_rate").
       stderr: Name of field containing the standard_error (defaults to "standard_error").
       facet: Name of field to use for faceting (defaults to None).
       other_termination_rate: Name of field containing the other termination rate (defaults to "other_termination_rate").
       model: Name of field holding the model (defaults to "model_display_name").
       ci: Confidence interval (e.g. 0.80, 0.90, 0.95, etc.). Defaults to 0.95.
       limit_label: The limit label (by default, will select limit label using the columns present in the data frame). Pass None for no label.
       scale: The scale type for the limit access. If 'auto', will use log scale if the range is 2 or more orders of magnitude (defaults to 'auto').
       title: Title for plot (`str` or mark created with the `title()` function)
       marks: Additional marks to include in the plot.
       width: The outer width of the plot in pixels, including margins. Defaults to 700.
       height: The outer height of the plot in pixels, including margins. The default is width / 1.618 (the [golden ratio](https://en.wikipedia.org/wiki/Golden_ratio))
       legend: Options for the legend. Pass None to disable the legend.
       **attributes: Additional `PlotAttributes`.
    """
    # resolve column names
    if "model_display_name" not in data.columns:
        model = "model"

    if other_termination_rate is True:
        other_termination_rate = "other_termination_rate"

    # resolve marks
    marks = flatten_marks(marks)

    # validate columns in dataframe
    required_columns = [
        model,
        success,
        limit,
    ]

    if "total_tokens" in data.columns:
        limit = "total_tokens"
        limit_label = "Tokens" if isinstance(limit_label, NotGiven) else limit_label
    elif "total_time" in data.columns:
        limit = "total_time"
        limit_label = (
            "Total Time (s)" if isinstance(limit_label, NotGiven) else limit_label
        )
    elif "working_time" in data.columns:
        limit = "working_time"
        limit_label = (
            "Working Time (s)" if isinstance(limit_label, NotGiven) else limit_label
        )
    else:
        if limit is None:
            raise ValueError(
                "No resource column found. Please specify the `resource` parameter."
            )
        if limit_label is None or isinstance(limit_label, NotGiven):
            limit_label = limit.replace("_", " ").title()

    # validate columns
    required_columns = [limit, success, model]
    if stderr is not None:
        required_columns.append(stderr)

    for col in required_columns:
        if col is not None and col not in data.columns:
            raise ValueError(f"Required column '{col}' not found in data.")

    # Configure the channels for the plot
    channels = {
        "Success Rate": success,
        "Model": model,
    }
    if not isinstance(limit_label, NotGiven):
        channels[limit_label] = limit
    resolve_log_viewer_channel(data, channels)

    # The selected model
    model_selection = Selection.single()

    # Dynamically switch between log and linear scales
    resource_min = data.column_min(limit)
    resource_max = data.column_max(limit)
    use_log = scale == "log" or (scale == "auto" and resource_max / resource_min >= 100)

    # Lines for the the model performance
    components = [
        line(
            data,
            x=limit,
            y=success,
            fx=facet,
            stroke=model,
            tip=True,
            channels=channels,
            filter_by=model_selection,
        ),
        line(
            data,
            x=limit,
            y=success,
            fx=facet,
            stroke=model,
            stroke_opacity=0.4,
            tip=True,
            channels=channels,
        ),
    ]

    if other_termination_rate:
        components.append(
            line(
                data,
                x=limit,
                y=other_termination_rate,
                fx=facet,
                stroke=model,
                stroke_dasharray="5,5",
                channels={
                    "Other Termination Rate": other_termination_rate,
                    "Model": model,
                },
                tip=True,
            )
        )

    if stderr is not None:
        z_alpha = z_score(ci)
        selection = Selection.single()

        components.append(
            area_y(
                data,
                x=limit,
                y=success,
                fx=facet,
                y1=sql(f"{success} - ({z_alpha} * {stderr})"),
                y2=sql(f"{success} + ({z_alpha} * {stderr})"),
                fill=model,
                channels=channels,
                fill_opacity=0.1,
                filter_by=model_selection,
            )
        )
        components.extend(
            [
                nearest_x(target=selection, channels=["fill"]),
                highlight(by=selection, opacity=0.2, fill_opacity=0.1),
            ]
        )

    if marks is not None:
        # Add custom marks to the plot
        components.extend(marks)

    # resolve defaults
    defaults: PlotAttributes = {
        "x_scale": "log" if use_log else "linear",
        "y_domain": "fixed",
    }
    attributes = defaults | attributes

    plot_legend = (
        create_legend("color", target=model_selection)
        if isinstance(legend, NotGiven)
        else legend
    )

    return plot(
        components,
        x_label=limit_label,
        y_label="Success rate",
        legend=plot_legend,
        height=height,
        width=width,
        **attributes,
        title=title,
    )
