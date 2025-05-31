from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .channel import Channel
from .mark import Mark, MarkOptions
from .types import FrameAnchor, Symbol


def dot(
    data: Data,
    x: Channel | Param,
    y: Channel | Param,
    z: Channel | Param | None = None,
    r: Channel | float | Param | None = None,
    filter_by: Selection | None = None,
    rotate: Channel | float | Param | None = None,
    symbol: Channel | Param | Symbol | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A dot mark that draws circles, or other symbols, as in a scatterplot.

    Args:
        data: The data source for the mark.
        x: Horizontal position channel specifying the dot’s center.
        y: The vertical position channel specifying the dot’s center.
        z: An ptional ordinal channel for grouping data into series.
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
    config: dict[str, Any] = dict(
        data=data.plot_from(filter_by),
        x=x,
        y=y,
    )
    if z is not None:
        config["z"] = z
    if r is not None:
        config["r"] = r
    if rotate is not None:
        config["rotate"] = r
    if symbol is not None:
        config["symbol"] = symbol
    if frame_anchor is not None:
        config["frameAnchor"] = frame_anchor

    return Mark("dot", config, options)
