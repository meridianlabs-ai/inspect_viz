from typing_extensions import Literal, Unpack

from inspect_viz._core.component import Component
from inspect_viz._core.data import Data
from inspect_viz._util.channels import resolve_log_viewer_channel
from inspect_viz._util.notgiven import NOT_GIVEN, NotGiven
from inspect_viz.mark._channel import SortOrder
from inspect_viz.mark._mark import Marks
from inspect_viz.mark._title import Title
from inspect_viz.plot._attributes import PlotAttributes
from inspect_viz.plot._legend import Legend

from ._heatmap import CellOptions, heatmap


def scores_heatmap(
    data: Data,
    task_name: str = "task_display_name",
    task_label: str | None | NotGiven = None,
    model_name: str = "model_display_name",
    model_label: str | None | NotGiven = None,
    score_value: str = "score_headline_value",
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
    Creates a heatmap plot of success rate of eval data.

    Args:
       data: Evals data table.
       task_name: Name of column to use for columns.
       task_label: x-axis label (defaults to None).
       model_name: Name of column to use for rows.
       model_label: y-axis label (defaults to None).
       score_value: Name of the column to use as values to determine cell color.
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
    # resolve x
    if task_name == "task_display_name" and task_name not in data.columns:
        task_name = "task_name"

    # Resolve the y column to average
    margin_left = None
    if model_name == "model_display_name":
        margin_left = 120
        if "model_display_name" not in data.columns:
            # fallback to using the raw model string
            model_name = "model"
            margin_left = 220

    # Compute the color domain
    min_value = data.column_min(score_value)
    max_value = data.column_max(score_value)

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

    # channels
    channels: dict[str, str] = {}
    if task_name == "task_name" or task_name == "task_display_name":
        channels["Task"] = task_name
    if model_name == "model" or model_name == "model_display_name":
        channels["Model"] = model_name
    if score_value == "score_headline_value":
        channels["Score"] = score_value
    resolve_log_viewer_channel(data, channels)

    return heatmap(
        data,
        x_value=task_name,
        x_label=task_label,
        y_value=model_name,
        y_label=model_label,
        color_value=score_value,
        cell=cell,
        tip=tip,
        title=title,
        marks=marks,
        height=height,
        width=width,
        legend=legend,
        sort=sort,
        orientation=orientation,
        channels=channels if channels else {},
        **attributes,
    )
