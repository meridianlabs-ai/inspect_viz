from pydantic import JsonValue

from .._core.component import Component
from .._core.selection import Selection
from .._util.marshall import dict_remove_none
from ._brush import Brush, brush_as_camel


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


def interval_xy(
    selection: Selection,
    xfield: str | None = None,
    yfield: str | None = None,
    pixel_size: float | None = None,
    peers: bool | None = None,
    brush: Brush | None = None,
) -> Interactor:
    """Select a continuous 2D interval selection over the `x` and `y` scale domains.

    Args:
       selection: The output selection. A clause of the form `(xfield BETWEEN x1 AND x2) AND (yfield BETWEEN y1 AND y2)` is added for the currently selected intervals.
       xfield: The name of the field (database column) over which the `x`-component of the interval selection should be defined. If unspecified, the `x` channel field of the first valid prior mark definition is used.
       yfield: The name of the field (database column) over which the `y`-component of the interval selection should be defined. If unspecified, the `y` channel field of the first valid prior mark definition is used.
       pixel_size: The size of an interative pixel (default `1`). Larger pixel sizes reduce the brush resolution, which can reduce the size of pre-aggregated materialized views.
       peers: A flag indicating if peer (sibling) marks are excluded when cross-filtering (default `true`). If set, peer marks will not be filtered by this interactor's selection in cross-filtering setups.
       brush: CSS styles for the brush (SVG `rect`) element.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "as": selection,
            "xfield": xfield,
            "yfield": yfield,
            "pixelSize": pixel_size,
            "peers": peers,
            "brush": brush_as_camel(brush) if brush is not None else None,
        }
    )

    return Interactor("intervalXY", config)


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


def nearest_x(
    selection: Selection,
    channels: list[str] | None = None,
    fields: list[str] | None = None,
    max_radius: float | None = None,
) -> Interactor:
    """Select values from the mark closest to the pointer *x* location.

    Args:
       selection: The output selection. A clause of the form `field = value` is added for the currently nearest value.
       channels: The encoding channels whose domain values should be selected. For example, a setting of `['color']` selects the data value backing the color channel, whereas `['x', 'z']` selects both x and z channel domain values. If unspecified, the selected channels default to match the current pointer settings: a `nearestX` interactor selects the `['x']` channels, while a `nearest` interactor selects the `['x', 'y']` channels.
       fields: The fields (database column names) to use in generated selection clause predicates. If unspecified, the fields backing the selected *channels* in the first valid prior mark definition are used by default.
       max_radius: The maximum radius of a nearest selection (default 40). Marks with (x, y) coordinates outside this radius will not be selected as nearest points.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "as": selection,
            "channels": channels,
            "fields": fields,
            "maxRadius": max_radius,
        }
    )

    return Interactor("nearestX", config)


def nearest_y(
    selection: Selection,
    channels: list[str] | None = None,
    fields: list[str] | None = None,
    max_radius: float | None = None,
) -> Interactor:
    """Select values from the mark closest to the pointer *y* location.

    Args:
       selection: The output selection. A clause of the form `field = value` is added for the currently nearest value.
       channels: The encoding channels whose domain values should be selected. For example, a setting of `['color']` selects the data value backing the color channel, whereas `['x', 'z']` selects both x and z channel domain values. If unspecified, the selected channels default to match the current pointer settings: a `nearestX` interactor selects the `['x']` channels, while a `nearest` interactor selects the `['x', 'y']` channels.
       fields: The fields (database column names) to use in generated selection clause predicates. If unspecified, the fields backing the selected *channels* in the first valid prior mark definition are used by default.
       max_radius: The maximum radius of a nearest selection (default 40). Marks with (x, y) coordinates outside this radius will not be selected as nearest points.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "as": selection,
            "channels": channels,
            "fields": fields,
            "maxRadius": max_radius,
        }
    )

    return Interactor("nearestY", config)


def region(
    selection: Selection,
    channels: list[str],
    peers: bool | None = None,
    brush: Brush | None = None,
) -> Interactor:
    """Select aspects of individual marks within a 2D range.

    Args:
       selection: The output selection. A clause of the form `(field = value1) OR (field = value2) ...` is added for the currently selected values.
       channels: The encoding channels over which to select values (e.g. "x", "y", "color", etc.). For a selected mark, selection clauses will cover the backing data fields for each channel.
       peers: A flag indicating if peer (sibling) marks are excluded when
         cross-filtering (default `true`). If set, peer marks will not be
         filtered by this interactor's selection in cross-filtering setups.
       brush: CSS styles for the brush (SVG `rect`) element.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "as": selection,
            "channels": channels,
            "peers": peers,
            "brush": brush_as_camel(brush) if brush is not None else None,
        }
    )

    return Interactor("region", config)


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


def pan(
    x: Selection | None = None,
    y: Selection | None = None,
    xfield: str | None = None,
    yfield: str | None = None,
) -> Interactor:
    """Pan a plot along both the `x` and `y` scales.

    Args:
       x: The output selection for the `x` domain. A clause of the form `field BETWEEN x1 AND x2` is added for the current pan/zom interval [x1, x2].
       y: The output selection for the `y` domain. A clause of the form `field BETWEEN y1 AND y2` is added for the current pan/zom interval [y1, y2].
       xfield: The name of the field (database column) over which the `x`-component of the pan/zoom interval should be defined. If unspecified, the `x` channel field of the first valid prior mark definition is used.
       yfield: The name of the field (database column) over which the `y`-component of the pan/zoom interval should be defined. If unspecified, the `y` channel field of the first valid prior mark definition is used.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "x": x,
            "y": y,
            "xfield": xfield,
            "yfield": yfield,
        }
    )
    return Interactor("pan", config)


def pan_x(
    x: Selection | None = None,
    y: Selection | None = None,
    xfield: str | None = None,
    yfield: str | None = None,
) -> Interactor:
    """Pan a plot along the `x` scale only.

    Args:
       x: The output selection for the `x` domain. A clause of the form `field BETWEEN x1 AND x2` is added for the current pan/zom interval [x1, x2].
       y: The output selection for the `y` domain. A clause of the form `field BETWEEN y1 AND y2` is added for the current pan/zom interval [y1, y2].
       xfield: The name of the field (database column) over which the `x`-component of the pan/zoom interval should be defined. If unspecified, the `x` channel field of the first valid prior mark definition is used.
       yfield: The name of the field (database column) over which the `y`-component of the pan/zoom interval should be defined. If unspecified, the `y` channel field of the first valid prior mark definition is used.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "x": x,
            "y": y,
            "xfield": xfield,
            "yfield": yfield,
        }
    )
    return Interactor("panX", config)


def pan_y(
    x: Selection | None = None,
    y: Selection | None = None,
    xfield: str | None = None,
    yfield: str | None = None,
) -> Interactor:
    """Pan a plot along the `y` scale only.

    Args:
       x: The output selection for the `x` domain. A clause of the form `field BETWEEN x1 AND x2` is added for the current pan/zom interval [x1, x2].
       y: The output selection for the `y` domain. A clause of the form `field BETWEEN y1 AND y2` is added for the current pan/zom interval [y1, y2].
       xfield: The name of the field (database column) over which the `x`-component of the pan/zoom interval should be defined. If unspecified, the `x` channel field of the first valid prior mark definition is used.
       yfield: The name of the field (database column) over which the `y`-component of the pan/zoom interval should be defined. If unspecified, the `y` channel field of the first valid prior mark definition is used.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "x": x,
            "y": y,
            "xfield": xfield,
            "yfield": yfield,
        }
    )
    return Interactor("panY", config)


def pan_zoom(
    x: Selection | None = None,
    y: Selection | None = None,
    xfield: str | None = None,
    yfield: str | None = None,
) -> Interactor:
    """Pan and zoom a plot along both the `x` and `y` scales.

    Args:
       x: The output selection for the `x` domain. A clause of the form `field BETWEEN x1 AND x2` is added for the current pan/zom interval [x1, x2].
       y: The output selection for the `y` domain. A clause of the form `field BETWEEN y1 AND y2` is added for the current pan/zom interval [y1, y2].
       xfield: The name of the field (database column) over which the `x`-component of the pan/zoom interval should be defined. If unspecified, the `x` channel field of the first valid prior mark definition is used.
       yfield: The name of the field (database column) over which the `y`-component of the pan/zoom interval should be defined. If unspecified, the `y` channel field of the first valid prior mark definition is used.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "x": x,
            "y": y,
            "xfield": xfield,
            "yfield": yfield,
        }
    )
    return Interactor("panZoom", config)


def pan_zoom_x(
    x: Selection | None = None,
    y: Selection | None = None,
    xfield: str | None = None,
    yfield: str | None = None,
) -> Interactor:
    """Pan and zoom a plot along the `x` scale only.

    Args:
       x: The output selection for the `x` domain. A clause of the form `field BETWEEN x1 AND x2` is added for the current pan/zom interval [x1, x2].
       y: The output selection for the `y` domain. A clause of the form `field BETWEEN y1 AND y2` is added for the current pan/zom interval [y1, y2].
       xfield: The name of the field (database column) over which the `x`-component of the pan/zoom interval should be defined. If unspecified, the `x` channel field of the first valid prior mark definition is used.
       yfield: The name of the field (database column) over which the `y`-component of the pan/zoom interval should be defined. If unspecified, the `y` channel field of the first valid prior mark definition is used.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "x": x,
            "y": y,
            "xfield": xfield,
            "yfield": yfield,
        }
    )
    return Interactor("panZoomX", config)


def pan_zoom_y(
    x: Selection | None = None,
    y: Selection | None = None,
    xfield: str | None = None,
    yfield: str | None = None,
) -> Interactor:
    """Pan and zoom a plot along the `y` scale only.

    Args:
       x: The output selection for the `x` domain. A clause of the form `field BETWEEN x1 AND x2` is added for the current pan/zom interval [x1, x2].
       y: The output selection for the `y` domain. A clause of the form `field BETWEEN y1 AND y2` is added for the current pan/zom interval [y1, y2].
       xfield: The name of the field (database column) over which the `x`-component of the pan/zoom interval should be defined. If unspecified, the `x` channel field of the first valid prior mark definition is used.
       yfield: The name of the field (database column) over which the `y`-component of the pan/zoom interval should be defined. If unspecified, the `y` channel field of the first valid prior mark definition is used.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "x": x,
            "y": y,
            "xfield": xfield,
            "yfield": yfield,
        }
    )
    return Interactor("panZoomY", config)
