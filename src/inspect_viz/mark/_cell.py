from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ._channel import ChannelValueSpec
from ._mark import Mark
from ._options import MarkOptions
from ._util import column_param


def cell(
    data: Data,
    x: ChannelValueSpec | Param | None = None,
    y: ChannelValueSpec | Param | None = None,
    filter_by: Selection | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A cell mark that draws axis-aligned rectangles for categorical data.

    Cells are typically used to create heatmaps and other grid-based visualizations
    where both x and y represent categorical or ordinal data.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        filter_by: A selection to filter the data.
        inset: Shorthand to set the same default for all four insets.
        inset_top: Insets the top edge by the specified number of pixels.
        inset_right: Insets the right edge by the specified number of pixels.
        inset_bottom: Insets the bottom edge by the specified number of pixels.
        inset_left: Insets the left edge by the specified number of pixels.
        rx: The rounded corner x-radius, either in pixels or as a percentage of the cell width.
        ry: The rounded corner y-radius, either in pixels or as a percentage of the cell height.
        **options: Additional mark options from MarkOptions.

    Returns:
        A cell mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            inset=inset,
            insetTop=inset_top,
            insetRight=inset_right,
            insetBottom=inset_bottom,
            insetLeft=inset_left,
            rx=rx,
            ry=ry,
        )
    )

    return Mark("cell", config, options)


def cell_x(
    data: Data,
    x: ChannelValueSpec | Param | None = None,
    y: ChannelValueSpec | Param | None = None,
    filter_by: Selection | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A cellX mark that draws axis-aligned rectangles with ordinal positioning.

    The *x* values should be ordinal (categories), and the optional *y* values should also be ordinal.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        filter_by: A selection to filter the data.
        inset: Shorthand to set the same default for all four insets.
        inset_top: Insets the top edge by the specified number of pixels.
        inset_right: Insets the right edge by the specified number of pixels.
        inset_bottom: Insets the bottom edge by the specified number of pixels.
        inset_left: Insets the left edge by the specified number of pixels.
        rx: The rounded corner x-radius, either in pixels or as a percentage of the cell width.
        ry: The rounded corner y-radius, either in pixels or as a percentage of the cell height.
        **options: Additional mark options from MarkOptions.

    Returns:
        A cellX mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            inset=inset,
            insetTop=inset_top,
            insetRight=inset_right,
            insetBottom=inset_bottom,
            insetLeft=inset_left,
            rx=rx,
            ry=ry,
        )
    )

    return Mark("cellX", config, options)


def cell_y(
    data: Data,
    x: ChannelValueSpec | Param | None = None,
    y: ChannelValueSpec | Param | None = None,
    filter_by: Selection | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A cellY mark that draws axis-aligned rectangles with ordinal positioning.

    The *y* values should be ordinal (categories), and the optional *x* values should also be ordinal.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        filter_by: A selection to filter the data.
        inset: Shorthand to set the same default for all four insets.
        inset_top: Insets the top edge by the specified number of pixels.
        inset_right: Insets the right edge by the specified number of pixels.
        inset_bottom: Insets the bottom edge by the specified number of pixels.
        inset_left: Insets the left edge by the specified number of pixels.
        rx: The rounded corner x-radius, either in pixels or as a percentage of the cell width.
        ry: The rounded corner y-radius, either in pixels or as a percentage of the cell height.
        **options: Additional mark options from MarkOptions.

    Returns:
        A cellY mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            inset=inset,
            insetTop=inset_top,
            insetRight=inset_right,
            insetBottom=inset_bottom,
            insetLeft=inset_left,
            rx=rx,
            ry=ry,
        )
    )

    return Mark("cellY", config, options)
