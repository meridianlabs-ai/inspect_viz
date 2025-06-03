from typing import Any, Literal, Unpack

from .._core.data import Data
from .._core.param import Param
from .._core.selection import Selection
from .._util.marshall import dict_remove_none
from ..transform import column
from ._channel import Channel
from ._mark import Mark, MarkOptions
from ._text import TextStyles, text_styles_config
from ._types import FrameAnchor, Symbol

Interpolate = Literal["none", "linear", "nearest", "barycentric", "random-walk"]

DensityType = Literal["dot", "circle", "hexagon", "cell", "text"]


def density(
    data: Data,
    x: Channel | Param,
    y: Channel | Param,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    type: DensityType | Param | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    pixel_size: float | Param | None = None,
    pad: float | Param | None = None,
    bandwidth: float | Param | None = None,
    interpolate: Interpolate | Param | None = None,
    symbol: Symbol | Param | None = None,
    r: Channel | float | Param | None = None,
    rotate: Channel | float | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    styles: TextStyles | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a 2D density mark that shows smoothed point cloud densities.

    The density mark bins the data, counts the number of records that fall into
    each bin, and smooths the resulting counts, then plots the smoothed distribution,
    by default using a circular dot mark. The density mark calculates density values
    that can be mapped to encoding channels such as fill or r using the special
    field name "density".

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
            Domain values are binned into a grid with *width* horizontal bins.
        y: The vertical position channel, typically bound to the *y* scale.
            Domain values are binned into a grid with *height* vertical bins.
        z: An optional ordinal channel for grouping data into series.
        filter_by: A selection to filter the data.
        type: The base mark type to use for rendering; defaults to "dot".
        width: The number of horizontal bins for density calculation.
        height: The number of vertical bins for density calculation.
        pixel_size: The size of each pixel for the grid, in data units.
        pad: The bin padding, one of 1 (default) to include extra padding for
            the final bin, or 0 to make the bins flush with the maximum domain value.
        bandwidth: The kernel density bandwidth for smoothing, in pixels.
        interpolate: The spatial interpolation method; one of:
            - *none* - do not perform interpolation (the default)
            - *linear* - apply proportional linear interpolation across adjacent bins
            - *nearest* - assign each pixel to the closest sample's value (Voronoi diagram)
            - *barycentric* - apply barycentric interpolation over the Delaunay triangulation
            - *random-walk* - apply a random walk from each pixel
        symbol: The symbol type for dots; defaults to "circle".
        r: The radius channel, typically bound to the *radius* scale.
        rotate: The rotation angle in degrees clockwise.
        frame_anchor: The frame anchor position for legend placement.
        styles: Text styles to apply.
        **options: Additional mark options from MarkOptions.

    Returns:
        A density mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column(x) if isinstance(x, str) else x,
            y=column(y) if isinstance(y, str) else y,
            z=column(z) if isinstance(z, str) else z,
            type=type,
            width=width,
            height=height,
            pixelSize=pixel_size,
            pad=pad,
            bandwidth=bandwidth,
            interpolate=interpolate,
            symbol=symbol,
            r=column(r) if isinstance(r, str) else r,
            rotate=rotate,
            frameAnchor=frame_anchor,
        )
        | text_styles_config(styles)
    )

    return Mark("density", config, options)
