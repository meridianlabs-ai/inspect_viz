from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ..transform._column import column
from ._channel import Channel
from ._mark import Mark, MarkOptions


def arrow(
    data: Data,
    x: Channel | Param | None = None,
    y: Channel | Param | None = None,
    x1: Channel | Param | None = None,
    y1: Channel | Param | None = None,
    x2: Channel | Param | None = None,
    y2: Channel | Param | None = None,
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
            x=column(x) if isinstance(x, str) else x,
            y=column(y) if isinstance(y, str) else y,
            x1=column(x1) if isinstance(x1, str) else x1,
            y1=column(y1) if isinstance(y1, str) else y1,
            x2=column(x2) if isinstance(x2, str) else x2,
            y2=column(y2) if isinstance(y2, str) else y2,
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
