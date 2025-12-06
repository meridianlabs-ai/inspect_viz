from typing import Any, TypedDict

from typing_extensions import Literal, Unpack

from inspect_viz._core.component import Component
from inspect_viz._core.data import Data
from inspect_viz._util.notgiven import NOT_GIVEN, NotGiven
from inspect_viz.mark import cell as cell_mark
from inspect_viz.mark._channel import SortOrder
from inspect_viz.mark._mark import Marks
from inspect_viz.mark._text import text
from inspect_viz.mark._title import Title
from inspect_viz.mark._title import title as title_mark
from inspect_viz.mark._util import flatten_marks
from inspect_viz.plot import plot
from inspect_viz.plot._attributes import PlotAttributes
from inspect_viz.plot._legend import Legend
from inspect_viz.plot._legend import legend as create_legend
from inspect_viz.transform._aggregate import avg


class CellOptions(TypedDict, total=False):
    """Cell options for the heatmap."""

    inset: float | None
    """Inset for the cell marks. Defaults to 1 pixel."""

    text: str | None
    """Text color for the cell marks. Defaults to "white". Set to None to disable text."""


def heatmap(
    data: Data,
    x_value: str = "id",
    x_label: str | None | NotGiven = None,
    y_value: str = "model_display_name",
    y_label: str | None | NotGiven = None,
    color_value: str | None = None,
    channels: dict[str, Any] | None = None,
    cell: CellOptions | None = None,
    tip: bool = True,
    title: str | Title | None = None,
    marks: Marks | None = None,
    height: float | None = None,
    width: float | None = None,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    sort: Literal["ascending", "descending"] | SortOrder | None = "ascending",
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    **attributes: Unpack[PlotAttributes],
) -> Component:
    """
    Creates a heatmap plot of arbitrary data.

    Args:
       data: Evals data table.
       x_value:  x-axis value
       x_label: x-axis label (defaults to None).
       y_value: y axis value
       y_label: y-axis label (defaults to None).
       color_value: Name of the column to use as values to determine cell color.
       channels: Channels to use for the plot. If None, the default channels are used.
       cell: Options for the cell marks.
       sort: Sort order for the x and y axes. If ascending, the highest values will be sorted to the top right. If descending, the highest values will appear in the bottom left. If None, no sorting is applied. If a SortOrder is provided, it will be used to sort the x and y axes.
       tip: Whether to show a tooltip with the value when hovering over a cell (defaults to True).
       legend: Options for the legend. Pass None to disable the legend.
       title: Title for plot (`str` or mark created with the `title()` function)
       marks: Additional marks to include in the plot.
       height: The outer height of the plot in pixels, including margins. The default is width / 1.618 (the [golden ratio](https://en.wikipedia.org/wiki/Golden_ratio)).
       width: The outer width of the plot in pixels, including margins. Defaults to 700.
       orientation: The orientation of the heatmap. If "horizontal", the tasks will be on the x-axis and models on the y-axis. If "vertical", the tasks will be on the y-axis and models on the x-axis.
       **attributes: Additional `PlotAttributes
    """
    # validate columns
    if x_value not in data.columns:
        raise ValueError(f"Column '{x_value}' not found in data.")

    if color_value is None:
        raise ValueError(
            "Please provide the color_value in order to generate a heatmap."
        )

    # resolve title
    if isinstance(title, str):
        title = title_mark(title, margin_top=20)

    # resolve marks
    marks = flatten_marks(marks)

    # Compute the color domain
    min_value = data.column_min(color_value)
    max_value = data.column_max(color_value)

    color_domain = [min_value, max_value]
    if min_value >= 0 and max_value <= 1:
        # If the values are all within 0 to 1, set the color
        # domain to that range
        color_domain = [0, 1.0]

    # Resolve default values
    defaultAttributes = PlotAttributes(
        x_tick_rotate=45,
        margin_bottom=75,
        color_scale="linear",
        x_scale="band",
        padding=0,
        color_scheme="greens",
        color_domain=color_domain,
    )
    attributes = defaultAttributes | attributes

    # resolve cell options
    default_cell_options = CellOptions(
        inset=1,
        text="white",
    )
    cell = default_cell_options | (cell or {})

    # resolve the text marks
    components = []
    if cell is not None:
        components.append(
            text(
                data,
                x=x_value if orientation == "horizontal" else y_value,
                y=y_value if orientation == "horizontal" else x_value,
                text=avg(color_value),
                fill=cell["text"],
                styles={"font_weight": 600},
            )
        )

    # add custom marks
    components.extend(marks)

    # resolve the sort order
    resolved_sort: SortOrder | None = None
    if sort == "ascending" or sort == "descending":
        resolved_sort = {
            "y": {"value": "fill", "reduce": "sum", "reverse": sort == "ascending"},
            "x": {"value": "fill", "reduce": "sum", "reverse": sort != "ascending"},
        }
    else:
        resolved_sort = sort

    plot_legend = (
        create_legend(
            legend="color",
            frame_anchor="bottom",
            columns="auto",
            width=(width / 2 if width is not None else 370),
            border=False,
            background=False,
        )
        if isinstance(legend, NotGiven)
        else legend
    )

    heatmap = plot(
        cell_mark(
            data,
            x=x_value if orientation == "horizontal" else y_value,
            y=y_value if orientation == "horizontal" else x_value,
            fill=avg(color_value),
            tip=tip,
            inset=cell["inset"] if cell else None,
            sort=resolved_sort,
            channels=channels if channels is not None else {},
        ),
        *components,
        legend=plot_legend,
        title=title,
        width=width,
        height=height,
        x_label=x_label,
        y_label=y_label,
        **attributes,
    )

    return heatmap
