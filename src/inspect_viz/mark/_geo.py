from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ._channel import Channel, ChannelSpec
from ._mark import Mark, MarkOptions
from ._util import column_param


def geo(
    data: Data,
    geometry: Channel | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    filter_by: Selection | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a geo mark for rendering geographic data.

    The geo mark renders geographic data, typically GeoJSON objects, with support
    for map projections and geographic styling. It's designed for displaying
    geographic features like countries, states, cities, or any spatial geometry.

    Args:
        data: The data source for the mark.
        geometry: A channel for the geometry to render; defaults to identity,
            assuming data is a GeoJSON object or iterable of GeoJSON objects.
            Supports various geographic data types and transformations.
        r: The radius channel for point geometries, typically bound to the
            *radius* scale.
        filter_by: Selection to filter by (defaults to data source selection).
        **options: Additional mark options from MarkOptions. Note that clip
            can be set to "sphere" for projection-aware clipping when using
            spherical projections.

    Returns:
        A geo mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            geometry=column_param(data, geometry),
            r=column_param(data, r),
        )
    )

    return Mark("geo", config, options)


def sphere(
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a sphere mark that renders the outline of the projection sphere.

    The sphere mark renders the outline of the sphere on the projection's plane.
    This is typically used with spherical projections to show the boundary of
    the projected world. The sphere mark automatically generates the appropriate
    geometry for the current projection.

    This mark is particularly useful for:
    - Adding a border around world maps with spherical projections
    - Showing the extent of the projection
    - Creating a background for geographic visualizations

    Args:
        **options: Options from MarkOptions. Note that this
            mark is designed for use with spherical projections only.

    Returns:
        A sphere mark.
    """
    return Mark("sphere", {}, options)


def graticule(
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a graticule mark that renders a global coordinate grid.

    The graticule mark renders a 10° global graticule (coordinate grid) showing
    lines of longitude and latitude. This provides a reference grid for geographic
    visualizations and helps users understand the projection and scale.

    This mark is particularly useful for:
    - Adding coordinate reference lines to world maps
    - Showing distortion in map projections
    - Providing spatial reference for geographic data

    Args:
        **options: Options from MarkOptions. Note that this
            mark is designed for use with spherical projections only.

    Returns:
        A graticule mark.
    """
    return Mark("graticule", {}, options)
