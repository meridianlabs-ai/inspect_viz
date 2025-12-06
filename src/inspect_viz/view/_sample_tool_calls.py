from typing_extensions import Unpack

from inspect_viz import Component, Data
from inspect_viz._util.channels import resolve_log_viewer_channel
from inspect_viz._util.notgiven import NOT_GIVEN, NotGiven
from inspect_viz.mark import cell, text
from inspect_viz.mark._mark import Marks
from inspect_viz.mark._title import Title
from inspect_viz.mark._types import TextStyles
from inspect_viz.mark._util import flatten_marks
from inspect_viz.plot import legend as create_legend
from inspect_viz.plot import plot
from inspect_viz.plot._attributes import PlotAttributes
from inspect_viz.plot._legend import Legend
from inspect_viz.transform._aggregate import first


def sample_tool_calls(
    data: Data,
    x: str = "order",
    y: str = "id",
    tool: str = "tool_call_function",
    limit: str = "limit",
    tools: list[str] | None = None,
    x_label: str | None = "Message",
    y_label: str | None = "Sample",
    title: str | Title | None = None,
    marks: Marks | None = None,
    width: float | None = None,
    height: float | None = None,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    **attributes: Unpack[PlotAttributes],
) -> Component:
    """Heat map visualising tool calls over evaluation turns.

    Args:
       data: Messages data table. This is typically created using a data frame read with the inspect `messages_df()` function.
       x: Name of field for x axis (defaults to "order")
       y: Name of field for y axis (defaults to "id").
       tool: Name of field with tool name (defaults to "tool_call_function")
       limit: Name of field with sample limit (defaults to "limit").
       tools: Tools to include in plot (and order to include them). Defaults to all tools found in `data`.
       x_label: x-axis label (defaults to "Message").
       y_label: y-axis label (defaults to "Sample").
       title: Title for plot (`str` or mark created with the `title()` function)
       marks: Additional marks to include in the plot.
       width: The outer width of the plot in pixels, including margins. Defaults to 700.
       height: The outer height of the plot in pixels, including margins. The default is width / 1.618 (the [golden ratio](https://en.wikipedia.org/wiki/Golden_ratio))
       legend: Options for the legend. Pass None to disable the legend.
       **attributes: Additional `PlotAttributes`. By default, the `margin_top` is set to 0, `margin_left` to 20, `margin_right` to 100, `color_label` is "Tool", `y_ticks` is empty,  and `x_ticks` and `color_domain` are calculated from `data`.
    """
    # determine unique values for tools
    if tools is None:
        tools = data.column_unique(tool)
        tools = [tool for tool in tools if isinstance(tool, str)]

    # determine range for x
    x_ticks: list[int] = []
    max_order = data.column_max(x)
    boundary = 25
    while True:
        if max_order < boundary:
            x_ticks = list(range(0, boundary, boundary // 5))
            break
        else:
            boundary = boundary * 2

    # resolve marks
    marks = flatten_marks(marks)

    # attribute defaults
    defaults = PlotAttributes(
        margin_top=None if title else 0,
        margin_left=20,
        margin_right=100,
        x_ticks=x_ticks,
        y_ticks=[],
        color_label="Tool",
        color_domain=tools,
    )
    attributes = defaults | attributes

    # configure channels
    channels: dict[str, str] = {
        "Message": x,
        "Sample": y,
        "Tool": tool,
    }
    resolve_log_viewer_channel(data, channels)

    plot_legend = (
        create_legend("color", frame_anchor="right")
        if isinstance(legend, NotGiven)
        else legend
    )

    return plot(
        cell(data, x=x, y=y, fill=tool, channels=channels),
        text(
            data,
            text=first(limit),
            y=y,
            frame_anchor="right",
            styles=TextStyles(
                font_size=8,
                font_weight=200,
            ),
            dx=50,
        ),
        *marks,
        title=title,
        width=width,
        height=height,
        legend=plot_legend,
        x_label=x_label,
        y_label=y_label,
        **attributes,
    )
