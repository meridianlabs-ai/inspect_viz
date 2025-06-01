from pydantic import JsonValue

from inspect_viz._util.marshall import dict_remove_none

from .._core.component import Component
from .._core.selection import Selection
from .brush import Brush, brush_as_camel


class Interactor(Component):
    """Interactors imbue plots with interactive behavior, such as selecting or highlighting values, and panning or zooming the display."""

    def __init__(self, select: str, config: dict[str, JsonValue]) -> None:
        interactor: dict[str, JsonValue] = {"select": select}
        super().__init__(interactor | config)


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
       opacity: The overall opacity of deemphasized marks. By default the
         opacity is set to 0.2.
       fill_opacity: The fill opacity of deemphasized marks. By default the
         fill opacity is unchanged.
       stroke_opacity: The stroke opacity of deemphasized marks. By default
         the stroke opacity is unchanged.
       fill: The fill color of deemphasized marks. By default the fill is
         unchanged.
       stroke: The stroke color of deemphasized marks. By default the stroke
         is unchanged.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "by": by,
            "opacity": opacity,
            "fill": fill,
            "fillOpacity": fill_opacity,
            "stroke": stroke,
            "strokeOpacity": stroke_opacity,
        }
    )

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
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "as": selection,
            "field": field,
            "pixelSize": pixel_size,
            "peers": peers,
            "brush": brush_as_camel(brush) if brush is not None else None,
        }
    )

    return Interactor("intervalX", config)


def interval_y(
    selection: Selection,
    field: str | None = None,
    pixel_size: float | None = None,
    peers: bool | None = None,
    brush: Brush | None = None,
) -> Interactor:
    """Select a continuous 1D interval selection over the `y` scale domain.

    Args:
       selection: The output selection. A clause of the form `field BETWEEN
         lo AND hi` is added for the currently selected interval [lo, hi].
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
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "as": selection,
            "field": field,
            "pixelSize": pixel_size,
            "peers": peers,
            "brush": brush_as_camel(brush) if brush is not None else None,
        }
    )

    return Interactor("intervalY", config)


def toggle(
    selection: Selection,
    channels: list[str],
    peers: bool | None = None,
) -> Interactor:
    """Select individal values.

    Args:
       selection: The output selection. A clause of the form `(field = value1) OR (field = value2) ...` is added for the currently selected values.
       channels: The encoding channels over which to select values. For a selected mark, selection clauses will cover the backing data fields for each channel.
       peers: A flag indicating if peer (sibling) marks are excluded when
         cross-filtering (default `true`). If set, peer marks will not be
         filtered by this interactor's selection in cross-filtering setups.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "as": selection,
            "channels": channels,
            "peers": peers,
        }
    )

    return Interactor("toggle", config)


def toggle_x(
    selection: Selection,
    peers: bool | None = None,
) -> Interactor:
    """Select individal values in the `x` scale domain. Clicking or touching a mark toggles its selection status.

    Args:
       selection: The output selection. A clause of the form `(field = value1) OR (field = value2) ...` is added for the currently selected values.
       peers: A flag indicating if peer (sibling) marks are excluded when
         cross-filtering (default `true`). If set, peer marks will not be
         filtered by this interactor's selection in cross-filtering setups.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "as": selection,
            "peers": peers,
        }
    )

    return Interactor("toggleX", config)


def toggle_color(
    selection: Selection,
    peers: bool | None = None,
) -> Interactor:
    """Select individal values in the `color` scale domain. Clicking or touching a mark toggles its selection status.

    Args:
       selection: The output selection. A clause of the form `(field = value1) OR (field = value2) ...` is added for the currently selected values.
       peers: A flag indicating if peer (sibling) marks are excluded when
         cross-filtering (default `true`). If set, peer marks will not be
         filtered by this interactor's selection in cross-filtering setups.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "as": selection,
            "peers": peers,
        }
    )

    return Interactor("toggleColor", config)


def toggle_y(
    selection: Selection,
    peers: bool | None = None,
) -> Interactor:
    """Toggle interactor over the `"y"` encoding channel only.

    Args:
       selection: The output selection. A clause of the form `(field = value1) OR (field = value2) ...` is added for the currently selected values.
       peers: A flag indicating if peer (sibling) marks are excluded when
         cross-filtering (default `true`). If set, peer marks will not be
         filtered by this interactor's selection in cross-filtering setups.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "as": selection,
            "peers": peers,
        }
    )
    return Interactor("toggleY", config)
