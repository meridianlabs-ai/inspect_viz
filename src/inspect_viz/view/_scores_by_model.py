from typing import Literal

from typing_extensions import Unpack

from inspect_viz._core.component import Component
from inspect_viz._core.data import Data
from inspect_viz._util.channels import resolve_log_viewer_channel
from inspect_viz._util.notgiven import NOT_GIVEN, NotGiven
from inspect_viz.mark._mark import Mark, Marks
from inspect_viz.mark._rule import rule_y
from inspect_viz.mark._title import Title
from inspect_viz.mark._util import flatten_marks
from inspect_viz.plot._attributes import PlotAttributes
from inspect_viz.plot._legend import Legend
from inspect_viz.plot._plot import plot
from inspect_viz.transform._ci import ci_bounds


def scores_by_model(
    data: Data,
    *,
    model_name: str = "model_display_name",
    score_value: str = "score_headline_value",
    score_stderr: str = "score_headline_stderr",
    ci: float = 0.95,
    sort: Literal["asc", "desc"] | None = None,
    score_label: str | None | NotGiven = None,
    model_label: str | None | NotGiven = None,
    color: str | None = None,
    title: str | Title | None = None,
    marks: Marks | None = None,
    width: float | None = None,
    height: float | None = None,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    **attributes: Unpack[PlotAttributes],
) -> Component:
    """Bar plot for comparing the scores of different models on a single evaluation.

    Summarize eval scores using a bar plot. By default, scores (`y`) are plotted by "model_display_name" (`y`). By default, confidence intervals are also plotted (disable this with `y_ci=False`).

    Args:
       data: Evals data table. This is typically created using a data frame read with the inspect `evals_df()` function.
       model_name: Column containing the model name (defaults to "model_display_name")
       score_value: Column containing the score value (defaults to "score_headline_value").
       score_stderr: Column containing the score standard error (defaults to "score_headline_stderr").
       ci: Confidence interval (e.g. 0.80, 0.90, 0.95, etc.). Defaults to 0.95.
       sort: Sort order for the bars (sorts using the 'x' value). Can be "asc" or "desc". Defaults to "asc".
       score_label: x-axis label (defaults to None).
       model_label: x-axis label (defaults to None).
       color: The color for the bars. Defaults to "#416AD0". Pass any valid hex color value.
       title: Title for plot (`str` or mark created with the `title()` function)
       marks: Additional marks to include in the plot.
       width: The outer width of the plot in pixels, including margins. Defaults to 700.
       height: The outer height of the plot in pixels, including margins. The default is width / 1.618 (the [golden ratio](https://en.wikipedia.org/wiki/Golden_ratio))
       legend: Options for the legend. Pass None to disable the legend.
       **attributes: Additional `PlotAttributes`. By default, the `y_inset_top` and `margin_bottom` are set to 10 pixels and `x_ticks` is set to `[]`.
    """
    # Resolve the y column
    margin_left = None
    if model_name == "model_display_name":
        margin_left = 120
        if "model_display_name" not in data.columns:
            # fallback to using the raw model string
            model_name = "model"
            margin_left = 210

    # Validate that there is only a single evaluation
    tasks = data.column_unique("task_name")
    if len(tasks) > 1:
        raise ValueError(
            "scores_by_model can only be used with a single evaluation. "
            f"Found {len(tasks)} tasks: {', '.join(tasks)}."
        )

    # compute default height
    if height is None:
        height = 30 * len(data.column_unique(model_name))

    # resolve marks
    marks = flatten_marks(marks)

    # compute the x_domain, setting it to 0 to 1 if the values are all
    # within that range
    max_score = data.column_max(score_value)
    min_score = data.column_min(score_value)
    if max_score <= 1 and min_score >= 0:
        x_domain = [0, 1.0]
    else:
        x_domain = None

    # Resolve default values
    defaultAttributes = PlotAttributes(
        x_domain=x_domain,
        margin_left=margin_left,
        color_domain=[1],
    )
    attributes = defaultAttributes | attributes

    # channels
    channels: dict[str, str] = {}
    if (
        model_name == "model" or model_name == "model_display_name"
    ) and model_label is None:
        channels["Model"] = model_name
    if score_value == "score_headline_value" and score_label is None:
        channels["Score"] = score_value
    resolve_log_viewer_channel(data, channels)

    components: list[Mark] = []

    # add the primary plot
    components.append(
        rule_y(
            data,
            x=score_value,
            y=model_name,
            sort={"y": "x", "reverse": sort != "asc"},
            stroke_width=4,
            stroke_linecap="round",
            marker_end="circle",
            tip=True,
            channels=channels,
            stroke=color or "#416AD0",
        ),
    )

    # add ci
    if ci is not False:
        ci = 0.95 if ci is True else ci
        ci_lower, ci_upper = ci_bounds(score_value, level=ci, stderr=score_stderr)
        components.append(
            rule_y(
                data,
                x1=ci_lower,
                x2=ci_upper,
                y=model_name,
                sort={"y": "x", "reverse": sort != "asc"},
                stroke=f"{color or '#416AD0'}20",
                stroke_width=15,
            ),
        )

    plot_legend = None if isinstance(legend, NotGiven) else legend

    # The plots
    return plot(
        *components,
        *marks,
        y_label=model_label,
        x_label=score_label,
        title=title,
        height=height,
        width=width,
        legend=plot_legend,
        **attributes,
    )
