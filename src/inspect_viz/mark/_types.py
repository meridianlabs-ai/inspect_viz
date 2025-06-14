from typing import Literal, TypeAlias, TypedDict

from inspect_viz._core import Param

from ._channel import ChannelValue

Curve: TypeAlias = Literal[
    "basis",
    "basis-closed",
    "basis-open",
    "bundle",
    "bump-x",
    "bump-y",
    "cardinal",
    "cardinal-closed",
    "cardinal-open",
    "catmull-rom",
    "catmull-rom-closed",
    "catmull-rom-open",
    "linear",
    "linear-closed",
    "monotone-x",
    "monotone-y",
    "natural",
    "step",
    "step-after",
    "step-before",
]
"""The curve (interpolation) method for connecting adjacent points."""


Interpolate: TypeAlias = Literal[
    "none", "linear", "nearest", "barycentric", "random-walk"
]
"""The spatial interpolation method.

- *none* - do not perform interpolation (the default)
- *linear* - apply proportional linear interpolation across adjacent bins
- *nearest* - assign each pixel to the closest sample's value (Voronoi diagram)
- *barycentric* - apply barycentric interpolation over the Delaunay triangulation
- *random-walk* - apply a random walk from each pixel
"""


Symbol: TypeAlias = Literal[
    "asterisk",
    "circle",
    "cross",
    "diamond",
    "diamond2",
    "hexagon",
    "plus",
    "square",
    "square2",
    "star",
    "times",
    "triangle",
    "triangle2",
    "wye",
]
"""Symbol type for dot or density plot."""

FrameAnchor: TypeAlias = Literal[
    "middle",
    "top-left",
    "top",
    "top-right",
    "right",
    "bottom-right",
    "bottom",
    "bottom-left",
    "left",
]
"""Defaults for **x** and **y** based on the plot's frame."""

Marker: TypeAlias = Literal[
    "arrow",
    "arrow-reverse",
    "dot",
    "circle",
    "circle-fill",
    "circle-stroke",
    "tick",
    "tick-x",
    "tick-y",
]
"""Symbols used as plot markers."""

TextOverflow: TypeAlias = Literal[
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
"""The line anchor controls how text is aligned (typically vertically) relative to its anchor point."""


class TextStyles(TypedDict, total=False):
    """Text styling options."""

    text_anchor: Literal["start", "middle", "end"] | Param
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

    font_size: ChannelValue | float | Param
    """The font size in pixels; either a constant or a channel; defaults to the plot's font size, which is typically 10. When a number, it is interpreted as a constant; otherwise it is interpreted as a channel."""

    font_variant: str | Param
    """The font variant; a constant; if the **text** channel contains numbers or dates, defaults to *tabular-nums* to facilitate comparing numbers; otherwise defaults to the plot's font style, which is typically *normal*."""

    font_weight: float | Param
    """The font weight; a constant; defaults to the plot's font weight, which is typically *normal*."""
