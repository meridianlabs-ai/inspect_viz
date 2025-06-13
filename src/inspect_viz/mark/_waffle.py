from typing import Any, Literal, Sequence

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._core.types import Interval
from .._util.marshall import dict_remove_none
from ._channel import Channel
from ._mark import Mark, MarkOptions
from ._util import column_param


def waffle_x(
    data: Data,
    x: Channel | Param,
    x1: Channel | Param | None = None,
    x2: Channel | Param | None = None,
    y: Channel | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    multiple: float | Param | None = None,
    unit: float | Param | None = None,
    gap: float | Param | None = None,
    round: bool | Param | None = None,
    interval: Interval | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A waffleX mark that creates horizontal waffle charts.

    Waffle charts are a form of unit chart where data is represented as a grid
    of small squares or rectangles, useful for showing part-to-whole relationships
    and making proportions more tangible.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        x1: The starting horizontal position channel, typically bound to the *x* scale.
        x2: The ending horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        z: The **z** channel defines the series of each value in the stack.
        filter_by: A selection to filter the data.
        multiple: The number of units per tile; defaults to 1.
        unit: The size of each unit in the waffle; defaults to 1.
        gap: The gap between waffle units; defaults to 1.
        round: Whether to round values to the nearest unit; defaults to false.
        interval: How to convert a continuous value into an interval.
        offset: After stacking, an optional **offset** can be applied to translate and scale stacks.
        order: The order in which stacks are layered.
        inset: Shorthand to set the same default for all four insets.
        inset_top: Insets the top edge by the specified number of pixels.
        inset_right: Insets the right edge by the specified number of pixels.
        inset_bottom: Insets the bottom edge by the specified number of pixels.
        inset_left: Insets the left edge by the specified number of pixels.
        rx: The rounded corner x-radius, either in pixels or as a percentage.
        ry: The rounded corner y-radius, either in pixels or as a percentage.
        **options: Additional mark options from MarkOptions.

    Returns:
        A waffleX mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            x1=column_param(data, x1),
            x2=column_param(data, x2),
            y=column_param(data, y),
            z=column_param(data, z),
            multiple=multiple,
            unit=unit,
            gap=gap,
            round=round,
            interval=interval,
            offset=offset,
            order=order,
            inset=inset,
            insetTop=inset_top,
            insetRight=inset_right,
            insetBottom=inset_bottom,
            insetLeft=inset_left,
            rx=rx,
            ry=ry,
        )
    )

    return Mark("waffleX", config, options)


def waffle_y(
    data: Data,
    y: Channel | Param,
    y1: Channel | Param | None = None,
    y2: Channel | Param | None = None,
    x: Channel | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    multiple: float | Param | None = None,
    unit: float | Param | None = None,
    gap: float | Param | None = None,
    round: bool | Param | None = None,
    interval: Interval | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A waffleY mark that creates vertical waffle charts.

    Waffle charts are a form of unit chart where data is represented as a grid
    of small squares or rectangles, useful for showing part-to-whole relationships
    and making proportions more tangible.

    Args:
        data: The data source for the mark.
        y: The vertical position channel, typically bound to the *y* scale.
        y1: The starting vertical position channel, typically bound to the *y* scale.
        y2: The ending vertical position channel, typically bound to the *y* scale.
        x: The horizontal position channel, typically bound to the *x* scale.
        z: The **z** channel defines the series of each value in the stack.
        filter_by: A selection to filter the data.
        multiple: The number of units per tile; defaults to 1.
        unit: The size of each unit in the waffle; defaults to 1.
        gap: The gap between waffle units; defaults to 1.
        round: Whether to round values to the nearest unit; defaults to false.
        interval: How to convert a continuous value into an interval.
        offset: After stacking, an optional **offset** can be applied to translate and scale stacks.
        order: The order in which stacks are layered.
        inset: Shorthand to set the same default for all four insets.
        inset_top: Insets the top edge by the specified number of pixels.
        inset_right: Insets the right edge by the specified number of pixels.
        inset_bottom: Insets the bottom edge by the specified number of pixels.
        inset_left: Insets the left edge by the specified number of pixels.
        rx: The rounded corner x-radius, either in pixels or as a percentage.
        ry: The rounded corner y-radius, either in pixels or as a percentage.
        **options: Additional mark options from MarkOptions.

    Returns:
        A waffleY mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            y=column_param(data, y),
            y1=column_param(data, y1),
            y2=column_param(data, y2),
            x=column_param(data, x),
            z=column_param(data, z),
            multiple=multiple,
            unit=unit,
            gap=gap,
            round=round,
            interval=interval,
            offset=offset,
            order=order,
            inset=inset,
            insetTop=inset_top,
            insetRight=inset_right,
            insetBottom=inset_bottom,
            insetLeft=inset_left,
            rx=rx,
            ry=ry,
        )
    )

    return Mark("waffleY", config, options)
