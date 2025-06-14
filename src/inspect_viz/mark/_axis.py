from typing import Any, Sequence

from typing_extensions import Unpack

from .._core import Param
from .._core.types import Interval
from .._util.marshall import dict_remove_none
from ..transform._column import column
from ._channel import ChannelSpec
from ._mark import Mark, MarkOptions
from ._text import TextStyles, text_styles_config
from ._types import FrameAnchor


def axis_x(
    x: ChannelSpec | Param | None = None,
    interval: Interval | None = None,
    text: ChannelSpec | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    line_anchor: str | Param | None = None,
    rotate: ChannelSpec | float | Param | None = None,
    text_stroke: ChannelSpec | Param | None = None,
    text_stroke_opacity: ChannelSpec | float | Param | None = None,
    text_stroke_width: ChannelSpec | float | Param | None = None,
    styles: TextStyles | None = None,
    anchor: str | Param | None = None,
    color: ChannelSpec | str | Param | None = None,
    ticks: int | Sequence[Any] | Param | None = None,
    tick_spacing: float | Param | None = None,
    tick_size: float | Param | None = None,
    tick_padding: float | Param | None = None,
    tick_format: str | Param | None = None,
    tick_rotate: float | Param | None = None,
    label: str | Param | None = None,
    label_offset: float | Param | None = None,
    label_anchor: str | Param | None = None,
    label_arrow: str | bool | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A horizontal axis mark.

    The axisX mark draws a horizontal axis at the bottom or top of the plot (or both).
    It is primarily used for displaying scales and reference lines along the x-axis.

    Args:
        x: The horizontal position channel, typically bound to the *x* scale.
        interval: How to convert a continuous value into an interval.
        text: The text channel for tick labels.
        frame_anchor: The frame anchor specifies defaults for **x** and **y** based on the plot's frame.
        line_anchor: The line anchor controls how text is aligned relative to its anchor point.
        rotate: The rotation angle of the axis in degrees clockwise.
        text_stroke: The stroke color for text labels.
        text_stroke_opacity: The stroke opacity for text labels.
        text_stroke_width: The stroke width for text labels.
        styles: `TextStyles` to apply to axis text.
        anchor: The side of the frame on which to place the axis (*top* or *bottom*).
        color: Shorthand for setting both fill and stroke color.
        ticks: The desired number of ticks, or an array of tick values, or null to disable ticks.
        tick_spacing: The desired spacing between ticks in pixels.
        tick_size: The length of tick marks in pixels.
        tick_padding: The distance between the tick mark and its label in pixels.
        tick_format: A d3-format string for formatting tick labels.
        tick_rotate: The rotation angle of tick labels in degrees clockwise.
        label: The axis label text.
        label_offset: The distance between the axis and its label in pixels.
        label_anchor: The label anchor position.
        label_arrow: Whether to show an arrow on the axis label.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            x=column(x) if isinstance(x, str) else x,
            interval=interval,
            text=column(text) if isinstance(text, str) else text,
            frameAnchor=frame_anchor,
            lineAnchor=line_anchor,
            rotate=rotate,
            textStroke=text_stroke,
            textStrokeOpacity=text_stroke_opacity,
            textStrokeWidth=text_stroke_width,
            anchor=anchor,
            color=color,
            ticks=ticks,
            tickSpacing=tick_spacing,
            tickSize=tick_size,
            tickPadding=tick_padding,
            tickFormat=tick_format,
            tickRotate=tick_rotate,
            label=label,
            labelOffset=label_offset,
            labelAnchor=label_anchor,
            labelArrow=label_arrow,
        )
        | text_styles_config(styles)
    )

    return Mark("axisX", config, options)


def axis_y(
    y: ChannelSpec | Param | None = None,
    interval: Interval | None = None,
    text: ChannelSpec | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    line_anchor: str | Param | None = None,
    rotate: ChannelSpec | float | Param | None = None,
    text_stroke: ChannelSpec | Param | None = None,
    text_stroke_opacity: ChannelSpec | float | Param | None = None,
    text_stroke_width: ChannelSpec | float | Param | None = None,
    styles: TextStyles | None = None,
    anchor: str | Param | None = None,
    color: ChannelSpec | str | Param | None = None,
    ticks: int | Sequence[Any] | Param | None = None,
    tick_spacing: float | Param | None = None,
    tick_size: float | Param | None = None,
    tick_padding: float | Param | None = None,
    tick_format: str | Param | None = None,
    tick_rotate: float | Param | None = None,
    label: str | Param | None = None,
    label_offset: float | Param | None = None,
    label_anchor: str | Param | None = None,
    label_arrow: str | bool | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A vertical axis mark.

    The axisY mark draws a vertical axis at the left or right of the plot (or both).
    It is primarily used for displaying scales and reference lines along the y-axis.

    Args:
        y: The vertical position channel, typically bound to the *y* scale.
        interval: How to convert a continuous value into an interval.
        text: The text channel for tick labels.
        frame_anchor: The frame anchor specifies defaults for **x** and **y** based on the plot's frame.
        line_anchor: The line anchor controls how text is aligned relative to its anchor point.
        rotate: The rotation angle of the axis in degrees clockwise.
        text_stroke: The stroke color for text labels.
        text_stroke_opacity: The stroke opacity for text labels.
        text_stroke_width: The stroke width for text labels.
        styles: `TextStyles` to apply to axis text.
        anchor: The side of the frame on which to place the axis (*left* or *right*).
        color: Shorthand for setting both fill and stroke color.
        ticks: The desired number of ticks, or an array of tick values, or null to disable ticks.
        tick_spacing: The desired spacing between ticks in pixels.
        tick_size: The length of tick marks in pixels.
        tick_padding: The distance between the tick mark and its label in pixels.
        tick_format: A d3-format string for formatting tick labels.
        tick_rotate: The rotation angle of tick labels in degrees clockwise.
        label: The axis label text.
        label_offset: The distance between the axis and its label in pixels.
        label_anchor: The label anchor position.
        label_arrow: Whether to show an arrow on the axis label.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            y=column(y) if isinstance(y, str) else y,
            interval=interval,
            text=column(text) if isinstance(text, str) else text,
            frameAnchor=frame_anchor,
            lineAnchor=line_anchor,
            rotate=rotate,
            textStroke=text_stroke,
            textStrokeOpacity=text_stroke_opacity,
            textStrokeWidth=text_stroke_width,
            anchor=anchor,
            color=color,
            ticks=ticks,
            tickSpacing=tick_spacing,
            tickSize=tick_size,
            tickPadding=tick_padding,
            tickFormat=tick_format,
            tickRotate=tick_rotate,
            label=label,
            labelOffset=label_offset,
            labelAnchor=label_anchor,
            labelArrow=label_arrow,
        )
        | text_styles_config(styles)
    )

    return Mark("axisY", config, options)


def axis_fx(
    x: ChannelSpec | Param | None = None,
    interval: Interval | None = None,
    text: ChannelSpec | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    line_anchor: str | Param | None = None,
    rotate: ChannelSpec | float | Param | None = None,
    text_stroke: ChannelSpec | Param | None = None,
    text_stroke_opacity: ChannelSpec | float | Param | None = None,
    text_stroke_width: ChannelSpec | float | Param | None = None,
    styles: TextStyles | None = None,
    anchor: str | Param | None = None,
    color: ChannelSpec | str | Param | None = None,
    ticks: int | Sequence[Any] | Param | None = None,
    tick_spacing: float | Param | None = None,
    tick_size: float | Param | None = None,
    tick_padding: float | Param | None = None,
    tick_format: str | Param | None = None,
    tick_rotate: float | Param | None = None,
    label: str | Param | None = None,
    label_offset: float | Param | None = None,
    label_anchor: str | Param | None = None,
    label_arrow: str | bool | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A horizontal facet axis mark.

    The axisFx mark draws a horizontal axis for faceted plots.
    It is primarily used for displaying scales and reference lines along the fx-axis in faceted visualizations.

    Args:
        x: The horizontal position channel, typically bound to the *x* scale.
        interval: How to convert a continuous value into an interval.
        text: The text channel for tick labels.
        frame_anchor: The frame anchor specifies defaults for **x** and **y** based on the plot's frame.
        line_anchor: The line anchor controls how text is aligned relative to its anchor point.
        rotate: The rotation angle of the axis in degrees clockwise.
        text_stroke: The stroke color for text labels.
        text_stroke_opacity: The stroke opacity for text labels.
        text_stroke_width: The stroke width for text labels.
        styles: `TextStyles` to apply to axis text.
        anchor: The side of the frame on which to place the axis (*top* or *bottom*).
        color: Shorthand for setting both fill and stroke color.
        ticks: The desired number of ticks, or an array of tick values, or null to disable ticks.
        tick_spacing: The desired spacing between ticks in pixels.
        tick_size: The length of tick marks in pixels.
        tick_padding: The distance between the tick mark and its label in pixels.
        tick_format: A d3-format string for formatting tick labels.
        tick_rotate: The rotation angle of tick labels in degrees clockwise.
        label: The axis label text.
        label_offset: The distance between the axis and its label in pixels.
        label_anchor: The label anchor position.
        label_arrow: Whether to show an arrow on the axis label.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            x=column(x) if isinstance(x, str) else x,
            interval=interval,
            text=column(text) if isinstance(text, str) else text,
            frameAnchor=frame_anchor,
            lineAnchor=line_anchor,
            rotate=rotate,
            textStroke=text_stroke,
            textStrokeOpacity=text_stroke_opacity,
            textStrokeWidth=text_stroke_width,
            anchor=anchor,
            color=color,
            ticks=ticks,
            tickSpacing=tick_spacing,
            tickSize=tick_size,
            tickPadding=tick_padding,
            tickFormat=tick_format,
            tickRotate=tick_rotate,
            label=label,
            labelOffset=label_offset,
            labelAnchor=label_anchor,
            labelArrow=label_arrow,
        )
        | text_styles_config(styles)
    )

    return Mark("axisFx", config, options)


def axis_fy(
    y: ChannelSpec | Param | None = None,
    interval: Interval | None = None,
    text: ChannelSpec | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    line_anchor: str | Param | None = None,
    rotate: ChannelSpec | float | Param | None = None,
    text_stroke: ChannelSpec | Param | None = None,
    text_stroke_opacity: ChannelSpec | float | Param | None = None,
    text_stroke_width: ChannelSpec | float | Param | None = None,
    styles: TextStyles | None = None,
    anchor: str | Param | None = None,
    color: ChannelSpec | str | Param | None = None,
    ticks: int | Sequence[Any] | Param | None = None,
    tick_spacing: float | Param | None = None,
    tick_size: float | Param | None = None,
    tick_padding: float | Param | None = None,
    tick_format: str | Param | None = None,
    tick_rotate: float | Param | None = None,
    label: str | Param | None = None,
    label_offset: float | Param | None = None,
    label_anchor: str | Param | None = None,
    label_arrow: str | bool | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A vertical facet axis mark.

    The axisFy mark draws a vertical axis for faceted plots.
    It is primarily used for displaying scales and reference lines along the fy-axis in faceted visualizations.

    Args:
        y: The vertical position channel, typically bound to the *y* scale.
        interval: How to convert a continuous value into an interval.
        text: The text channel for tick labels.
        frame_anchor: The frame anchor specifies defaults for **x** and **y** based on the plot's frame.
        line_anchor: The line anchor controls how text is aligned relative to its anchor point.
        rotate: The rotation angle of the axis in degrees clockwise.
        text_stroke: The stroke color for text labels.
        text_stroke_opacity: The stroke opacity for text labels.
        text_stroke_width: The stroke width for text labels.
        styles: `TextStyles` to apply to axis text.
        anchor: The side of the frame on which to place the axis (*left* or *right*).
        color: Shorthand for setting both fill and stroke color.
        ticks: The desired number of ticks, or an array of tick values, or null to disable ticks.
        tick_spacing: The desired spacing between ticks in pixels.
        tick_size: The length of tick marks in pixels.
        tick_padding: The distance between the tick mark and its label in pixels.
        tick_format: A d3-format string for formatting tick labels.
        tick_rotate: The rotation angle of tick labels in degrees clockwise.
        label: The axis label text.
        label_offset: The distance between the axis and its label in pixels.
        label_anchor: The label anchor position.
        label_arrow: Whether to show an arrow on the axis label.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            y=column(y) if isinstance(y, str) else y,
            interval=interval,
            text=column(text) if isinstance(text, str) else text,
            frameAnchor=frame_anchor,
            lineAnchor=line_anchor,
            rotate=rotate,
            textStroke=text_stroke,
            textStrokeOpacity=text_stroke_opacity,
            textStrokeWidth=text_stroke_width,
            anchor=anchor,
            color=color,
            ticks=ticks,
            tickSpacing=tick_spacing,
            tickSize=tick_size,
            tickPadding=tick_padding,
            tickFormat=tick_format,
            tickRotate=tick_rotate,
            label=label,
            labelOffset=label_offset,
            labelAnchor=label_anchor,
            labelArrow=label_arrow,
        )
        | text_styles_config(styles)
    )

    return Mark("axisFy", config, options)
