from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ._channel import Channel, ChannelSpec
from ._mark import Mark, MarkOptions
from ._types import Curve, Marker
from ._util import column_param


def line(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A line mark that connects control points.

    Points along the line are connected in input order. If there are multiple series via the **z**, **fill**, or **stroke** channel, series are drawn in input order such that the last series is drawn on top.

    Args:
        data: The data source for the mark.
        x: The required horizontal position channel, typically bound to the *x* scale.
        y: The required vertical position channel, typically bound to the *y* scale.
        z: An optional ordinal channel for grouping data into series.
        filter_by: Selection to filter by (defaults to data source selection).
        marker: Shorthand to set the same default for marker_start, marker_mid, and marker_end.
        marker_start: The marker for the starting point of a line segment.
        marker_mid: The marker for any middle (interior) points of a line segment.
        marker_end: The marker for the ending point of a line segment.
        curve: The curve (interpolation) method for connecting adjacent points.
        tension: The tension option for bundle, cardinal and Catmull-Rom splines.
        options: Additional `MarkOptions`.
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

    return Mark("line", config, options)


def line_x(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A horizontal line mark that connects control points.

    Like line, except that **y** defaults to the zero-based index of the data [0, 1, 2, …].

    Args:
        data: The data source for the mark.
        x: The required horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale; defaults to the zero-based index of the data [0, 1, 2, …].
        z: An optional ordinal channel for grouping data into series.
        filter_by: Selection to filter by (defaults to data source selection).
        marker: Shorthand to set the same default for marker_start, marker_mid, and marker_end.
        marker_start: The marker for the starting point of a line segment.
        marker_mid: The marker for any middle (interior) points of a line segment.
        marker_end: The marker for the ending point of a line segment.
        curve: The curve (interpolation) method for connecting adjacent points.
        tension: The tension option for bundle, cardinal and Catmull-Rom splines.
        options: Additional `MarkOptions`.
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

    return Mark("lineX", config, options)


def line_y(
    data: Data,
    y: ChannelSpec | Param,
    x: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A vertical line mark that connects control points.

    Like line, except that **x** defaults to the zero-based index of the data [0, 1, 2, …].

    Args:
        data: The data source for the mark.
        y: The required vertical position channel, typically bound to the *y* scale.
        x: The horizontal position channel, typically bound to the *x* scale; defaults to the zero-based index of the data [0, 1, 2, …].
        z: An optional ordinal channel for grouping data into series.
        filter_by: Selection to filter by (defaults to data source selection).
        marker: Shorthand to set the same default for marker_start, marker_mid, and marker_end.
        marker_start: The marker for the starting point of a line segment.
        marker_mid: The marker for any middle (interior) points of a line segment.
        marker_end: The marker for the ending point of a line segment.
        curve: The curve (interpolation) method for connecting adjacent points.
        tension: The tension option for bundle, cardinal and Catmull-Rom splines.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            y=column_param(data, y),
            x=column_param(data, x),
            z=column_param(data, z),
            marker=marker,
            markerStart=marker_start,
            markerMid=marker_mid,
            markerEnd=marker_end,
            curve=curve,
            tension=tension,
        )
    )

    return Mark("lineY", config, options)
