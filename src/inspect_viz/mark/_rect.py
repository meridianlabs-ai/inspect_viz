from typing import Any, Literal, Sequence

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._core.types import Interval
from .._util.marshall import dict_remove_none
from ..transform._column import column
from ._channel import Channel
from ._mark import Mark, MarkOptions
from ._util import column_param


def rect(
    data: Data,
    x: Channel | Param | None = None,
    x1: Channel | Param | None = None,
    x2: Channel | Param | None = None,
    y: Channel | Param | None = None,
    y1: Channel | Param | None = None,
    y2: Channel | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    interval: Interval | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A rect mark that draws axis-aligned rectangles.

    Both *x* and *y* should be quantitative or temporal; rect does not perform
    grouping, so use rectX or rectY for ordinal data.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        x1: The starting horizontal position channel, typically bound to the *x* scale.
        x2: The ending horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        y1: The starting vertical position channel, typically bound to the *y* scale.
        y2: The ending vertical position channel, typically bound to the *y* scale.
        z: The **z** channel defines the series of each value in the stack
        filter_by: A selection to filter the data.
        interval: How to convert a continuous value into an interval; one of:
            - a named time interval such as *day* (for date intervals)
            - a number (for number intervals), defining intervals at integer multiples of *n*
        inset: Shorthand to set the same default for all four insets.
        inset_top: Insets the top edge by the specified number of pixels.
        inset_right: Insets the right edge by the specified number of pixels.
        inset_bottom: Insets the bottom edge by the specified number of pixels.
        inset_left: Insets the left edge by the specified number of pixels.
        rx: The rounded corner x-radius, either in pixels or as a percentage of the rect width.
        ry: The rounded corner y-radius, either in pixels or as a percentage of the rect height.
        offset: After stacking, an optional **offset** can be applied to translate and scale stacks.
        order: The order in which stacks are layered; one of:
            - null (default) for input order
            - a named stack order method such as *inside-out* or *sum*
            - a field name, for natural order of the corresponding values
            - a function of data, for natural order of the corresponding values
            - an array of explicit **z** values in the desired order.
        **options: Additional mark options from MarkOptions.

    Returns:
        A rect mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            x1=column_param(data, x1),
            x2=column_param(data, x2),
            y=column_param(data, y),
            y1=column_param(data, y1),
            y2=column_param(data, y2),
            z=column_param(data, z),
            interval=interval,
            inset=inset,
            insetTop=inset_top,
            insetRight=inset_right,
            insetBottom=inset_bottom,
            insetLeft=inset_left,
            rx=rx,
            ry=ry,
            offset=offset,
            order=order,
        )
    )

    return Mark("rect", config, options)


def rect_x(
    data: Data,
    x: Channel | Param | None = None,
    x1: Channel | Param | None = None,
    x2: Channel | Param | None = None,
    y: Channel | Param | None = None,
    y1: Channel | Param | None = None,
    y2: Channel | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    interval: Interval | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A rectX mark that draws axis-aligned rectangles.

    The *x* values should be quantitative or temporal, and the optional *y* values should be ordinal.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        x1: The starting horizontal position channel, typically bound to the *x* scale.
        x2: The ending horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        y1: The starting vertical position channel, typically bound to the *y* scale.
        y2: The ending vertical position channel, typically bound to the *y* scale.
        z: The **z** channel defines the series of each value in the stack.
        filter_by: A selection to filter the data.
        interval: How to convert a continuous value into an interval; one of:
            - a named time interval such as *day* (for date intervals)
            - a number (for number intervals), defining intervals at integer multiples of *n*
        inset: Shorthand to set the same default for all four insets.
        inset_top: Insets the top edge by the specified number of pixels.
        inset_right: Insets the right edge by the specified number of pixels.
        inset_bottom: Insets the bottom edge by the specified number of pixels.
        inset_left: Insets the left edge by the specified number of pixels.
        rx: The rounded corner x-radius, either in pixels or as a percentage of the rect width.
        ry: The rounded corner y-radius, either in pixels or as a percentage of the rect height.
        offset: After stacking, an optional **offset** can be applied to translate and scale stacks.
        order: The order in which stacks are layered; one of:
            - null (default) for input order
            - a named stack order method such as *inside-out* or *sum*
            - a field name, for natural order of the corresponding values
            - a function of data, for natural order of the corresponding values
            - an array of explicit **z** values in the desired order
        **options: Additional mark options from MarkOptions.

    Returns:
        A rectX mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column(x) if isinstance(x, str) else x,
            x1=column(x1) if isinstance(x1, str) else x1,
            x2=column(x2) if isinstance(x2, str) else x2,
            y=column(y) if isinstance(y, str) else y,
            y1=column(y1) if isinstance(y1, str) else y1,
            y2=column(y2) if isinstance(y2, str) else y2,
            interval=interval,
            inset=inset,
            insetTop=inset_top,
            insetRight=inset_right,
            insetBottom=inset_bottom,
            insetLeft=inset_left,
            rx=rx,
            ry=ry,
            offset=offset,
            order=order,
            z=column(z) if isinstance(z, str) else z,
        )
    )

    return Mark("rectX", config, options)


def rect_y(
    data: Data,
    x: Channel | Param | None = None,
    x1: Channel | Param | None = None,
    x2: Channel | Param | None = None,
    y: Channel | Param | None = None,
    y1: Channel | Param | None = None,
    y2: Channel | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    interval: Interval | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A rectY mark that draws axis-aligned rectangles.

    The *y* values should be quantitative or temporal, and the optional *x* values should be ordinal.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        x1: The starting horizontal position channel, typically bound to the *x* scale.
        x2: The ending horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        y1: The starting vertical position channel, typically bound to the *y* scale.
        y2: The ending vertical position channel, typically bound to the *y* scale.
        z: The **z** channel defines the series of each value in the stack.
        filter_by: A selection to filter the data.
        interval: How to convert a continuous value into an interval; one of:
            - a named time interval such as *day* (for date intervals)
            - a number (for number intervals), defining intervals at integer multiples of *n*
        inset: Shorthand to set the same default for all four insets.
        inset_top: Insets the top edge by the specified number of pixels.
        inset_right: Insets the right edge by the specified number of pixels.
        inset_bottom: Insets the bottom edge by the specified number of pixels.
        inset_left: Insets the left edge by the specified number of pixels.
        rx: The rounded corner x-radius, either in pixels or as a percentage of the rect width.
        ry: The rounded corner y-radius, either in pixels or as a percentage of the rect height.
        offset: After stacking, an optional **offset** can be applied to translate and scale stacks.
        order: The order in which stacks are layered; one of:
            - null (default) for input order
            - a named stack order method such as *inside-out* or *sum*
            - a field name, for natural order of the corresponding values
            - a function of data, for natural order of the corresponding values
            - an array of explicit **z** values in the desired order
        **options: Additional mark options from MarkOptions.

    Returns:
        A rectY mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column(x) if isinstance(x, str) else x,
            x1=column(x1) if isinstance(x1, str) else x1,
            x2=column(x2) if isinstance(x2, str) else x2,
            y=column(y) if isinstance(y, str) else y,
            y1=column(y1) if isinstance(y1, str) else y1,
            y2=column(y2) if isinstance(y2, str) else y2,
            interval=interval,
            inset=inset,
            insetTop=inset_top,
            insetRight=inset_right,
            insetBottom=inset_bottom,
            insetLeft=inset_left,
            rx=rx,
            ry=ry,
            offset=offset,
            order=order,
            z=column(z) if isinstance(z, str) else z,
        )
    )

    return Mark("rectY", config, options)
