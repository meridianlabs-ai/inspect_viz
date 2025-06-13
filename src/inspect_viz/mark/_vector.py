from typing import Any, Literal

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ..transform._column import column
from ._channel import Channel
from ._mark import Mark, MarkOptions
from ._types import FrameAnchor


def vector(
    data: Data,
    x: Channel | Param | None = None,
    y: Channel | Param | None = None,
    r: Channel | float | Param | None = None,
    filter_by: Selection | None = None,
    length: Channel | float | Param | None = None,
    rotate: Channel | float | Param | None = None,
    shape: Literal["arrow", "spike"] | Param | None = None,
    anchor: Literal["start", "middle", "end"] | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A vector mark that draws arrows or other directional shapes.

    Vectors are typically used to represent direction and magnitude in data,
    such as wind vectors, force fields, or gradients.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        r: The radius or magnitude channel; either a constant or a channel.
        filter_by: A selection to filter the data.
        length: The length of the vector; either a constant or a channel.
        rotate: The rotation angle in degrees clockwise; either a constant or a channel.
        shape: The shape of the vector; one of "arrow" or "spike".
        anchor: The anchor position; one of "start", "middle", or "end".
        frame_anchor: The frame anchor position for legend placement.
        **options: Additional mark options from MarkOptions.

    Returns:
        A vector mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column(x) if isinstance(x, str) else x,
            y=column(y) if isinstance(y, str) else y,
            r=r,
            length=length,
            rotate=rotate,
            shape=shape,
            anchor=anchor,
            frameAnchor=frame_anchor,
        )
    )

    return Mark("vector", config, options)


def vector_x(
    data: Data,
    x: Channel | Param | None = None,
    y: Channel | Param | None = None,
    r: Channel | float | Param | None = None,
    filter_by: Selection | None = None,
    length: Channel | float | Param | None = None,
    rotate: Channel | float | Param | None = None,
    shape: Literal["arrow", "spike"] | Param | None = None,
    anchor: Literal["start", "middle", "end"] | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A vectorX mark that draws horizontal directional vectors.

    VectorX marks are oriented primarily along the x-axis and are useful for
    showing horizontal flow or direction.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        r: The radius or magnitude channel; either a constant or a channel.
        filter_by: A selection to filter the data.
        length: The length of the vector; either a constant or a channel.
        rotate: The rotation angle in degrees clockwise; either a constant or a channel.
        shape: The shape of the vector; one of "arrow" or "spike".
        anchor: The anchor position; one of "start", "middle", or "end".
        frame_anchor: The frame anchor position for legend placement.
        **options: Additional mark options from MarkOptions.

    Returns:
        A vectorX mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column(x) if isinstance(x, str) else x,
            y=column(y) if isinstance(y, str) else y,
            r=r,
            length=length,
            rotate=rotate,
            shape=shape,
            anchor=anchor,
            frameAnchor=frame_anchor,
        )
    )

    return Mark("vectorX", config, options)


def vector_y(
    data: Data,
    x: Channel | Param | None = None,
    y: Channel | Param | None = None,
    r: Channel | float | Param | None = None,
    filter_by: Selection | None = None,
    length: Channel | float | Param | None = None,
    rotate: Channel | float | Param | None = None,
    shape: Literal["arrow", "spike"] | Param | None = None,
    anchor: Literal["start", "middle", "end"] | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A vectorY mark that draws vertical directional vectors.

    VectorY marks are oriented primarily along the y-axis and are useful for
    showing vertical flow or direction.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        r: The radius or magnitude channel; either a constant or a channel.
        filter_by: A selection to filter the data.
        length: The length of the vector; either a constant or a channel.
        rotate: The rotation angle in degrees clockwise; either a constant or a channel.
        shape: The shape of the vector; one of "arrow" or "spike".
        anchor: The anchor position; one of "start", "middle", or "end".
        frame_anchor: The frame anchor position for legend placement.
        **options: Additional mark options from MarkOptions.

    Returns:
        A vectorY mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column(x) if isinstance(x, str) else x,
            y=column(y) if isinstance(y, str) else y,
            r=r,
            length=length,
            rotate=rotate,
            shape=shape,
            anchor=anchor,
            frameAnchor=frame_anchor,
        )
    )

    return Mark("vectorY", config, options)


def spike(
    data: Data,
    x: Channel | Param | None = None,
    y: Channel | Param | None = None,
    r: Channel | float | Param | None = None,
    length: Channel | float | Param | None = None,
    rotate: Channel | float | Param | None = None,
    shape: Literal["arrow", "spike"] | Param | None = None,
    anchor: Literal["start", "middle", "end"] | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    filter_by: Selection | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A spike mark that draws spike-shaped directional indicators.

    Spikes are a specialized type of vector that typically appear as thin
    lines or needles, useful for showing precise directional data or impulses.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel, typically bound to the *x* scale.
        y: The vertical position channel, typically bound to the *y* scale.
        r: The radius or magnitude channel; either a constant or a channel.
        length: The length of the spike; either a constant or a channel.
        rotate: The rotation angle in degrees clockwise; either a constant or a channel.
        shape: The shape of the spike; one of "arrow" or "spike".
        anchor: The anchor position; one of "start", "middle", or "end".
        frame_anchor: The frame anchor position for legend placement.
        filter_by: A selection to filter the data.
        **options: Additional mark options from MarkOptions.

    Returns:
        A spike mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column(x) if isinstance(x, str) else x,
            y=column(y) if isinstance(y, str) else y,
            r=r,
            length=length,
            rotate=rotate,
            shape=shape,
            anchor=anchor,
            frameAnchor=frame_anchor,
        )
    )

    return Mark("spike", config, options)
