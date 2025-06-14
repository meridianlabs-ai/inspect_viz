from typing import Any, Literal

from typing_extensions import Unpack

from .._core import Param
from .._util.marshall import dict_remove_none
from ._mark import Mark
from ._options import MarkOptions


def frame(
    anchor: Literal["top", "right", "bottom", "left"] | Param | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: str | float | Param | None = None,
    ry: str | float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a frame mark that draws a rectangular outline around the plot area.

    The frame mark draws a rectangular border around the plot's frame area. By default,
    it draws a complete rectangular outline, but when an anchor is specified, it draws
    only a line on the given side (ignoring rx, ry, fill, and fillOpacity).

    The frame mark is commonly used for visual separation of facets, providing
    backgrounds for plot areas, or creating borders around visualizations.

    Args:
        anchor: Controls how the frame is drawn. If null (default), draws a complete
            rectangular outline. If specified, draws a line only on the given side
            (*top*, *right*, *bottom*, or *left*), ignoring rx, ry, fill, and fillOpacity.
        inset: Shorthand to set the same default for all four insets.
        inset_top: Insets the top edge by the specified number of pixels. A positive
            value insets towards the bottom edge (reducing effective area), while a
            negative value insets away from the bottom edge (increasing it).
        inset_right: Insets the right edge by the specified number of pixels. A positive
            value insets towards the left edge (reducing effective area), while a
            negative value insets away from the left edge (increasing it).
        inset_bottom: Insets the bottom edge by the specified number of pixels. A positive
            value insets towards the top edge (reducing effective area), while a
            negative value insets away from the top edge (increasing it).
        inset_left: Insets the left edge by the specified number of pixels. A positive
            value insets towards the right edge (reducing effective area), while a
            negative value insets away from the right edge (increasing it).
        rx: The rounded corner x-radius, either in pixels or as a percentage of the
            frame width. If rx is not specified, it defaults to ry if present, and
            otherwise draws square corners.
        ry: The rounded corner y-radius, either in pixels or as a percentage of the
            frame height. If ry is not specified, it defaults to rx if present, and
            otherwise draws square corners.
        **options: Additional mark options from MarkOptions.

    Returns:
        A frame mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            anchor=anchor,
            inset=inset,
            insetTop=inset_top,
            insetRight=inset_right,
            insetBottom=inset_bottom,
            insetLeft=inset_left,
            rx=rx,
            ry=ry,
        )
    )

    return Mark("frame", config, options)
