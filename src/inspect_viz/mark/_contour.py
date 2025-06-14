from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ._channel import ChannelValueSpec
from ._mark import Mark
from ._options import MarkOptions
from ._types import Interpolate
from ._util import column_param


def contour(
    data: Data,
    x: ChannelValueSpec | Param,
    y: ChannelValueSpec | Param,
    filter_by: Selection | None = None,
    thresholds: float | list[float] | Param | None = None,
    bandwidth: float | Param | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    pixel_size: float | Param | None = None,
    pad: float | Param | None = None,
    interpolate: Interpolate | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a contour mark that draws contour lines of equal value.

    The contour mark creates isolines showing contours of equal value. It bins the
    given data into a 2D grid, computes density estimates, and draws contour lines
    at specified threshold levels. The contour mark is useful for visualizing the
    density or distribution of 2D point data.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
            Domain values are binned into a grid with *width* horizontal bins.
        y: The vertical position channel, typically bound to the *y* scale.
            Domain values are binned into a grid with *height* vertical bins.
        filter_by: Selection to filter by (defaults to data source selection).
        thresholds: The number of contour thresholds to subdivide the domain into
            discrete level sets; defaults to 10. Can be a count or an array of
            threshold values.
        bandwidth: The kernel density bandwidth for smoothing, in pixels.
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
        **options: Additional mark options from MarkOptions.

    Returns:
        A contour mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            thresholds=thresholds,
            bandwidth=bandwidth,
            width=width,
            height=height,
            pixelSize=pixel_size,
            pad=pad,
            interpolate=interpolate,
        )
    )

    return Mark("contour", config, options)
