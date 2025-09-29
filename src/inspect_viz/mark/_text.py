from typing import Any

from typing_extensions import Unpack

from inspect_viz.mark._types import TextStyles

from .._core import Data, Param, Selection
from .._core.types import Interval
from .._util.marshall import dict_remove_none, dict_to_camel
from ..transform._column import column
from ._channel import Channel, ChannelIntervalSpec, ChannelSpec
from ._mark import Mark
from ._options import MarkOptions
from ._types import FrameAnchor, LineAnchor
from ._util import args_to_data, check_column_names, column_param


def text(
    data: Data | None = None,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    text: Channel | Param | None = None,
    filter_by: Selection | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    line_anchor: LineAnchor | Param | None = None,
    rotate: Channel | float | Param | None = None,
    styles: TextStyles | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    r"""A text mark that displays textual labels.

    Args:
        data: The data source for the mark (not required if not binding `text` to a column). If None, any of x, y, z, text can be provided as sequences.
        x: The horizontal position channel specifying the text's anchor point, typically bound to the *x* scale. When data is None, can be a sequence of x-coordinates.
        y: The vertical position channel specifying the text's anchor point, typically bound to the *y* scale. When data is None, can be a sequence of y-coordinates.
        z: An optional ordinal channel for grouping data into series. When data is None, can be a sequence of z-values.
        text: The text contents channel, possibly with line breaks (\n, \r\n, or \r). When data is None, can be a sequence of text values. To place a single piece of text specify the text as a string[] (e.g. `["My Text"]`).
        filter_by: Selection to filter by (defaults to data source selection).
        frame_anchor: The frame anchor specifies defaults for **x** and **y**, along with **textAnchor** and **lineAnchor**, based on the plot's frame; it may be one of the four sides (*top*, *right*, *bottom*, *left*), one of the four corners (*top-left*, *top-right*, *bottom-right*, *bottom-left*), or the *middle* of the frame.
        line_anchor: The line anchor controls how text is aligned (typically vertically) relative to its anchor point; it is one of *top*, *bottom*, or *middle*. If the frame anchor is *top*, *top-left*, or *top-right*, the default line anchor is *top*; if the frame anchor is *bottom*, *bottom-right*, or *bottom-left*, the default is *bottom*; otherwise it is *middle*.
        rotate: The rotation angle in degrees clockwise; a constant or a channel; defaults to 0°. When a number, it is interpreted as a constant; otherwise it is interpreted as a channel.
        styles: `TextStyles` to apply.
        **options: Additional `MarkOptions`.
    """
    if data is None:
        data, x, y, z, text = infer_text_mark_config_inputs(data, x, y, z, text)  # type: ignore

    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data._plot_from(filter_by) if data else None,
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
    x: ChannelSpec | Param,
    y: ChannelIntervalSpec | Param | None = None,
    z: Channel | Param | None = None,
    text: Channel | Param | None = None,
    interval: Interval | Param | None = None,
    filter_by: Selection | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    line_anchor: LineAnchor | Param | None = None,
    rotate: Channel | float | Param | None = None,
    styles: TextStyles | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    r"""A horizontal text mark that displays textual labels.

    Like text, except that **y** defaults to the zero-based index of the data [0, 1, 2, …].

    If an **interval** is specified, such as *day*, **y** is transformed to the middle of the interval.

    Args:
        data: The data source for the mark. If None, any of x, y, z, text can be provided as sequences.
        x: The horizontal position channel specifying the text's anchor point, typically bound to the *x* scale. When data is None, can be a sequence of x-coordinates.
        y: The vertical position channel specifying the text's anchor point, typically bound to the *y* scale; defaults to the zero-based index of the data [0, 1, 2, …].
        z: An optional ordinal channel for grouping data into series. When data is None, can be a sequence of z-values.
        text: The text contents channel, possibly with line breaks (\n, \r\n, or \r). When data is None, can be a sequence of text values. If not specified, defaults to the zero-based index [0, 1, 2, …].
        interval: An interval (such as *day* or a number), to transform **y** values to the middle of the interval.
        filter_by: Selection to filter by (defaults to data source selection).
        frame_anchor: The frame anchor specifies defaults for **x** and **y**, along with **textAnchor** and **lineAnchor**, based on the plot's frame; it may be one of the four sides (*top*, *right*, *bottom*, *left*), one of the four corners (*top-left*, *top-right*, *bottom-right*, *bottom-left*), or the *middle* of the frame.
        line_anchor: The line anchor controls how text is aligned (typically vertically) relative to its anchor point; it is one of *top*, *bottom*, or *middle*. If the frame anchor is *top*, *top-left*, or *top-right*, the default line anchor is *top*; if the frame anchor is *bottom*, *bottom-right*, or *bottom-left*, the default is *bottom*; otherwise it is *middle*.
        rotate: The rotation angle in degrees clockwise; a constant or a channel; defaults to 0°. When a number, it is interpreted as a constant; otherwise it is interpreted as a channel.
        styles: `TextStyles` to apply.
        **options: Additional `MarkOptions`.
    """
    if data is None:
        data, x, y, z, text = infer_text_mark_config_inputs(data, x, y, z, text)  # type: ignore

    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data._plot_from(filter_by) if data else None,
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
    y: ChannelSpec | Param,
    x: ChannelIntervalSpec | Param | None = None,
    z: Channel | Param | None = None,
    text: Channel | Param | None = None,
    interval: Interval | Param | None = None,
    filter_by: Selection | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    line_anchor: LineAnchor | Param | None = None,
    rotate: Channel | float | Param | None = None,
    styles: TextStyles | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    r"""A vertical text mark that displays textual labels.

    Like text, except that **x** defaults to the zero-based index of the data [0, 1, 2, …].

    If an **interval** is specified, such as *day*, **x** is transformed to the middle of the interval.

    Args:
        data: The data source for the mark. If None, any of x, y, z, text can be provided as sequences.
        y: The vertical position channel specifying the text's anchor point, typically bound to the *y* scale. When data is None, can be a sequence of y-coordinates.
        x: The horizontal position channel specifying the text's anchor point, typically bound to the *x* scale; defaults to the zero-based index of the data [0, 1, 2, …].
        z: An optional ordinal channel for grouping data into series. When data is None, can be a sequence of z-values.
        text: The text contents channel, possibly with line breaks (\n, \r\n, or \r). When data is None, can be a sequence of text values. If not specified, defaults to the zero-based index [0, 1, 2, …].
        interval: An interval (such as *day* or a number), to transform **x** values to the middle of the interval.
        filter_by: Selection to filter by (defaults to data source selection).
        frame_anchor: The frame anchor specifies defaults for **x** and **y**, along with **textAnchor** and **lineAnchor**, based on the plot's frame; it may be one of the four sides (*top*, *right*, *bottom*, *left*), one of the four corners (*top-left*, *top-right*, *bottom-right*, *bottom-left*), or the *middle* of the frame.
        line_anchor: The line anchor controls how text is aligned (typically vertically) relative to its anchor point; it is one of *top*, *bottom*, or *middle*. If the frame anchor is *top*, *top-left*, or *top-right*, the default line anchor is *top*; if the frame anchor is *bottom*, *bottom-right*, or *bottom-left*, the default is *bottom*; otherwise it is *middle*.
        rotate: The rotation angle in degrees clockwise; a constant or a channel; defaults to 0°. When a number, it is interpreted as a constant; otherwise it is interpreted as a channel.
        styles: `TextStyles` to apply.
        **options: Additional `MarkOptions`.
    """
    if data is None:
        data, x, y, z, text = infer_text_mark_config_inputs(data, x, y, z, text)  # type: ignore

    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data._plot_from(filter_by) if data else None,
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


def infer_text_mark_config_inputs(
    x: ChannelIntervalSpec | ChannelSpec | Param | None,
    y: ChannelIntervalSpec | ChannelSpec | Param | None,
    z: Channel | Param | None,
    text: Channel | Param | None,
) -> tuple[
    Data | None,
    ChannelIntervalSpec | ChannelSpec | Param | None,
    ChannelIntervalSpec | ChannelSpec | Param | None,
    Channel | Param | None,
    Channel | Param | None,
]:
    """Helper function to infer the text mark config inputs when data is created from args."""
    data = args_to_data({"x": x, "y": y, "z": z, "text": text})

    # data might be empty if no args are provided (this is intended behavior that's why we don't raise)
    if data:
        # reassign parameters to column names for column_param
        x, y, z, text = check_column_names(data, ["x", "y", "z", "text"])
    return data, x, y, z, text
