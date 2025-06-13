from typing import Any, Literal

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ..transform._column import column
from ._channel import Channel
from ._mark import Mark, MarkOptions
from ._text import TextStyles, text_styles_config
from ._types import FrameAnchor


def hexbin(
    data: Data,
    x: Channel | Param,
    y: Channel | Param,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    bin_width: float | Param | None = None,
    type: Literal["hexagon", "dot", "text"] | Param | None = None,
    r: Channel | float | Param | None = None,
    rotate: Channel | float | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    styles: TextStyles | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a hexbin mark for hexagonal binning of point data.

    The hexbin mark bins two-dimensional point data into hexagonal bins and
    displays aggregated values for each bin. This is useful for visualizing
    density patterns in large datasets and for creating hexagonal heatmaps.

    The mark creates a hexagonal grid and counts or aggregates data points
    within each hexagon, then renders the results using the specified mark type.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
            Specifies the data to be binned horizontally.
        y: The vertical position channel, typically bound to the *y* scale.
            Specifies the data to be binned vertically.
        z: How to subdivide bins. Defaults to the *fill* channel, if any, or
            the *stroke* channel, if any. If null, bins will not be subdivided.
        filter_by: Selection to filter by (defaults to data source selection).
        bin_width: The distance between centers of neighboring hexagons, in pixels;
            defaults to 20.
        type: The basic mark type to use for hex-binned values. Defaults to a
            hexagon mark; dot and text marks are also supported.
        r: The radius of dots or hexagons; either a channel or constant.
        rotate: The rotation angle in degrees clockwise.
        frame_anchor: The frame anchor position for legend placement.
        styles: Text styles to apply when using text mark type.
        **options: Additional mark options from MarkOptions.

    Returns:
        A hexbin mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column(x) if isinstance(x, str) else x,
            y=column(y) if isinstance(y, str) else y,
            z=column(z) if isinstance(z, str) else z,
            binWidth=bin_width,
            type=type,
            r=column(r) if isinstance(r, str) else r,
            rotate=rotate,
            frameAnchor=frame_anchor,
        )
        | text_styles_config(styles)
    )

    return Mark("hexbin", config, options)
