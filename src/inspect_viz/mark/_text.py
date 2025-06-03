from typing import Any, Literal, TypedDict, cast

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._core.types import Interval
from .._util.marshall import dict_remove_none, dict_to_camel
from ..transform._column import column
from ._channel import Channel
from ._mark import Mark, MarkOptions
from ._types import FrameAnchor

TextAnchor = Literal["start", "middle", "end"]

TextOverflow = Literal[
    "clip",
    "ellipsis",
    "clip-start",
    "clip-end",
    "ellipsis-start",
    "ellipsis-middle",
    "ellipsis-end",
]
"""How to truncate (or wrap) lines of text longer than the given **line_width**; one of: 

- null (default) preserve overflowing characters (and wrap if needed);
- *clip* or *clip-end* remove characters from the end;
- *clip-start* remove characters from the start;
- *ellipsis* or *ellipsis-end* replace characters from the end with an ellipsis (…);
- *ellipsis-start* replace characters from the start with an ellipsis (…);
- *ellipsis-middle* replace characters from the middle with an ellipsis (…).

If no **title** was specified, if text requires truncation, a title containing the non-truncated text will be implicitly added."""

LineAnchor = Literal["top", "bottom", "middle"]


class TextStyles(TypedDict, total=False):
    """Text styling options."""

    text_anchor: TextAnchor | Param
    """The text anchor controls how text is aligned (typically horizontally) relative to its anchor point; it is one of *start*, *end*, or *middle*. If the frame anchor is *left*, *top-left*, or *bottom-left*, the default text anchor is *start*; if the frame anchor is *right*, *top-right*, or *bottom-right*, the default is *end*; otherwise it is *middle*."""

    line_height: float | Param
    """The line height in ems; defaults to 1. The line height affects the (typically vertical) separation between adjacent baselines of text, as well as the separation between the text and its anchor point."""

    line_width: float | Param
    """The line width in ems (e.g., 10 for about 20 characters); defaults to infinity, disabling wrapping and clipping. If **text_overflow** is null, lines will be wrapped at the specified length. If a line is split at a soft hyphen (\xad), a hyphen (-) will be displayed at the end of the line. If **text_overflow** is not null, lines will be clipped according to the given strategy."""

    text_overflow: TextOverflow | Param
    """Text overflow behavior."""

    monospace: bool | Param
    """If `True`, changes the default **font_family** to *monospace*, and uses simplified monospaced text metrics calculations."""

    font_family: str | Param
    """The font-family; a constant; defaults to the plot's font family, which is typically *system-ui*"""

    font_size: Channel | float | Param
    """The font size in pixels; either a constant or a channel; defaults to the plot's font size, which is typically 10. When a number, it is interpreted as a constant; otherwise it is interpreted as a channel."""

    font_variant: str | Param
    """The font variant; a constant; if the **text** channel contains numbers or dates, defaults to *tabular-nums* to facilitate comparing numbers; otherwise defaults to the plot's font style, which is typically *normal*."""

    font_weight: float | Param
    """The font weight; a constant; defaults to the plot's font weight, which is typically *normal*."""


def text(
    data: Data,
    x: Channel | Param,
    y: Channel | Param,
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
            data=data.plot_from(filter_by),
            x=column(x) if isinstance(x, str) else x,
            y=column(y) if isinstance(y, str) else y,
            z=column(z) if isinstance(z, str) else z,
            text=column(text) if isinstance(text, str) else text,
            frameAnchor=frame_anchor,
            lineAnchor=line_anchor,
            rotate=rotate,
        )
        | text_styles_config(styles)
    )

    return Mark("text", config, options)


def text_x(
    data: Data,
    x: Channel | Param,
    y: Channel | Param | None = None,
    z: Channel | Param | None = None,
    text: Channel | Param | None = None,
    interval: Interval | None = None,
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
            data=data.plot_from(filter_by),
            x=column(x) if isinstance(x, str) else x,
            y=column(y) if isinstance(y, str) else y,
            z=column(z) if isinstance(z, str) else z,
            text=column(text) if isinstance(text, str) else text,
            interval=interval,
            frameAnchor=frame_anchor,
            lineAnchor=line_anchor,
            rotate=rotate,
        )
        | text_styles_config(styles)
    )

    return Mark("textX", config, options)


def text_y(
    data: Data,
    y: Channel | Param,
    x: Channel | Param | None = None,
    z: Channel | Param | None = None,
    text: Channel | Param | None = None,
    interval: Interval | None = None,
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
            data=data.plot_from(filter_by),
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
