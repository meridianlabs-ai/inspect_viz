from typing import Any

from typing_extensions import Unpack

from inspect_viz.mark._types import TextStyles

from .._core import Data, Param, Selection
from .._core.types import Interval
from .._util.marshall import dict_remove_none, dict_to_camel
from ..transform._column import column
from ._channel import ChannelValue, ChannelValueIntervalSpec, ChannelValueSpec
from ._mark import Mark
from ._options import MarkOptions
from ._types import FrameAnchor, LineAnchor
from ._util import column_param


def text(
    data: Data | None,
    x: ChannelValueSpec | Param,
    y: ChannelValueSpec | Param,
    z: ChannelValue | Param | None = None,
    text: ChannelValue | Param | None = None,
    filter_by: Selection | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    line_anchor: LineAnchor | Param | None = None,
    rotate: ChannelValue | float | Param | None = None,
    styles: TextStyles | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    r"""A text mark that displays textual labels.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel specifying the text's anchor point, typically bound to the *x* scale.
        y: The vertical position channel specifying the text's anchor point, typically bound to the *y* scale.
        z: An optional ordinal channel for grouping data into series.
        text: The text contents channel, possibly with line breaks (\n, \r\n, or \r). If not specified, defaults to the zero-based index [0, 1, 2, …].
        filter_by: Selection to filter by (defaults to data source selection).
        frame_anchor: The frame anchor specifies defaults for **x** and **y**, along with **textAnchor** and **lineAnchor**, based on the plot's frame; it may be one of the four sides (*top*, *right*, *bottom*, *left*), one of the four corners (*top-left*, *top-right*, *bottom-right*, *bottom-left*), or the *middle* of the frame.
        line_anchor: The line anchor controls how text is aligned (typically vertically) relative to its anchor point; it is one of *top*, *bottom*, or *middle*. If the frame anchor is *top*, *top-left*, or *top-right*, the default line anchor is *top*; if the frame anchor is *bottom*, *bottom-right*, or *bottom-left*, the default is *bottom*; otherwise it is *middle*.
        rotate: The rotation angle in degrees clockwise; a constant or a channel; defaults to 0°. When a number, it is interpreted as a constant; otherwise it is interpreted as a channel.
        styles: `TextStyles` to apply.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by) if data else None,
            x=column_param(data, x),
            y=column_param(data, y),
            z=column_param(data, z),
            text=column_param(data, text),
            frameAnchor=frame_anchor,
            lineAnchor=line_anchor,
            rotate=rotate,
        )
        | text_styles_config(styles)
    )

    return Mark("text", config, options)


def text_x(
    data: Data | None,
    x: ChannelValueSpec | Param,
    y: ChannelValueIntervalSpec | Param | None = None,
    z: ChannelValue | Param | None = None,
    text: ChannelValue | Param | None = None,
    interval: Interval | Param | None = None,
    filter_by: Selection | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    line_anchor: LineAnchor | Param | None = None,
    rotate: ChannelValue | float | Param | None = None,
    styles: TextStyles | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    r"""A horizontal text mark that displays textual labels.

    Like text, except that **y** defaults to the zero-based index of the data [0, 1, 2, …].

    If an **interval** is specified, such as *day*, **y** is transformed to the middle of the interval.

    Args:
        data: The data source for the mark.
        x: The horizontal position channel specifying the text's anchor point, typically bound to the *x* scale.
        y: The vertical position channel specifying the text's anchor point, typically bound to the *y* scale; defaults to the zero-based index of the data [0, 1, 2, …].
        z: An optional ordinal channel for grouping data into series.
        text: The text contents channel, possibly with line breaks (\n, \r\n, or \r). If not specified, defaults to the zero-based index [0, 1, 2, …].
        interval: An interval (such as *day* or a number), to transform **y** values to the middle of the interval.
        filter_by: Selection to filter by (defaults to data source selection).
        frame_anchor: The frame anchor specifies defaults for **x** and **y**, along with **textAnchor** and **lineAnchor**, based on the plot's frame; it may be one of the four sides (*top*, *right*, *bottom*, *left*), one of the four corners (*top-left*, *top-right*, *bottom-right*, *bottom-left*), or the *middle* of the frame.
        line_anchor: The line anchor controls how text is aligned (typically vertically) relative to its anchor point; it is one of *top*, *bottom*, or *middle*. If the frame anchor is *top*, *top-left*, or *top-right*, the default line anchor is *top*; if the frame anchor is *bottom*, *bottom-right*, or *bottom-left*, the default is *bottom*; otherwise it is *middle*.
        rotate: The rotation angle in degrees clockwise; a constant or a channel; defaults to 0°. When a number, it is interpreted as a constant; otherwise it is interpreted as a channel.
        styles: `TextStyles` to apply.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by) if data else None,
            x=column_param(data, x),
            y=column_param(data, y),
            z=column_param(data, z),
            text=column_param(data, text),
            interval=interval,
            frameAnchor=frame_anchor,
            lineAnchor=line_anchor,
            rotate=rotate,
        )
        | text_styles_config(styles)
    )

    return Mark("textX", config, options)


def text_y(
    data: Data | None,
    y: ChannelValueSpec | Param,
    x: ChannelValueIntervalSpec | Param | None = None,
    z: ChannelValue | Param | None = None,
    text: ChannelValue | Param | None = None,
    interval: Interval | Param | None = None,
    filter_by: Selection | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    line_anchor: LineAnchor | Param | None = None,
    rotate: ChannelValue | float | Param | None = None,
    styles: TextStyles | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    r"""A vertical text mark that displays textual labels.

    Like text, except that **x** defaults to the zero-based index of the data [0, 1, 2, …].

    If an **interval** is specified, such as *day*, **x** is transformed to the middle of the interval.

    Args:
        data: The data source for the mark.
        y: The vertical position channel specifying the text's anchor point, typically bound to the *y* scale.
        x: The horizontal position channel specifying the text's anchor point, typically bound to the *x* scale; defaults to the zero-based index of the data [0, 1, 2, …].
        z: An optional ordinal channel for grouping data into series.
        text: The text contents channel, possibly with line breaks (\n, \r\n, or \r). If not specified, defaults to the zero-based index [0, 1, 2, …].
        interval: An interval (such as *day* or a number), to transform **x** values to the middle of the interval.
        filter_by: Selection to filter by (defaults to data source selection).
        frame_anchor: The frame anchor specifies defaults for **x** and **y**, along with **textAnchor** and **lineAnchor**, based on the plot's frame; it may be one of the four sides (*top*, *right*, *bottom*, *left*), one of the four corners (*top-left*, *top-right*, *bottom-right*, *bottom-left*), or the *middle* of the frame.
        line_anchor: The line anchor controls how text is aligned (typically vertically) relative to its anchor point; it is one of *top*, *bottom*, or *middle*. If the frame anchor is *top*, *top-left*, or *top-right*, the default line anchor is *top*; if the frame anchor is *bottom*, *bottom-right*, or *bottom-left*, the default is *bottom*; otherwise it is *middle*.
        rotate: The rotation angle in degrees clockwise; a constant or a channel; defaults to 0°. When a number, it is interpreted as a constant; otherwise it is interpreted as a channel.
        styles: `TextStyles` to apply.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by) if data else None,
            y=column(y) if isinstance(y, str) else y,
            x=column(x) if isinstance(x, str) else x,
            z=column(z) if isinstance(z, str) else z,
            text=column(text) if isinstance(text, str) else text,
            interval=interval,
            frameAnchor=frame_anchor,
            lineAnchor=line_anchor,
            rotate=rotate,
        )
        | text_styles_config(styles)
    )

    return Mark("textY", config, options)


def text_styles_config(styles: TextStyles | None) -> dict[str, Any]:
    return dict_to_camel(dict(styles)) if styles else {}
