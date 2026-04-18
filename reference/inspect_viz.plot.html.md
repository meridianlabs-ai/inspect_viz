# inspect_viz.plot – Inspect Viz

## Plot

### plot

Create a plot.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_plot.py#L21)

``` python
def plot(
    plot: Mark | Interactor | Legend | Sequence[Mark | Interactor | Legend] = ...,
    *,
    x_label: str | Param | None | NotGiven = ...,
    fx_label: str | Param | None | NotGiven = ...,
    y_label: str | Param | None | NotGiven = ...,
    fy_label: str | Param | None | NotGiven = ...,
    title: str | Title | None = ...,
    width: float | Param | None = ...,
    height: float | Param | None = ...,
    name: str | None = ...,
    legend: Literal['color', 'opacity', 'symbol'] | Sequence[Literal['color', 'opacity', 'symbol']] | Legend | Sequence[Legend] | None = ...,
    aspect_ratio: float | bool | None | Param | None = ...,
    margin: float | Param | None = ...,
    margin_top: float | Param | None = ...,
    margin_right: float | Param | None = ...,
    margin_bottom: float | Param | None = ...,
    margin_left: float | Param | None = ...,
    margins: dict[str, float | Param] | None = ...,
    inset: float | Param | None = ...,
    style: str | dict[str, str] | None | Param = ...,
    align: float | Param | None = ...,
    padding: float | Param | None = ...,
    axis: Literal['top', 'right', 'bottom', 'left', 'both'] | bool | None | Param = ...,
    grid: bool | str | Param = ...,
    aria_label: str | None = ...,
    aria_description: str | None = ...,
    clip: Literal['frame', 'sphere'] | bool | None | Param = ...,
    x_scale: PositionScale | None | Param | None = ...,
    x_domain: Literal['fixed'] | Sequence[str | float | bool] | Param | None = ...,
    x_range: Sequence[str | float | bool] | Param | None = ...,
    x_nice: bool | float | Interval | Param | None = ...,
    x_inset: float | Param | None = ...,
    x_inset_right: float | Param | None = ...,
    x_inset_left: float | Param | None = ...,
    x_clamp: bool | Param | None = ...,
    x_round: bool | Param | None = ...,
    x_align: float | Param | None = ...,
    x_padding: float | Param | None = ...,
    x_padding_inner: float | Param | None = ...,
    x_padding_outer: float | Param | None = ...,
    x_axis: Literal['top', 'bottom', 'both'] | bool | None | Param | None = ...,
    x_ticks: float | Interval | Sequence[str | float | bool] | Param | None = ...,
    x_tick_size: float | Param | None = ...,
    x_tick_spacing: float | Param | None = ...,
    x_tick_padding: float | Param | None = ...,
    x_tick_format: str | None | Param | None = ...,
    x_tick_rotate: float | Param | None = ...,
    x_grid: bool | str | Interval | list[str | float] | Param = ...,
    x_line: bool | Param | None = ...,
    x_label_anchor: Literal['right', 'left', 'center'] | Param | None = ...,
    x_label_arrow: LabelArrow | Param | None = ...,
    x_label_offset: float | Param | None = ...,
    x_font_variant: str | Param | None = ...,
    x_aria_label: str | Param | None = ...,
    x_aria_description: str | Param | None = ...,
    x_percent: bool | Param | None = ...,
    x_reverse: bool | Param | None = ...,
    x_zero: bool | Param | None = ...,
    x_exponent: float | Param | None = ...,
    x_base: float | Param | None = ...,
    x_constant: float | Param | None = ...,
    y_scale: PositionScale | None | Param | None = ...,
    y_domain: Literal['fixed'] | Sequence[str | float | bool] | Param | None = ...,
    y_range: Sequence[str | float | bool] | Param | None = ...,
    y_nice: bool | float | Interval | Param | None = ...,
    y_inset: float | Param | None = ...,
    y_inset_top: float | Param | None = ...,
    y_inset_bottom: float | Param | None = ...,
    y_clamp: bool | Param | None = ...,
    y_round: bool | Param | None = ...,
    y_align: float | Param | None = ...,
    y_padding: float | Param | None = ...,
    y_padding_inner: float | Param | None = ...,
    y_padding_outer: float | Param | None = ...,
    y_axis: Literal['left', 'right', 'both'] | bool | None | Param | None = ...,
    y_ticks: float | Interval | Sequence[str | float | bool] | Param | None = ...,
    y_tick_size: float | Param | None = ...,
    y_tick_spacing: float | Param | None = ...,
    y_tick_padding: float | Param | None = ...,
    y_tick_format: str | None | Param | None = ...,
    y_tick_rotate: float | Param | None = ...,
    y_grid: bool | str | Interval | list[str | float] | Param = ...,
    y_line: bool | Param | None = ...,
    y_label_anchor: Literal['top', 'bottom', 'center'] | Param | None = ...,
    y_label_arrow: LabelArrow | Param | None = ...,
    y_label_offset: float | Param | None = ...,
    y_font_variant: str | Param | None = ...,
    y_aria_label: str | Param | None = ...,
    y_aria_description: str | Param | None = ...,
    y_percent: bool | Param | None = ...,
    y_reverse: bool | Param | None = ...,
    y_zero: bool | Param | None = ...,
    y_exponent: float | Param | None = ...,
    y_base: float | Param | None = ...,
    y_constant: float | Param | None = ...,
    xy_domain: Literal['fixed'] | Sequence[str | float | bool] | Param | None = ...,
    facet_margin: float | Param | None = ...,
    facet_margin_top: float | Param | None = ...,
    facet_margin_bottom: float | Param | None = ...,
    facet_margin_left: float | Param | None = ...,
    facet_margin_right: float | Param | None = ...,
    facet_grid: bool | str | Interval | Sequence[str | float | bool] | Param | None = ...,
    facet_label: str | None | Param | None = ...,
    fx_domain: Literal['fixed'] | Sequence[str | float | bool] | Param | None = ...,
    fx_range: Sequence[str | float | bool] | Param | None = ...,
    fx_inset: float | Param | None = ...,
    fx_inset_right: float | Param | None = ...,
    fx_inset_left: float | Param | None = ...,
    fx_round: bool | Param | None = ...,
    fx_align: float | Param | None = ...,
    fx_padding: float | Param | None = ...,
    fx_padding_inner: float | Param | None = ...,
    fx_padding_outer: float | Param | None = ...,
    fx_axis: Literal['top', 'bottom', 'both'] | bool | None | Param | None = ...,
    fx_ticks: float | Interval | Sequence[str | float | bool] | Param | None = ...,
    fx_tick_size: float | Param | None = ...,
    fx_tick_spacing: float | Param | None = ...,
    fx_tick_padding: float | Param | None = ...,
    fx_tick_format: str | None | Param | None = ...,
    fx_tick_rotate: float | Param | None = ...,
    fx_grid: bool | str | Interval | Sequence[str | float | bool] | Param | None = ...,
    fx_line: bool | Param | None = ...,
    fx_label_anchor: Literal['right', 'left', 'center'] | Param | None = ...,
    fx_label_offset: float | Param | None = ...,
    fx_font_variant: str | Param | None = ...,
    fx_aria_label: str | Param | None = ...,
    fx_aria_description: str | Param | None = ...,
    fx_reverse: bool | Param | None = ...,
    fy_domain: Literal['fixed'] | Sequence[str | float | bool] | Param | None = ...,
    fy_range: Sequence[str | float | bool] | Param | None = ...,
    fy_inset: float | Param | None = ...,
    fy_inset_top: float | Param | None = ...,
    fy_inset_bottom: float | Param | None = ...,
    fy_round: bool | Param | None = ...,
    fy_align: float | Param | None = ...,
    fy_padding: float | Param | None = ...,
    fy_padding_inner: float | Param | None = ...,
    fy_padding_outer: float | Param | None = ...,
    fy_axis: Literal['left', 'right', 'both'] | bool | None | Param | None = ...,
    fy_ticks: float | Interval | Sequence[str | float | bool] | Param | None = ...,
    fy_tick_size: float | Param | None = ...,
    fy_tick_spacing: float | Param | None = ...,
    fy_tick_padding: float | Param | None = ...,
    fy_tick_format: str | None | Param | None = ...,
    fy_tick_rotate: float | Param | None = ...,
    fy_grid: bool | str | Interval | Sequence[str | float | bool] | Param | None = ...,
    fy_line: bool | Param | None = ...,
    fy_label_anchor: Literal['top', 'bottom', 'center'] | Param | None = ...,
    fy_label_offset: float | Param | None = ...,
    fy_font_variant: str | Param | None = ...,
    fy_aria_label: str | Param | None = ...,
    fy_aria_description: str | Param | None = ...,
    fy_reverse: bool | Param | None = ...,
    color_scale: ColorScale | None | Param | None = ...,
    color_domain: Literal['fixed'] | Sequence[str | float | bool] | Param | None = ...,
    color_range: Sequence[str | float | bool] | Param | None = ...,
    color_clamp: bool | Param | None = ...,
    color_n: float | Param | None = ...,
    color_nice: bool | float | Interval | Param | None = ...,
    color_scheme: ColorScheme | Param | None = ...,
    color_interpolate: Interpolate | Param | None = ...,
    color_pivot: Any | Param | None = ...,
    color_symmetric: bool | Param | None = ...,
    color_label: str | None | Param | None = ...,
    color_percent: bool | Param | None = ...,
    color_reverse: bool | Param | None = ...,
    color_zero: bool | Param | None = ...,
    color_tick_format: str | None | Param | None = ...,
    color_exponent: float | Param | None = ...,
    color_base: float | Param | None = ...,
    color_constant: float | Param | None = ...,
    opacity_scale: ContinuousScale | None | Param | None = ...,
    opacity_domain: Literal['fixed'] | Sequence[str | float | bool] | Param | None = ...,
    opacity_range: Sequence[str | float | bool] | Param | None = ...,
    opacity_clamp: bool | Param | None = ...,
    opacity_nice: bool | float | Interval | Param | None = ...,
    opacity_label: str | None | Param | None = ...,
    opacity_percent: bool | Param | None = ...,
    opacity_reverse: bool | Param | None = ...,
    opacity_zero: bool | Param | None = ...,
    opacity_tick_format: str | None | Param | None = ...,
    opacity_exponent: float | Param | None = ...,
    opacity_base: float | Param | None = ...,
    opacity_constant: float | Param | None = ...,
    symbol_scale: Literal['ordinal', 'categorical', 'threshold', 'quantile', 'quantize'] | None | Param = ...,
    symbol_domain: Literal['fixed'] | Sequence[str | float | bool] | Param | None = ...,
    symbol_range: Sequence[str | float | bool] | Param | None = ...,
    r_scale: ContinuousScale | None | Param | None = ...,
    r_domain: Literal['fixed'] | Sequence[str | float | bool] | Param | None = ...,
    r_range: Sequence[str | float | bool] | Param | None = ...,
    r_clamp: Any | None = ...,
    r_nice: bool | float | Interval | Param | None = ...,
    r_label: str | None | Param | None = ...,
    r_percent: bool | Param | None = ...,
    r_zero: bool | Param | None = ...,
    r_exponent: float | Param | None = ...,
    r_base: float | Param | None = ...,
    r_constant: float | Param | None = ...,
    length_scale: ContinuousScale | None | Param | None = ...,
    length_domain: Literal['fixed'] | Sequence[str | float | bool] | Param | None = ...,
    length_range: Sequence[str | float | bool] | Param | None = ...,
    length_clamp: Any | None = ...,
    length_nice: bool | float | Interval | Param | None = ...,
    length_percent: bool | Param | None = ...,
    length_zero: bool | Param | None = ...,
    length_exponent: float | Param | None = ...,
    length_base: float | Param | None = ...,
    length_constant: float | Param | None = ...,
    projection_type: Projection | None | Param | None = ...,
    projection_domain: object | Param | None = ...,
    projection_rotate: Sequence[float | Param] | Param | None = ...,
    projection_parallels: Sequence[float | Param] | Param | None = ...,
    projection_precision: float | Param | None = ...,
    projection_clip: bool | float | Literal['frame'] | None | Param | None = ...,
    projection_inset: float | Param | None = ...,
    projection_inset_top: float | Param | None = ...,
    projection_inset_right: float | Param | None = ...,
    projection_inset_bottom: float | Param | None = ...,
    projection_inset_left: float | Param | None = ...,
) -> Component
```

`*plot` [Mark](../reference/inspect_viz.mark.html.md#mark) \| [Interactor](../reference/inspect_viz.interactor.html.md#interactor) \| [Legend](../reference/inspect_viz.plot.html.md#legend) \| Sequence\[[Mark](../reference/inspect_viz.mark.html.md#mark) \| [Interactor](../reference/inspect_viz.interactor.html.md#interactor) \| [Legend](../reference/inspect_viz.plot.html.md#legend)\]  
Plot elements (marks, interactors, legends)

`x_label` str \| [Param](../reference/inspect_viz.html.md#param) \| None \| NotGiven  
A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value. Pass `None` for no x_label.

`fx_label` str \| [Param](../reference/inspect_viz.html.md#param) \| None \| NotGiven  
A textual label to show on the axis or legend; if `None`, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

`y_label` str \| [Param](../reference/inspect_viz.html.md#param) \| None \| NotGiven  
A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value. Pass `None` for no y_label.

`fy_label` str \| [Param](../reference/inspect_viz.html.md#param) \| None \| NotGiven  
A textual label to show on the axis or legend; if `None`, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

`title` str \| [Title](../reference/inspect_viz.mark.html.md#title) \| None  
Title for plot (`str` or mark created with the [title()](../reference/inspect_viz.mark.html.md#title) function).

`width` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The outer width of the plot in pixels, including margins. Defaults to 700.

`height` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The outer height of the plot in pixels, including margins. The default is width / 1.618 (the [golden ratio](https://en.wikipedia.org/wiki/Golden_ratio))

`name` str \| None  
A unique name for the plot. The name is used by standalone legend components to to lookup the plot and access scale mappings.

`legend` Literal\['color', 'opacity', 'symbol'\] \| Sequence\[Literal\['color', 'opacity', 'symbol'\]\] \| [Legend](../reference/inspect_viz.plot.html.md#legend) \| Sequence\[[Legend](../reference/inspect_viz.plot.html.md#legend)\] \| None  
Plot legend.

`aspect_ratio` float \| bool \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
The desired aspect ratio of the *x* and *y* scales, affecting the default height. Given an aspect ratio of *dx* / *dy*, and assuming that the *x* and *y* scales represent equivalent units (say, degrees Celsius or meters), computes a default height such that *dx* pixels along *x* represents the same variation as *dy* pixels along *y*. Note: when faceting, set the *fx* and *fy* scales’ **round** option to false for an exact aspect ratio.

`margin` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four margins: **margin_top**, **margin_right**, **margin_bottom**, and **margin_left**. Otherwise, the default margins depend on the maximum margins of the plot’s marks. While most marks default to zero margins (because they are drawn inside the chart area), Plot’s axis marks have non-zero default margins.

`margin_top` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The top margin; the distance in pixels between the top edges of the inner and outer plot area. Defaults to the maximum top margin of the plot’s marks.

`margin_right` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The right margin; the distance in pixels between the right edges of the inner and outer plot area. Defaults to the maximum right margin of the plot’s marks.

`margin_bottom` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The bottom margin; the distance in pixels between the bottom edges of the inner and outer plot area. Defaults to the maximum bottom margin of the plot’s marks.

`margin_left` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The left margin; the distance in pixels between the left edges of the inner and outer plot area. Defaults to the maximum left margin of the plot’s marks.

`margins` dict\[str, float \| [Param](../reference/inspect_viz.html.md#param)\] \| None  
A shorthand object notation for setting multiple margin values. The object keys are margin names (top, right, etc).

`inset` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four insets: **inset_top**, **inset_right**, **inset_bottom**, and **inset_left**. All insets typically default to zero, though not always (say when using bin transform). A positive inset reduces effective area, while a negative inset increases it.

`style` str \| dict\[str, str\] \| None \| [Param](../reference/inspect_viz.html.md#param)  
Custom styles to override Plot’s defaults. Styles may be specified either as a string of inline styles (*e.g.*, `"color: red;"`, in the same fashion as assigning [*element*.style](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style)) or an object of properties (*e.g.*, `{color: "red"}`, in the same fashion as assigning [*element*.style properties](https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleDeclaration)). Note that unitless numbers ([quirky lengths](https://www.w3.org/TR/css-values-4/#deprecated-quirky-length)) such as `{padding: 20}` may not supported by some browsers; you should instead specify a string with units such as `{padding: "20px"}`. By default, the returned plot has a max-width of 100%, and the system-ui font. Plot’s marks and axes default to [currentColor](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value#currentcolor_keyword), meaning that they will inherit the surrounding content’s color.

`align` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
How to distribute unused space in the **range** for *point* and *band* scales. A number in \[0, 1\], such as:

- 0 - use the start of the range, putting unused space at the end
- 0.5 (default) - use the middle, distributing unused space evenly
- 1 use the end, putting unused space at the start

For ordinal position scales only.

`padding` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
For *band* scales, how much of the **range** to reserve to separate adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of inset for the first and last value as a proportion of the bandwidth; defaults to 0.5 (50%).

For ordinal position scales only.

`axis` Literal\['top', 'right', 'bottom', 'left', 'both'\] \| bool \| None \| [Param](../reference/inspect_viz.html.md#param)  
The side of the frame on which to place the implicit axis: *top* or *bottom* for *x* or *fx*, or *left* or *right* for *y* or *fy*. The default depends on the scale:

- *x* - *bottom*
- *y* - *left*
- *fx* - *top* if there is a *bottom* *x* axis, and otherwise *bottom*
- *fy* - *right* if there is a *left* *y* axis, and otherwise *right*

If *both*, an implicit axis will be rendered on both sides of the plot (*top* and *bottom* for *x* or *fx*, or *left* and *right* for *y* or *fy*). If null, the implicit axis is suppressed.

For position axes only.

`grid` bool \| str \| [Param](../reference/inspect_viz.html.md#param)  
Whether to show a grid aligned with the scale’s ticks. If true, show a grid with the currentColor stroke; if a string, show a grid with the specified stroke color.

`aria_label` str \| None  
The [aria-label attribute](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-label) on the SVG root.

`aria_description` str \| None  
The [aria-description attribute](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-description) on the SVG root.

`clip` Literal\['frame', 'sphere'\] \| bool \| None \| [Param](../reference/inspect_viz.html.md#param)  
The default clip for all marks.

`x_scale` [PositionScale](../reference/inspect_viz.plot.html.md#positionscale) \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
The *x* scale type, affecting how the scale encodes abstract data, say by applying a mathematical transformation. If null, the scale is disabled.

For quantitative data (numbers), defaults to *linear*; for temporal data (dates), defaults to *utc*; for ordinal data (strings or booleans), defaults to *point* for position scales, *categorical* for color scales, and otherwise *ordinal*. However, the radius scale defaults to *sqrt*, and the length and opacity scales default to *linear*; these scales are intended for quantitative data. The plot’s marks may also impose a scale type; for example, the barY mark requires that *x* is a *band* scale.

`x_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For continuous data (numbers and dates), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

Linear scales have a default domain of \[0, 1\]. Log scales have a default domain of \[1, 10\] and cannot include zero. Radius scales have a default domain from 0 to the median first quartile of associated channels. Length have a default domain from 0 to the median median of associated channels. Opacity scales have a default domain from 0 to the maximum value of associated channels.

`x_range` Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**, and for position scales, the plot’s dimensions. For continuous data (numbers and dates), and for ordinal position scales (*point* and *band*), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale.

`x_nice` bool \| float \| Interval \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, or a tick count or interval, extend the domain to nice round values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and nice time intervals for *utc* and *time* scales. Pass an interval such as *minute*, *wednesday* or *month* to specify what constitutes a nice interval.

For continuous scales only.

`x_inset` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four insets: **inset_top**, **inset_right**, **inset_bottom**, and **inset_left**. All insets typically default to zero, though not always (say when using bin transform). A positive inset reduces effective area, while a negative inset increases it.

`x_inset_right` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Insets the right edge by the specified number of pixels. A positive value insets towards the left edge (reducing effective area), while a negative value insets away from the left edge (increasing it).

`x_inset_left` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Insets the left edge by the specified number of pixels. A positive value insets towards the right edge (reducing effective area), while a negative value insets away from the right edge (increasing it).

`x_clamp` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, values below the domain minimum are treated as the domain minimum, and values above the domain maximum are treated as the domain maximum.

Clamping is useful for focusing on a subset of the data while ensuring that extreme values remain visible, but use caution: clamped values may need an annotation to avoid misinterpretation. Clamping typically requires setting an explicit **domain** since if the domain is inferred, no values will be outside the domain.

For continuous scales only.

`x_round` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, round the output value to the nearest integer (pixel); useful for crisp edges when rendering.

For position scales only.

`x_align` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
How to distribute unused space in the **range** for *point* and *band* scales. A number in \[0, 1\], such as:

- 0 - use the start of the range, putting unused space at the end
- 0.5 (default) - use the middle, distributing unused space evenly
- 1 use the end, putting unused space at the start

For ordinal position scales only.

`x_padding` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
For *band* scales, how much of the **range** to reserve to separate adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of inset for the first and last value as a proportion of the bandwidth; defaults to 0.5 (50%).

For ordinal position scales only.

`x_padding_inner` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to separate adjacent bands.

`x_padding_outer` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to inset first and last bands.

`x_axis` Literal\['top', 'bottom', 'both'\] \| bool \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
The side of the frame on which to place the implicit axis: *top* or *bottom* for *x*. Defaults to *bottom* for an *x* scale.

If *both*, an implicit axis will be rendered on both sides of the plot (*top* and *bottom* for *x*). If null, the implicit axis is suppressed.

`x_ticks` float \| Interval \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The desired approximate number of axis ticks, or an explicit array of tick values, or an interval such as *day* or *month*.

`x_tick_size` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The length of axis tick marks in pixels; negative values extend in the opposite direction. Defaults to 6 for *x* and *y* axes and *color* and *opacity* *ramp* legends, and 0 for *fx* and *fy* axes.

`x_tick_spacing` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The desired approximate spacing between adjacent axis ticks, affecting the default **ticks**; defaults to 80 pixels for *x* and *fx*, and 35 pixels for *y* and *fy*.

`x_tick_padding` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The distance between an axis tick mark and its associated text label (in pixels); often defaults to 3, but may be affected by **x_tick_size** and **x_tick_rotate**.

`x_tick_format` str \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
How to format inputs (abstract values) for axis tick labels; one of:

- a [d3-format](https://d3js.org/d3-time) string for numeric scales
- a [d3-time-format](https://d3js.org/d3-time-format) string for temporal scales

`x_tick_rotate` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The rotation angle of axis tick labels in degrees clocksize; defaults to 0.

`x_grid` bool \| str \| Interval \| list\[str \| float\] \| [Param](../reference/inspect_viz.html.md#param)  
Whether to show a grid aligned with the scale’s ticks. If true, show a grid with the currentColor stroke; if a string, show a grid with the specified stroke color; if an approximate number of ticks, an interval, or an array of tick values, show corresponding grid lines.

`x_line` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, draw a line along the axis; if false (default), do not.

`x_label_anchor` Literal\['right', 'left', 'center'\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
Where to place the axis **label** relative to the plot’s frame. For vertical position scales (*y* and *fy*), may be *top*, *bottom*, or *center*; for horizontal position scales (*x* and *fx*), may be *left*, *right*, or *center*. Defaults to *center* for ordinal scales (including *fx* and *fy*), and otherwise *top* for *y*, and *right* for *x*.

`x_label_arrow` [LabelArrow](../reference/inspect_viz.plot.html.md#labelarrow) \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether to apply a directional arrow such as → or ↑ to the x-axis scale label. If *auto* (the default), the presence of the arrow depends on whether the scale is ordinal.

`x_label_offset` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The axis **label** position offset (in pixels); default depends on margins and orientation.

`x_font_variant` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
The font-variant attribute for axis ticks; defaults to *tabular-nums* for quantitative axes.

`x_aria_label` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
A short label representing the axis in the accessibility tree.

`x_aria_description` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
A textual description for the axis in the accessibility tree.

`x_percent` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, shorthand for a transform suitable for percentages, mapping proportions in \[0, 1\] to \[0, 100\].

`x_reverse` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether to reverse the scale’s encoding; equivalent to reversing either the **domain** or **range**.

`x_zero` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether the **domain** must include zero. If the domain minimum is positive, it will be set to zero; otherwise if the domain maximum is negative, it will be set to zero.

For quantitative scales only.

`x_exponent` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A power scale’s exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a linear scale. For *pow* scales only.

`x_base` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A log scale’s base; defaults to 10. Does not affect the scale’s encoding, but rather the default ticks. For *log* scales only.

`x_constant` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A symlog scale’s constant, expressing the magnitude of the linear region around the origin; defaults to 1. For *symlog* scales only.

`y_scale` [PositionScale](../reference/inspect_viz.plot.html.md#positionscale) \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
The *y* scale type, affecting how the scale encodes abstract data, say by applying a mathematical transformation. If null, the scale is disabled.

For quantitative data (numbers), defaults to *linear*; for temporal data (dates), defaults to *utc*; for ordinal data (strings or booleans), defaults to *point* for position scales, The plot’s marks may also impose a scale type; for example, the barY mark requires that *x* is a *band* scale.

`y_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For continuous data (numbers and dates), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

Linear scales have a default domain of \[0, 1\]. Log scales have a default domain of \[1, 10\] and cannot include zero.

`y_range` Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**, and for position scales, the plot’s dimensions. For continuous data (numbers and dates), and for ordinal position scales (*point* and *band*), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale.

`y_nice` bool \| float \| Interval \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, or a tick count or interval, extend the domain to nice round values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and nice time intervals for *utc* and *time* scales. Pass an interval such as *minute*, *wednesday* or *month* to specify what constitutes a nice interval.

For continuous scales only.

`y_inset` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four insets: **inset_top**, **inset_right**, **inset_bottom**, and **inset_left**. All insets typically default to zero, though not always (say when using bin transform). A positive inset reduces effective area, while a negative inset increases it.

`y_inset_top` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Insets the top edge by the specified number of pixels. A positive value insets towards the bottom edge (reducing effective area), while a negative value insets away from the bottom edge (increasing it).

`y_inset_bottom` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Insets the bottom edge by the specified number of pixels. A positive value insets towards the top edge (reducing effective area), while a negative value insets away from the top edge (increasing it).

`y_clamp` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, values below the domain minimum are treated as the domain minimum, and values above the domain maximum are treated as the domain maximum.

Clamping is useful for focusing on a subset of the data while ensuring that extreme values remain visible, but use caution: clamped values may need an annotation to avoid misinterpretation. Clamping typically requires setting an explicit **domain** since if the domain is inferred, no values will be outside the domain.

For continuous scales only.

`y_round` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, round the output value to the nearest integer (pixel); useful for crisp edges when rendering.

For position scales only.

`y_align` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
How to distribute unused space in the **range** for *point* and *band* scales. A number in \[0, 1\], such as:

- 0 - use the start of the range, putting unused space at the end
- 0.5 (default) - use the middle, distributing unused space evenly
- 1 use the end, putting unused space at the start

For ordinal position scales only.

`y_padding` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
For *band* scales, how much of the **range** to reserve to separate adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of inset for the first and last value as a proportion of the bandwidth; defaults to 0.5 (50%).

For ordinal position scales only.

`y_padding_inner` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to separate adjacent bands.

`y_padding_outer` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to inset first and last bands.

`y_axis` Literal\['left', 'right', 'both'\] \| bool \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
The side of the frame on which to place the implicit axis: *left* or *right* for *y*. Defaults to *left* for a *y* scale.

If *both*, an implicit axis will be rendered on both sides of the plot (*left* and *right* for *y*). If null, the implicit axis is suppressed.

`y_ticks` float \| Interval \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The desired approximate number of axis ticks, or an explicit array of tick values, or an interval such as *day* or *month*.

`y_tick_size` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The length of axis tick marks in pixels; negative values extend in the opposite direction. Defaults to 6 for *x* and *y* axes and *color* and *opacity* *ramp* legends, and 0 for *fx* and *fy* axes.

`y_tick_spacing` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The desired approximate spacing between adjacent axis ticks, affecting the default **ticks**; defaults to 80 pixels for *x* and *fx*, and 35 pixels for *y* and *fy*.

`y_tick_padding` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The distance between an axis tick mark and its associated text label (in pixels); often defaults to 3, but may be affected by **y_tick_size** and **y_tick_rotate**.

`y_tick_format` str \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
How to format inputs (abstract values) for axis tick labels; one of:

- a [d3-format](https://d3js.org/d3-time) string for numeric scales
- a [d3-time-format](https://d3js.org/d3-time-format) string for temporal scales

`y_tick_rotate` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The rotation angle of axis tick labels in degrees clocksize; defaults to 0.

`y_grid` bool \| str \| Interval \| list\[str \| float\] \| [Param](../reference/inspect_viz.html.md#param)  
Whether to show a grid aligned with the scale’s ticks. If true, show a grid with the currentColor stroke; if a string, show a grid with the specified stroke color; if an approximate number of ticks, an interval, or an array of tick values, show corresponding grid lines.

`y_line` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, draw a line along the axis; if false (default), do not.

`y_label_anchor` Literal\['top', 'bottom', 'center'\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
Where to place the axis **label** relative to the plot’s frame. For vertical position scales (*y* and *fy*), may be *top*, *bottom*, or *center*; for horizontal position scales (*x* and *fx*), may be *left*, *right*, or *center*. Defaults to *center* for ordinal scales (including *fx* and *fy*), and otherwise *top* for *y*, and *right* for *x*.

`y_label_arrow` [LabelArrow](../reference/inspect_viz.plot.html.md#labelarrow) \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether to apply a directional arrow such as → or ↑ to the x-axis scale label. If *auto* (the default), the presence of the arrow depends on whether the scale is ordinal.

`y_label_offset` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The axis **label** position offset (in pixels); default depends on margins and orientation.

`y_font_variant` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
The font-variant attribute for axis ticks; defaults to *tabular-nums* for quantitative axes.

`y_aria_label` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
A short label representing the axis in the accessibility tree.

`y_aria_description` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
A textual description for the axis in the accessibility tree.

`y_percent` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, shorthand for a transform suitable for percentages, mapping proportions in \[0, 1\] to \[0, 100\].

`y_reverse` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether to reverse the scale’s encoding; equivalent to reversing either the **domain** or **range**. Note that by default, when the *y* scale is continuous, the *max* value points to the top of the screen, whereas ordinal values are ranked from top to bottom.

`y_zero` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether the **domain** must include zero. If the domain minimum is positive, it will be set to zero; otherwise if the domain maximum is negative, it will be set to zero.

For quantitative scales only.

`y_exponent` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A power scale’s exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a linear scale. For *pow* scales only.

`y_base` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A log scale’s base; defaults to 10. Does not affect the scale’s encoding, but rather the default ticks. For *log* scales only.

`y_constant` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A symlog scale’s constant, expressing the magnitude of the linear region around the origin; defaults to 1. For *symlog* scales only.

`xy_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
Set the *x* and *y* scale domains.

`facet_margin` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four facet margins: margin_top, margin_right, margin_bottom, and margin_left.

`facet_margin_top` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The top facet margin; the (minimum) distance in pixels between the top edges of the inner and outer plot area.

`facet_margin_bottom` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The right facet margin; the (minimum) distance in pixels between the right edges of the inner and outer plot area.

`facet_margin_left` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The bottom facet margin; the (minimum) distance in pixels between the bottom edges of the inner and outer plot area.

`facet_margin_right` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The left facet margin; the (minimum) distance in pixels between the left edges of the inner and outer plot area.

`facet_grid` bool \| str \| Interval \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
Default axis grid for fx and fy scales; typically set to true to enable.

`facet_label` str \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
Default axis label for fx and fy scales; typically set to null to disable.

`fx_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

`fx_range` Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**, and the plot’s dimensions. For ordinal position scales (*point* and *band*), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale.

`fx_inset` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four insets: **inset_top**, **inset_right**, **inset_bottom**, and **inset_left**. All insets typically default to zero, though not always (say when using bin transform). A positive inset reduces effective area, while a negative inset increases it.

`fx_inset_right` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Insets the right edge by the specified number of pixels. A positive value insets towards the left edge (reducing effective area), while a negative value insets away from the left edge (increasing it).

`fx_inset_left` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Insets the left edge by the specified number of pixels. A positive value insets towards the right edge (reducing effective area), while a negative value insets away from the right edge (increasing it).

`fx_round` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, round the output value to the nearest integer (pixel); useful for crisp edges when rendering.

For position scales only.

`fx_align` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
How to distribute unused space in the **range** for *point* and *band* scales. A number in \[0, 1\], such as:

- 0 - use the start of the range, putting unused space at the end
- 0.5 (default) - use the middle, distributing unused space evenly
- 1 use the end, putting unused space at the start

For ordinal position scales only.

`fx_padding` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
For *band* scales, how much of the **range** to reserve to separate adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of inset for the first and last value as a proportion of the bandwidth; defaults to 0.5 (50%).

For ordinal position scales only.

`fx_padding_inner` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to separate adjacent bands.

`fx_padding_outer` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to inset first and last bands.

`fx_axis` Literal\['top', 'bottom', 'both'\] \| bool \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
The side of the frame on which to place the implicit axis: *top* or *bottom* for *fx*. Defaults to *top* if there is a *bottom* *x* axis, and otherwise *bottom*.

If *both*, an implicit axis will be rendered on both sides of the plot (*top* and *bottom* for *fx*). If null, the implicit axis is suppressed.

`fx_ticks` float \| Interval \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The desired approximate number of axis ticks, or an explicit array of tick values, or an interval such as *day* or *month*.

`fx_tick_size` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The length of axis tick marks in pixels; negative values extend in the opposite direction. Defaults to 6 for *x* and *y* axes and *color* and *opacity* *ramp* legends, and 0 for *fx* and *fy* axes.

`fx_tick_spacing` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The desired approximate spacing between adjacent axis ticks, affecting the default **ticks**; defaults to 80 pixels for *x* and *fx*, and 35 pixels for *y* and *fy*.

`fx_tick_padding` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The distance between an axis tick mark and its associated text label (in pixels); often defaults to 3, but may be affected by **fx_tick_size** and **fx_tick_rotate**.

`fx_tick_format` str \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
How to format inputs (abstract values) for axis tick labels; one of:

- a [d3-format](https://d3js.org/d3-time) string for numeric scales
- a [d3-time-format](https://d3js.org/d3-time-format) string for temporal scales

`fx_tick_rotate` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The rotation angle of axis tick labels in degrees clocksize; defaults to 0.

`fx_grid` bool \| str \| Interval \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether to show a grid aligned with the scale’s ticks. If true, show a grid with the currentColor stroke; if a string, show a grid with the specified stroke color; if an approximate number of ticks, an interval, or an array of tick values, show corresponding grid lines. See also the grid mark.

For axes only.

`fx_line` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, draw a line along the axis; if false (default), do not.

`fx_label_anchor` Literal\['right', 'left', 'center'\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
Where to place the axis **label** relative to the plot’s frame. For vertical position scales (*y* and *fy*), may be *top*, *bottom*, or *center*; for horizontal position scales (*x* and *fx*), may be *left*, *right*, or *center*. Defaults to *center* for ordinal scales (including *fx* and *fy*), and otherwise *top* for *y*, and *right* for *x*.

`fx_label_offset` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The axis **label** position offset (in pixels); default depends on margins and orientation.

`fx_font_variant` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
The font-variant attribute for axis ticks; defaults to *tabular-nums* for quantitative axes.

`fx_aria_label` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
A short label representing the axis in the accessibility tree.

`fx_aria_description` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
A textual description for the axis in the accessibility tree.

`fx_reverse` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether to reverse the scale’s encoding; equivalent to reversing either the **domain** or **range**.

`fy_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

`fy_range` Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**, and the plot’s dimensions. For ordinal position scales (*point* and *band*), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale.

`fy_inset` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four insets: **inset_top**, **inset_right**, **inset_bottom**, and **inset_left**. All insets typically default to zero, though not always (say when using bin transform). A positive inset reduces effective area, while a negative inset increases it.

`fy_inset_top` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Insets the top edge by the specified number of pixels. A positive value insets towards the bottom edge (reducing effective area), while a negative value insets away from the bottom edge (increasing it).

`fy_inset_bottom` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Insets the bottom edge by the specified number of pixels. A positive value insets towards the top edge (reducing effective area), while a negative value insets away from the top edge (increasing it).

`fy_round` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, round the output value to the nearest integer (pixel); useful for crisp edges when rendering.

For position scales only.

`fy_align` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
How to distribute unused space in the **range** for *point* and *band* scales. A number in \[0, 1\], such as:

- 0 - use the start of the range, putting unused space at the end
- 0.5 (default) - use the middle, distributing unused space evenly
- 1 use the end, putting unused space at the start

For ordinal position scales only.

`fy_padding` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
For *band* scales, how much of the **range** to reserve to separate adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of inset for the first and last value as a proportion of the bandwidth; defaults to 0.5 (50%).

For ordinal position scales only.

`fy_padding_inner` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to separate adjacent bands.

`fy_padding_outer` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to inset first and last bands.

`fy_axis` Literal\['left', 'right', 'both'\] \| bool \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
The side of the frame on which to place the implicit axis: *left* or *right* for *fy*. Defaults to *left* for an *fy* scale.

If *both*, an implicit axis will be rendered on both sides of the plot (*left* and *right* for *fy*). If null, the implicit axis is suppressed.

`fy_ticks` float \| Interval \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The desired approximate number of axis ticks, or an explicit array of tick values, or an interval such as *day* or *month*.

`fy_tick_size` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The length of axis tick marks in pixels; negative values extend in the opposite direction. Defaults to 6 for *x* and *y* axes and *color* and *opacity* *ramp* legends, and 0 for *fx* and *fy* axes.

`fy_tick_spacing` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The desired approximate spacing between adjacent axis ticks, affecting the default **ticks**; defaults to 80 pixels for *x* and *fx*, and 35 pixels for *y* and *fy*.

`fy_tick_padding` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The distance between an axis tick mark and its associated text label (in pixels); often defaults to 3, but may be affected by **fy_tick_size** and **fy_tick_rotate**.

`fy_tick_format` str \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
How to format inputs (abstract values) for axis tick labels; one of:

- a [d3-format](https://d3js.org/d3-time) string for numeric scales
- a [d3-time-format](https://d3js.org/d3-time-format) string for temporal scales

`fy_tick_rotate` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The rotation angle of axis tick labels in degrees clocksize; defaults to 0.

`fy_grid` bool \| str \| Interval \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether to show a grid aligned with the scale’s ticks. If true, show a grid with the currentColor stroke; if a string, show a grid with the specified stroke color; if an approximate number of ticks, an interval, or an array of tick values, show corresponding grid lines. See also the grid mark.

For axes only.

`fy_line` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, draw a line along the axis; if false (default), do not.

`fy_label_anchor` Literal\['top', 'bottom', 'center'\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
Where to place the axis **label** relative to the plot’s frame. For vertical position scales (*y* and *fy*), may be *top*, *bottom*, or *center*; for horizontal position scales (*x* and *fx*), may be *left*, *right*, or *center*. Defaults to *center* for ordinal scales (including *fx* and *fy*), and otherwise *top* for *y*, and *right* for *x*.

`fy_label_offset` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The axis **label** position offset (in pixels); default depends on margins and orientation.

`fy_font_variant` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
The font-variant attribute for axis ticks; defaults to *tabular-nums* for quantitative axes.

`fy_aria_label` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
A short label representing the axis in the accessibility tree.

`fy_aria_description` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
A textual description for the axis in the accessibility tree.

`fy_reverse` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether to reverse the scale’s encoding; equivalent to reversing either the **domain** or **range**.

`color_scale` [ColorScale](../reference/inspect_viz.plot.html.md#colorscale) \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
The *color* scale type, affecting how the scale encodes abstract data, say by applying a mathematical transformation. If null, the scale is disabled.

For quantitative data (numbers), defaults to *linear*; for temporal data (dates), defaults to *utc*; for ordinal data (strings or booleans), defaults to *point* for position scales, *categorical* for color scales, and otherwise *ordinal*.

`color_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For continuous data (numbers and dates), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

`color_range` Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**. For other ordinal data, it is an array (or iterable) of output values in the same order as the **domain**.

`color_clamp` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, values below the domain minimum are treated as the domain minimum, and values above the domain maximum are treated as the domain maximum.

Clamping is useful for focusing on a subset of the data while ensuring that extreme values remain visible, but use caution: clamped values may need an annotation to avoid misinterpretation. Clamping typically requires setting an explicit **domain** since if the domain is inferred, no values will be outside the domain.

For continuous scales only.

`color_n` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
For a *quantile* scale, the number of quantiles (creates *n* - 1 thresholds); for a *quantize* scale, the approximate number of thresholds; defaults to 5.

`color_nice` bool \| float \| Interval \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, or a tick count or interval, extend the domain to nice round values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and nice time intervals for *utc* and *time* scales. Pass an interval such as *minute*, *wednesday* or *month* to specify what constitutes a nice interval.

For continuous scales only.

`color_scheme` [ColorScheme](../reference/inspect_viz.plot.html.md#colorscheme) \| [Param](../reference/inspect_viz.html.md#param) \| None  
If specified, shorthand for setting the **color_range** or **color_interpolate** option of a *color* scale.

`color_interpolate` [Interpolate](../reference/inspect_viz.plot.html.md#interpolate) \| [Param](../reference/inspect_viz.html.md#param) \| None  
How to interpolate color range values. For quantitative scales only. This attribute can be used to specify a color space for interpolating colors specified in the **color_range**.

`color_pivot` Any \| [Param](../reference/inspect_viz.html.md#param) \| None  
For a diverging color scale, the input value (abstract value) that divides the domain into two parts; defaults to 0 for *diverging* scales, dividing the domain into negative and positive parts; defaults to 1 for *diverging-log* scales. By default, diverging scales are symmetric around the pivot; see the **symmetric** option.

`color_symmetric` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
For a diverging color scale, if true (the default), extend the domain to ensure that the lower part of the domain (below the **pivot**) is commensurate with the upper part of the domain (above the **pivot**).

A symmetric diverging color scale may not use all of its output **range**; this reduces contrast but ensures that deviations both below and above the **pivot** are represented proportionally. Otherwise if false, the full output **range** will be used; this increases contrast but values on opposite sides of the **pivot** may not be meaningfully compared.

`color_label` str \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

For axes and legends only.

`color_percent` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, shorthand for a transform suitable for percentages, mapping proportions in \[0, 1\] to \[0, 100\].

`color_reverse` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether to reverse the scale’s encoding; equivalent to reversing either the **domain** or **range**.

`color_zero` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether the **domain** must include zero. If the domain minimum is positive, it will be set to zero; otherwise if the domain maximum is negative, it will be set to zero.

For quantitative scales only.

`color_tick_format` str \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
How to format inputs (abstract values) for axis tick labels; one of:

- a [d3-format](https://d3js.org/d3-time) string for numeric scales
- a [d3-time-format](https://d3js.org/d3-time-format) string for temporal scales

`color_exponent` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A power scale’s exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a linear scale. For *pow* and *diverging-pow* scales only.

`color_base` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A log scale’s base; defaults to 10. Does not affect the scale’s encoding, but rather the default ticks. For *log* and *diverging-log* scales only.

`color_constant` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A symlog scale’s constant, expressing the magnitude of the linear region around the origin; defaults to 1. For *symlog* and *diverging-symlog* scales only.

`opacity_scale` [ContinuousScale](../reference/inspect_viz.plot.html.md#continuousscale) \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
The *opacity* scale type, affecting how the scale encodes abstract data, say by applying a mathematical transformation. If null, the scale is disabled. The opacity scale defaults to *linear*; this scales is intended for quantitative data.

`opacity_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For continuous data (numbers and dates), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

Opacity scales have a default domain from 0 to the maximum value of associated channels.

`opacity_range` Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values).

Opacity scales have a default range of \[0, 1\].

`opacity_clamp` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, values below the domain minimum are treated as the domain minimum, and values above the domain maximum are treated as the domain maximum.

Clamping is useful for focusing on a subset of the data while ensuring that extreme values remain visible, but use caution: clamped values may need an annotation to avoid misinterpretation. Clamping typically requires setting an explicit **domain** since if the domain is inferred, no values will be outside the domain.

For continuous scales only.

`opacity_nice` bool \| float \| Interval \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, or a tick count or interval, extend the domain to nice round values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and nice time intervals for *utc* and *time* scales. Pass an interval such as *minute*, *wednesday* or *month* to specify what constitutes a nice interval.

For continuous scales only.

`opacity_label` str \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

For axes and legends only.

`opacity_percent` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, shorthand for a transform suitable for percentages, mapping proportions in \[0, 1\] to \[0, 100\].

`opacity_reverse` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether to reverse the scale’s encoding; equivalent to reversing either the **domain** or **range**.

`opacity_zero` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether the **domain** must include zero. If the domain minimum is positive, it will be set to zero; otherwise if the domain maximum is negative, it will be set to zero.

For quantitative scales only.

`opacity_tick_format` str \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
How to format inputs (abstract values) for axis tick labels; one of:

- a [d3-format](https://d3js.org/d3-time) string for numeric scales
- a [d3-time-format](https://d3js.org/d3-time-format) string for temporal scales

`opacity_exponent` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A power scale’s exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a linear scale. For *pow* scales only.

`opacity_base` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A log scale’s base; defaults to 10. Does not affect the scale’s encoding, but rather the default ticks. For *log* scales only.

`opacity_constant` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A symlog scale’s constant, expressing the magnitude of the linear region around the origin; defaults to 1. For *symlog* scales only.

`symbol_scale` Literal\['ordinal', 'categorical', 'threshold', 'quantile', 'quantize'\] \| None \| [Param](../reference/inspect_viz.html.md#param)  
The *symbol* scale type, affecting how the scale encodes abstract data, say by applying a mathematical transformation. If null, the scale is disabled. Defaults to an *ordinal* scale type.

`symbol_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. As symbol scales are discrete, the domain is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

`symbol_range` Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**, and for position scales, the plot’s dimensions. For continuous data (numbers and dates), and for ordinal position scales (*point* and *band*), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For other ordinal data, such as for a *color* scale, it is an array (or iterable) of output values in the same order as the **domain**.

Symbol scales have a default range of categorical symbols; the choice of symbols depends on whether the associated dot mark is filled or stroked.

`r_scale` [ContinuousScale](../reference/inspect_viz.plot.html.md#continuousscale) \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
The *r* (radius) scale type, affecting how the scale encodes abstract data, say by applying a mathematical transformation. If null, the scale is disabled. The radius scale defaults to *sqrt*; this scale is intended for quantitative data.

`r_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For continuous data (numbers and dates), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

Radius scales have a default domain from 0 to the median first quartile of associated channels.

`r_range` Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**, and for position scales, the plot’s dimensions. For continuous data (numbers and dates), and for ordinal position scales (*point* and *band*), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For other ordinal data, such as for a *color* scale, it is an array (or iterable) of output values in the same order as the **domain**.

Radius scales have a default range of \[0, 3\].

`r_clamp` Any \| None  
If true, values below the domain minimum are treated as the domain minimum, and values above the domain maximum are treated as the domain maximum.

Clamping is useful for focusing on a subset of the data while ensuring that extreme values remain visible, but use caution: clamped values may need an annotation to avoid misinterpretation. Clamping typically requires setting an explicit **domain** since if the domain is inferred, no values will be outside the domain.

For continuous scales only.

`r_nice` bool \| float \| Interval \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, or a tick count or interval, extend the domain to nice round values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and nice time intervals for *utc* and *time* scales. Pass an interval such as *minute*, *wednesday* or *month* to specify what constitutes a nice interval.

For continuous scales only.

`r_label` str \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

`r_percent` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, shorthand for a transform suitable for percentages, mapping proportions in \[0, 1\] to \[0, 100\].

`r_zero` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether the **domain** must include zero. If the domain minimum is positive, it will be set to zero; otherwise if the domain maximum is negative, it will be set to zero.

For quantitative scales only.

`r_exponent` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A power scale’s exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a linear scale. For *pow* scales only.

`r_base` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A log scale’s base; defaults to 10. Does not affect the scale’s encoding, but rather the default ticks. For *log* scales only.

`r_constant` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A symlog scale’s constant, expressing the magnitude of the linear region around the origin; defaults to 1. For *symlog* scales only.

`length_scale` [ContinuousScale](../reference/inspect_viz.plot.html.md#continuousscale) \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
The *length* scale type, affecting how the scale encodes abstract data, say by applying a mathematical transformation. If null, the scale is disabled. The length scale defaults to *linear*, as this scale is intended for quantitative data.

`length_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For continuous data (numbers and dates), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

Linear scales have a default domain of \[0, 1\]. Log scales have a default domain of \[1, 10\] and cannot include zero. Radius scales have a default domain from 0 to the median first quartile of associated channels. Length have a default domain from 0 to the median median of associated channels. Opacity scales have a default domain from 0 to the maximum value of associated channels.

`length_range` Sequence\[str \| float \| bool\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**, and for position scales, the plot’s dimensions. For continuous data (numbers and dates), and for ordinal position scales (*point* and *band*), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For other ordinal data, such as for a *color* scale, it is an array (or iterable) of output values in the same order as the **domain**.

Length scales have a default range of \[0, 12\].

`length_clamp` Any \| None  
If true, values below the domain minimum are treated as the domain minimum, and values above the domain maximum are treated as the domain maximum.

Clamping is useful for focusing on a subset of the data while ensuring that extreme values remain visible, but use caution: clamped values may need an annotation to avoid misinterpretation. Clamping typically requires setting an explicit **domain** since if the domain is inferred, no values will be outside the domain.

For continuous scales only.

`length_nice` bool \| float \| Interval \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, or a tick count or interval, extend the domain to nice round values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and nice time intervals for *utc* and *time* scales. Pass an interval such as *minute*, *wednesday* or *month* to specify what constitutes a nice interval.

For continuous scales only.

`length_percent` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
If true, shorthand for a transform suitable for percentages, mapping proportions in \[0, 1\] to \[0, 100\].

`length_zero` bool \| [Param](../reference/inspect_viz.html.md#param) \| None  
Whether the **domain** must include zero. If the domain minimum is positive, it will be set to zero; otherwise if the domain maximum is negative, it will be set to zero.

For quantitative scales only.

`length_exponent` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A power scale’s exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a linear scale. For *pow* scales only.

`length_base` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A log scale’s base; defaults to 10. Does not affect the scale’s encoding, but rather the default ticks. For *log* scales only.

`length_constant` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
A symlog scale’s constant, expressing the magnitude of the linear region around the origin; defaults to 1. For *symlog* scales only.

`projection_type` [Projection](../reference/inspect_viz.plot.html.md#projection) \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
The desired projection; one of:

- a named built-in projection such as *albers-usa*
- null, for no projection

Named projections are scaled and translated to fit the **domain** to the plot’s frame (minus insets).

`projection_domain` object \| [Param](../reference/inspect_viz.html.md#param) \| None  
A GeoJSON object to fit to the plot’s frame (minus insets); defaults to a Sphere for spherical projections (outline of the the whole globe).

`projection_rotate` Sequence\[float \| [Param](../reference/inspect_viz.html.md#param)\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
A rotation of the sphere before projection; defaults to \[0, 0, 0\]. Specified as Euler angles λ (yaw, or reference longitude), φ (pitch, or reference latitude), and optionally γ (roll), in degrees.

`projection_parallels` Sequence\[float \| [Param](../reference/inspect_viz.html.md#param)\] \| [Param](../reference/inspect_viz.html.md#param) \| None  
The [standard parallels](https://d3js.org/d3-geo/conic#conic_parallels). For conic projections only.

`projection_precision` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
The projection’s [sampling threshold](https://d3js.org/d3-geo/projection#projection_precision).

`projection_clip` bool \| float \| Literal\['frame'\] \| None \| [Param](../reference/inspect_viz.html.md#param) \| None  
The projection’s clipping method; one of:

- *frame* or true (default) - clip to the plot’s frame (including margins but not insets)
- a number - clip to a circle of the given radius in degrees centered around the origin
- null or false - do not clip

Some projections (such as [*armadillo*](https://observablehq.com/@d3/armadillo) and [*berghaus*](https://observablehq.com/@d3/berghaus-star)) require spherical clipping: in that case set the marks’ **clip** option to *sphere*.

`projection_inset` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four projection insets. All insets typically default to zero, though not always. A positive inset reduces effective area, while a negative inset increases it.

`projection_inset_top` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Insets the top edge of the projection by the specified number of pixels. A positive value insets towards the bottom edge (reducing effective area), while a negative value insets away from the bottom edge (increasing it).

`projection_inset_right` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Insets the right edge of the projection by the specified number of pixels. A positive value insets towards the left edge (reducing effective area), while a negative value insets away from the left edge (increasing it).

`projection_inset_bottom` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Insets the bottom edge of the projection by the specified number of pixels. A positive value insets towards the top edge (reducing effective area), while a negative value insets away from the top edge (increasing it).

`projection_inset_left` float \| [Param](../reference/inspect_viz.html.md#param) \| None  
Insets the left edge of the projection by the specified number of pixels. A positive value insets towards the right edge (reducing effective area), while a negative value insets away from the right edge (increasing it).

### PlotAttributes

Plot attributes.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_attributes.py#L155)

``` python
class PlotAttributes(TypedDict, total=False)
```

## Legend

### legend

Create a legend.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_legend.py#L54)

``` python
def legend(
    legend: Literal["color", "opacity", "symbol"],
    *,
    columns: Literal["auto"] | int | None = "auto",
    label: str | None = None,
    target: Selection | None = None,
    field: str | None = None,
    width: float | None = None,
    height: float | None = None,
    tick_size: float | None = None,
    margin_bottom: float | None = None,
    margin_left: float | None = None,
    margin_right: float | None = None,
    margin_top: float | None = None,
    for_plot: str | None = None,
    frame_anchor: FrameAnchor | None = None,
    inset: float | None = None,
    inset_x: float | None = None,
    inset_y: float | None = None,
    border: str | bool = True,
    background: str | bool = True,
) -> Legend
```

`legend` Literal\['color', 'opacity', 'symbol'\]  
Legend type (`"color"`, `"opacity"`, or `"symbol"`).

`columns` Literal\['auto'\] \| int \| None  
The number of columns to use to layout a discrete legend (defaults to “auto”, which uses 1 column for location “left” or “right”)

`label` str \| None  
The legend label.

`target` [Selection](../reference/inspect_viz.html.md#selection) \| None  
The target selection. If specified, the legend is interactive, using a `toggle` interaction for discrete legends or an `intervalX` interaction for continuous legends.

`field` str \| None  
The data field over which to generate output selection clauses. If unspecified, a matching field is retrieved from existing plot marks.

`width` float \| None  
Width of the legend in pixels.

`height` float \| None  
Height of the legend in pixels.

`tick_size` float \| None  
The size of legend ticks in a continuous legend, in pixels.

`margin_bottom` float \| None  
The bottom margin of the legend component, in pixels.

`margin_left` float \| None  
The left margin of the legend component, in pixels.

`margin_right` float \| None  
The right margin of the legend component, in pixels.

`margin_top` float \| None  
The top margin of the legend component, in pixels.

`for_plot` str \| None  
The name of the plot this legend applies to. A plot must include a `name` attribute to be referenced. Note that this is not use when passing a legend to the [plot()](../reference/inspect_viz.plot.html.md#plot) function.

`frame_anchor` [FrameAnchor](../reference/inspect_viz.mark.html.md#frameanchor) \| None  
Where to position the relative the plot frame. Defaults to “right”.

`inset` float \| None  
The inset of the legend from the plot frame, in pixels. If no inset is specified, the legend will be positioned outside the plot frame.

`inset_x` float \| None  
The horizontal inset of the legend from the plot frame, in pixels.

`inset_y` float \| None  
The vertical inset of the legend from the plot frame, in pixels.

`border` str \| bool  
The border color for the legend. Pass ‘True’ to use the default border color, or a string to specify a custom color. Pass ‘False’ to disable the border. Defaults to `True`.

`background` str \| bool  
The background color for the legend. Pass ‘True’ to use the default background color, or a string to specify a custom color. Pass ‘False’ to disable the background. Defaults to `True`.

### Legend

Plot legend (create legends using the [legend()](../reference/inspect_viz.plot.html.md#legend) function).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_legend.py#L11)

``` python
class Legend(Component)
```

#### Attributes

`frame_anchor` [FrameAnchor](../reference/inspect_viz.mark.html.md#frameanchor)  
The frame anchor for the legend.

## Export

### to_html

Generate a self-contained HTML snippet for a plot or other component.

The returned snippet embeds the inspect-viz widget ESM plus a small bootstrap inline — no external Jupyter-widget (`embed-amd.js`, `requirejs`, `jquery`) dependencies. Suitable for Playwright headless rendering (`write_png`) and general embedding.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_write.py#L18)

``` python
def to_html(component: Component, dependencies: bool = True) -> str
```

`component` [Component](../reference/inspect_viz.html.md#component)  
Component to export.

`dependencies` bool  
Accepted for backward compatibility; the returned snippet is always self-contained, so this parameter has no effect.

### write_html

Write an HTML file for a plot or other component.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_write.py#L52)

``` python
def write_html(
    file: str | Path, component: Component, dependencies: bool = True
) -> None
```

`file` str \| Path  
Target filename.

`component` [Component](../reference/inspect_viz.html.md#component)  
Compontent to export.

`dependencies` bool  
Include JavaScript dependencies required for Jupyter widget rendering. Dependencies should only be included once per web-page, so if you already have them on a page you might want to disable including them when generating HTML.

### write_png

Export a plot or table to a PNG.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_write.py#L80)

``` python
def write_png(
    file: str | Path | None, component: Component, scale: int = 2, padding: int = 8
) -> tuple[bytes, int, int] | tuple[int, int] | None
```

`file` str \| Path \| None  
Target filename (pass `None` to return the image as bytes)

`component` [Component](../reference/inspect_viz.html.md#component)  
Component to export.

`scale` int  
Device scale to capture plot at. Use 2 (the default) for retina quality images suitable for high resolution displays or print output)

`padding` int  
Padding (in pixels) around plot.

## Defaults

### plot_defaults

Set global plot defaults.

Note that this function should be called once at the outset (subsequent calls to it do not reset the defaults).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_defaults.py#L42)

``` python
def plot_defaults(
    *,
    x_label: str | Param = ...,
    fx_label: str | Param = ...,
    y_label: str | Param = ...,
    fy_label: str | Param = ...,
    width: float | Param = ...,
    height: float | Param = ...,
) -> None
```

`x_label` str \| [Param](../reference/inspect_viz.html.md#param)  
A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

`fx_label` str \| [Param](../reference/inspect_viz.html.md#param)  
A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

For axes and legends only.

`y_label` str \| [Param](../reference/inspect_viz.html.md#param)  
A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

`fy_label` str \| [Param](../reference/inspect_viz.html.md#param)  
A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

For axes and legends only.

`width` float \| [Param](../reference/inspect_viz.html.md#param)  
The outer width of the plot in pixels, including margins. Defaults to 640.

`height` float \| [Param](../reference/inspect_viz.html.md#param)  
The outer height of the plot in pixels, including margins. The default depends on the plot’s scales, and the plot’s width if an aspectRatio is specified. For example, if the *y* scale is linear and there is no *fy* scale, it might be 396.

### PlotDefaults

Default options for plots.

Use the [plot_defaults()](../reference/inspect_viz.plot.html.md#plot_defaults) function to set global defaults for plot options.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_defaults.py#L9)

``` python
class PlotDefaults(PlotAttributes, total=False)
```

#### Attributes

`x_label` str \| [Param](../reference/inspect_viz.html.md#param)  
A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

`fx_label` str \| [Param](../reference/inspect_viz.html.md#param)  
    A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

For axes and legends only.

`y_label` str \| [Param](../reference/inspect_viz.html.md#param)  
A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

`fy_label` str \| [Param](../reference/inspect_viz.html.md#param)  
    A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

For axes and legends only.

`width` float \| [Param](../reference/inspect_viz.html.md#param)  
The outer width of the plot in pixels, including margins. Defaults to 640.

`height` float \| [Param](../reference/inspect_viz.html.md#param)  
The outer height of the plot in pixels, including margins. The default depends on the plot’s scales, and the plot’s width if an aspectRatio is specified. For example, if the *y* scale is linear and there is no *fy* scale, it might be 396.

## Types

### PositionScale

How a scale encodes abstract data, say by applying a mathematical transformation.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_attributes.py#L7)

``` python
PositionScale: TypeAlias = Literal[
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
```

### Projection

Built-in projection types.

Named projections are scaled and translated to fit the **domain** to the plot’s frame (minus insets).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_attributes.py#L25)

``` python
Projection: TypeAlias = Literal[
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
```

### ContinuousScale

Continuous scaling transformations.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_attributes.py#L48)

``` python
ContinuousScale: TypeAlias = Literal[
    "linear",
    "log",
    "pow",
    "sqrt",
    "symlog",
    "utc",
    "time",
    "identity",
]
```

### ColorScale

Color scale tranformations.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_attributes.py#L60)

``` python
ColorScale: TypeAlias = Literal[
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
```

### ColorScheme

Color schemes.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_attributes.py#L84)

``` python
ColorScheme: TypeAlias = Literal[
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
```

### Interpolate

How to interpolate color range values.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_attributes.py#L130)

``` python
Interpolate: TypeAlias = Literal[
    "rgb",
    "hsl",
    "lab",
    "hcl",
    "cubehelix",
]
```

### LabelArrow

Whether to apply a directional arrow to an axis scale label.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/plot/_attributes.py#L140)

``` python
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
```
