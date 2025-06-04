from typing import Any, Sequence

from typing_extensions import Unpack

from .._core import Param
from .._core.types import Interval
from .._util.marshall import dict_remove_none
from ..transform._column import column
from ._channel import Channel
from ._mark import Mark, MarkOptions


def grid_x(
    x: Channel | Param | None = None,
    y1: Channel | Param | None = None,
    y2: Channel | Param | None = None,
    interval: Interval | None = None,
    anchor: str | Param | None = None,
    color: Channel | str | Param | None = None,
    ticks: int | Sequence[Any] | Param | None = None,
    tick_spacing: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A horizontal grid mark.

    The gridX mark draws horizontal grid lines across the plot area.
    It is primarily used for adding visual reference lines along the x-axis.

    Args:
        x: The horizontal position channel, typically bound to the *x* scale.
        y1: The primary (starting, often bottom) vertical position of the grid line.
        y2: The secondary (ending, often top) vertical position of the grid line.
        interval: How to convert a continuous value into an interval.
        anchor: The side of the frame on which to place the grid (*top* or *bottom*).
        color: Shorthand for setting both fill and stroke color.
        ticks: The desired number of ticks, or an array of tick values, or null to disable ticks.
        tick_spacing: The desired spacing between ticks in pixels.
        options: Additional `MarkOptions` (including stroke, stroke_width, stroke_opacity, stroke_dasharray).
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            x=column(x) if isinstance(x, str) else x,
            y1=column(y1) if isinstance(y1, str) else y1,
            y2=column(y2) if isinstance(y2, str) else y2,
            interval=interval,
            anchor=anchor,
            color=color,
            ticks=ticks,
            tickSpacing=tick_spacing,
        )
    )

    return Mark("gridX", config, options)


def grid_y(
    y: Channel | Param | None = None,
    x1: Channel | Param | None = None,
    x2: Channel | Param | None = None,
    interval: Interval | None = None,
    anchor: str | Param | None = None,
    color: Channel | str | Param | None = None,
    ticks: int | Sequence[Any] | Param | None = None,
    tick_spacing: float | Param | None = None,
    inset_left: float | Param | None = None,
    inset_right: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A vertical grid mark.

    The gridY mark draws vertical grid lines across the plot area.
    It is primarily used for adding visual reference lines along the y-axis.

    Args:
        y: The vertical position channel, typically bound to the *y* scale.
        x1: The primary (starting, often left) horizontal position of the grid line.
        x2: The secondary (ending, often right) horizontal position of the grid line.
        interval: How to convert a continuous value into an interval.
        anchor: The side of the frame on which to place the grid (*left* or *right*).
        color: Shorthand for setting both fill and stroke color.
        ticks: The desired number of ticks, or an array of tick values, or null to disable ticks.
        tick_spacing: The desired spacing between ticks in pixels.
        inset_left: Insets the left edge by the specified number of pixels.
        inset_right: Insets the right edge by the specified number of pixels.
        options: Additional `MarkOptions` (including stroke, stroke_width, stroke_opacity, stroke_dasharray).
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            y=column(y) if isinstance(y, str) else y,
            x1=column(x1) if isinstance(x1, str) else x1,
            x2=column(x2) if isinstance(x2, str) else x2,
            interval=interval,
            anchor=anchor,
            color=color,
            ticks=ticks,
            tickSpacing=tick_spacing,
            insetLeft=inset_left,
            insetRight=inset_right,
        )
    )

    return Mark("gridY", config, options)


def grid_fx(
    x: Channel | Param | None = None,
    y1: Channel | Param | None = None,
    y2: Channel | Param | None = None,
    interval: Interval | None = None,
    anchor: str | Param | None = None,
    color: Channel | str | Param | None = None,
    ticks: int | Sequence[Any] | Param | None = None,
    tick_spacing: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A horizontal facet grid mark.

    The gridFx mark draws horizontal grid lines for faceted plots.
    It is primarily used for adding visual reference lines along the fx-axis in faceted visualizations.

    Args:
        x: The horizontal position channel, typically bound to the *x* scale.
        y1: The primary (starting, often bottom) vertical position of the grid line.
        y2: The secondary (ending, often top) vertical position of the grid line.
        interval: How to convert a continuous value into an interval.
        anchor: The side of the frame on which to place the grid (*top* or *bottom*).
        color: Shorthand for setting both fill and stroke color.
        ticks: The desired number of ticks, or an array of tick values, or null to disable ticks.
        tick_spacing: The desired spacing between ticks in pixels.
        options: Additional `MarkOptions` (including stroke, stroke_width, stroke_opacity, stroke_dasharray).
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            x=column(x) if isinstance(x, str) else x,
            y1=column(y1) if isinstance(y1, str) else y1,
            y2=column(y2) if isinstance(y2, str) else y2,
            interval=interval,
            anchor=anchor,
            color=color,
            ticks=ticks,
            tickSpacing=tick_spacing,
        )
    )

    return Mark("gridFx", config, options)


def grid_fy(
    y: Channel | Param | None = None,
    x1: Channel | Param | None = None,
    x2: Channel | Param | None = None,
    interval: Interval | None = None,
    anchor: str | Param | None = None,
    color: Channel | str | Param | None = None,
    ticks: int | Sequence[Any] | Param | None = None,
    tick_spacing: float | Param | None = None,
    inset_left: float | Param | None = None,
    inset_right: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A vertical facet grid mark.

    The gridFy mark draws vertical grid lines for faceted plots.
    It is primarily used for adding visual reference lines along the fy-axis in faceted visualizations.

    Args:
        y: The vertical position channel, typically bound to the *y* scale.
        x1: The primary (starting, often left) horizontal position of the grid line.
        x2: The secondary (ending, often right) horizontal position of the grid line.
        interval: How to convert a continuous value into an interval.
        anchor: The side of the frame on which to place the grid (*left* or *right*).
        color: Shorthand for setting both fill and stroke color.
        ticks: The desired number of ticks, or an array of tick values, or null to disable ticks.
        tick_spacing: The desired spacing between ticks in pixels.
        inset_left: Insets the left edge by the specified number of pixels.
        inset_right: Insets the right edge by the specified number of pixels.
        options: Additional `MarkOptions` (including stroke, stroke_width, stroke_opacity, stroke_dasharray).
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            y=column(y) if isinstance(y, str) else y,
            x1=column(x1) if isinstance(x1, str) else x1,
            x2=column(x2) if isinstance(x2, str) else x2,
            interval=interval,
            anchor=anchor,
            color=color,
            ticks=ticks,
            tickSpacing=tick_spacing,
            insetLeft=inset_left,
            insetRight=inset_right,
        )
    )

    return Mark("gridFy", config, options)
