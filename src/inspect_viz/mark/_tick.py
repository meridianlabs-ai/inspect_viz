from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ..transform._column import column
from ._channel import ChannelValueSpec
from ._mark import Mark
from ._options import MarkOptions
from ._types import Marker
from ._util import column_param


def tick_x(
    data: Data,
    x: ChannelValueSpec | Param,
    y: ChannelValueSpec | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A tickX mark that draws horizontal tick marks.

    TickX marks are horizontal lines typically used for marking positions
    along the x-axis or creating horizontal reference lines.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        filter_by: A selection to filter the data.
        marker: The marker symbol to use at all positions along the tick.
        marker_start: The marker symbol to use at the start of the tick.
        marker_mid: The marker symbol to use at the middle of the tick.
        marker_end: The marker symbol to use at the end of the tick.
        inset: Shorthand to set the same default for top and bottom insets.
        inset_top: Insets the top edge by the specified number of pixels.
        inset_bottom: Insets the bottom edge by the specified number of pixels.
        **options: Additional mark options from MarkOptions.

    Returns:
        A tickX mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            marker=marker,
            markerStart=marker_start,
            markerMid=marker_mid,
            markerEnd=marker_end,
            inset=inset,
            insetTop=inset_top,
            insetBottom=inset_bottom,
        )
    )

    return Mark("tickX", config, options)


def tick_y(
    data: Data,
    y: ChannelValueSpec | Param,
    x: ChannelValueSpec | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    inset: float | Param | None = None,
    inset_left: float | Param | None = None,
    inset_right: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A tickY mark that draws vertical tick marks.

    TickY marks are vertical lines typically used for marking positions
    along the y-axis or creating vertical reference lines.

    Args:
        data: The data source for the mark.
        y: The vertical position channel, typically bound to the *y* scale.
        x: The horizontal position channel, typically bound to the *x* scale.
        filter_by: A selection to filter the data.
        marker: The marker symbol to use at all positions along the tick.
        marker_start: The marker symbol to use at the start of the tick.
        marker_mid: The marker symbol to use at the middle of the tick.
        marker_end: The marker symbol to use at the end of the tick.
        inset: Shorthand to set the same default for left and right insets.
        inset_left: Insets the left edge by the specified number of pixels.
        inset_right: Insets the right edge by the specified number of pixels.
        **options: Additional mark options from MarkOptions.

    Returns:
        A tickY mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            y=column(y) if isinstance(y, str) else y,
            x=column(x) if isinstance(x, str) else x,
            marker=marker,
            markerStart=marker_start,
            markerMid=marker_mid,
            markerEnd=marker_end,
            inset=inset,
            insetLeft=inset_left,
            insetRight=inset_right,
        )
    )

    return Mark("tickY", config, options)
