from typing_extensions import Unpack

from inspect_viz import Component, Data
from inspect_viz._core.param import Param
from inspect_viz._util.channels import resolve_log_viewer_channel
from inspect_viz._util.notgiven import NOT_GIVEN, NotGiven
from inspect_viz._util.stats import z_score
from inspect_viz.mark import bar_y, rule_x
from inspect_viz.mark._mark import Marks
from inspect_viz.mark._title import Title
from inspect_viz.mark._title import title as title_mark
from inspect_viz.mark._util import flatten_marks
from inspect_viz.plot import legend as create_legend
from inspect_viz.plot import plot
from inspect_viz.plot._attributes import PlotAttributes
from inspect_viz.plot._legend import Legend
from inspect_viz.transform import sql


def scores_by_task(
    data: Data,
    model_name: str = "model_display_name",
    task_name: str = "task_display_name",
    score_value: str = "score_headline_value",
    score_stderr: str = "score_headline_stderr",
    score_label: str | None | NotGiven = NOT_GIVEN,
    ci: bool | float = 0.95,
    title: str | Title | None = None,
    marks: Marks | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    **attributes: Unpack[PlotAttributes],
) -> Component:
    """Bar plot for comparing eval scores.

    Summarize eval scores using a bar plot. By default, scores (`y`) are plotted by "task_display_name" (`fx`) and "model_display_name" (`x`). By default, confidence intervals are also plotted (disable this with `y_ci=False`).

    Args:
       data: Evals data table. This is typically created using a data frame read with the inspect `evals_df()` function.
       model_name: Name of field for the model name (defaults to "model_display_name")
       task_name: Name of field for the task name (defaults to "task_display_name")
       score_value: Name of field for the score value (defaults to "score_headline_value").
       score_stderr: Name of field for stderr (defaults to "score_headline_metric").
       score_label: Score axis label (pass None for no label).
       ci: Confidence interval (e.g. 0.80, 0.90, 0.95, etc.). Defaults to 0.95.
       title: Title for plot (`str` or mark created with the `title()` function).
       marks: Additional marks to include in the plot.
       width: The outer width of the plot in pixels, including margins. Defaults to 700.
       height: The outer height of the plot in pixels, including margins. The default is width / 1.618 (the [golden ratio](https://en.wikipedia.org/wiki/Golden_ratio))
       legend: Options for the legend. Pass None to disable the legend.
       **attributes: Additional `PlotAttributes`. By default, the `margin_bottom` are is set to 10 pixels and `x_ticks` is set to `[]`.
    """
    # resolve the x
    if model_name == "model_display_name" and "model_display_name" not in data.columns:
        # fallback to using the raw model string
        model_name = "model"

    # resolve the fx
    if task_name == "task_display_name" and "task_display_name" not in data.columns:
        # fallback to using the raw task name string
        task_name = "task_name"

    # resolve the title
    if isinstance(title, str):
        title = title_mark(title, margin_top=40)

    # resolve marks
    marks = flatten_marks(marks)

    # establish channels
    channels: dict[str, str] = {}
    if task_name == "task_name" or task_name == "task_display_name":
        channels["Task"] = task_name
    if model_name == "model" or model_name == "model_display_name":
        channels["Model"] = model_name
    if score_value == "score_headline_value":
        channels["Score"] = score_value
    resolve_log_viewer_channel(data, channels)

    # start with bar plot
    components = [
        bar_y(
            data,
            x=model_name,
            fx=task_name,
            y=score_value,
            fill=model_name,
            channels=channels,
            tip=True,
        )
    ]

    # add ci if requested
    if ci is not False:
        ci = 0.95 if ci is True else ci
        z_alpha = z_score(ci)
        components.append(
            rule_x(
                data,
                x=model_name,
                fx=task_name,
                y1=sql(f"{score_value} - ({z_alpha} * {score_stderr})"),
                y2=sql(f"{score_value} + ({z_alpha} * {score_stderr})"),
                stroke="black",
                marker="tick-x",
            ),
        )

    # resolve defaults
    defaults: PlotAttributes = {
        "margin_bottom": 10,
        "x_ticks": [],
    }
    attributes = defaults | attributes

    # add custom marks
    components.extend(marks)

    plot_legend = (
        create_legend("color", frame_anchor="bottom")
        if isinstance(legend, NotGiven)
        else legend
    )

    # render plot
    return plot(
        components,
        legend=plot_legend,
        x_label=None,
        fx_label=None,
        y_label=score_label,
        title=title,
        width=width,
        height=height,
        **attributes,
    )
