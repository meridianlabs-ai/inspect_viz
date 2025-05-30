from pydantic import JsonValue
from typing_extensions import Literal

from .._core.component import Component
from .._core.selection import Selection


class Legend(Component):
    """Plot legend (create legends using the `legend()` function)."""

    def __init__(
        self,
        legend: Literal["color", "opacity", "symbol"],
        columns: int,
        config: dict[str, JsonValue],
    ) -> None:
        super().__init__({"legend": legend, "columns": columns} | config)


def legend(
    legend: Literal["color", "opacity", "symbol"],
    label: str | None = None,
    columns: int = 1,
    selection: Selection | None = None,
    field: str | None = None,
    width: float | None = None,
    height: float | None = None,
    tick_size: float | None = None,
    margin_bottom: float | None = None,
    margin_left: float | None = None,
    margin_right: float | None = None,
    margin_top: float | None = None,
    for_plot: str | None = None,
) -> Legend:
    """Plot legend.

    Args:
      legend: Legend type ()`"color"`, `"opacity"`, or `"symbol"`).
      label: The legend label.
      columns: The number of columns to use to layout a discrete legend
        (defaults to 1)
      selection: The output selection. If specified, the legend is interactive,
        using a `toggle` interaction for discrete legends or an `intervalX`
        interaction for continuous legends.
      field: The data field over which to generate output selection clauses.
        If unspecified, a matching field is retrieved from existing plot marks.
      width: Width of the legend in pixels.
      height: Height of the legend in pixels.
      tick_size: The size of legend ticks in a continuous legend, in pixels.
      margin_bottom: The bottom margin of the legend component, in pixels.
      margin_left: The left margin of the legend component, in pixels.
      margin_right: The right margin of the legend component, in pixels.
      margin_top: The top margin of the legend component, in pixels.
      for_plot: The name of the plot this legend applies to. A plot must include a
        `name` attribute to be referenced. Note that this is not required when
        passing a `Legend` to the `plot()` function.
    """
    config: dict[str, JsonValue] = {}
    if label is not None:
        config["label"] = label
    if selection is not None:
        config["as"] = selection
    if field is not None:
        config["field"] = field
    if width is not None:
        config["width"] = width
    if height is not None:
        config["height"] = height
    if margin_bottom is None:
        config["marginBottom"] = margin_bottom
    if margin_left is None:
        config["marginLeft"] = margin_left
    if margin_right is None:
        config["marginRight"] = margin_right
    if margin_top is None:
        config["marginTop"] = margin_top
    if tick_size is not None:
        config["tickSize"] = tick_size
    if for_plot is not None:
        config["for"] = for_plot

    return Legend(legend, columns, config=config)
