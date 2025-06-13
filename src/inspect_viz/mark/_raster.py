from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ._channel import Channel
from ._mark import Mark, MarkOptions
from ._types import Interpolate
from ._util import column_param


def raster(
    data: Data,
    x: Channel | Param,
    y: Channel | Param,
    filter_by: Selection | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    pixel_size: float | Param | None = None,
    pad: float | Param | None = None,
    interpolate: Interpolate | Param | None = None,
    bandwidth: float | Param | None = None,
    image_rendering: str | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a raster mark for spatial samples with optional interpolation and smoothing.

    The raster mark bins spatial data into a raster grid and optionally applies spatial
    interpolation and kernel density smoothing. The raster mark is useful for visualizing
    continuous spatial phenomena from discrete sample points.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
            Domain values are binned into a grid with *width* horizontal bins.
        y: The vertical position channel, typically bound to the *y* scale.
            Domain values are binned into a grid with *height* vertical bins.
        filter_by: Selection to filter by (defaults to data source selection).
        width: The width (number of columns) of the grid, in actual pixels.
        height: The height (number of rows) of the grid, in actual pixels.
        pixel_size: The effective screen size of a raster pixel, used to determine
            the height and width of the raster from the frame's dimensions; defaults to 1.
        pad: The bin padding, one of 1 (default) to include extra padding for
            the final bin, or 0 to make the bins flush with the maximum domain value.
        interpolate: The spatial interpolation method; one of:
            - *none* - do not perform interpolation (the default)
            - *linear* - apply proportional linear interpolation across adjacent bins
            - *nearest* - assign each pixel to the closest sample's value (Voronoi diagram)
            - *barycentric* - apply barycentric interpolation over the Delaunay triangulation
            - *random-walk* - apply a random walk from each pixel
        bandwidth: The kernel density bandwidth for smoothing, in pixels.
        image_rendering: The image-rendering attribute; defaults to *auto* (bilinear).
            May be set to *pixelated* to disable bilinear interpolation for a sharper image.
        **options: Additional mark options from MarkOptions.

    Returns:
        A raster mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            width=width,
            height=height,
            pixelSize=pixel_size,
            pad=pad,
            interpolate=interpolate,
            bandwidth=bandwidth,
            imageRendering=image_rendering,
        )
    )

    return Mark("raster", config, options)


def heatmap(
    data: Data,
    x: Channel | Param,
    y: Channel | Param,
    filter_by: Selection | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    pixel_size: float | Param | None = None,
    pad: float | Param | None = None,
    interpolate: Interpolate | Param | None = None,
    bandwidth: float | Param | None = None,
    image_rendering: str | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a heatmap mark for density visualization with optimized defaults.

    The heatmap mark is essentially a raster mark with different default options optimized
    for density visualization. It bins spatial data into a raster grid and applies kernel
    density smoothing to create smooth density surfaces from point data.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
            Domain values are binned into a grid with *width* horizontal bins.
        y: The vertical position channel, typically bound to the *y* scale.
            Domain values are binned into a grid with *height* vertical bins.
        filter_by: Selection to filter by (defaults to data source selection).
        width: The width (number of columns) of the grid, in actual pixels.
        height: The height (number of rows) of the grid, in actual pixels.
        pixel_size: The effective screen size of a raster pixel, used to determine
            the height and width of the raster from the frame's dimensions; defaults to 1.
        pad: The bin padding, one of 1 (default) to include extra padding for
            the final bin, or 0 to make the bins flush with the maximum domain value.
        interpolate: The spatial interpolation method; one of:
            - *none* - do not perform interpolation (the default)
            - *linear* - apply proportional linear interpolation across adjacent bins
            - *nearest* - assign each pixel to the closest sample's value (Voronoi diagram)
            - *barycentric* - apply barycentric interpolation over the Delaunay triangulation
            - *random-walk* - apply a random walk from each pixel
        bandwidth: The kernel density bandwidth for smoothing, in pixels; defaults to 20.
        image_rendering: The image-rendering attribute; defaults to *auto* (bilinear).
            May be set to *pixelated* to disable bilinear interpolation for a sharper image.
        **options: Additional mark options from MarkOptions.

    Returns:
        A heatmap mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            width=width,
            height=height,
            pixelSize=pixel_size,
            pad=pad,
            interpolate=interpolate,
            bandwidth=bandwidth,
            imageRendering=image_rendering,
        )
    )

    return Mark("heatmap", config, options)


def raster_tile(
    data: Data,
    x: Channel | Param,
    y: Channel | Param,
    filter_by: Selection | None = None,
    origin: list[float] | Param | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    pixel_size: float | Param | None = None,
    pad: float | Param | None = None,
    interpolate: Interpolate | Param | None = None,
    bandwidth: float | Param | None = None,
    image_rendering: str | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create an experimental raster tile mark with tiling and prefetching for scalable rasters.

    The rasterTile mark is an experimental version of the raster mark that supports tiling
    and prefetching for better performance with large datasets. It provides scalable
    raster visualization with efficient memory usage.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
            Domain values are binned into a grid with *width* horizontal bins.
        y: The vertical position channel, typically bound to the *y* scale.
            Domain values are binned into a grid with *height* vertical bins.
        filter_by: Selection to filter by (defaults to data source selection).
        origin: The coordinates of the tile origin in the x and y data domains;
            defaults to [0, 0].
        width: The width (number of columns) of the grid, in actual pixels.
        height: The height (number of rows) of the grid, in actual pixels.
        pixel_size: The effective screen size of a raster pixel, used to determine
            the height and width of the raster from the frame's dimensions; defaults to 1.
        pad: The bin padding, one of 1 (default) to include extra padding for
            the final bin, or 0 to make the bins flush with the maximum domain value.
        interpolate: The spatial interpolation method; one of:
            - *none* - do not perform interpolation (the default)
            - *linear* - apply proportional linear interpolation across adjacent bins
            - *nearest* - assign each pixel to the closest sample's value (Voronoi diagram)
            - *barycentric* - apply barycentric interpolation over the Delaunay triangulation
            - *random-walk* - apply a random walk from each pixel
        bandwidth: The kernel density bandwidth for smoothing, in pixels.
        image_rendering: The image-rendering attribute; defaults to *auto* (bilinear).
            May be set to *pixelated* to disable bilinear interpolation for a sharper image.
        **options: Additional mark options from MarkOptions.

    Returns:
        A raster tile mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            origin=origin,
            width=width,
            height=height,
            pixelSize=pixel_size,
            pad=pad,
            interpolate=interpolate,
            bandwidth=bandwidth,
            imageRendering=image_rendering,
        )
    )

    return Mark("rasterTile", config, options)
