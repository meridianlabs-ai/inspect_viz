from typing import Any

from pydantic import JsonValue

from .._core.component import Component
from .._core.selection import Selection
from .brush import Brush, brush_as_camel


class Interactor(Component):
    """Interactors imbue plots with interactive behavior, such as selecting or highlighting values, and panning or zooming the display."""

    def __init__(self, select: str, config: dict[str, JsonValue]) -> None:
        camel_config: dict[str, Any] = {
            key: value for key, value in config.items() if value is not None
        }
        super().__init__({"select": select} | camel_config)


def highlight(
    by: Selection,
    opacity: float | None = None,
    fill_opacity: float | None = None,
    stroke_opacity: float | None = None,
    fill: str | None = None,
    stroke: str | None = None,
) -> Interactor:
    """Highlight individual visualized data points based on a `Selection`.

    Selected values keep their normal appearance. Unselected values are deemphasized.

    Args:
       by: The input selection. Unselected marks are deemphasized.
       opacity: The overall opacity of deemphasized marks. By default the opacity is set to 0.2.
       fill_opacity: The fill opacity of deemphasized marks. By default the fill opacity is unchanged.
       stroke_opacity: The stroke opacity of deemphasized marks. By default the stroke opacity is unchanged.
       fill: The fill color of deemphasized marks. By default the fill is unchanged.
       stroke: The stroke color of deemphasized marks. By default the stroke is unchanged.


    """
    config: dict[str, JsonValue] = {
        "by": by,
        "fill": fill,
        "fillOpacity": fill_opacity,
        "opacity": opacity if opacity is not None else 0.2,
        "stroke": stroke,
        "strokeOpacity": stroke_opacity,
    }

    return Interactor("highlight", config)


def interval_x(
    selection: Selection,
    field: str | None = None,
    pixel_size: float | None = None,
    peers: bool | None = None,
    brush: Brush | None = None,
) -> Interactor:
    """Select a continuous 1D interval selection over the `x` scale domain.

    Args:
       selection: The output selection. A clause of the form `field BETWEEN
         lo AND hi` is added for the currently selected interval [lo, hi]."
       field: The name of the field (database column) over which the interval
         selection should be defined. If unspecified, the  channel field of
         the first valid prior mark definition is used.
       pixel_size: The size of an interative pixel (default `1`). Larger
         pixel sizes reduce the brush resolution, which can reduce the size
         of pre-aggregated materialized views.
       peers: A flag indicating if peer (sibling) marks are excluded when
         cross-filtering (default `true`). If set, peer marks will not be
         filtered by this interactor's selection in cross-filtering setups.
       brush: CSS styles for the brush (SVG `rect`) element.
    """
    config: dict[str, JsonValue] = {
        "as": selection,
        "field": field,
        "pixelSize": pixel_size,
        "peers": peers,
        "brush": brush_as_camel(brush) if brush is not None else None,
    }

    return Interactor("intervalX", config)
