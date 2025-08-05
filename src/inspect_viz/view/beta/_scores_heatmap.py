from typing import TypedDict, Unpack

from typing_extensions import Literal

from inspect_viz._core.component import Component
from inspect_viz._core.data import Data
from inspect_viz._util.channels import resolve_log_viewer_channel
from inspect_viz._util.notgiven import NotGiven
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


def scores_heatmap(
    data: Data,
    x: str = "task_display_name",
    y: str = "model_display_name",
    fill: str = "score_headline_value",
    cell: CellOptions | None = None,
    tip: bool = True,
    title: str | Title | None = None,
    marks: Marks | None = None,
    height: float | None = None,
    width: float | None = None,
    x_label: str | None | NotGiven = None,
    y_label: str | None | NotGiven = None,
    legend: Legend | bool | None = None,
    sort: Literal["ascending", "descending"] | SortOrder | None = "ascending",
    **attributes: Unpack[PlotAttributes],
) -> Component:
    """
    Creates a heatmap plot of success rate of eval data.

    Args:
       data: Evals data table.
       x: Name of column to use for columns.
       y: Name of column to use for rows.
       fill: Name of the column to use as values to determine cell color.
       cell: Options for the cell marks.
       sort: Sort order for the x and y axes. If ascending, the highest values will be sorted to the top right. If descending, the highest values will appear in the bottom left. If None, no sorting is applied. If a SortOrder is provided, it will be used to sort the x and y axes.
       tip: Whether to show a tooltip with the value when hovering over a cell (defaults to True).
       legend: Options for the legend. Pass None to disable the legend.
       title: Title for plot (`str` or mark created with the `title()` function)
       marks: Additional marks to include in the plot.
       height: The outer height of the plot in pixels, including margins. The default is width / 1.618 (the [golden ratio](https://en.wikipedia.org/wiki/Golden_ratio)).
       width: The outer width of the plot in pixels, including margins. Defaults to 700.
       x_label: x-axis label (defaults to None).
       y_label: y-axis label (defaults to None).
       **attributes: Additional `PlotAttributes
    """
    # resolve x
    if x == "task_display_name" and x not in data.columns:
        x = "task_name"

    # Resolve the y column to average
    margin_left = None
    if y == "model_display_name":
        margin_left = 120
        if "model_display_name" not in data.columns:
            # fallback to using the raw model string
            y = "model"
            margin_left = 220

    # resolve title
    if isinstance(title, str):
        title = title_mark(title, margin_top=20)

    # resolve marks
    marks = flatten_marks(marks)

    # Compute the color domain
    min_value = data.column_min(fill)
    max_value = data.column_max(fill)

    color_domain = [min_value, max_value]
    if min_value >= 0 and max_value <= 1:
        # If the values are all within 0 to 1, set the color
        # domain to that range
        color_domain = [0, 1.0]

    # Resolve default values
    defaultAttributes = PlotAttributes(
        margin_left=margin_left,
        x_tick_rotate=45,
        margin_bottom=75,
        color_scale="linear",
        padding=0,
        color_scheme="viridis",
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
                x=x,
                y=y,
                text=avg(fill),
                fill=cell["text"],
                styles={"font_weight": 600},
            )
        )

    # add custom marks
    components.extend(marks)

    # channels
    channels: dict[str, str] = {}
    if x == "task_name" or x == "task_display_name":
        channels["Task"] = x
    if y == "model" or y == "model_display_name":
        channels["Model"] = y
    if fill == "score_headline_value":
        channels["Score"] = fill
    resolve_log_viewer_channel(data, channels)

    # resolve the sort order
    resolved_sort: SortOrder | None = None
    if sort == "ascending" or sort == "descending":
        resolved_sort = {
            "y": {"value": "fill", "reduce": "sum", "reverse": sort == "ascending"},
            "x": {"value": "fill", "reduce": "sum", "reverse": sort != "ascending"},
        }
    else:
        resolved_sort = sort

    heatmap = plot(
        cell_mark(
            data,
            x=x,
            y=y,
            fill=avg(fill),
            tip=tip,
            inset=cell["inset"] if cell else None,
            sort=resolved_sort,
            channels=channels,
        ),
        *components,
        legend=(
            create_legend(
                legend="color",
                frame_anchor="bottom",
                columns="auto",
                width=370,
                border=False,
                background=False,
            )
            if legend is None or legend is True
            else legend
            if legend
            else None
        ),
        title=title,
        width=width,
        height=height,
        x_label=x_label,
        y_label=y_label,
        **attributes,
    )

    return heatmap
