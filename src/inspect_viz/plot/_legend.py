from typing import cast

from pydantic import JsonValue
from typing_extensions import Literal

from .._core.component import Component
from .._core.selection import Selection
from ..mark._types import FrameAnchor


class Legend(Component):
    """Plot legend (create legends using the `legend()` function)."""

    def __init__(
        self,
        legend: Literal["color", "opacity", "symbol"],
        columns: Literal["auto"] | int | None,
        frame_anchor: FrameAnchor | None,
        config: dict[str, JsonValue],
    ) -> None:
        # base config
        legend_config: dict[str, JsonValue] = {"legend": legend}

        # handle columns
        if columns == "auto":
            columns = (
                1
                if frame_anchor
                in [
                    "left",
                    "right",
                    "top-right",
                    "top-left",
                    "bottom-right",
                    "bottom-left",
                ]
                else None
            )
        if columns is not None:
            legend_config["columns"] = columns

        # capture frame anchor
        config["_frame_anchor"] = frame_anchor or "right"

        # forward super to config
        super().__init__(legend_config | config)

    @property
    def frame_anchor(self) -> FrameAnchor:
        """The frame anchor for the legend."""
        return cast(FrameAnchor, self.config["_frame_anchor"])


def legend(
    legend: Literal["color", "opacity", "symbol"],
    *,
    columns: Literal["auto"] | int | None = "auto",
    label: str | None = None,
    target: Selection | None = None,
    field: str | None = None,
    width: float | None = None,
    height: float | None = None,
    tick_size: float | None = None,
    margin_bottom: float | None = None,
    margin_left: float | None = None,
    margin_right: float | None = None,
    margin_top: float | None = None,
    for_plot: str | None = None,
    frame_anchor: FrameAnchor | None = None,
    inset: float | None = None,
    inset_x: float | None = None,
    inset_y: float | None = None,
    border: str | bool = True,
    background: str | bool = True,
) -> Legend:
    """Create a legend.

    Args:
      legend: Legend type (`"color"`, `"opacity"`, or `"symbol"`).
      label: The legend label.
      columns: The number of columns to use to layout a discrete legend
        (defaults to "auto", which uses 1 column for location "left" or "right")
      target: The target selection. If specified, the legend is interactive,
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
      frame_anchor: Where to position the relative the plot frame. Defaults to "right".
      inset: The inset of the legend from the plot frame, in pixels. If no inset is specified, the legend will be positioned outside the plot frame.
      inset_x: The horizontal inset of the legend from the plot frame, in pixels.
      inset_y: The vertical inset of the legend from the plot frame, in pixels.
      border: The border color for the legend. Pass 'True' to use the default border color, or a string to specify a custom color. Pass 'False' to disable the border. Defaults to `True`.
      background: The background color for the legend. Pass 'True' to use the default background color, or a string to specify a custom color. Pass 'False' to disable the background. Defaults to `True`.
    """
    config: dict[str, JsonValue] = {}
    if label is not None:
        config["label"] = label
    if target is not None:
        config["as"] = target
    if field is not None:
        config["field"] = field
    if width is not None:
        config["width"] = width
    if height is not None:
        config["height"] = height
    if margin_bottom is not None:
        config["marginBottom"] = margin_bottom
    if margin_left is not None:
        config["marginLeft"] = margin_left
    if margin_right is not None:
        config["marginRight"] = margin_right
    if margin_top is not None:
        config["marginTop"] = margin_top
    if tick_size is not None:
        config["tickSize"] = tick_size
    if for_plot is not None:
        config["for"] = for_plot

    # Forward options
    config["_inset"] = inset
    config["_inset_x"] = inset_x
    config["_inset_y"] = inset_y
    config["_border"] = border
    config["_background"] = background

    return Legend(legend, columns, frame_anchor or "right", config=config)
