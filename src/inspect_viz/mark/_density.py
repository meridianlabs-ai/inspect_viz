from typing import Any, Literal, Unpack

from .._core.data import Data
from .._core.param import Param
from .._core.selection import Selection
from .._util.marshall import dict_remove_none
from ._channel import ChannelValue, ChannelValueSpec
from ._mark import Mark
from ._options import MarkOptions
from ._text import text_styles_config
from ._types import FrameAnchor, Interpolate, Symbol, TextStyles
from ._util import column_param


def density(
    data: Data,
    x: ChannelValueSpec | Param,
    y: ChannelValueSpec | Param,
    z: ChannelValue | Param | None = None,
    filter_by: Selection | None = None,
    type: Literal["dot", "circle", "hexagon", "cell", "text"] | Param | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    pixel_size: float | Param | None = None,
    pad: float | Param | None = None,
    bandwidth: float | Param | None = None,
    interpolate: Interpolate | Param | None = None,
    symbol: Symbol | Param | None = None,
    r: ChannelValueSpec | float | Param | None = None,
    rotate: ChannelValue | float | Param | None = None,
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
            x=column_param(data, x),
            y=column_param(data, y),
            z=column_param(data, z),
            type=type,
            width=width,
            height=height,
            pixelSize=pixel_size,
            pad=pad,
            bandwidth=bandwidth,
            interpolate=interpolate,
            symbol=symbol,
            r=column_param(data, r),
            rotate=rotate,
            frameAnchor=frame_anchor,
        )
        | text_styles_config(styles)
    )

    return Mark("density", config, options)


def density_x(
    data: Data,
    y: ChannelValueSpec | Param | None = None,
    z: ChannelValue | Param | None = None,
    filter_by: Selection | None = None,
    type: Literal["areaX", "lineX", "dotX", "textX"] | Param = "areaX",
    stack: bool | Param | None = None,
    bandwidth: float | Param | None = None,
    bins: float | Param | None = None,
    normalize: bool | Literal["max", "sum", "none"] | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A densityX mark that visualizes smoothed point cloud densities along the **x** dimension.

    The mark bins the data, counts the number of records that fall into each bin, smooths the resulting counts, and then plots the smoothed distribution, by default using an areaX mark.

    Set the *type* property to use a different base mark type.

    Args:
        data: The data source for the mark.
        y: The vertical position channel, typically bound to the *y* scale;
            defaults to the zero-based index of the data [0, 1, 2, …].
        z: An optional ordinal channel for grouping data into series.
        filter_by: A selection to filter the data.
        type: The basic mark type to use to render 1D density values. Defaults
            to an areaX mark; lineX, dotX, and textX marks are also supported.
        stack: Flag indicating if densities should be stacked. Defaults to `False`.
        bandwidth: The kernel density bandwidth for smoothing, in pixels.
        bins: The number of bins over which to discretize the data prior to
            smoothing. Defaults to 1024.
        normalize: Normalization method for density estimates. If `False` or
            `'none'` (the default), the density estimates are smoothed weighted
            counts. If `True` or `'sum'`, density estimates are divided by the
            sum of the total point mass. If `'max'`, estimates are divided by
            the maximum smoothed value.
        **options: Additional mark options from MarkOptions.

    Returns:
        A density mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            y=column_param(data, y),
            z=column_param(data, z),
            type=type,
            bandwidth=bandwidth,
            bins=bins,
            normalize=normalize,
            stack=stack,
        )
    )

    return Mark("densityX", config, options)


def density_y(
    data: Data,
    x: ChannelValueSpec | Param | None = None,
    z: ChannelValue | Param | None = None,
    filter_by: Selection | None = None,
    type: Literal["areaY", "lineY", "dotY", "circle", "hexagon", "textY"]
    | Param = "areaY",
    stack: bool | Param | None = None,
    bandwidth: float | Param | None = None,
    bins: float | Param | None = None,
    normalize: bool | Literal["max", "sum", "none"] | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A densityY mark that visualizes smoothed point cloud densities along the **y** dimension.

    The mark bins the data, counts the number of records that fall into each bin, smooths the resulting counts, and then plots the smoothed distribution, by default using an areaY mark.

    Set the *type* property to use a different base mark type.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale;
            defaults to the zero-based index of the data [0, 1, 2, …].
        z: An optional ordinal channel for grouping data into series.
        filter_by: A selection to filter the data.
        type: The basic mark type to use to render 1D density values. Defaults
            to an areaY mark; lineY, dotY, circle, hexagon, and textY marks are also supported.
        stack: Flag indicating if densities should be stacked. Defaults to `False`.
        bandwidth: The kernel density bandwidth for smoothing, in pixels.
        bins: The number of bins over which to discretize the data prior to
            smoothing. Defaults to 1024.
        normalize: Normalization method for density estimates. If `False` or
            `'none'` (the default), the density estimates are smoothed weighted
            counts. If `True` or `'sum'`, density estimates are divided by the
            sum of the total point mass. If `'max'`, estimates are divided by
            the maximum smoothed value.
        **options: Additional mark options from MarkOptions.

    Returns:
        A density mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            z=column_param(data, z),
            type=type,
            bandwidth=bandwidth,
            bins=bins,
            normalize=normalize,
            stack=stack,
        )
    )

    return Mark("densityY", config, options)
