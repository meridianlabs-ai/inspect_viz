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
from ._util import args_to_data, column_param


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
    data, x_col, y_col, z_col, text_col = resolve_text_inputs(data, x, y, z, text)

    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data._plot_from(filter_by) if data else None,
            x=column_param(data, x_col),
            y=column_param(data, y_col),
            z=column_param(data, z_col),
            text=column_param(data, text_col),
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
    data, x_col, y_col, z_col, text_col = resolve_text_inputs(data, x, y, z, text)

    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data._plot_from(filter_by) if data else None,
            x=column_param(data, x_col),
            y=column_param(data, y_col),
            z=column_param(data, z_col),
            text=column_param(data, text_col),
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
    data, x_col, y_col, z_col, text_col = resolve_text_inputs(data, x, y, z, text)

    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data._plot_from(filter_by) if data else None,
            y=column(y_col) if isinstance(y_col, str) else y_col,
            x=column(x_col) if isinstance(x_col, str) else x_col,
            z=column(z_col) if isinstance(z_col, str) else z_col,
            text=column(text_col) if isinstance(text_col, str) else text_col,
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


def resolve_text_inputs(
    data: Data | None,
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
    """Helper function to resolve and validate text mark channel inputs.

    This function handles the conversion of channel parameters to column references:
    - If data is None and parameters contain sequences (lists/tuples), creates a Data
      object with those sequences as columns named "x", "y", "z", "text".
    - For string parameters (column names), validates they exist in the data. Returns
      None if a column name doesn't exist.
    - For list/tuple parameters that were converted to columns, returns the column name
      (e.g., "x", "y", "z", "text") instead of the original sequence.
    - For other parameter types (Param objects, dicts, None), returns them unchanged.

    Args:
        data: The data source, or None to create one from sequences in parameters.
        x: The x channel specification.
        y: The y channel specification.
        z: The z channel specification.
        text: The text channel specification.

    Returns:
        A tuple of (data, x_col, y_col, z_col, text_col) where:
        - data: The Data object (created if None was passed, otherwise the original).
        - x_col, y_col, z_col, text_col: Resolved column references - either validated
          string column names, converted sequence names, or the original parameter values.
    """
    params_to_cols = {"x": x, "y": y, "z": z, "text": text}

    if data is None:
        data = args_to_data(params_to_cols)

    # Initialize with original values
    x_col, y_col, z_col, text_col = x, y, z, text

    if data:
        # For each parameter, determine the appropriate column reference
        def resolve_param(param: Any, col_name: str) -> Any:
            # If param is a string (and not a Param object), validate it exists in data
            if isinstance(param, str) and not isinstance(param, Param):
                return param if param in data.columns else None
            # If param is a sequence/list (was converted to a column), use the column name
            elif isinstance(param, (list, tuple)) and col_name in data.columns:
                return col_name
            # Otherwise return as-is (Param objects, None, etc.)
            else:
                return param

        x_col = resolve_param(x, "x")
        y_col = resolve_param(y, "y")
        z_col = resolve_param(z, "z")
        text_col = resolve_param(text, "text")

    return data, x_col, y_col, z_col, text_col
