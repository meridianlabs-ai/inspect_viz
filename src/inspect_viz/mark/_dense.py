from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ._channel import Channel, ChannelSpec
from ._mark import Mark, MarkOptions
from ._types import Interpolate
from ._util import column_param


def dense_line(
    data: Data,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    bandwidth: float | Param | None = None,
    normalize: bool | Param | None = None,
    interpolate: Interpolate | Param | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    pixel_size: float | Param | None = None,
    pad: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a dense line mark that plots line densities rather than point densities.

    The denseLine mark forms a binned raster grid and "draws" straight lines into it,
    creating a density visualization of line segments rather than individual points.
    This is useful for visualizing the density of linear features, trajectories, or
    paths in spatial data.

    The mark bins the data into a 2D grid and renders density values as a raster image.
    Unlike traditional line marks that use curve interpolation, dense lines operate on
    a pixel grid to accumulate line density information.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
            Domain values are binned into a grid with *width* horizontal bins.
        y: The vertical position channel, typically bound to the *y* scale.
            Domain values are binned into a grid with *height* vertical bins.
        z: An ordinal channel for grouping data into series to be drawn as separate lines.
        filter_by: Selection to filter by (defaults to data source selection).
        bandwidth: The kernel density bandwidth for smoothing, in pixels.
        normalize: Flag to perform approximate arc length normalization of line segments
            to prevent artifacts due to overcounting steep lines; defaults to True.
        interpolate: The spatial interpolation method; one of:
            - *none* - do not perform interpolation (the default)
            - *linear* - apply proportional linear interpolation across adjacent bins
            - *nearest* - assign each pixel to the closest sample's value (Voronoi diagram)
            - *barycentric* - apply barycentric interpolation over the Delaunay triangulation
            - *random-walk* - apply a random walk from each pixel
        width: The width (number of columns) of the grid, in actual pixels.
        height: The height (number of rows) of the grid, in actual pixels.
        pixel_size: The effective screen size of a raster pixel, used to determine
            the height and width of the raster from the frame's dimensions; defaults to 1.
        pad: The bin padding, one of 1 (default) to include extra padding for
            the final bin, or 0 to make the bins flush with the maximum domain value.
        **options: Additional mark options from MarkOptions. Note that fill and
            fillOpacity can use the special value "density" to map computed density
            values to visual properties.

    Returns:
        A dense line mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            z=column_param(data, z),
            bandwidth=bandwidth,
            normalize=normalize,
            interpolate=interpolate,
            width=width,
            height=height,
            pixelSize=pixel_size,
            pad=pad,
        )
    )

    return Mark("denseLine", config, options)
