from typing import Any, Literal, TypedDict

from .._core.param import Param
from .._core.types import Interval
from .._util.marshall import snake_to_camel

# Type aliases for literal types
PositionScaleType = Literal[
    "linear",
    "log",
    "pow",
    "sqrt",
    "symlog",
    "utc",
    "time",
    "point",
    "band",
    "ordinal",
    "threshold",
    "quantile",
    "quantize",
    "identity",
]

DiscreteScaleType = Literal[
    "ordinal",
    "categorical",
    "threshold",
    "quantile",
    "quantize",
]

ProjectionName = Literal[
    "albers",
    "albers-usa",
    "azimuthal-equal-area",
    "azimuthal-equidistant",
    "conic-conformal",
    "conic-equal-area",
    "conic-equidistant",
    "equal-earth",
    "equirectangular",
    "gnomonic",
    "identity",
    "mercator",
    "natural-earth1",
    "orthographic",
    "stereographic",
    "transverse-mercator",
]

ContinuousScaleType = Literal[
    "linear",
    "log",
    "pow",
    "sqrt",
    "symlog",
    "utc",
    "time",
    "identity",
]

ColorScaleType = Literal[
    "linear",
    "log",
    "pow",
    "sqrt",
    "symlog",
    "utc",
    "time",
    "ordinal",
    "categorical",
    "threshold",
    "quantile",
    "quantize",
    "diverging",
    "diverging-log",
    "diverging-pow",
    "diverging-symlog",
    "cyclical",
    "sequential",
    "rainbow",
    "sinebow",
]

ColorScheme = Literal[
    "accent",
    "blues",
    "brbg",
    "bugn",
    "bupu",
    "category10",
    "dark2",
    "gnbu",
    "greens",
    "greys",
    "magma",
    "oranges",
    "orrd",
    "paired",
    "pastel1",
    "pastel2",
    "piyg",
    "plasma",
    "prgn",
    "pubu",
    "pubugn",
    "puor",
    "purd",
    "purples",
    "rdbu",
    "rdgy",
    "rdpu",
    "rdylbu",
    "rdylgn",
    "reds",
    "set1",
    "set2",
    "set3",
    "spectral",
    "tableau10",
    "turbo",
    "viridis",
    "warm",
    "cool",
    "cubehelix",
    "rainbow",
    "sinebow",
]

Interpolate = Literal[
    "rgb",
    "hsl",
    "lab",
    "hcl",
    "cubehelix",
]


LabelArrow = (
    Literal[
        "auto",
        "up",
        "right",
        "down",
        "left",
        "none",
    ]
    | bool
    | None
)


class PlotOptions(TypedDict, total=False):
    """Plot attributes."""

    aspect_ratio: float | bool | None | Param
    """The desired aspect ratio of the *x* and *y* scales, affecting the default
    height. Given an aspect ratio of *dx* / *dy*, and assuming that the *x* and
    *y* scales represent equivalent units (say, degrees Celsius or meters),
    computes a default height such that *dx* pixels along *x* represents the
    same variation as *dy* pixels along *y*. Note: when faceting, set the *fx*
    and *fy* scales' **round** option to false for an exact aspect ratio."""

    margin: float | Param
    """Shorthand to set the same default for all four margins: **margin_top**,
    **margin_right**, **margin_bottom**, and **margin_left**. Otherwise, the
    default margins depend on the maximum margins of the plot's marks. While
    most marks default to zero margins (because they are drawn inside the chart
    area), Plot's axis marks have non-zero default margins."""

    margin_top: float | Param
    """The top margin; the distance in pixels between the top edges of the inner
    and outer plot area. Defaults to the maximum top margin of the plot's
    marks."""

    margin_right: float | Param
    """The right margin; the distance in pixels between the right edges of the
    inner and outer plot area. Defaults to the maximum right margin of the
    plot's marks."""

    margin_bottom: float | Param
    """The bottom margin; the distance in pixels between the bottom edges of the
    inner and outer plot area. Defaults to the maximum bottom margin of the
    plot's marks."""

    margin_left: float | Param
    """The left margin; the distance in pixels between the left edges of the inner
    and outer plot area. Defaults to the maximum left margin of the plot's
    marks."""

    margins: dict[str, float | Param]
    """A shorthand object notation for setting multiple margin values.
    The object keys are margin names (top, right, etc)."""

    inset: float | Param
    """Shorthand to set the same default for all four insets: **inset_top**,
    **inset_right**, **inset_bottom**, and **inset_left**. All insets typically
    default to zero, though not always (say when using bin transform). A
    positive inset reduces effective area, while a negative inset increases it."""

    style: str | dict[str, str] | None | Param
    """Custom styles to override Plot's defaults. Styles may be specified either
    as a string of inline styles (*e.g.*, `"color: red;"`, in the same fashion
    as assigning [*element*.style][1]) or an object of properties (*e.g.*,
    `{color: "red"}`, in the same fashion as assigning [*element*.style
    properties][2]). Note that unitless numbers ([quirky lengths][3]) such as
    `{padding: 20}` may not supported by some browsers; you should instead
    specify a string with units such as `{padding: "20px"}`. By default, the
    returned plot has a max-width of 100%, and the system-ui font. Plot's marks
    and axes default to [currentColor][4], meaning that they will inherit the
    surrounding content's color.

    [1]: https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style
    [2]: https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleDeclaration
    [3]: https://www.w3.org/TR/css-values-4/#deprecated-quirky-length
    [4]: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value#currentcolor_keyword"""

    align: float | Param
    """How to distribute unused space in the **range** for *point* and *band*
    scales. A number in [0, 1], such as:

    - 0 - use the start of the range, putting unused space at the end
    - 0.5 (default) - use the middle, distributing unused space evenly
    - 1 use the end, putting unused space at the start

    For ordinal position scales only."""

    padding: float | Param
    """For *band* scales, how much of the **range** to reserve to separate
    adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of
    inset for the first and last value as a proportion of the bandwidth;
    defaults to 0.5 (50%).

    For ordinal position scales only."""

    axis: Literal["top", "right", "bottom", "left", "both"] | bool | None | Param
    """The side of the frame on which to place the implicit axis: *top* or
    *bottom* for *x* or *fx*, or *left* or *right* for *y* or *fy*. The default
    depends on the scale:

    - *x* - *bottom*
    - *y* - *left*
    - *fx* - *top* if there is a *bottom* *x* axis, and otherwise *bottom*
    - *fy* - *right* if there is a *left* *y* axis, and otherwise *right*

    If *both*, an implicit axis will be rendered on both sides of the plot
    (*top* and *bottom* for *x* or *fx*, or *left* and *right* for *y* or
    *fy*). If null, the implicit axis is suppressed.

    For position axes only."""

    aria_label: str | None
    """The [aria-label attribute][1] on the SVG root.

    [1]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-label"""

    aria_description: str | None
    """The [aria-description attribute][1] on the SVG root.

    [1]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-description"""

    clip: Literal["frame", "sphere"] | bool | None | Param
    """The default clip for all marks."""

    # x scale attributes

    x_scale: PositionScaleType | None | Param
    """The *x* scale type, affecting how the scale encodes abstract data, say by
    applying a mathematical transformation. If null, the scale is disabled.

    For quantitative data (numbers), defaults to *linear*; for temporal data
    (dates), defaults to *utc*; for ordinal data (strings or booleans),
    defaults to *point* for position scales, *categorical* for color scales,
    and otherwise *ordinal*. However, the radius scale defaults to *sqrt*, and
    the length and opacity scales default to *linear*; these scales are
    intended for quantitative data. The plot's marks may also impose a scale
    type; for example, the barY mark requires that *x* is a *band* scale."""

    x_domain: Literal["fixed"] | list[str | float | bool] | Param
    """The extent of the scale's inputs (abstract values). By default inferred
    from channel values. For continuous data (numbers and dates), it is
    typically [*min*, *max*]; it can be [*max*, *min*] to reverse the scale.
    For ordinal data (strings or booleans), it is an array (or iterable) of
    values is the desired order, defaulting to natural ascending order.

    Linear scales have a default domain of [0, 1]. Log scales have a default
    domain of [1, 10] and cannot include zero. Radius scales have a default
    domain from 0 to the median first quartile of associated channels. Length
    have a default domain from 0 to the median median of associated channels.
    Opacity scales have a default domain from 0 to the maximum value of
    associated channels."""

    x_range: list[str | float | bool] | Param
    """The extent of the scale's outputs (visual values). By default inferred from
    the scale's **type** and **domain**, and for position scales, the plot's
    dimensions. For continuous data (numbers and dates), and for ordinal
    position scales (*point* and *band*), it is typically [*min*, *max*]; it
    can be [*max*, *min*] to reverse the scale."""

    x_nice: bool | float | Interval | Param
    """If true, or a tick count or interval, extend the domain to nice round
    values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and
    nice time intervals for *utc* and *time* scales. Pass an interval such as
    *minute*, *wednesday* or *month* to specify what constitutes a nice
    interval.

    For continuous scales only."""

    x_inset: float | Param
    """Shorthand to set the same default for all four insets: **inset_top**,
    **inset_right**, **inset_bottom**, and **inset_left**. All insets typically
    default to zero, though not always (say when using bin transform). A
    positive inset reduces effective area, while a negative inset increases it."""

    x_inset_right: float | Param
    """Insets the right edge by the specified number of pixels. A positive value
    insets towards the left edge (reducing effective area), while a negative
    value insets away from the left edge (increasing it)."""

    x_inset_left: float | Param
    """Insets the left edge by the specified number of pixels. A positive value
    insets towards the right edge (reducing effective area), while a negative
    value insets away from the right edge (increasing it)."""

    x_clamp: bool | Param
    """If true, values below the domain minimum are treated as the domain minimum,
    and values above the domain maximum are treated as the domain maximum.

    Clamping is useful for focusing on a subset of the data while ensuring that
    extreme values remain visible, but use caution: clamped values may need an
    annotation to avoid misinterpretation. Clamping typically requires setting
    an explicit **domain** since if the domain is inferred, no values will be
    outside the domain.

    For continuous scales only."""

    x_round: bool | Param
    """If true, round the output value to the nearest integer (pixel); useful for
    crisp edges when rendering.

    For position scales only."""

    x_align: float | Param
    """How to distribute unused space in the **range** for *point* and *band*
    scales. A number in [0, 1], such as:

    - 0 - use the start of the range, putting unused space at the end
    - 0.5 (default) - use the middle, distributing unused space evenly
    - 1 use the end, putting unused space at the start

    For ordinal position scales only."""

    x_padding: float | Param
    """For *band* scales, how much of the **range** to reserve to separate
    adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of
    inset for the first and last value as a proportion of the bandwidth;
    defaults to 0.5 (50%).

    For ordinal position scales only."""

    x_padding_inner: float | Param
    """For a *band* scale, how much of the range to reserve to separate
    adjacent bands."""

    x_padding_outer: float | Param
    """For a *band* scale, how much of the range to reserve to inset first and
    last bands."""

    x_axis: Literal["top", "bottom", "both"] | bool | None | Param
    """The side of the frame on which to place the implicit axis: *top* or
    *bottom* for *x*. Defaults to *bottom* for an *x* scale.

    If *both*, an implicit axis will be rendered on both sides of the plot
    (*top* and *bottom* for *x*). If null, the implicit axis is suppressed."""

    x_ticks: float | Interval | list[str | float | bool] | Param
    """The desired approximate number of axis ticks, or an explicit array of tick
    values, or an interval such as *day* or *month*."""

    x_tick_size: float | Param
    """The length of axis tick marks in pixels; negative values extend in the
    opposite direction. Defaults to 6 for *x* and *y* axes and *color* and
    *opacity* *ramp* legends, and 0 for *fx* and *fy* axes."""

    x_tick_spacing: float | Param
    """The desired approximate spacing between adjacent axis ticks, affecting the
    default **ticks**; defaults to 80 pixels for *x* and *fx*, and 35 pixels
    for *y* and *fy*."""

    x_tick_padding: float | Param
    """The distance between an axis tick mark and its associated text label (in
    pixels); often defaults to 3, but may be affected by **x_tick_size** and
    **x_tick_rotate**."""

    x_tick_format: str | None | Param
    """How to format inputs (abstract values) for axis tick labels; one of:

    - a [d3-format][1] string for numeric scales
    - a [d3-time-format][2] string for temporal scales

    [1]: https://d3js.org/d3-time
    [2]: https://d3js.org/d3-time-format"""

    x_tick_rotate: float | Param
    """The rotation angle of axis tick labels in degrees clocksize; defaults to 0."""

    x_line: bool | Param
    """If true, draw a line along the axis; if false (default), do not."""

    x_label_anchor: Literal["top", "right", "bottom", "left", "center"] | Param
    """Where to place the axis **label** relative to the plot's frame. For
    vertical position scales (*y* and *fy*), may be *top*, *bottom*, or
    *center*; for horizontal position scales (*x* and *fx*), may be *left*,
    *right*, or *center*. Defaults to *center* for ordinal scales (including
    *fx* and *fy*), and otherwise *top* for *y*, and *right* for *x*."""

    x_label_arrow: LabelArrow | Param
    """Whether to apply a directional arrow such as → or ↑ to the x-axis scale
    label. If *auto* (the default), the presence of the arrow depends on
    whether the scale is ordinal."""

    x_label_offset: float | Param
    """The axis **label** position offset (in pixels); default depends on margins
    and orientation."""

    x_font_variant: str | Param
    """The font-variant attribute for axis ticks; defaults to *tabular-nums* for
    quantitative axes."""

    x_aria_label: str | Param
    """A short label representing the axis in the accessibility tree."""

    x_aria_description: str | Param
    """A textual description for the axis in the accessibility tree."""

    x_percent: bool | Param
    """If true, shorthand for a transform suitable for percentages, mapping
    proportions in [0, 1] to [0, 100]."""

    x_reverse: bool | Param
    """Whether to reverse the scale's encoding; equivalent to reversing either the
    **domain** or **range**."""

    x_zero: bool | Param
    """Whether the **domain** must include zero. If the domain minimum is
    positive, it will be set to zero; otherwise if the domain maximum is
    negative, it will be set to zero.

    For quantitative scales only."""

    x_exponent: float | Param
    """A power scale's exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a
    linear scale. For *pow* scales only."""

    x_base: float | Param
    """A log scale's base; defaults to 10. Does not affect the scale's encoding,
    but rather the default ticks. For *log* scales only."""

    x_constant: float | Param
    """A symlog scale's constant, expressing the magnitude of the linear region
    around the origin; defaults to 1. For *symlog* scales only."""

    # y scale attributes

    y_scale: PositionScaleType | None | Param
    """The *y* scale type, affecting how the scale encodes abstract data, say by
    applying a mathematical transformation. If null, the scale is disabled.

    For quantitative data (numbers), defaults to *linear*; for temporal data
    (dates), defaults to *utc*; for ordinal data (strings or booleans),
    defaults to *point* for position scales,  The plot's marks may also impose
    a scale type; for example, the barY mark requires that *x* is a *band*
    scale."""

    y_domain: Literal["fixed"] | list[str | float | bool] | Param
    """The extent of the scale's inputs (abstract values). By default inferred
    from channel values. For continuous data (numbers and dates), it is
    typically [*min*, *max*]; it can be [*max*, *min*] to reverse the scale.
    For ordinal data (strings or booleans), it is an array (or iterable) of
    values is the desired order, defaulting to natural ascending order.

    Linear scales have a default domain of [0, 1]. Log scales have a default
    domain of [1, 10] and cannot include zero."""

    y_range: list[str | float | bool] | Param
    """The extent of the scale's outputs (visual values). By default inferred
    from the scale's **type** and **domain**, and for position scales, the
    plot's dimensions. For continuous data (numbers and dates), and for
    ordinal position scales (*point* and *band*), it is typically [*min*,
    *max*]; it can be [*max*, *min*] to reverse the scale."""

    y_nice: bool | float | Interval | Param
    """If true, or a tick count or interval, extend the domain to nice round
    values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and
    nice time intervals for *utc* and *time* scales. Pass an interval such as
    *minute*, *wednesday* or *month* to specify what constitutes a nice
    interval.

    For continuous scales only."""

    y_inset: float | Param
    """Shorthand to set the same default for all four insets: **inset_top**,
    **inset_right**, **inset_bottom**, and **inset_left**. All insets typically
    default to zero, though not always (say when using bin transform). A
    positive inset reduces effective area, while a negative inset increases it."""

    y_inset_top: float | Param
    """Insets the top edge by the specified number of pixels. A positive value
    insets towards the bottom edge (reducing effective area), while a negative
    value insets away from the bottom edge (increasing it)."""

    y_inset_bottom: float | Param
    """Insets the bottom edge by the specified number of pixels. A positive value
    insets towards the top edge (reducing effective area), while a negative
    value insets away from the top edge (increasing it)."""

    y_clamp: bool | Param
    """If true, values below the domain minimum are treated as the domain minimum,
    and values above the domain maximum are treated as the domain maximum.

    Clamping is useful for focusing on a subset of the data while ensuring that
    extreme values remain visible, but use caution: clamped values may need an
    annotation to avoid misinterpretation. Clamping typically requires setting
    an explicit **domain** since if the domain is inferred, no values will be
    outside the domain.

    For continuous scales only."""

    y_round: bool | Param
    """If true, round the output value to the nearest integer (pixel); useful for
    crisp edges when rendering.

    For position scales only."""

    y_align: float | Param
    """How to distribute unused space in the **range** for *point* and *band*
    scales. A number in [0, 1], such as:

    - 0 - use the start of the range, putting unused space at the end
    - 0.5 (default) - use the middle, distributing unused space evenly
    - 1 use the end, putting unused space at the start

    For ordinal position scales only."""

    y_padding: float | Param
    """For *band* scales, how much of the **range** to reserve to separate
    adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of
    inset for the first and last value as a proportion of the bandwidth;
    defaults to 0.5 (50%).

    For ordinal position scales only."""

    y_padding_inner: float | Param
    """For a *band* scale, how much of the range to reserve to separate
    adjacent bands."""

    y_padding_outer: float | Param
    """For a *band* scale, how much of the range to reserve to inset first and
    last bands."""

    y_axis: Literal["left", "right", "both"] | bool | None | Param
    """The side of the frame on which to place the implicit axis: *left* or
    *right* for *y*. Defaults to *left* for a *y* scale.

    If *both*, an implicit axis will be rendered on both sides of the plot
    (*left* and *right* for *y*). If null, the implicit axis is suppressed."""

    y_ticks: float | Interval | list[str | float | bool] | Param
    """The desired approximate number of axis ticks, or an explicit array of tick
    values, or an interval such as *day* or *month*."""

    y_tick_size: float | Param
    """The length of axis tick marks in pixels; negative values extend in the
    opposite direction. Defaults to 6 for *x* and *y* axes and *color* and
    *opacity* *ramp* legends, and 0 for *fx* and *fy* axes."""

    y_tick_spacing: float | Param
    """The desired approximate spacing between adjacent axis ticks, affecting the
    default **ticks**; defaults to 80 pixels for *x* and *fx*, and 35 pixels
    for *y* and *fy*."""

    y_tick_padding: float | Param
    """The distance between an axis tick mark and its associated text label (in
    pixels); often defaults to 3, but may be affected by **y_tick_size** and
    **y_tick_rotate**."""

    y_tick_format: str | None | Param
    """How to format inputs (abstract values) for axis tick labels; one of:

    - a [d3-format][1] string for numeric scales
    - a [d3-time-format][2] string for temporal scales

    [1]: https://d3js.org/d3-time
    [2]: https://d3js.org/d3-time-format"""

    y_tick_rotate: float | Param
    """The rotation angle of axis tick labels in degrees clocksize; defaults to 0."""

    y_line: bool | Param
    """If true, draw a line along the axis; if false (default), do not."""

    y_label_anchor: Literal["top", "right", "bottom", "left", "center"] | Param
    """Where to place the axis **label** relative to the plot's frame. For
    vertical position scales (*y* and *fy*), may be *top*, *bottom*, or
    *center*; for horizontal position scales (*x* and *fx*), may be *left*,
    *right*, or *center*. Defaults to *center* for ordinal scales (including
    *fx* and *fy*), and otherwise *top* for *y*, and *right* for *x*."""

    y_label_arrow: LabelArrow | Param
    """Whether to apply a directional arrow such as → or ↑ to the x-axis scale
    label. If *auto* (the default), the presence of the arrow depends on
    whether the scale is ordinal."""

    y_label_offset: float | Param
    """The axis **label** position offset (in pixels); default depends on margins
    and orientation."""

    y_font_variant: str | Param
    """The font-variant attribute for axis ticks; defaults to *tabular-nums* for
    quantitative axes."""

    y_aria_label: str | Param
    """A short label representing the axis in the accessibility tree."""

    y_aria_description: str | Param
    """A textual description for the axis in the accessibility tree."""

    y_percent: bool | Param
    """If true, shorthand for a transform suitable for percentages, mapping
    proportions in [0, 1] to [0, 100]."""

    y_reverse: bool | Param
    """Whether to reverse the scale's encoding; equivalent to reversing either the
    **domain** or **range**. Note that by default, when the *y* scale is
    continuous, the *max* value points to the top of the screen, whereas
    ordinal values are ranked from top to bottom."""

    y_zero: bool | Param
    """Whether the **domain** must include zero. If the domain minimum is
    positive, it will be set to zero; otherwise if the domain maximum is
    negative, it will be set to zero.

    For quantitative scales only."""

    y_exponent: float | Param
    """A power scale's exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a
    linear scale. For *pow* scales only."""

    y_base: float | Param
    """A log scale's base; defaults to 10. Does not affect the scale's encoding,
    but rather the default ticks. For *log* scales only."""

    y_constant: float | Param
    """A symlog scale's constant, expressing the magnitude of the linear region
    around the origin; defaults to 1. For *symlog* scales only."""

    xy_domain: Literal["fixed"] | list[str | float | bool] | Param
    """Set the *x* and *y* scale domains."""

    # facet attributes

    facet_margin: float | Param
    """Shorthand to set the same default for all four facet margins: margin_top,
    margin_right, margin_bottom, and margin_left."""

    facet_margin_top: float | Param
    """The top facet margin; the (minimum) distance in pixels between the top
    edges of the inner and outer plot area."""

    facet_margin_bottom: float | Param
    """The right facet margin; the (minimum) distance in pixels between the right
    edges of the inner and outer plot area."""

    facet_margin_left: float | Param
    """The bottom facet margin; the (minimum) distance in pixels between the
    bottom edges of the inner and outer plot area."""

    facet_margin_right: float | Param
    """The left facet margin; the (minimum) distance in pixels between the left
    edges of the inner and outer plot area."""

    facet_grid: bool | str | Interval | list[str | float | bool] | Param
    """Default axis grid for fx and fy scales; typically set to true to enable."""

    facet_label: str | None | Param
    """Default axis label for fx and fy scales; typically set to null to disable."""

    # fx scale attributes

    fx_domain: Literal["fixed"] | list[str | float | bool] | Param
    """The extent of the scale's inputs (abstract values). By default inferred
    from channel values. For ordinal data (strings or booleans), it is an
    array (or iterable) of values is the desired order, defaulting to natural
    ascending order."""

    fx_range: list[str | float | bool] | Param
    """The extent of the scale's outputs (visual values). By default inferred from
    the scale's **type** and **domain**, and the plot's dimensions. For ordinal
    position scales (*point* and *band*), it is typically [*min*, *max*]; it
    can be [*max*, *min*] to reverse the scale."""

    fx_inset: float | Param
    """Shorthand to set the same default for all four insets: **inset_top**,
    **inset_right**, **inset_bottom**, and **inset_left**. All insets typically
    default to zero, though not always (say when using bin transform). A
    positive inset reduces effective area, while a negative inset increases it."""

    fx_inset_right: float | Param
    """Insets the right edge by the specified number of pixels. A positive value
    insets towards the left edge (reducing effective area), while a negative
    value insets away from the left edge (increasing it)."""

    fx_inset_left: float | Param
    """Insets the left edge by the specified number of pixels. A positive value
    insets towards the right edge (reducing effective area), while a negative
    value insets away from the right edge (increasing it)."""

    fx_round: bool | Param
    """If true, round the output value to the nearest integer (pixel); useful for
    crisp edges when rendering.

    For position scales only."""

    fx_align: float | Param
    """How to distribute unused space in the **range** for *point* and *band*
    scales. A number in [0, 1], such as:

    - 0 - use the start of the range, putting unused space at the end
    - 0.5 (default) - use the middle, distributing unused space evenly
    - 1 use the end, putting unused space at the start

    For ordinal position scales only."""

    fx_padding: float | Param
    """For *band* scales, how much of the **range** to reserve to separate
    adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of
    inset for the first and last value as a proportion of the bandwidth;
    defaults to 0.5 (50%).

    For ordinal position scales only."""

    fx_padding_inner: float | Param
    """For a *band* scale, how much of the range to reserve to separate
    adjacent bands."""

    fx_padding_outer: float | Param
    """For a *band* scale, how much of the range to reserve to inset first and
    last bands."""

    fx_axis: Literal["top", "bottom", "both"] | bool | None | Param
    """The side of the frame on which to place the implicit axis: *top* or
    *bottom* for *fx*. Defaults to *top* if there is a *bottom* *x* axis,
    and otherwise *bottom*.

    If *both*, an implicit axis will be rendered on both sides of the plot
    (*top* and *bottom* for *fx*). If null, the implicit axis is suppressed."""

    fx_ticks: float | Interval | list[str | float | bool] | Param
    """The desired approximate number of axis ticks, or an explicit array of tick
    values, or an interval such as *day* or *month*."""

    fx_tick_size: float | Param
    """The length of axis tick marks in pixels; negative values extend in the
    opposite direction. Defaults to 6 for *x* and *y* axes and *color* and
    *opacity* *ramp* legends, and 0 for *fx* and *fy* axes."""

    fx_tick_spacing: float | Param
    """The desired approximate spacing between adjacent axis ticks, affecting the
    default **ticks**; defaults to 80 pixels for *x* and *fx*, and 35 pixels
    for *y* and *fy*."""

    fx_tick_padding: float | Param
    """The distance between an axis tick mark and its associated text label (in
    pixels); often defaults to 3, but may be affected by **fx_tick_size** and
    **fx_tick_rotate**."""

    fx_tick_format: str | None | Param
    """How to format inputs (abstract values) for axis tick labels; one of:

    - a [d3-format][1] string for numeric scales
    - a [d3-time-format][2] string for temporal scales

    [1]: https://d3js.org/d3-time
    [2]: https://d3js.org/d3-time-format"""

    fx_tick_rotate: float | Param
    """The rotation angle of axis tick labels in degrees clocksize; defaults to 0."""

    fx_grid: bool | str | Interval | list[str | float | bool] | Param
    """Whether to show a grid aligned with the scale's ticks. If true, show a grid
    with the currentColor stroke; if a string, show a grid with the specified
    stroke color; if an approximate number of ticks, an interval, or an array
    of tick values, show corresponding grid lines. See also the grid mark.

    For axes only."""

    fx_line: bool | Param
    """If true, draw a line along the axis; if false (default), do not."""

    fx_label: str | None | Param
    """A textual label to show on the axis or legend; if null, show no label. By
    default the scale label is inferred from channel definitions, possibly with
    an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

    For axes and legends only."""

    fx_label_anchor: Literal["top", "right", "bottom", "left", "center"] | Param
    """Where to place the axis **label** relative to the plot's frame. For
    vertical position scales (*y* and *fy*), may be *top*, *bottom*, or
    *center*; for horizontal position scales (*x* and *fx*), may be *left*,
    *right*, or *center*. Defaults to *center* for ordinal scales (including
    *fx* and *fy*), and otherwise *top* for *y*, and *right* for *x*."""

    fx_label_offset: float | Param
    """The axis **label** position offset (in pixels); default depends on margins
    and orientation."""

    fx_font_variant: str | Param
    """The font-variant attribute for axis ticks; defaults to *tabular-nums* for
    quantitative axes."""

    fx_aria_label: str | Param
    """A short label representing the axis in the accessibility tree."""

    fx_aria_description: str | Param
    """A textual description for the axis in the accessibility tree."""

    fx_reverse: bool | Param
    """Whether to reverse the scale's encoding; equivalent to reversing either the
    **domain** or **range**."""

    # fy scale attributes

    fy_domain: Literal["fixed"] | list[str | float | bool] | Param
    """The extent of the scale's inputs (abstract values). By default inferred
    from channel values. For ordinal data (strings or booleans), it is an
    array (or iterable) of values is the desired order, defaulting to natural
    ascending order."""

    fy_range: list[str | float | bool] | Param
    """The extent of the scale's outputs (visual values). By default inferred from
    the scale's **type** and **domain**, and the plot's dimensions. For ordinal
    position scales (*point* and *band*), it is typically [*min*, *max*]; it
    can be [*max*, *min*] to reverse the scale."""

    fy_inset: float | Param
    """Shorthand to set the same default for all four insets: **inset_top**,
    **inset_right**, **inset_bottom**, and **inset_left**. All insets typically
    default to zero, though not always (say when using bin transform). A
    positive inset reduces effective area, while a negative inset increases it."""

    fy_inset_top: float | Param
    """Insets the top edge by the specified number of pixels. A positive value
    insets towards the bottom edge (reducing effective area), while a negative
    value insets away from the bottom edge (increasing it)."""

    fy_inset_bottom: float | Param
    """Insets the bottom edge by the specified number of pixels. A positive value
    insets towards the top edge (reducing effective area), while a negative
    value insets away from the top edge (increasing it)."""

    fy_round: bool | Param
    """If true, round the output value to the nearest integer (pixel); useful for
    crisp edges when rendering.

    For position scales only."""

    fy_align: float | Param
    """How to distribute unused space in the **range** for *point* and *band*
    scales. A number in [0, 1], such as:

    - 0 - use the start of the range, putting unused space at the end
    - 0.5 (default) - use the middle, distributing unused space evenly
    - 1 use the end, putting unused space at the start

    For ordinal position scales only."""

    fy_padding: float | Param
    """For *band* scales, how much of the **range** to reserve to separate
    adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of
    inset for the first and last value as a proportion of the bandwidth;
    defaults to 0.5 (50%).

    For ordinal position scales only."""

    fy_padding_inner: float | Param
    """For a *band* scale, how much of the range to reserve to separate
    adjacent bands."""

    fy_padding_outer: float | Param
    """For a *band* scale, how much of the range to reserve to inset first and
    last bands."""

    fy_axis: Literal["left", "right", "both"] | bool | None | Param
    """The side of the frame on which to place the implicit axis: *left* or
    *right* for *fy*. Defaults to *left* for an *fy* scale.

    If *both*, an implicit axis will be rendered on both sides of the plot
    (*left* and *right* for *fy*). If null, the implicit axis is suppressed."""

    fy_ticks: float | Interval | list[str | float | bool] | Param
    """The desired approximate number of axis ticks, or an explicit array of tick
    values, or an interval such as *day* or *month*."""

    fy_tick_size: float | Param
    """The length of axis tick marks in pixels; negative values extend in the
    opposite direction. Defaults to 6 for *x* and *y* axes and *color* and
    *opacity* *ramp* legends, and 0 for *fx* and *fy* axes."""

    fy_tick_spacing: float | Param
    """The desired approximate spacing between adjacent axis ticks, affecting the
    default **ticks**; defaults to 80 pixels for *x* and *fx*, and 35 pixels
    for *y* and *fy*."""

    fy_tick_padding: float | Param
    """The distance between an axis tick mark and its associated text label (in
    pixels); often defaults to 3, but may be affected by **fy_tick_size** and
    **fy_tick_rotate**."""

    fy_tick_format: str | None | Param
    """How to format inputs (abstract values) for axis tick labels; one of:

    - a [d3-format][1] string for numeric scales
    - a [d3-time-format][2] string for temporal scales

    [1]: https://d3js.org/d3-time
    [2]: https://d3js.org/d3-time-format"""

    fy_tick_rotate: float | Param
    """The rotation angle of axis tick labels in degrees clocksize; defaults to 0."""

    fy_grid: bool | str | Interval | list[str | float | bool] | Param
    """Whether to show a grid aligned with the scale's ticks. If true, show a grid
    with the currentColor stroke; if a string, show a grid with the specified
    stroke color; if an approximate number of ticks, an interval, or an array
    of tick values, show corresponding grid lines. See also the grid mark.

    For axes only."""

    fy_line: bool | Param
    """If true, draw a line along the axis; if false (default), do not."""

    fy_label: str | None | Param
    """A textual label to show on the axis or legend; if null, show no label. By
    default the scale label is inferred from channel definitions, possibly with
    an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

    For axes and legends only."""

    fy_label_anchor: Literal["top", "right", "bottom", "left", "center"] | Param
    """Where to place the axis **label** relative to the plot's frame. For
    vertical position scales (*y* and *fy*), may be *top*, *bottom*, or
    *center*; for horizontal position scales (*x* and *fx*), may be *left*,
    *right*, or *center*. Defaults to *center* for ordinal scales (including
    *fx* and *fy*), and otherwise *top* for *y*, and *right* for *x*."""

    fy_label_offset: float | Param
    """The axis **label** position offset (in pixels); default depends on margins
    and orientation."""

    fy_font_variant: str | Param
    """The font-variant attribute for axis ticks; defaults to *tabular-nums* for
    quantitative axes."""

    fy_aria_label: str | Param
    """A short label representing the axis in the accessibility tree."""

    fy_aria_description: str | Param
    """A textual description for the axis in the accessibility tree."""

    fy_reverse: bool | Param
    """Whether to reverse the scale's encoding; equivalent to reversing either the
    **domain** or **range**."""

    # color scale attributes

    color_scale: ColorScaleType | None | Param
    """The *color* scale type, affecting how the scale encodes abstract data, say
    by applying a mathematical transformation. If null, the scale is disabled.

    For quantitative data (numbers), defaults to *linear*; for temporal data
    (dates), defaults to *utc*; for ordinal data (strings or booleans),
    defaults to *point* for position scales, *categorical* for color scales,
    and otherwise *ordinal*."""

    color_domain: Literal["fixed"] | list[str | float | bool] | Param
    """The extent of the scale's inputs (abstract values). By default inferred
    from channel values. For continuous data (numbers and dates), it is
    typically [*min*, *max*]; it can be [*max*, *min*] to reverse the scale.
    For ordinal data (strings or booleans), it is an array (or iterable) of
    values is the desired order, defaulting to natural ascending order."""

    color_range: list[str | float | bool] | Param
    """The extent of the scale's outputs (visual values). By default inferred from
    the scale's **type** and **domain**. For other ordinal data, it is an array
    (or iterable) of output values in the same order as the **domain**."""

    color_clamp: bool | Param
    """If true, values below the domain minimum are treated as the domain minimum,
    and values above the domain maximum are treated as the domain maximum.

    Clamping is useful for focusing on a subset of the data while ensuring that
    extreme values remain visible, but use caution: clamped values may need an
    annotation to avoid misinterpretation. Clamping typically requires setting
    an explicit **domain** since if the domain is inferred, no values will be
    outside the domain.

    For continuous scales only."""

    color_n: float | Param
    """For a *quantile* scale, the number of quantiles (creates *n* - 1
    thresholds); for a *quantize* scale, the approximate number of thresholds;
    defaults to 5."""

    color_nice: bool | float | Interval | Param
    """If true, or a tick count or interval, extend the domain to nice round
    values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and
    nice time intervals for *utc* and *time* scales. Pass an interval such as
    *minute*, *wednesday* or *month* to specify what constitutes a nice
    interval.

    For continuous scales only."""

    color_scheme: ColorScheme | Param
    """If specified, shorthand for setting the **color_range**
    or **color_interpolate** option of a *color* scale."""

    color_interpolate: Interpolate | Param
    """How to interpolate color range values. For quantitative scales only.
    This attribute can be used to specify a color space for interpolating
    colors specified in the **color_range**."""

    color_pivot: Any | Param
    """For a diverging color scale, the input value (abstract value) that divides
    the domain into two parts; defaults to 0 for *diverging* scales, dividing
    the domain into negative and positive parts; defaults to 1 for
    *diverging-log* scales. By default, diverging scales are symmetric around
    the pivot; see the **symmetric** option."""

    color_symmetric: bool | Param
    """For a diverging color scale, if true (the default), extend the domain to
    ensure that the lower part of the domain (below the **pivot**) is
    commensurate with the upper part of the domain (above the **pivot**).

    A symmetric diverging color scale may not use all of its output **range**;
    this reduces contrast but ensures that deviations both below and above the
    **pivot** are represented proportionally. Otherwise if false, the full
    output **range** will be used; this increases contrast but values on
    opposite sides of the **pivot** may not be meaningfully compared."""

    color_label: str | None | Param
    """A textual label to show on the axis or legend; if null, show no label. By
    default the scale label is inferred from channel definitions, possibly with
    an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

    For axes and legends only."""

    color_percent: bool | Param
    """If true, shorthand for a transform suitable for percentages, mapping
    proportions in [0, 1] to [0, 100]."""

    color_reverse: bool | Param
    """Whether to reverse the scale's encoding; equivalent to reversing either the
    **domain** or **range**."""

    color_zero: bool | Param
    """Whether the **domain** must include zero. If the domain minimum is
    positive, it will be set to zero; otherwise if the domain maximum is
    negative, it will be set to zero.

    For quantitative scales only."""

    color_tick_format: str | None | Param
    """How to format inputs (abstract values) for axis tick labels; one of:

    - a [d3-format][1] string for numeric scales
    - a [d3-time-format][2] string for temporal scales

    [1]: https://d3js.org/d3-time
    [2]: https://d3js.org/d3-time-format"""

    color_exponent: float | Param
    """A power scale's exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a
    linear scale. For *pow* and *diverging-pow* scales only."""

    color_base: float | Param
    """A log scale's base; defaults to 10. Does not affect the scale's encoding,
    but rather the default ticks. For *log* and *diverging-log* scales only."""

    color_constant: float | Param
    """A symlog scale's constant, expressing the magnitude of the linear region
    around the origin; defaults to 1. For *symlog* and *diverging-symlog*
    scales only."""

    # opacity scale attributes

    opacity_scale: ContinuousScaleType | None | Param
    """The *opacity* scale type, affecting how the scale encodes abstract data,
    say by applying a mathematical transformation. If null, the scale is
    disabled. The opacity scale defaults to *linear*; this scales is intended
    for quantitative data."""

    opacity_domain: Literal["fixed"] | list[str | float | bool] | Param
    """The extent of the scale's inputs (abstract values). By default inferred
    from channel values. For continuous data (numbers and dates), it is
    typically [*min*, *max*]; it can be [*max*, *min*] to reverse the scale.
    For ordinal data (strings or booleans), it is an array (or iterable) of
    values is the desired order, defaulting to natural ascending order.

    Opacity scales have a default domain from 0 to the maximum value of
    associated channels."""

    opacity_range: list[str | float | bool] | Param
    """The extent of the scale's outputs (visual values).

    Opacity scales have a default range of [0, 1]."""

    opacity_clamp: bool | Param
    """If true, values below the domain minimum are treated as the domain minimum,
    and values above the domain maximum are treated as the domain maximum.

    Clamping is useful for focusing on a subset of the data while ensuring that
    extreme values remain visible, but use caution: clamped values may need an
    annotation to avoid misinterpretation. Clamping typically requires setting
    an explicit **domain** since if the domain is inferred, no values will be
    outside the domain.

    For continuous scales only."""

    opacity_nice: bool | float | Interval | Param
    """If true, or a tick count or interval, extend the domain to nice round
    values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and
    nice time intervals for *utc* and *time* scales. Pass an interval such as
    *minute*, *wednesday* or *month* to specify what constitutes a nice
    interval.

    For continuous scales only."""

    opacity_label: str | None | Param
    """A textual label to show on the axis or legend; if null, show no label. By
    default the scale label is inferred from channel definitions, possibly with
    an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

    For axes and legends only."""

    opacity_percent: bool | Param
    """If true, shorthand for a transform suitable for percentages, mapping
    proportions in [0, 1] to [0, 100]."""

    opacity_reverse: bool | Param
    """Whether to reverse the scale's encoding; equivalent to reversing either the
    **domain** or **range**."""

    opacity_zero: bool | Param
    """Whether the **domain** must include zero. If the domain minimum is
    positive, it will be set to zero; otherwise if the domain maximum is
    negative, it will be set to zero.

    For quantitative scales only."""

    opacity_tick_format: str | None | Param
    """How to format inputs (abstract values) for axis tick labels; one of:

    - a [d3-format][1] string for numeric scales
    - a [d3-time-format][2] string for temporal scales

    [1]: https://d3js.org/d3-time
    [2]: https://d3js.org/d3-time-format"""

    opacity_exponent: float | Param
    """A power scale's exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a
    linear scale. For *pow* scales only."""

    opacity_base: float | Param
    """A log scale's base; defaults to 10. Does not affect the scale's encoding,
    but rather the default ticks. For *log* scales only."""

    opacity_constant: float | Param
    """A symlog scale's constant, expressing the magnitude of the linear region
    around the origin; defaults to 1. For *symlog* scales only."""

    # symbol scale attributes

    symbol_scale: DiscreteScaleType | None | Param
    """The *symbol* scale type, affecting how the scale encodes abstract data,
    say by applying a mathematical transformation. If null, the scale is
    disabled. Defaults to an *ordinal* scale type."""

    symbol_domain: Literal["fixed"] | list[str | float | bool] | Param
    """The extent of the scale's inputs (abstract values). By default inferred
    from channel values. As symbol scales are discrete, the domain is an array
    (or iterable) of values is the desired order, defaulting to natural
    ascending order."""

    symbol_range: list[str | float | bool] | Param
    """The extent of the scale's outputs (visual values). By default inferred from
    the scale's **type** and **domain**, and for position scales, the plot's
    dimensions. For continuous data (numbers and dates), and for ordinal
    position scales (*point* and *band*), it is typically [*min*, *max*]; it
    can be [*max*, *min*] to reverse the scale. For other ordinal data, such as
    for a *color* scale, it is an array (or iterable) of output values in the
    same order as the **domain**.

    Symbol scales have a default range of categorical symbols; the choice of
    symbols depends on whether the associated dot mark is filled or stroked."""

    # r scale attributes

    r_scale: ContinuousScaleType | None | Param
    """The *r* (radius) scale type, affecting how the scale encodes abstract
    data, say by applying a mathematical transformation. If null, the scale
    is disabled. The radius scale defaults to *sqrt*; this scale is intended
    for quantitative data."""

    r_domain: Literal["fixed"] | list[str | float | bool] | Param
    """The extent of the scale's inputs (abstract values). By default inferred
    from channel values. For continuous data (numbers and dates), it is
    typically [*min*, *max*]; it can be [*max*, *min*] to reverse the scale.
    For ordinal data (strings or booleans), it is an array (or iterable) of
    values is the desired order, defaulting to natural ascending order.

    Radius scales have a default domain from 0 to the median first quartile
    of associated channels."""

    r_range: list[str | float | bool] | Param
    """The extent of the scale's outputs (visual values). By default inferred from
    the scale's **type** and **domain**, and for position scales, the plot's
    dimensions. For continuous data (numbers and dates), and for ordinal
    position scales (*point* and *band*), it is typically [*min*, *max*]; it
    can be [*max*, *min*] to reverse the scale. For other ordinal data, such as
    for a *color* scale, it is an array (or iterable) of output values in the
    same order as the **domain**.

    Radius scales have a default range of [0, 3]."""

    r_clamp: Any
    """If true, values below the domain minimum are treated as the domain minimum,
    and values above the domain maximum are treated as the domain maximum.

    Clamping is useful for focusing on a subset of the data while ensuring that
    extreme values remain visible, but use caution: clamped values may need an
    annotation to avoid misinterpretation. Clamping typically requires setting
    an explicit **domain** since if the domain is inferred, no values will be
    outside the domain.

    For continuous scales only."""

    r_nice: bool | float | Interval | Param
    """If true, or a tick count or interval, extend the domain to nice round
    values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and
    nice time intervals for *utc* and *time* scales. Pass an interval such as
    *minute*, *wednesday* or *month* to specify what constitutes a nice
    interval.

    For continuous scales only."""

    r_label: str | None | Param
    """A textual label to show on the axis or legend; if null, show no label. By
    default the scale label is inferred from channel definitions, possibly with
    an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value."""

    r_percent: bool | Param
    """If true, shorthand for a transform suitable for percentages, mapping
    proportions in [0, 1] to [0, 100]."""

    r_zero: bool | Param
    """Whether the **domain** must include zero. If the domain minimum is
    positive, it will be set to zero; otherwise if the domain maximum is
    negative, it will be set to zero.

    For quantitative scales only."""

    r_exponent: float | Param
    """A power scale's exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a
    linear scale. For *pow* scales only."""

    r_base: float | Param
    """A log scale's base; defaults to 10. Does not affect the scale's encoding,
    but rather the default ticks. For *log* scales only."""

    r_constant: float | Param
    """A symlog scale's constant, expressing the magnitude of the linear region
    around the origin; defaults to 1. For *symlog* scales only."""

    # length scale attributes

    length_scale: ContinuousScaleType | None | Param
    """The *length* scale type, affecting how the scale encodes abstract data,
    say by applying a mathematical transformation. If null, the scale is
    disabled. The length scale defaults to *linear*, as this scale is intended
    for quantitative data."""

    length_domain: Literal["fixed"] | list[str | float | bool] | Param
    """The extent of the scale's inputs (abstract values). By default inferred
    from channel values. For continuous data (numbers and dates), it is
    typically [*min*, *max*]; it can be [*max*, *min*] to reverse the scale.
    For ordinal data (strings or booleans), it is an array (or iterable) of
    values is the desired order, defaulting to natural ascending order.

    Linear scales have a default domain of [0, 1]. Log scales have a default
    domain of [1, 10] and cannot include zero. Radius scales have a default
    domain from 0 to the median first quartile of associated channels. Length
    have a default domain from 0 to the median median of associated channels.
    Opacity scales have a default domain from 0 to the maximum value of
    associated channels."""

    length_range: list[str | float | bool] | Param
    """The extent of the scale's outputs (visual values). By default inferred from
    the scale's **type** and **domain**, and for position scales, the plot's
    dimensions. For continuous data (numbers and dates), and for ordinal
    position scales (*point* and *band*), it is typically [*min*, *max*]; it
    can be [*max*, *min*] to reverse the scale. For other ordinal data, such as
    for a *color* scale, it is an array (or iterable) of output values in the
    same order as the **domain**.

    Length scales have a default range of [0, 12]."""

    length_clamp: Any
    """If true, values below the domain minimum are treated as the domain minimum,
    and values above the domain maximum are treated as the domain maximum.

    Clamping is useful for focusing on a subset of the data while ensuring that
    extreme values remain visible, but use caution: clamped values may need an
    annotation to avoid misinterpretation. Clamping typically requires setting
    an explicit **domain** since if the domain is inferred, no values will be
    outside the domain.

    For continuous scales only."""

    length_nice: bool | float | Interval | Param
    """If true, or a tick count or interval, extend the domain to nice round
    values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and
    nice time intervals for *utc* and *time* scales. Pass an interval such as
    *minute*, *wednesday* or *month* to specify what constitutes a nice
    interval.

    For continuous scales only."""

    length_percent: bool | Param
    """If true, shorthand for a transform suitable for percentages, mapping
    proportions in [0, 1] to [0, 100]."""

    length_zero: bool | Param
    """Whether the **domain** must include zero. If the domain minimum is
    positive, it will be set to zero; otherwise if the domain maximum is
    negative, it will be set to zero.

    For quantitative scales only."""

    length_exponent: float | Param
    """A power scale's exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a
    linear scale. For *pow* scales only."""

    length_base: float | Param
    """A log scale's base; defaults to 10. Does not affect the scale's encoding,
    but rather the default ticks. For *log* scales only."""

    length_constant: float | Param
    """A symlog scale's constant, expressing the magnitude of the linear region
    around the origin; defaults to 1. For *symlog* scales only."""

    # projection attributes

    projection_type: ProjectionName | None | Param
    """The desired projection; one of:

    - a named built-in projection such as *albers-usa*
    - null, for no projection

    Named projections are scaled and translated to fit
    the **domain** to the plot's frame (minus insets)."""

    projection_domain: object | Param
    """A GeoJSON object to fit to the plot's frame (minus insets); defaults to a
    Sphere for spherical projections (outline of the the whole globe)."""

    projection_rotate: list[float | Param] | Param
    """A rotation of the sphere before projection; defaults to [0, 0, 0].
    Specified as Euler angles λ (yaw, or reference longitude), φ (pitch, or
    reference latitude), and optionally γ (roll), in degrees."""

    projection_parallels: list[float | Param] | Param
    """The [standard parallels][1]. For conic projections only.

    [1]: https://d3js.org/d3-geo/conic#conic_parallels"""

    projection_precision: float | Param
    """The projection's [sampling threshold][1].

    [1]: https://d3js.org/d3-geo/projection#projection_precision"""

    projection_clip: bool | float | Literal["frame"] | None | Param
    """The projection's clipping method; one of:

    - *frame* or true (default) - clip to the plot's frame (including margins but not insets)
    - a number - clip to a circle of the given radius in degrees centered around the origin
    - null or false - do not clip

    Some projections (such as [*armadillo*][1] and [*berghaus*][2]) require
    spherical clipping: in that case set the marks' **clip** option to
    *sphere*.

    [1]: https://observablehq.com/@d3/armadillo
    [2]: https://observablehq.com/@d3/berghaus-star"""

    projection_inset: float | Param
    """Shorthand to set the same default for all four projection insets.
    All insets typically default to zero, though not always. A positive
    inset reduces effective area, while a negative inset increases it."""

    projection_inset_top: float | Param
    """Insets the top edge of the projection by the specified number of pixels.
    A positive value insets towards the bottom edge (reducing effective area),
    while a negative value insets away from the bottom edge (increasing it)."""

    projection_inset_right: float | Param
    """Insets the right edge of the projection by the specified number of pixels.
    A positive value insets towards the left edge (reducing effective area),
    while a negative value insets away from the left edge (increasing it)."""

    projection_inset_bottom: float | Param
    """Insets the bottom edge of the projection by the specified number of pixels.
    A positive value insets towards the top edge (reducing effective area),
    while a negative value insets away from the top edge (increasing it)."""

    projection_inset_left: float | Param
    """Insets the left edge of the projection by the specified number of pixels.
    A positive value insets towards the right edge (reducing effective area),
    while a negative value insets away from the right edge (increasing it)."""


def plot_options_mosaic(options: PlotOptions) -> dict[str, Any]:
    mosaic_options: dict[str, Any] = {}
    for key, value in options.items():
        if key.endswith("_domain") and value == "fixed":
            value = "Fixed"
        mosaic_options[snake_to_camel(key)] = value

    return mosaic_options
