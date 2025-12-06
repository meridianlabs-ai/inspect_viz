from typing import Literal

import pandas as pd
from typing_extensions import Unpack

from inspect_viz import Component, Data
from inspect_viz._core.param import Param
from inspect_viz._util.channels import resolve_log_viewer_channel
from inspect_viz._util.notgiven import NOT_GIVEN, NotGiven
from inspect_viz.input import checkbox_group, select
from inspect_viz.layout._concat import vconcat
from inspect_viz.layout._space import vspace
from inspect_viz.mark._dot import dot
from inspect_viz.mark._mark import Marks
from inspect_viz.mark._regression import regression_y
from inspect_viz.mark._rule import rule_x
from inspect_viz.mark._text import text
from inspect_viz.mark._title import Title
from inspect_viz.mark._util import flatten_marks
from inspect_viz.plot._attributes import PlotAttributes
from inspect_viz.plot._legend import Legend
from inspect_viz.plot._legend import legend as legend_fn
from inspect_viz.plot._plot import plot
from inspect_viz.transform import ci_bounds
from inspect_viz.transform._column import epoch_ms
from inspect_viz.transform._transform import Transform


def scores_timeline(
    data: Data,
    task_name: str = "task_display_name",
    model_name: str = "model_display_name",
    model_organization: str = "model_organization_name",
    model_release_date: str = "model_release_date",
    score_name: str = "score_headline_name",
    score_value: str = "score_headline_value",
    score_stderr: str = "score_headline_stderr",
    organizations: list[str] | None = None,
    filters: bool | list[Literal["task", "organization"]] = True,
    ci: float | bool | NotGiven = NOT_GIVEN,
    time_label: str = "Release Date",
    score_label: str = "Score",
    eval_label: str = "Eval",
    title: str | Title | None = None,
    marks: Marks | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    regression: bool = False,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    **attributes: Unpack[PlotAttributes],
) -> Component:
    """Eval scores by model, organization, and release date.

    Args:
       data: Data read using `evals_df()` and amended with model metadata using the `model_info()` prepare operation (see [Data Preparation](https://inspect.aisi.org.uk/dataframe.html#data-preparation) for details).
       task_name: Column for task name (defaults to "task_display_name").
       model_name: Column for model name (defaults to "model_display_name").
       model_organization: Column for model organization (defaults to "model_organization_name").
       model_release_date: Column for model release date (defaults to "model_release_date").
       score_name: Column for scorer name (defaults to "score_headline_name").
       score_value: Column for score value (defaults to "score_headline_value").
       score_stderr: Column for score stderr (defaults to "score_headline_stderr")
       organizations: List of organizations to include (in order of desired presentation).
       filters: Provide UI to filter plot by task and organization(s).
       ci: Confidence interval (defaults to 0.95, pass `False` for no confidence intervals)
       time_label: Label for time (x-axis).
       score_label: Label for score (y-axis).
       eval_label: Label for eval select input.
       title: Title for plot (`str` or mark created with the `title()` function).
       marks: Additional marks to include in the plot.
       width: The outer width of the plot in pixels, including margins. Defaults to 700.
       height: The outer height of the plot in pixels, including margins. The default is width / 1.618 (the [golden ratio](https://en.wikipedia.org/wiki/Golden_ratio))
       regression: If `True`, adds a regression line to the plot (uses the confidence interval passed using ci). Defaults to False.
       legend: Legend to use for the plot (defaults to `None`, which uses the default legend).
       **attributes: Additional `PlotAttributes`. By default, the `x_domain` is set to "fixed", the `y_domain` is set to `[0,1.0]`, `color_label` is set to "Organizations", and `color_domain` is set to `organizations`.
    """
    # fallback to task_name if required
    if task_name == "task_display_name" and task_name not in data.columns:
        task_name = "task_name"

    # resolve the confidence interval
    max = data.column_max(score_stderr)
    min = data.column_min(score_stderr)
    if isinstance(ci, NotGiven):
        # See if the stderr field contains actual values
        if pd.isna(max) or pd.isna(min):
            # no values, just disable CI
            ci = False
        else:
            # use the default ci
            ci = 0.95

    # Validate that stderr values are present if ci is requested
    if ci is not False and (pd.isna(max) or pd.isna(min)):
        raise ValueError(
            f"Confidence intervals requested (ci={ci}) but no values found in '{score_stderr}' column."
        )

    # validate the required fields
    required_fields = [
        model_name,
        model_organization,
        model_release_date,
        task_name,
        score_name,
        score_value,
    ]
    if ci is not False:
        required_fields.append(score_stderr)

    for field in required_fields:
        if field is not None and field not in data.columns:
            raise ValueError(f"Field '{field}' not provided in passed 'data'.")

    model_date_transform: str | Transform = model_release_date
    if regression:
        model_date_transform = epoch_ms(model_release_date)

    # resolve marks
    marks = flatten_marks(marks)

    # count unique tasks and organizations
    num_tasks = len(data.column_unique(task_name))
    num_organizations = len(data.column_unique(model_organization))

    # build inputs
    task_filter = filters if isinstance(filters, bool) else "task" in filters
    inputs: list[Component] = []
    if num_tasks > 1 and task_filter:
        inputs.append(
            select(
                data,
                label=f"{eval_label}: ",
                column=task_name,
                value="auto",
                width=370,
            )
        )
    organizations_filter = (
        filters if isinstance(filters, bool) else "organization" in filters
    )
    if num_organizations > 1 and organizations_filter:
        inputs.append(
            checkbox_group(
                data,
                column=model_organization,
                options=organizations,
            )
        )

    # build channels (log_viewer is optional)
    channels: dict[str, str] = {
        "Organization": model_organization,
        "Model": model_name,
        "Release Date": model_release_date,
        "Scorer": score_name,
        "Score": score_value,
    }
    if ci is not False:
        channels["Stderr"] = score_stderr

    resolve_log_viewer_channel(data, channels)

    # start with dot plot
    components = [
        dot(
            data,
            x=model_date_transform,
            y=score_value,
            r=3,
            fill=model_organization,
            channels=channels,
        )
    ]

    # add frontier label
    if "frontier" in data.columns:
        components.append(
            text(
                data,
                text=model_name,
                x=model_date_transform,
                y=score_value,
                line_anchor="middle",
                frame_anchor="right",
                filter="frontier",
                dx=-4,
                fill=model_organization,
                shift_overlapping_text=True,
            )
        )

    # add ci if requested
    if ci is not False:
        ci = 0.95 if ci is True else ci
        ci_lower, ci_upper = ci_bounds(score_value, level=ci, stderr=score_stderr)
        components.append(
            rule_x(
                data,
                x=model_date_transform,
                y=score_value,
                y1=ci_lower,
                y2=ci_upper,
                stroke=model_organization,
                stroke_opacity=0.4,
                marker="tick-x",
            ),
        )

    # add regression line if requested
    if regression:
        components.append(
            regression_y(
                data,
                x=model_date_transform,
                y=score_value,
                ci=ci,
                precision=4,
                stroke="#CCCCCC",
                fill_opacity=0.2,
            )
        )

    # resolve the y-axis domain
    y_min = data.column_min(score_value)
    y_max = data.column_max(score_value)
    if y_min >= 0 and y_max <= 1.0:
        y_domain = [0, 1.0]
    else:
        y_domain = [y_min + (0.1 * y_min), y_max + (0.1 * y_max)]

    # resolve defaults
    defaults: PlotAttributes = {
        "x_domain": "fixed",
        "y_domain": y_domain,
        "y_inset_top": 10,
        "color_label": "Organizations",
        "color_domain": organizations or "fixed",
        "grid": True,
        "x_tick_format": "%b. %Y",
    }
    attributes = defaults | attributes

    # add custom marks
    components.extend(marks)

    # resolve legend
    plot_legend: Legend | None
    if num_organizations > 1:
        plot_legend = (
            legend_fn("color", target=data.selection)
            if isinstance(legend, NotGiven)
            else legend
        )
    else:
        plot_legend = None

    # plot
    pl = plot(
        components,
        legend=plot_legend,
        x_label=time_label,
        y_label=score_label,
        title=title,
        width=width,
        height=height,
        **attributes,
    )

    # layout
    if len(inputs) > 0:
        return vconcat(*inputs, vspace(), pl)
    else:
        return pl
