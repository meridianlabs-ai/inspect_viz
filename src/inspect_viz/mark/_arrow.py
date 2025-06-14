from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ._channel import ChannelValueSpec
from ._mark import Mark
from ._options import MarkOptions
from ._util import column_param


def arrow(
    data: Data,
    x: ChannelValueSpec | Param | None = None,
    y: ChannelValueSpec | Param | None = None,
    x1: ChannelValueSpec | Param | None = None,
    y1: ChannelValueSpec | Param | None = None,
    x2: ChannelValueSpec | Param | None = None,
    y2: ChannelValueSpec | Param | None = None,
    filter_by: Selection | None = None,
    bend: float | bool | Param | None = None,
    head_angle: float | Param | None = None,
    head_length: float | Param | None = None,
    inset: float | Param | None = None,
    inset_start: float | Param | None = None,
    inset_end: float | Param | None = None,
    sweep: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """An arrow mark.

    The arrow mark draws arrows between two points, with customizable arrowheads and curved paths.
    It is useful for indicating direction, flow, or relationships between data points.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, shorthand for both x1 and x2.
        y: The vertical position channel, shorthand for both y1 and y2.
        x1: The starting horizontal position of the arrow.
        y1: The starting vertical position of the arrow.
        x2: The ending horizontal position of the arrow.
        y2: The ending vertical position of the arrow.
        filter_by: Selection to filter by (defaults to data source selection).
        options: Additional `MarkOptions`.
        bend: The angle between straight line and outgoing tangent (±90°, use True for 22.5°).
        head_angle: How pointy the arrowhead is in degrees (0°-180°, defaults to 60°).
        head_length: Size of arrowhead relative to stroke width.
        inset: Shorthand for both inset_start and inset_end.
        inset_start: Starting inset in pixels (defaults to 0).
        inset_end: Ending inset in pixels (defaults to 0).
        sweep: Sweep order (1=clockwise, -1=anticlockwise, 0=no bend).
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            x1=column_param(data, x1),
            y1=column_param(data, y1),
            x2=column_param(data, x2),
            y2=column_param(data, y2),
            bend=bend,
            headAngle=head_angle,
            headLength=head_length,
            inset=inset,
            insetStart=inset_start,
            insetEnd=inset_end,
            sweep=sweep,
        )
    )

    return Mark("arrow", config, options)
