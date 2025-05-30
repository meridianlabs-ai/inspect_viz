from pydantic import JsonValue
from typing_extensions import Literal

from .._core.component import Component
from .._core.selection import Selection


class Legend(Component):
    """Plot legend (create legends using the `legend()` function)."""

    def __init__(
        self,
        legend: Literal["color", "opacity", "symbol"],
        location: Literal["bottom", "left", "right", "top"],
        columns: Literal["auto"] | int | None,
        config: dict[str, JsonValue],
    ) -> None:
        # base config
        legend_config: dict[str, JsonValue] = {"legend": legend}

        # handle columns
        if columns == "auto":
            columns = 1 if location in ["left", "right"] else None
        if columns is not None:
            legend_config["columns"] = columns

        # forward super to config
        super().__init__(legend_config | config)

        # save location
        self._location = location

    @property
    def location(self) -> Literal["bottom", "left", "right", "top"]:
        return self._location


def legend(
    legend: Literal["color", "opacity", "symbol"],
    location: Literal["bottom", "left", "right", "top"] = "right",
    columns: Literal["auto"] | int | None = "auto",
    label: str | None = None,
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
      location: The legend location (used for display only when passing a legend
        to the`plot()` function). Also affects default value for `columns`.
      columns: The number of columns to use to layout a discrete legend
        (defaults to "auto", which uses 1 column for location "left" or "right")
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
        `name` attribute to be referenced. Note that this is not use when
        passing a legend to the `plot()` function.
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

    return Legend(legend, location, columns, config=config)
