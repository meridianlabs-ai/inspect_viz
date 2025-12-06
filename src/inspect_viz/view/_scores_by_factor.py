from typing_extensions import Unpack

from inspect_viz import Component, Data, Param
from inspect_viz._util.channels import resolve_log_viewer_channel
from inspect_viz._util.color import lighten_color_hsl
from inspect_viz._util.notgiven import NOT_GIVEN, NotGiven
from inspect_viz.mark import frame, rule_y
from inspect_viz.mark._mark import Mark, Marks
from inspect_viz.mark._util import flatten_marks
from inspect_viz.plot import PlotAttributes, plot
from inspect_viz.plot import legend as create_legend
from inspect_viz.plot._legend import Legend
from inspect_viz.transform import ci_bounds, sql


def scores_by_factor(
    data: Data,
    factor: str,
    factor_labels: tuple[str, str],
    score_value: str = "score_headline_value",
    score_stderr: str = "score_headline_stderr",
    score_label: str = "Score",
    model: str = "model",
    model_label: str = "Model",
    ci: bool | float = 0.95,
    color: str | tuple[str, str] = "#3266ae",
    title: str | Mark | None = None,
    marks: Marks | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    **attributes: Unpack[PlotAttributes],
) -> Component:
    """Summarize eval scores with a factor of variation (e.g 'No hint' vs. 'Hint').

    Args:
       data: Evals data table. This is typically created using a data frame read with the inspect `evals_df()` function.
       factor: Field with factor of variation (should be of type boolean).
       factor_labels: Tuple of labels for factor of variation. `False` value should be first, e.g. `("No hint", "Hint")`.
       score_value: Name of field for x (scoring) axis (defaults to "score_headline_value").
       score_stderr: Name of field for scoring stderr (defaults to "score_headline_stderr").
       score_label: Label for x-axis (defaults to "Score").
       model: Name of field for y axis (defaults to "model").
       model_label: Lable for y axis (defaults to "Model").
       ci: Confidence interval (e.g. 0.80, 0.90, 0.95, etc.). Defaults to 0.95.)
       color: Hex color value (or tuple of two values). If one value is provided the second is computed by lightening the main color.
       title: Title for plot (`str` or mark created with the `title()` function).
       marks: Additional marks to include in the plot.
       width: The outer width of the plot in pixels, including margins. Defaults to 700.
       height: The outer height of the plot in pixels, including margins. Default to 65 pixels for each item on the "y" axis.
       legend: Options for the legend. Pass None to disable the legend.
       **attributes: Additional `PlotAttributes
    """
    # provide secondary color if necessary
    if isinstance(color, str):
        color = (color, lighten_color_hsl(color, 0.6))

    # compute default height
    if height is None:
        height = 65 * len(data.column_unique(model))

    # validate that we have labels
    if not isinstance(factor_labels, tuple) or len(factor_labels) != 2:
        raise ValueError("factor_labels must be a tuple of 2 strings.")

    # resolve marks
    marks = flatten_marks(marks)

    # default attributes
    defaults = PlotAttributes(
        margin_left=100,
        y_ticks=[],
        y_tick_size=0,
        fy_axis="left",
        color_domain=factor_labels,
        color_range=color,
    )
    attributes = defaults | attributes

    # build channels
    channels = {model_label: model, score_label: score_value}
    if ci is not False:
        channels["Stderr"] = score_stderr
    resolve_log_viewer_channel(data, channels)

    # start w/ bars
    components = [
        frame("left", inset_top=5, inset_bottom=5),
        rule_y(
            data,
            x=score_value,
            y=factor,
            fy=model,
            sort={"fy": "-x"},
            stroke=sql(f"IF(NOT {factor}, '{factor_labels[0]}', '{factor_labels[1]}')"),
            stroke_width=3,
            stroke_linecap="round",
            marker_end="circle",
            tip=True,
            channels={
                model_label: model,
                score_label: score_value,
                "Stderr": score_stderr,
            },
        ),
    ]

    # add ci
    if ci is not False:
        ci = 0.95 if ci is True else ci
        ci_lower, ci_upper = ci_bounds(score_value, level=ci, stderr=score_stderr)
        components.append(
            rule_y(
                data,
                x1=ci_lower,
                x2=ci_upper,
                y=factor,
                fy=model,
                sort={"fy": "-x"},
                stroke=f"{color[0]}20",
                stroke_width=15,
            ),
        )

    # add custom marks
    components.extend(marks)

    plot_legend = (
        create_legend("color", target=data.selection)
        if isinstance(legend, NotGiven)
        else legend
    )

    return plot(
        *components,
        legend=plot_legend,
        x_label=score_label,
        y_label=None,
        fy_label=None,
        title=title,
        width=width,
        height=height,
        **attributes,
    )
