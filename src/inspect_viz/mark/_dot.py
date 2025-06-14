from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._core.types import Interval
from .._util.marshall import dict_remove_none
from ._channel import Channel, ChannelIntervalSpec, ChannelSpec
from ._mark import Mark, MarkOptions
from ._types import FrameAnchor, Symbol
from ._util import column_param


def dot(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    z: Channel | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    filter_by: Selection | None = None,
    rotate: Channel | float | Param | None = None,
    symbol: ChannelSpec | Param | Symbol | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A dot mark that draws circles, or other symbols, as in a scatterplot.

    Args:
        data: The data source for the mark.
        x: Horizontal position channel specifying the dot’s center.
        y: The vertical position channel specifying the dot’s center.
        z: An optional ordinal channel for grouping data into series.
        r: The radius of dots; either a channel or constant. When a number, it is interpreted as a constant radius
           in pixels. Otherwise it is interpreted as a channel, typically bound to the *r* channel, which defaults
           to the *sqrt* type for proportional symbols. The radius defaults to 4.5 pixels when using the **symbol**
           channel, and otherwise 3 pixels. Dots with a nonpositive radius are not drawn.
        filter_by: Selection to filter by (defaults to data source selection).
        rotate: The rotation angle of dots in degrees clockwise; either a channel or a constant. When a number, it is interpreted as a constant; otherwise it is interpreted as a channel. Defaults to 0°, pointing up.
        symbol: Categorical column to bind symbols to or CSS color string.
        frame_anchor: The frame anchor specifies defaults for **x** and **y** based on the plot’s frame; it may be
           one of the four sides (*top*, *right*, *bottom*, *left*), one of the four corners (*top-left*,
           *top-right*, *bottom-right*, *bottom-left*), or the *middle* of the frame.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            z=column_param(data, z),
            r=r,
            rotate=rotate,
            symbol=symbol,
            frameAnchor=frame_anchor,
        )
    )

    return Mark("dot", config, options)


def dot_x(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelIntervalSpec | None = None,
    z: Channel | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    interval: Interval | None = None,
    filter_by: Selection | None = None,
    rotate: Channel | float | Param | None = None,
    symbol: ChannelSpec | Param | Symbol | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A horizontal dot mark that draws circles, or other symbols.

    Like dot, except that **y** defaults to the identity function, assuming that
    *data* = [*y₀*, *y₁*, *y₂*, …].

    If an **interval** is specified, such as *day*, **y** is transformed to the middle of the interval.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel specifying the dot's center.
        y: The vertical position of the dot’s center,typically bound to the *y* scale.
        z: An optional ordinal channel for grouping data into series.
        r: The radius of dots; either a channel or constant. When a number, it is interpreted as a constant radius
           in pixels. Otherwise it is interpreted as a channel, typically bound to the *r* channel, which defaults
           to the *sqrt* type for proportional symbols. The radius defaults to 4.5 pixels when using the **symbol**
           channel, and otherwise 3 pixels. Dots with a nonpositive radius are not drawn.
        interval: An interval (such as *day* or a number), to transform **y** values to the middle of the interval.
        filter_by: Selection to filter by (defaults to data source selection).
        rotate: The rotation angle of dots in degrees clockwise; either a channel or a constant. When a number, it is interpreted as a constant; otherwise it is interpreted as a channel. Defaults to 0°, pointing up.
        symbol: Categorical column to bind symbols to or CSS color string.
        frame_anchor: The frame anchor specifies defaults for **x** and **y** based on the plot's frame; it may be
           one of the four sides (*top*, *right*, *bottom*, *left*), one of the four corners (*top-left*,
           *top-right*, *bottom-right*, *bottom-left*), or the *middle* of the frame.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            z=column_param(data, z),
            r=r,
            interval=interval,
            rotate=rotate,
            symbol=symbol,
            frameAnchor=frame_anchor,
        )
    )

    return Mark("dotX", config, options)


def dot_y(
    data: Data,
    y: ChannelSpec | Param,
    x: ChannelIntervalSpec | None = None,
    z: Channel | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    interval: Interval | None = None,
    filter_by: Selection | None = None,
    rotate: Channel | float | Param | None = None,
    symbol: ChannelSpec | Param | Symbol | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A vertical dot mark that draws circles, or other symbols.

    Like dot, except that **x** defaults to the identity function, assuming that
    *data* = [*x₀*, *x₁*, *x₂*, …].

    If an **interval** is specified, such as *day*, **x** is transformed to the middle of the interval.

    Args:
        data: The data source for the mark.
        y: The vertical position channel specifying the dot's center.
        x: The horizontal position of the dot’s center, typically bound to the *x* scale.
        z: An optional ordinal channel for grouping data into series.
        r: The radius of dots; either a channel or constant. When a number, it is interpreted as a constant radius
           in pixels. Otherwise it is interpreted as a channel, typically bound to the *r* channel, which defaults
           to the *sqrt* type for proportional symbols. The radius defaults to 4.5 pixels when using the **symbol**
           channel, and otherwise 3 pixels. Dots with a nonpositive radius are not drawn.
        interval: An interval (such as *day* or a number), to transform **x** values to the middle of the interval.
        filter_by: Selection to filter by (defaults to data source selection).
        rotate: The rotation angle of dots in degrees clockwise; either a channel or a constant. When a number, it is interpreted as a constant; otherwise it is interpreted as a channel. Defaults to 0°, pointing up.
        symbol: Categorical column to bind symbols to or CSS color string.
        frame_anchor: The frame anchor specifies defaults for **x** and **y** based on the plot's frame; it may be
           one of the four sides (*top*, *right*, *bottom*, *left*), one of the four corners (*top-left*,
           *top-right*, *bottom-right*, *bottom-left*), or the *middle* of the frame.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            y=column_param(data, y),
            x=column_param(data, x),
            z=column_param(data, z),
            r=r,
            interval=interval,
            rotate=rotate,
            symbol=symbol,
            frameAnchor=frame_anchor,
        )
    )

    return Mark("dotY", config, options)


def circle(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    z: ChannelSpec | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    filter_by: Selection | None = None,
    rotate: ChannelSpec | float | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A circle mark that draws circles as in a scatterplot.

    Like dot, but with the symbol fixed to be a circle.

    Args:
        data: The data source for the mark.
        x: Horizontal position channel specifying the circle's center.
        y: The vertical position channel specifying the circle's center.
        z: An optional ordinal channel for grouping data into series.
        r: The radius of circles; either a channel or constant. When a number, it is interpreted as a constant radius
           in pixels. Otherwise it is interpreted as a channel, typically bound to the *r* channel, which defaults
           to the *sqrt* type for proportional symbols. The radius defaults to 3 pixels. Circles with a nonpositive
           radius are not drawn.
        filter_by: Selection to filter by (defaults to data source selection).
        rotate: The rotation angle of circles in degrees clockwise; either a channel or a constant. When a number, it is interpreted as a constant; otherwise it is interpreted as a channel. Defaults to 0°, pointing up.
        frame_anchor: The frame anchor specifies defaults for **x** and **y** based on the plot's frame; it may be
           one of the four sides (*top*, *right*, *bottom*, *left*), one of the four corners (*top-left*,
           *top-right*, *bottom-right*, *bottom-left*), or the *middle* of the frame.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            z=column_param(data, z),
            r=r,
            rotate=rotate,
            frameAnchor=frame_anchor,
        )
    )

    return Mark("circle", config, options)


def hexagon(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    z: ChannelSpec | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    filter_by: Selection | None = None,
    rotate: ChannelSpec | float | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A hexagon mark that draws hexagons as in a scatterplot.

    Like dot, but with the symbol fixed to be a hexagon.

    Args:
        data: The data source for the mark.
        x: Horizontal position channel specifying the hexagon's center.
        y: The vertical position channel specifying the hexagon's center.
        z: An optional ordinal channel for grouping data into series.
        r: The radius of hexagons; either a channel or constant. When a number, it is interpreted as a constant radius
           in pixels. Otherwise it is interpreted as a channel, typically bound to the *r* channel, which defaults
           to the *sqrt* type for proportional symbols. The radius defaults to 4.5 pixels. Hexagons with a nonpositive
           radius are not drawn.
        filter_by: Selection to filter by (defaults to data source selection).
        rotate: The rotation angle of hexagons in degrees clockwise; either a channel or a constant. When a number, it is interpreted as a constant; otherwise it is interpreted as a channel. Defaults to 0°, pointing up.
        frame_anchor: The frame anchor specifies defaults for **x** and **y** based on the plot's frame; it may be
           one of the four sides (*top*, *right*, *bottom*, *left*), one of the four corners (*top-left*,
           *top-right*, *bottom-right*, *bottom-left*), or the *middle* of the frame.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            z=column_param(data, z),
            r=r,
            rotate=rotate,
            frameAnchor=frame_anchor,
        )
    )

    return Mark("hexagon", config, options)
