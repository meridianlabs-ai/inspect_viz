# Scores by Task

## Overview

The [scores_by_task()](reference/inspect_viz.view.html.md#scores_by_task) function renders a bar plot for comparing eval scores.

``` python
from inspect_viz import Data
from inspect_viz.view import scores_by_task

evals = Data.from_file("evals.parquet")
scores_by_task(evals)
```

## Data Preparation

Above we read the data for the plot from a parquet file. This file was in turn created by:

1.  Reading logs into a data frame with [evals_df()](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evals_df).

2.  Using the [prepare()](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#prepare) function to add [model_info()](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info) and [log_viewer()](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info) columns to the data frame.

``` python
from inspect_ai.analysis import evals_df, log_viewer, model_info, prepare

df = evals_df("logs")
df = prepare(df, [
    model_info(),
    log_viewer("eval", {"logs": "https://samples.meridianlabs.ai/"})
])
df.to_parquet("evals.parquet")
```

You can additionally use the [task_info()](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#task_info) operation to map lower-level task names to task display names (e.g. “gpqa_diamond” -\> “GPQA Diamond”).

Note that both the log viewer links and model names are optional (the plot will render without links and use raw model strings if the data isn’t prepared with [log_viewer()](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#log_viewer) and [model_info()](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info)).

## Function Reference

Bar plot for comparing eval scores.

Summarize eval scores using a bar plot. By default, scores (`y`) are plotted by “task_display_name” (`fx`) and “model_display_name” (`x`). By default, confidence intervals are also plotted (disable this with `y_ci=False`).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/3bd2ebf265e271209a81bcaf0bca12c3a765297d/src/inspect_viz/view/_scores_by_task.py#L20)

``` python
def scores_by_task(
    data: Data,
    model_name: str = ...,
    task_name: str = ...,
    score_value: str = ...,
    score_stderr: str = ...,
    score_label: str | None | NotGiven = ...,
    ci: bool | float = ...,
    title: str | Title | None = ...,
    marks: Marks | None = ...,
    width: float | Param | None = ...,
    height: float | Param | None = ...,
    legend: Legend | NotGiven | None = ...,
    *,
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

`data` [Data](reference/inspect_viz.html.md#data)  
Evals data table. This is typically created using a data frame read with the inspect [evals_df()](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evals_df) function.

`model_name` str  
Name of field for the model name (defaults to “model_display_name”)

`task_name` str  
Name of field for the task name (defaults to “task_display_name”)

`score_value` str  
Name of field for the score value (defaults to “score_headline_value”).

`score_stderr` str  
Name of field for stderr (defaults to “score_headline_metric”).

`score_label` str \| None \| NotGiven  
Score axis label (pass None for no label).

`ci` bool \| float  
Confidence interval (e.g. 0.80, 0.90, 0.95, etc.). Defaults to 0.95.

`title` str \| [Title](reference/inspect_viz.mark.html.md#title) \| None  
Title for plot (`str` or mark created with the [title()](reference/inspect_viz.mark.html.md#title) function).

`marks` [Marks](reference/inspect_viz.mark.html.md#marks) \| None  
Additional marks to include in the plot.

`width` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The outer width of the plot in pixels, including margins. Defaults to 700.

`height` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The outer height of the plot in pixels, including margins. The default is width / 1.618 (the [golden ratio](https://en.wikipedia.org/wiki/Golden_ratio))

`legend` [Legend](reference/inspect_viz.plot.html.md#legend) \| NotGiven \| None  
Options for the legend. Pass None to disable the legend.

`aspect_ratio` float \| bool \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
The desired aspect ratio of the *x* and *y* scales, affecting the default height. Given an aspect ratio of *dx* / *dy*, and assuming that the *x* and *y* scales represent equivalent units (say, degrees Celsius or meters), computes a default height such that *dx* pixels along *x* represents the same variation as *dy* pixels along *y*. Note: when faceting, set the *fx* and *fy* scales’ **round** option to false for an exact aspect ratio.

`margin` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four margins: **margin_top**, **margin_right**, **margin_bottom**, and **margin_left**. Otherwise, the default margins depend on the maximum margins of the plot’s marks. While most marks default to zero margins (because they are drawn inside the chart area), Plot’s axis marks have non-zero default margins.

`margin_top` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The top margin; the distance in pixels between the top edges of the inner and outer plot area. Defaults to the maximum top margin of the plot’s marks.

`margin_right` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The right margin; the distance in pixels between the right edges of the inner and outer plot area. Defaults to the maximum right margin of the plot’s marks.

`margin_bottom` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The bottom margin; the distance in pixels between the bottom edges of the inner and outer plot area. Defaults to the maximum bottom margin of the plot’s marks.

`margin_left` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The left margin; the distance in pixels between the left edges of the inner and outer plot area. Defaults to the maximum left margin of the plot’s marks.

`margins` dict\[str, float \| [Param](reference/inspect_viz.html.md#param)\] \| None  
A shorthand object notation for setting multiple margin values. The object keys are margin names (top, right, etc).

`inset` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four insets: **inset_top**, **inset_right**, **inset_bottom**, and **inset_left**. All insets typically default to zero, though not always (say when using bin transform). A positive inset reduces effective area, while a negative inset increases it.

`style` str \| dict\[str, str\] \| None \| [Param](reference/inspect_viz.html.md#param)  
Custom styles to override Plot’s defaults. Styles may be specified either as a string of inline styles (*e.g.*, `"color: red;"`, in the same fashion as assigning [*element*.style](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style)) or an object of properties (*e.g.*, `{color: "red"}`, in the same fashion as assigning [*element*.style properties](https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleDeclaration)). Note that unitless numbers ([quirky lengths](https://www.w3.org/TR/css-values-4/#deprecated-quirky-length)) such as `{padding: 20}` may not supported by some browsers; you should instead specify a string with units such as `{padding: "20px"}`. By default, the returned plot has a max-width of 100%, and the system-ui font. Plot’s marks and axes default to [currentColor](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value#currentcolor_keyword), meaning that they will inherit the surrounding content’s color.

`align` float \| [Param](reference/inspect_viz.html.md#param) \| None  
How to distribute unused space in the **range** for *point* and *band* scales. A number in \[0, 1\], such as:

- 0 - use the start of the range, putting unused space at the end
- 0.5 (default) - use the middle, distributing unused space evenly
- 1 use the end, putting unused space at the start

For ordinal position scales only.

`padding` float \| [Param](reference/inspect_viz.html.md#param) \| None  
For *band* scales, how much of the **range** to reserve to separate adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of inset for the first and last value as a proportion of the bandwidth; defaults to 0.5 (50%).

For ordinal position scales only.

`axis` Literal\['top', 'right', 'bottom', 'left', 'both'\] \| bool \| None \| [Param](reference/inspect_viz.html.md#param)  
The side of the frame on which to place the implicit axis: *top* or *bottom* for *x* or *fx*, or *left* or *right* for *y* or *fy*. The default depends on the scale:

- *x* - *bottom*
- *y* - *left*
- *fx* - *top* if there is a *bottom* *x* axis, and otherwise *bottom*
- *fy* - *right* if there is a *left* *y* axis, and otherwise *right*

If *both*, an implicit axis will be rendered on both sides of the plot (*top* and *bottom* for *x* or *fx*, or *left* and *right* for *y* or *fy*). If null, the implicit axis is suppressed.

For position axes only.

`grid` bool \| str \| [Param](reference/inspect_viz.html.md#param)  
Whether to show a grid aligned with the scale’s ticks. If true, show a grid with the currentColor stroke; if a string, show a grid with the specified stroke color.

`aria_label` str \| None  
The [aria-label attribute](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-label) on the SVG root.

`aria_description` str \| None  
The [aria-description attribute](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-description) on the SVG root.

`clip` Literal\['frame', 'sphere'\] \| bool \| None \| [Param](reference/inspect_viz.html.md#param)  
The default clip for all marks.

`x_scale` [PositionScale](reference/inspect_viz.plot.html.md#positionscale) \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
The *x* scale type, affecting how the scale encodes abstract data, say by applying a mathematical transformation. If null, the scale is disabled.

For quantitative data (numbers), defaults to *linear*; for temporal data (dates), defaults to *utc*; for ordinal data (strings or booleans), defaults to *point* for position scales, *categorical* for color scales, and otherwise *ordinal*. However, the radius scale defaults to *sqrt*, and the length and opacity scales default to *linear*; these scales are intended for quantitative data. The plot’s marks may also impose a scale type; for example, the barY mark requires that *x* is a *band* scale.

`x_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For continuous data (numbers and dates), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

Linear scales have a default domain of \[0, 1\]. Log scales have a default domain of \[1, 10\] and cannot include zero. Radius scales have a default domain from 0 to the median first quartile of associated channels. Length have a default domain from 0 to the median median of associated channels. Opacity scales have a default domain from 0 to the maximum value of associated channels.

`x_range` Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**, and for position scales, the plot’s dimensions. For continuous data (numbers and dates), and for ordinal position scales (*point* and *band*), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale.

`x_nice` bool \| float \| Interval \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, or a tick count or interval, extend the domain to nice round values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and nice time intervals for *utc* and *time* scales. Pass an interval such as *minute*, *wednesday* or *month* to specify what constitutes a nice interval.

For continuous scales only.

`x_inset` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four insets: **inset_top**, **inset_right**, **inset_bottom**, and **inset_left**. All insets typically default to zero, though not always (say when using bin transform). A positive inset reduces effective area, while a negative inset increases it.

`x_inset_right` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Insets the right edge by the specified number of pixels. A positive value insets towards the left edge (reducing effective area), while a negative value insets away from the left edge (increasing it).

`x_inset_left` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Insets the left edge by the specified number of pixels. A positive value insets towards the right edge (reducing effective area), while a negative value insets away from the right edge (increasing it).

`x_clamp` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, values below the domain minimum are treated as the domain minimum, and values above the domain maximum are treated as the domain maximum.

Clamping is useful for focusing on a subset of the data while ensuring that extreme values remain visible, but use caution: clamped values may need an annotation to avoid misinterpretation. Clamping typically requires setting an explicit **domain** since if the domain is inferred, no values will be outside the domain.

For continuous scales only.

`x_round` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, round the output value to the nearest integer (pixel); useful for crisp edges when rendering.

For position scales only.

`x_align` float \| [Param](reference/inspect_viz.html.md#param) \| None  
How to distribute unused space in the **range** for *point* and *band* scales. A number in \[0, 1\], such as:

- 0 - use the start of the range, putting unused space at the end
- 0.5 (default) - use the middle, distributing unused space evenly
- 1 use the end, putting unused space at the start

For ordinal position scales only.

`x_padding` float \| [Param](reference/inspect_viz.html.md#param) \| None  
For *band* scales, how much of the **range** to reserve to separate adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of inset for the first and last value as a proportion of the bandwidth; defaults to 0.5 (50%).

For ordinal position scales only.

`x_padding_inner` float \| [Param](reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to separate adjacent bands.

`x_padding_outer` float \| [Param](reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to inset first and last bands.

`x_axis` Literal\['top', 'bottom', 'both'\] \| bool \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
The side of the frame on which to place the implicit axis: *top* or *bottom* for *x*. Defaults to *bottom* for an *x* scale.

If *both*, an implicit axis will be rendered on both sides of the plot (*top* and *bottom* for *x*). If null, the implicit axis is suppressed.

`x_ticks` float \| Interval \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The desired approximate number of axis ticks, or an explicit array of tick values, or an interval such as *day* or *month*.

`x_tick_size` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The length of axis tick marks in pixels; negative values extend in the opposite direction. Defaults to 6 for *x* and *y* axes and *color* and *opacity* *ramp* legends, and 0 for *fx* and *fy* axes.

`x_tick_spacing` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The desired approximate spacing between adjacent axis ticks, affecting the default **ticks**; defaults to 80 pixels for *x* and *fx*, and 35 pixels for *y* and *fy*.

`x_tick_padding` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The distance between an axis tick mark and its associated text label (in pixels); often defaults to 3, but may be affected by **x_tick_size** and **x_tick_rotate**.

`x_tick_format` str \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
How to format inputs (abstract values) for axis tick labels; one of:

- a [d3-format](https://d3js.org/d3-time) string for numeric scales
- a [d3-time-format](https://d3js.org/d3-time-format) string for temporal scales

`x_tick_rotate` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The rotation angle of axis tick labels in degrees clocksize; defaults to 0.

`x_grid` bool \| str \| Interval \| list\[str \| float\] \| [Param](reference/inspect_viz.html.md#param)  
Whether to show a grid aligned with the scale’s ticks. If true, show a grid with the currentColor stroke; if a string, show a grid with the specified stroke color; if an approximate number of ticks, an interval, or an array of tick values, show corresponding grid lines.

`x_line` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, draw a line along the axis; if false (default), do not.

`x_label_anchor` Literal\['right', 'left', 'center'\] \| [Param](reference/inspect_viz.html.md#param) \| None  
Where to place the axis **label** relative to the plot’s frame. For vertical position scales (*y* and *fy*), may be *top*, *bottom*, or *center*; for horizontal position scales (*x* and *fx*), may be *left*, *right*, or *center*. Defaults to *center* for ordinal scales (including *fx* and *fy*), and otherwise *top* for *y*, and *right* for *x*.

`x_label_arrow` [LabelArrow](reference/inspect_viz.plot.html.md#labelarrow) \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether to apply a directional arrow such as → or ↑ to the x-axis scale label. If *auto* (the default), the presence of the arrow depends on whether the scale is ordinal.

`x_label_offset` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The axis **label** position offset (in pixels); default depends on margins and orientation.

`x_font_variant` str \| [Param](reference/inspect_viz.html.md#param) \| None  
The font-variant attribute for axis ticks; defaults to *tabular-nums* for quantitative axes.

`x_aria_label` str \| [Param](reference/inspect_viz.html.md#param) \| None  
A short label representing the axis in the accessibility tree.

`x_aria_description` str \| [Param](reference/inspect_viz.html.md#param) \| None  
A textual description for the axis in the accessibility tree.

`x_percent` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, shorthand for a transform suitable for percentages, mapping proportions in \[0, 1\] to \[0, 100\].

`x_reverse` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether to reverse the scale’s encoding; equivalent to reversing either the **domain** or **range**.

`x_zero` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether the **domain** must include zero. If the domain minimum is positive, it will be set to zero; otherwise if the domain maximum is negative, it will be set to zero.

For quantitative scales only.

`x_exponent` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A power scale’s exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a linear scale. For *pow* scales only.

`x_base` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A log scale’s base; defaults to 10. Does not affect the scale’s encoding, but rather the default ticks. For *log* scales only.

`x_constant` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A symlog scale’s constant, expressing the magnitude of the linear region around the origin; defaults to 1. For *symlog* scales only.

`y_scale` [PositionScale](reference/inspect_viz.plot.html.md#positionscale) \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
The *y* scale type, affecting how the scale encodes abstract data, say by applying a mathematical transformation. If null, the scale is disabled.

For quantitative data (numbers), defaults to *linear*; for temporal data (dates), defaults to *utc*; for ordinal data (strings or booleans), defaults to *point* for position scales, The plot’s marks may also impose a scale type; for example, the barY mark requires that *x* is a *band* scale.

`y_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For continuous data (numbers and dates), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

Linear scales have a default domain of \[0, 1\]. Log scales have a default domain of \[1, 10\] and cannot include zero.

`y_range` Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**, and for position scales, the plot’s dimensions. For continuous data (numbers and dates), and for ordinal position scales (*point* and *band*), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale.

`y_nice` bool \| float \| Interval \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, or a tick count or interval, extend the domain to nice round values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and nice time intervals for *utc* and *time* scales. Pass an interval such as *minute*, *wednesday* or *month* to specify what constitutes a nice interval.

For continuous scales only.

`y_inset` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four insets: **inset_top**, **inset_right**, **inset_bottom**, and **inset_left**. All insets typically default to zero, though not always (say when using bin transform). A positive inset reduces effective area, while a negative inset increases it.

`y_inset_top` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Insets the top edge by the specified number of pixels. A positive value insets towards the bottom edge (reducing effective area), while a negative value insets away from the bottom edge (increasing it).

`y_inset_bottom` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Insets the bottom edge by the specified number of pixels. A positive value insets towards the top edge (reducing effective area), while a negative value insets away from the top edge (increasing it).

`y_clamp` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, values below the domain minimum are treated as the domain minimum, and values above the domain maximum are treated as the domain maximum.

Clamping is useful for focusing on a subset of the data while ensuring that extreme values remain visible, but use caution: clamped values may need an annotation to avoid misinterpretation. Clamping typically requires setting an explicit **domain** since if the domain is inferred, no values will be outside the domain.

For continuous scales only.

`y_round` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, round the output value to the nearest integer (pixel); useful for crisp edges when rendering.

For position scales only.

`y_align` float \| [Param](reference/inspect_viz.html.md#param) \| None  
How to distribute unused space in the **range** for *point* and *band* scales. A number in \[0, 1\], such as:

- 0 - use the start of the range, putting unused space at the end
- 0.5 (default) - use the middle, distributing unused space evenly
- 1 use the end, putting unused space at the start

For ordinal position scales only.

`y_padding` float \| [Param](reference/inspect_viz.html.md#param) \| None  
For *band* scales, how much of the **range** to reserve to separate adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of inset for the first and last value as a proportion of the bandwidth; defaults to 0.5 (50%).

For ordinal position scales only.

`y_padding_inner` float \| [Param](reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to separate adjacent bands.

`y_padding_outer` float \| [Param](reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to inset first and last bands.

`y_axis` Literal\['left', 'right', 'both'\] \| bool \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
The side of the frame on which to place the implicit axis: *left* or *right* for *y*. Defaults to *left* for a *y* scale.

If *both*, an implicit axis will be rendered on both sides of the plot (*left* and *right* for *y*). If null, the implicit axis is suppressed.

`y_ticks` float \| Interval \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The desired approximate number of axis ticks, or an explicit array of tick values, or an interval such as *day* or *month*.

`y_tick_size` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The length of axis tick marks in pixels; negative values extend in the opposite direction. Defaults to 6 for *x* and *y* axes and *color* and *opacity* *ramp* legends, and 0 for *fx* and *fy* axes.

`y_tick_spacing` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The desired approximate spacing between adjacent axis ticks, affecting the default **ticks**; defaults to 80 pixels for *x* and *fx*, and 35 pixels for *y* and *fy*.

`y_tick_padding` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The distance between an axis tick mark and its associated text label (in pixels); often defaults to 3, but may be affected by **y_tick_size** and **y_tick_rotate**.

`y_tick_format` str \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
How to format inputs (abstract values) for axis tick labels; one of:

- a [d3-format](https://d3js.org/d3-time) string for numeric scales
- a [d3-time-format](https://d3js.org/d3-time-format) string for temporal scales

`y_tick_rotate` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The rotation angle of axis tick labels in degrees clocksize; defaults to 0.

`y_grid` bool \| str \| Interval \| list\[str \| float\] \| [Param](reference/inspect_viz.html.md#param)  
Whether to show a grid aligned with the scale’s ticks. If true, show a grid with the currentColor stroke; if a string, show a grid with the specified stroke color; if an approximate number of ticks, an interval, or an array of tick values, show corresponding grid lines.

`y_line` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, draw a line along the axis; if false (default), do not.

`y_label_anchor` Literal\['top', 'bottom', 'center'\] \| [Param](reference/inspect_viz.html.md#param) \| None  
Where to place the axis **label** relative to the plot’s frame. For vertical position scales (*y* and *fy*), may be *top*, *bottom*, or *center*; for horizontal position scales (*x* and *fx*), may be *left*, *right*, or *center*. Defaults to *center* for ordinal scales (including *fx* and *fy*), and otherwise *top* for *y*, and *right* for *x*.

`y_label_arrow` [LabelArrow](reference/inspect_viz.plot.html.md#labelarrow) \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether to apply a directional arrow such as → or ↑ to the x-axis scale label. If *auto* (the default), the presence of the arrow depends on whether the scale is ordinal.

`y_label_offset` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The axis **label** position offset (in pixels); default depends on margins and orientation.

`y_font_variant` str \| [Param](reference/inspect_viz.html.md#param) \| None  
The font-variant attribute for axis ticks; defaults to *tabular-nums* for quantitative axes.

`y_aria_label` str \| [Param](reference/inspect_viz.html.md#param) \| None  
A short label representing the axis in the accessibility tree.

`y_aria_description` str \| [Param](reference/inspect_viz.html.md#param) \| None  
A textual description for the axis in the accessibility tree.

`y_percent` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, shorthand for a transform suitable for percentages, mapping proportions in \[0, 1\] to \[0, 100\].

`y_reverse` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether to reverse the scale’s encoding; equivalent to reversing either the **domain** or **range**. Note that by default, when the *y* scale is continuous, the *max* value points to the top of the screen, whereas ordinal values are ranked from top to bottom.

`y_zero` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether the **domain** must include zero. If the domain minimum is positive, it will be set to zero; otherwise if the domain maximum is negative, it will be set to zero.

For quantitative scales only.

`y_exponent` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A power scale’s exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a linear scale. For *pow* scales only.

`y_base` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A log scale’s base; defaults to 10. Does not affect the scale’s encoding, but rather the default ticks. For *log* scales only.

`y_constant` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A symlog scale’s constant, expressing the magnitude of the linear region around the origin; defaults to 1. For *symlog* scales only.

`xy_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
Set the *x* and *y* scale domains.

`facet_margin` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four facet margins: margin_top, margin_right, margin_bottom, and margin_left.

`facet_margin_top` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The top facet margin; the (minimum) distance in pixels between the top edges of the inner and outer plot area.

`facet_margin_bottom` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The right facet margin; the (minimum) distance in pixels between the right edges of the inner and outer plot area.

`facet_margin_left` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The bottom facet margin; the (minimum) distance in pixels between the bottom edges of the inner and outer plot area.

`facet_margin_right` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The left facet margin; the (minimum) distance in pixels between the left edges of the inner and outer plot area.

`facet_grid` bool \| str \| Interval \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
Default axis grid for fx and fy scales; typically set to true to enable.

`facet_label` str \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
Default axis label for fx and fy scales; typically set to null to disable.

`fx_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

`fx_range` Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**, and the plot’s dimensions. For ordinal position scales (*point* and *band*), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale.

`fx_inset` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four insets: **inset_top**, **inset_right**, **inset_bottom**, and **inset_left**. All insets typically default to zero, though not always (say when using bin transform). A positive inset reduces effective area, while a negative inset increases it.

`fx_inset_right` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Insets the right edge by the specified number of pixels. A positive value insets towards the left edge (reducing effective area), while a negative value insets away from the left edge (increasing it).

`fx_inset_left` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Insets the left edge by the specified number of pixels. A positive value insets towards the right edge (reducing effective area), while a negative value insets away from the right edge (increasing it).

`fx_round` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, round the output value to the nearest integer (pixel); useful for crisp edges when rendering.

For position scales only.

`fx_align` float \| [Param](reference/inspect_viz.html.md#param) \| None  
How to distribute unused space in the **range** for *point* and *band* scales. A number in \[0, 1\], such as:

- 0 - use the start of the range, putting unused space at the end
- 0.5 (default) - use the middle, distributing unused space evenly
- 1 use the end, putting unused space at the start

For ordinal position scales only.

`fx_padding` float \| [Param](reference/inspect_viz.html.md#param) \| None  
For *band* scales, how much of the **range** to reserve to separate adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of inset for the first and last value as a proportion of the bandwidth; defaults to 0.5 (50%).

For ordinal position scales only.

`fx_padding_inner` float \| [Param](reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to separate adjacent bands.

`fx_padding_outer` float \| [Param](reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to inset first and last bands.

`fx_axis` Literal\['top', 'bottom', 'both'\] \| bool \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
The side of the frame on which to place the implicit axis: *top* or *bottom* for *fx*. Defaults to *top* if there is a *bottom* *x* axis, and otherwise *bottom*.

If *both*, an implicit axis will be rendered on both sides of the plot (*top* and *bottom* for *fx*). If null, the implicit axis is suppressed.

`fx_ticks` float \| Interval \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The desired approximate number of axis ticks, or an explicit array of tick values, or an interval such as *day* or *month*.

`fx_tick_size` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The length of axis tick marks in pixels; negative values extend in the opposite direction. Defaults to 6 for *x* and *y* axes and *color* and *opacity* *ramp* legends, and 0 for *fx* and *fy* axes.

`fx_tick_spacing` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The desired approximate spacing between adjacent axis ticks, affecting the default **ticks**; defaults to 80 pixels for *x* and *fx*, and 35 pixels for *y* and *fy*.

`fx_tick_padding` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The distance between an axis tick mark and its associated text label (in pixels); often defaults to 3, but may be affected by **fx_tick_size** and **fx_tick_rotate**.

`fx_tick_format` str \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
How to format inputs (abstract values) for axis tick labels; one of:

- a [d3-format](https://d3js.org/d3-time) string for numeric scales
- a [d3-time-format](https://d3js.org/d3-time-format) string for temporal scales

`fx_tick_rotate` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The rotation angle of axis tick labels in degrees clocksize; defaults to 0.

`fx_grid` bool \| str \| Interval \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether to show a grid aligned with the scale’s ticks. If true, show a grid with the currentColor stroke; if a string, show a grid with the specified stroke color; if an approximate number of ticks, an interval, or an array of tick values, show corresponding grid lines. See also the grid mark.

For axes only.

`fx_line` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, draw a line along the axis; if false (default), do not.

`fx_label_anchor` Literal\['right', 'left', 'center'\] \| [Param](reference/inspect_viz.html.md#param) \| None  
Where to place the axis **label** relative to the plot’s frame. For vertical position scales (*y* and *fy*), may be *top*, *bottom*, or *center*; for horizontal position scales (*x* and *fx*), may be *left*, *right*, or *center*. Defaults to *center* for ordinal scales (including *fx* and *fy*), and otherwise *top* for *y*, and *right* for *x*.

`fx_label_offset` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The axis **label** position offset (in pixels); default depends on margins and orientation.

`fx_font_variant` str \| [Param](reference/inspect_viz.html.md#param) \| None  
The font-variant attribute for axis ticks; defaults to *tabular-nums* for quantitative axes.

`fx_aria_label` str \| [Param](reference/inspect_viz.html.md#param) \| None  
A short label representing the axis in the accessibility tree.

`fx_aria_description` str \| [Param](reference/inspect_viz.html.md#param) \| None  
A textual description for the axis in the accessibility tree.

`fx_reverse` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether to reverse the scale’s encoding; equivalent to reversing either the **domain** or **range**.

`fy_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

`fy_range` Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**, and the plot’s dimensions. For ordinal position scales (*point* and *band*), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale.

`fy_inset` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four insets: **inset_top**, **inset_right**, **inset_bottom**, and **inset_left**. All insets typically default to zero, though not always (say when using bin transform). A positive inset reduces effective area, while a negative inset increases it.

`fy_inset_top` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Insets the top edge by the specified number of pixels. A positive value insets towards the bottom edge (reducing effective area), while a negative value insets away from the bottom edge (increasing it).

`fy_inset_bottom` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Insets the bottom edge by the specified number of pixels. A positive value insets towards the top edge (reducing effective area), while a negative value insets away from the top edge (increasing it).

`fy_round` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, round the output value to the nearest integer (pixel); useful for crisp edges when rendering.

For position scales only.

`fy_align` float \| [Param](reference/inspect_viz.html.md#param) \| None  
How to distribute unused space in the **range** for *point* and *band* scales. A number in \[0, 1\], such as:

- 0 - use the start of the range, putting unused space at the end
- 0.5 (default) - use the middle, distributing unused space evenly
- 1 use the end, putting unused space at the start

For ordinal position scales only.

`fy_padding` float \| [Param](reference/inspect_viz.html.md#param) \| None  
For *band* scales, how much of the **range** to reserve to separate adjacent bands; defaults to 0.1 (10%). For *point* scales, the amount of inset for the first and last value as a proportion of the bandwidth; defaults to 0.5 (50%).

For ordinal position scales only.

`fy_padding_inner` float \| [Param](reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to separate adjacent bands.

`fy_padding_outer` float \| [Param](reference/inspect_viz.html.md#param) \| None  
For a *band* scale, how much of the range to reserve to inset first and last bands.

`fy_axis` Literal\['left', 'right', 'both'\] \| bool \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
The side of the frame on which to place the implicit axis: *left* or *right* for *fy*. Defaults to *left* for an *fy* scale.

If *both*, an implicit axis will be rendered on both sides of the plot (*left* and *right* for *fy*). If null, the implicit axis is suppressed.

`fy_ticks` float \| Interval \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The desired approximate number of axis ticks, or an explicit array of tick values, or an interval such as *day* or *month*.

`fy_tick_size` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The length of axis tick marks in pixels; negative values extend in the opposite direction. Defaults to 6 for *x* and *y* axes and *color* and *opacity* *ramp* legends, and 0 for *fx* and *fy* axes.

`fy_tick_spacing` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The desired approximate spacing between adjacent axis ticks, affecting the default **ticks**; defaults to 80 pixels for *x* and *fx*, and 35 pixels for *y* and *fy*.

`fy_tick_padding` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The distance between an axis tick mark and its associated text label (in pixels); often defaults to 3, but may be affected by **fy_tick_size** and **fy_tick_rotate**.

`fy_tick_format` str \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
How to format inputs (abstract values) for axis tick labels; one of:

- a [d3-format](https://d3js.org/d3-time) string for numeric scales
- a [d3-time-format](https://d3js.org/d3-time-format) string for temporal scales

`fy_tick_rotate` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The rotation angle of axis tick labels in degrees clocksize; defaults to 0.

`fy_grid` bool \| str \| Interval \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether to show a grid aligned with the scale’s ticks. If true, show a grid with the currentColor stroke; if a string, show a grid with the specified stroke color; if an approximate number of ticks, an interval, or an array of tick values, show corresponding grid lines. See also the grid mark.

For axes only.

`fy_line` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, draw a line along the axis; if false (default), do not.

`fy_label_anchor` Literal\['top', 'bottom', 'center'\] \| [Param](reference/inspect_viz.html.md#param) \| None  
Where to place the axis **label** relative to the plot’s frame. For vertical position scales (*y* and *fy*), may be *top*, *bottom*, or *center*; for horizontal position scales (*x* and *fx*), may be *left*, *right*, or *center*. Defaults to *center* for ordinal scales (including *fx* and *fy*), and otherwise *top* for *y*, and *right* for *x*.

`fy_label_offset` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The axis **label** position offset (in pixels); default depends on margins and orientation.

`fy_font_variant` str \| [Param](reference/inspect_viz.html.md#param) \| None  
The font-variant attribute for axis ticks; defaults to *tabular-nums* for quantitative axes.

`fy_aria_label` str \| [Param](reference/inspect_viz.html.md#param) \| None  
A short label representing the axis in the accessibility tree.

`fy_aria_description` str \| [Param](reference/inspect_viz.html.md#param) \| None  
A textual description for the axis in the accessibility tree.

`fy_reverse` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether to reverse the scale’s encoding; equivalent to reversing either the **domain** or **range**.

`color_scale` [ColorScale](reference/inspect_viz.plot.html.md#colorscale) \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
The *color* scale type, affecting how the scale encodes abstract data, say by applying a mathematical transformation. If null, the scale is disabled.

For quantitative data (numbers), defaults to *linear*; for temporal data (dates), defaults to *utc*; for ordinal data (strings or booleans), defaults to *point* for position scales, *categorical* for color scales, and otherwise *ordinal*.

`color_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For continuous data (numbers and dates), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

`color_range` Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**. For other ordinal data, it is an array (or iterable) of output values in the same order as the **domain**.

`color_clamp` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, values below the domain minimum are treated as the domain minimum, and values above the domain maximum are treated as the domain maximum.

Clamping is useful for focusing on a subset of the data while ensuring that extreme values remain visible, but use caution: clamped values may need an annotation to avoid misinterpretation. Clamping typically requires setting an explicit **domain** since if the domain is inferred, no values will be outside the domain.

For continuous scales only.

`color_n` float \| [Param](reference/inspect_viz.html.md#param) \| None  
For a *quantile* scale, the number of quantiles (creates *n* - 1 thresholds); for a *quantize* scale, the approximate number of thresholds; defaults to 5.

`color_nice` bool \| float \| Interval \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, or a tick count or interval, extend the domain to nice round values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and nice time intervals for *utc* and *time* scales. Pass an interval such as *minute*, *wednesday* or *month* to specify what constitutes a nice interval.

For continuous scales only.

`color_scheme` [ColorScheme](reference/inspect_viz.plot.html.md#colorscheme) \| [Param](reference/inspect_viz.html.md#param) \| None  
If specified, shorthand for setting the **color_range** or **color_interpolate** option of a *color* scale.

`color_interpolate` [Interpolate](reference/inspect_viz.plot.html.md#interpolate) \| [Param](reference/inspect_viz.html.md#param) \| None  
How to interpolate color range values. For quantitative scales only. This attribute can be used to specify a color space for interpolating colors specified in the **color_range**.

`color_pivot` Any \| [Param](reference/inspect_viz.html.md#param) \| None  
For a diverging color scale, the input value (abstract value) that divides the domain into two parts; defaults to 0 for *diverging* scales, dividing the domain into negative and positive parts; defaults to 1 for *diverging-log* scales. By default, diverging scales are symmetric around the pivot; see the **symmetric** option.

`color_symmetric` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
For a diverging color scale, if true (the default), extend the domain to ensure that the lower part of the domain (below the **pivot**) is commensurate with the upper part of the domain (above the **pivot**).

A symmetric diverging color scale may not use all of its output **range**; this reduces contrast but ensures that deviations both below and above the **pivot** are represented proportionally. Otherwise if false, the full output **range** will be used; this increases contrast but values on opposite sides of the **pivot** may not be meaningfully compared.

`color_label` str \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

For axes and legends only.

`color_percent` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, shorthand for a transform suitable for percentages, mapping proportions in \[0, 1\] to \[0, 100\].

`color_reverse` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether to reverse the scale’s encoding; equivalent to reversing either the **domain** or **range**.

`color_zero` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether the **domain** must include zero. If the domain minimum is positive, it will be set to zero; otherwise if the domain maximum is negative, it will be set to zero.

For quantitative scales only.

`color_tick_format` str \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
How to format inputs (abstract values) for axis tick labels; one of:

- a [d3-format](https://d3js.org/d3-time) string for numeric scales
- a [d3-time-format](https://d3js.org/d3-time-format) string for temporal scales

`color_exponent` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A power scale’s exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a linear scale. For *pow* and *diverging-pow* scales only.

`color_base` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A log scale’s base; defaults to 10. Does not affect the scale’s encoding, but rather the default ticks. For *log* and *diverging-log* scales only.

`color_constant` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A symlog scale’s constant, expressing the magnitude of the linear region around the origin; defaults to 1. For *symlog* and *diverging-symlog* scales only.

`opacity_scale` [ContinuousScale](reference/inspect_viz.plot.html.md#continuousscale) \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
The *opacity* scale type, affecting how the scale encodes abstract data, say by applying a mathematical transformation. If null, the scale is disabled. The opacity scale defaults to *linear*; this scales is intended for quantitative data.

`opacity_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For continuous data (numbers and dates), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

Opacity scales have a default domain from 0 to the maximum value of associated channels.

`opacity_range` Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values).

Opacity scales have a default range of \[0, 1\].

`opacity_clamp` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, values below the domain minimum are treated as the domain minimum, and values above the domain maximum are treated as the domain maximum.

Clamping is useful for focusing on a subset of the data while ensuring that extreme values remain visible, but use caution: clamped values may need an annotation to avoid misinterpretation. Clamping typically requires setting an explicit **domain** since if the domain is inferred, no values will be outside the domain.

For continuous scales only.

`opacity_nice` bool \| float \| Interval \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, or a tick count or interval, extend the domain to nice round values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and nice time intervals for *utc* and *time* scales. Pass an interval such as *minute*, *wednesday* or *month* to specify what constitutes a nice interval.

For continuous scales only.

`opacity_label` str \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

For axes and legends only.

`opacity_percent` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, shorthand for a transform suitable for percentages, mapping proportions in \[0, 1\] to \[0, 100\].

`opacity_reverse` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether to reverse the scale’s encoding; equivalent to reversing either the **domain** or **range**.

`opacity_zero` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether the **domain** must include zero. If the domain minimum is positive, it will be set to zero; otherwise if the domain maximum is negative, it will be set to zero.

For quantitative scales only.

`opacity_tick_format` str \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
How to format inputs (abstract values) for axis tick labels; one of:

- a [d3-format](https://d3js.org/d3-time) string for numeric scales
- a [d3-time-format](https://d3js.org/d3-time-format) string for temporal scales

`opacity_exponent` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A power scale’s exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a linear scale. For *pow* scales only.

`opacity_base` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A log scale’s base; defaults to 10. Does not affect the scale’s encoding, but rather the default ticks. For *log* scales only.

`opacity_constant` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A symlog scale’s constant, expressing the magnitude of the linear region around the origin; defaults to 1. For *symlog* scales only.

`symbol_scale` Literal\['ordinal', 'categorical', 'threshold', 'quantile', 'quantize'\] \| None \| [Param](reference/inspect_viz.html.md#param)  
The *symbol* scale type, affecting how the scale encodes abstract data, say by applying a mathematical transformation. If null, the scale is disabled. Defaults to an *ordinal* scale type.

`symbol_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. As symbol scales are discrete, the domain is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

`symbol_range` Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**, and for position scales, the plot’s dimensions. For continuous data (numbers and dates), and for ordinal position scales (*point* and *band*), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For other ordinal data, such as for a *color* scale, it is an array (or iterable) of output values in the same order as the **domain**.

Symbol scales have a default range of categorical symbols; the choice of symbols depends on whether the associated dot mark is filled or stroked.

`r_scale` [ContinuousScale](reference/inspect_viz.plot.html.md#continuousscale) \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
The *r* (radius) scale type, affecting how the scale encodes abstract data, say by applying a mathematical transformation. If null, the scale is disabled. The radius scale defaults to *sqrt*; this scale is intended for quantitative data.

`r_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For continuous data (numbers and dates), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

Radius scales have a default domain from 0 to the median first quartile of associated channels.

`r_range` Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**, and for position scales, the plot’s dimensions. For continuous data (numbers and dates), and for ordinal position scales (*point* and *band*), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For other ordinal data, such as for a *color* scale, it is an array (or iterable) of output values in the same order as the **domain**.

Radius scales have a default range of \[0, 3\].

`r_clamp` Any \| None  
If true, values below the domain minimum are treated as the domain minimum, and values above the domain maximum are treated as the domain maximum.

Clamping is useful for focusing on a subset of the data while ensuring that extreme values remain visible, but use caution: clamped values may need an annotation to avoid misinterpretation. Clamping typically requires setting an explicit **domain** since if the domain is inferred, no values will be outside the domain.

For continuous scales only.

`r_nice` bool \| float \| Interval \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, or a tick count or interval, extend the domain to nice round values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and nice time intervals for *utc* and *time* scales. Pass an interval such as *minute*, *wednesday* or *month* to specify what constitutes a nice interval.

For continuous scales only.

`r_label` str \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.

`r_percent` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, shorthand for a transform suitable for percentages, mapping proportions in \[0, 1\] to \[0, 100\].

`r_zero` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether the **domain** must include zero. If the domain minimum is positive, it will be set to zero; otherwise if the domain maximum is negative, it will be set to zero.

For quantitative scales only.

`r_exponent` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A power scale’s exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a linear scale. For *pow* scales only.

`r_base` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A log scale’s base; defaults to 10. Does not affect the scale’s encoding, but rather the default ticks. For *log* scales only.

`r_constant` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A symlog scale’s constant, expressing the magnitude of the linear region around the origin; defaults to 1. For *symlog* scales only.

`length_scale` [ContinuousScale](reference/inspect_viz.plot.html.md#continuousscale) \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
The *length* scale type, affecting how the scale encodes abstract data, say by applying a mathematical transformation. If null, the scale is disabled. The length scale defaults to *linear*, as this scale is intended for quantitative data.

`length_domain` Literal\['fixed'\] \| Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s inputs (abstract values). By default inferred from channel values. For continuous data (numbers and dates), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For ordinal data (strings or booleans), it is an array (or iterable) of values is the desired order, defaulting to natural ascending order.

Linear scales have a default domain of \[0, 1\]. Log scales have a default domain of \[1, 10\] and cannot include zero. Radius scales have a default domain from 0 to the median first quartile of associated channels. Length have a default domain from 0 to the median median of associated channels. Opacity scales have a default domain from 0 to the maximum value of associated channels.

`length_range` Sequence\[str \| float \| bool\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The extent of the scale’s outputs (visual values). By default inferred from the scale’s **type** and **domain**, and for position scales, the plot’s dimensions. For continuous data (numbers and dates), and for ordinal position scales (*point* and *band*), it is typically \[*min*, *max*\]; it can be \[*max*, *min*\] to reverse the scale. For other ordinal data, such as for a *color* scale, it is an array (or iterable) of output values in the same order as the **domain**.

Length scales have a default range of \[0, 12\].

`length_clamp` Any \| None  
If true, values below the domain minimum are treated as the domain minimum, and values above the domain maximum are treated as the domain maximum.

Clamping is useful for focusing on a subset of the data while ensuring that extreme values remain visible, but use caution: clamped values may need an annotation to avoid misinterpretation. Clamping typically requires setting an explicit **domain** since if the domain is inferred, no values will be outside the domain.

For continuous scales only.

`length_nice` bool \| float \| Interval \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, or a tick count or interval, extend the domain to nice round values. Defaults to 1, 2 or 5 times a power of 10 for *linear* scales, and nice time intervals for *utc* and *time* scales. Pass an interval such as *minute*, *wednesday* or *month* to specify what constitutes a nice interval.

For continuous scales only.

`length_percent` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
If true, shorthand for a transform suitable for percentages, mapping proportions in \[0, 1\] to \[0, 100\].

`length_zero` bool \| [Param](reference/inspect_viz.html.md#param) \| None  
Whether the **domain** must include zero. If the domain minimum is positive, it will be set to zero; otherwise if the domain maximum is negative, it will be set to zero.

For quantitative scales only.

`length_exponent` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A power scale’s exponent (*e.g.*, 0.5 for sqrt); defaults to 1 for a linear scale. For *pow* scales only.

`length_base` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A log scale’s base; defaults to 10. Does not affect the scale’s encoding, but rather the default ticks. For *log* scales only.

`length_constant` float \| [Param](reference/inspect_viz.html.md#param) \| None  
A symlog scale’s constant, expressing the magnitude of the linear region around the origin; defaults to 1. For *symlog* scales only.

`projection_type` [Projection](reference/inspect_viz.plot.html.md#projection) \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
The desired projection; one of:

- a named built-in projection such as *albers-usa*
- null, for no projection

Named projections are scaled and translated to fit the **domain** to the plot’s frame (minus insets).

`projection_domain` object \| [Param](reference/inspect_viz.html.md#param) \| None  
A GeoJSON object to fit to the plot’s frame (minus insets); defaults to a Sphere for spherical projections (outline of the the whole globe).

`projection_rotate` Sequence\[float \| [Param](reference/inspect_viz.html.md#param)\] \| [Param](reference/inspect_viz.html.md#param) \| None  
A rotation of the sphere before projection; defaults to \[0, 0, 0\]. Specified as Euler angles λ (yaw, or reference longitude), φ (pitch, or reference latitude), and optionally γ (roll), in degrees.

`projection_parallels` Sequence\[float \| [Param](reference/inspect_viz.html.md#param)\] \| [Param](reference/inspect_viz.html.md#param) \| None  
The [standard parallels](https://d3js.org/d3-geo/conic#conic_parallels). For conic projections only.

`projection_precision` float \| [Param](reference/inspect_viz.html.md#param) \| None  
The projection’s [sampling threshold](https://d3js.org/d3-geo/projection#projection_precision).

`projection_clip` bool \| float \| Literal\['frame'\] \| None \| [Param](reference/inspect_viz.html.md#param) \| None  
The projection’s clipping method; one of:

- *frame* or true (default) - clip to the plot’s frame (including margins but not insets)
- a number - clip to a circle of the given radius in degrees centered around the origin
- null or false - do not clip

Some projections (such as [*armadillo*](https://observablehq.com/@d3/armadillo) and [*berghaus*](https://observablehq.com/@d3/berghaus-star)) require spherical clipping: in that case set the marks’ **clip** option to *sphere*.

`projection_inset` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Shorthand to set the same default for all four projection insets. All insets typically default to zero, though not always. A positive inset reduces effective area, while a negative inset increases it.

`projection_inset_top` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Insets the top edge of the projection by the specified number of pixels. A positive value insets towards the bottom edge (reducing effective area), while a negative value insets away from the bottom edge (increasing it).

`projection_inset_right` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Insets the right edge of the projection by the specified number of pixels. A positive value insets towards the left edge (reducing effective area), while a negative value insets away from the left edge (increasing it).

`projection_inset_bottom` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Insets the bottom edge of the projection by the specified number of pixels. A positive value insets towards the top edge (reducing effective area), while a negative value insets away from the top edge (increasing it).

`projection_inset_left` float \| [Param](reference/inspect_viz.html.md#param) \| None  
Insets the left edge of the projection by the specified number of pixels. A positive value insets towards the right edge (reducing effective area), while a negative value insets away from the right edge (increasing it).

## Implementation

The [Scores by Task](examples/inspect/scores-by-task/index.html.md) example demonstrates how this view was implemented using lower level plotting components.
