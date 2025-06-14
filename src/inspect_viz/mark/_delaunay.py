from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ._channel import ChannelValue, ChannelValueSpec
from ._mark import Mark
from ._options import MarkOptions
from ._types import Curve, Marker
from ._util import column_param


def delaunay_link(
    data: Data,
    x: ChannelValueSpec | Param,
    y: ChannelValueSpec | Param,
    z: ChannelValue | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a Delaunay link mark that draws links for each edge of the Delaunay triangulation.

    The delaunayLink mark computes the Delaunay triangulation of the data and draws
    a line segment for each edge of the triangulation. This is useful for visualizing
    spatial relationships and adjacencies in scattered point data.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        z: An optional ordinal channel for grouping to produce multiple
            (possibly overlapping) triangulations.
        filter_by: Selection to filter by (defaults to data source selection).
        marker: Shorthand to set the same default for marker_start, marker_mid, and marker_end.
        marker_start: The marker for the starting point of a line segment.
        marker_mid: The marker for any middle (interior) points of a line segment.
        marker_end: The marker for the ending point of a line segment.
        curve: The curve interpolation method; defaults to *linear*.
        tension: The tension option only has an effect on bundle, cardinal and Catmull–Rom splines.
        **options: Additional mark options from MarkOptions.

    Returns:
        A delaunay link mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            z=column_param(data, z),
            marker=marker,
            markerStart=marker_start,
            markerMid=marker_mid,
            markerEnd=marker_end,
            curve=curve,
            tension=tension,
        )
    )

    return Mark("delaunayLink", config, options)


def delaunay_mesh(
    data: Data,
    x: ChannelValueSpec | Param,
    y: ChannelValueSpec | Param,
    z: ChannelValue | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a Delaunay mesh mark that draws a mesh of the Delaunay triangulation.

    The delaunayMesh mark computes the Delaunay triangulation of the data and draws
    filled triangular polygons for each triangle in the triangulation. This creates
    a continuous mesh surface useful for spatial interpolation and surface visualization.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        z: An optional ordinal channel for grouping to produce multiple
            (possibly overlapping) triangulations.
        filter_by: Selection to filter by (defaults to data source selection).
        marker: Shorthand to set the same default for marker_start, marker_mid, and marker_end.
        marker_start: The marker for the starting point of a line segment.
        marker_mid: The marker for any middle (interior) points of a line segment.
        marker_end: The marker for the ending point of a line segment.
        curve: The curve interpolation method; defaults to *linear*.
        tension: The tension option only has an effect on bundle, cardinal and Catmull–Rom splines.
        **options: Additional mark options from MarkOptions.

    Returns:
        A delaunay mesh mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            z=column_param(data, z),
            marker=marker,
            markerStart=marker_start,
            markerMid=marker_mid,
            markerEnd=marker_end,
            curve=curve,
            tension=tension,
        )
    )

    return Mark("delaunayMesh", config, options)


def hull(
    data: Data,
    x: ChannelValueSpec | Param,
    y: ChannelValueSpec | Param,
    z: ChannelValue | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a hull mark that draws a convex hull around points.

    The hull mark computes the convex hull of the data points and draws a polygon
    representing the smallest convex shape that contains all the points. This is
    useful for showing the overall extent or boundary of a point cloud.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        z: An optional ordinal channel for grouping to produce multiple hulls;
            defaults to fill or stroke channel if not specified.
        filter_by: Selection to filter by (defaults to data source selection).
        marker: Shorthand to set the same default for marker_start, marker_mid, and marker_end.
        marker_start: The marker for the starting point of a line segment.
        marker_mid: The marker for any middle (interior) points of a line segment.
        marker_end: The marker for the ending point of a line segment.
        curve: The curve interpolation method; defaults to *linear*.
        tension: The tension option only has an effect on bundle, cardinal and Catmull–Rom splines.
        **options: Additional mark options from MarkOptions.

    Returns:
        A hull mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            z=column_param(data, z),
            marker=marker,
            markerStart=marker_start,
            markerMid=marker_mid,
            markerEnd=marker_end,
            curve=curve,
            tension=tension,
        )
    )

    return Mark("hull", config, options)


def voronoi(
    data: Data,
    x: ChannelValueSpec | Param,
    y: ChannelValueSpec | Param,
    z: ChannelValue | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a Voronoi mark that draws polygons for each cell of the Voronoi tessellation.

    The voronoi mark computes the Voronoi tessellation (also known as Thiessen polygons)
    of the data points and draws filled polygons for each cell. Each cell contains all
    points that are closer to the cell's generator point than to any other generator.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        z: An optional ordinal channel for grouping to produce multiple tessellations.
        filter_by: Selection to filter by (defaults to data source selection).
        marker: Shorthand to set the same default for marker_start, marker_mid, and marker_end.
        marker_start: The marker for the starting point of a line segment.
        marker_mid: The marker for any middle (interior) points of a line segment.
        marker_end: The marker for the ending point of a line segment.
        curve: The curve interpolation method; defaults to *linear*.
        tension: The tension option only has an effect on bundle, cardinal and Catmull–Rom splines.
        **options: Additional mark options from MarkOptions.

    Returns:
        A voronoi mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            z=column_param(data, z),
            marker=marker,
            markerStart=marker_start,
            markerMid=marker_mid,
            markerEnd=marker_end,
            curve=curve,
            tension=tension,
        )
    )

    return Mark("voronoi", config, options)


def voronoi_mesh(
    data: Data,
    x: ChannelValueSpec | Param,
    y: ChannelValueSpec | Param,
    z: ChannelValue | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a Voronoi mesh mark that draws a mesh for the cell boundaries of the Voronoi tessellation.

    The voronoiMesh mark computes the Voronoi tessellation of the data points and draws
    line segments for the boundaries between cells. This creates a mesh of cell edges
    useful for visualizing the spatial partitioning without filled polygons.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        z: An optional ordinal channel for grouping to produce multiple tessellations.
        filter_by: Selection to filter by (defaults to data source selection).
        marker: Shorthand to set the same default for marker_start, marker_mid, and marker_end.
        marker_start: The marker for the starting point of a line segment.
        marker_mid: The marker for any middle (interior) points of a line segment.
        marker_end: The marker for the ending point of a line segment.
        curve: The curve interpolation method; defaults to *linear*.
        tension: The tension option only has an effect on bundle, cardinal and Catmull–Rom splines.
        **options: Additional mark options from MarkOptions.

    Returns:
        A voronoi mesh mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            z=column_param(data, z),
            marker=marker,
            markerStart=marker_start,
            markerMid=marker_mid,
            markerEnd=marker_end,
            curve=curve,
            tension=tension,
        )
    )

    return Mark("voronoiMesh", config, options)
