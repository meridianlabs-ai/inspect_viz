from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ._channel import Channel
from ._mark import Mark, MarkOptions
from ._types import Curve, Marker
from ._util import column_param


def link(
    data: Data,
    x: Channel | Param | None = None,
    y: Channel | Param | None = None,
    x1: Channel | Param | None = None,
    y1: Channel | Param | None = None,
    x2: Channel | Param | None = None,
    y2: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a link mark that draws line segments between pairs of points.

    The link mark connects pairs of points with line segments. It supports both
    simple positioning using x and y (which serve as shorthand for x1/x2 and y1/y2),
    and explicit positioning using x1/y1 and x2/y2 coordinates for full control
    over link endpoints.

    For vertical links, specify **x** (or **x1** and **x2**) for the horizontal
    position and **y1** and **y2** for the vertical endpoints. For horizontal links,
    specify **y** (or **y1** and **y2**) for the vertical position and **x1** and
    **x2** for the horizontal endpoints.

    Args:
        data: The data source for the mark.
        x: The horizontal position for vertical links; shorthand for x1 and x2.
        y: The vertical position for horizontal links; shorthand for y1 and y2.
        x1: The starting horizontal position; also sets default for x2.
        y1: The starting vertical position; also sets default for y2.
        x2: The ending horizontal position; also sets default for x1.
        y2: The ending vertical position; also sets default for y1.
        filter_by: Selection to filter by (defaults to data source selection).
        marker: Shorthand to set the same default for marker_start, marker_mid, and marker_end.
        marker_start: The marker for the starting point of a line segment.
        marker_mid: The marker for any middle (interior) points of a line segment.
        marker_end: The marker for the ending point of a line segment.
        curve: The curve interpolation method for connecting adjacent points.
            Recommended for links: *linear*, *step*, *step-after*, *step-before*,
            *bump-x*, *bump-y*.
        tension: The tension option only has an effect on bundle, cardinal and Catmull–Rom splines.
        **options: Additional mark options from MarkOptions.

    Returns:
        A link mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            x1=column_param(data, x1),
            y1=column_param(data, y1),
            x2=column_param(data, x2),
            y2=column_param(data, y2),
            marker=marker,
            markerStart=marker_start,
            markerMid=marker_mid,
            markerEnd=marker_end,
            curve=curve,
            tension=tension,
        )
    )

    return Mark("link", config, options)
