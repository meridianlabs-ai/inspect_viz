from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ..transform._column import column
from ._channel import Channel
from ._mark import Mark, MarkOptions
from ._types import FrameAnchor
from ._util import column_param


def image(
    data: Data,
    x: Channel | Param | None = None,
    y: Channel | Param | None = None,
    filter_by: Selection | None = None,
    width: Channel | float | Param | None = None,
    height: Channel | float | Param | None = None,
    r: Channel | float | Param | None = None,
    rotate: Channel | float | Param | None = None,
    src: Channel | str | Param | None = None,
    preserve_aspect_ratio: str | Param | None = None,
    cross_origin: str | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    image_rendering: str | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create an image mark for displaying images in visualizations.

    The image mark displays raster images (PNG, JPEG, etc.) at specified positions
    and sizes. Images can be positioned using x/y coordinates, sized with width/height,
    and styled with various options including aspect ratio preservation and rendering modes.

    This mark is useful for:
    - Adding logos, icons, or other imagery to visualizations
    - Creating image-based scatter plots or dashboards
    - Displaying photographs or other raster content within plots

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        filter_by: Selection to filter by (defaults to data source selection).
        width: The image width in pixels. When a number, it is interpreted as a
            constant; otherwise it is interpreted as a channel. Defaults to 16
            if neither width nor height are set.
        height: The image height in pixels. When a number, it is interpreted as a
            constant; otherwise it is interpreted as a channel. Defaults to 16
            if neither width nor height are set.
        r: The image clip radius for circular images. If null (default), images
            are not clipped; when a number, it is interpreted as a constant in
            pixels; otherwise it is interpreted as a channel.
        rotate: The rotation angle in degrees clockwise.
        src: The required image URL (or relative path). If a string that starts
            with a dot, slash, or URL protocol it is assumed to be a constant;
            otherwise it is interpreted as a channel.
        preserve_aspect_ratio: The image aspect ratio; defaults to "xMidYMid meet".
            To crop the image instead of scaling it to fit, use "xMidYMid slice".
        cross_origin: The cross-origin behavior for loading images from external domains.
        frame_anchor: The frame anchor position for legend placement.
        image_rendering: The image-rendering attribute; defaults to "auto" (bilinear).
            May be set to "pixelated" to disable bilinear interpolation for a
            sharper image.
        **options: Additional mark options from MarkOptions.

    Returns:
        An image mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            width=column_param(data, width),
            height=column_param(data, height),
            r=column_param(data, r),
            rotate=rotate,
            src=column(src) if isinstance(src, str) else src,
            preserveAspectRatio=preserve_aspect_ratio,
            crossOrigin=cross_origin,
            frameAnchor=frame_anchor,
            imageRendering=image_rendering,
        )
    )

    return Mark("image", config, options)
