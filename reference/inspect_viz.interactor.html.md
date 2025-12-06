# inspect_viz.interactor


## Selection

### interval_x

Select a continuous 1D interval selection over the `x` scale domain.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L56)

``` python
def interval_x(
    target: Selection,
    field: str | None = None,
    pixel_size: float | None = None,
    peers: bool | None = None,
    brush: Brush | None = None,
) -> Interactor
```

`target` [Selection](inspect_viz.qmd#selection)  
The target selection. A clause of the form `field BETWEEN lo AND hi` is
added for the currently selected interval \[lo, hi\].

`field` str \| None  
The name of the field (database column) over which the interval
selection should be defined. If unspecified, the channel field of the
first valid prior mark definition is used.

`pixel_size` float \| None  
The size of an interative pixel (default `1`). Larger pixel sizes reduce
the brush resolution, which can reduce the size of pre-aggregated
materialized views.

`peers` bool \| None  
A flag indicating if peer (sibling) marks are excluded when
cross-filtering (default `true`). If set, peer marks will not be
filtered by this interactor’s selection in cross-filtering setups.

`brush` [Brush](inspect_viz.interactor.qmd#brush) \| None  
CSS styles for the brush (SVG `rect`) element.

### interval_y

Select a continuous 1D interval selection over the `y` scale domain.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L123)

``` python
def interval_y(
    target: Selection,
    field: str | None = None,
    pixel_size: float | None = None,
    peers: bool | None = None,
    brush: Brush | None = None,
) -> Interactor
```

`target` [Selection](inspect_viz.qmd#selection)  
The target selection. A clause of the form `field BETWEEN lo AND hi` is
added for the currently selected interval \[lo, hi\].

`field` str \| None  
The name of the field (database column) over which the interval
selection should be defined. If unspecified, the channel field of the
first valid prior mark definition is used.

`pixel_size` float \| None  
The size of an interative pixel (default `1`). Larger pixel sizes reduce
the brush resolution, which can reduce the size of pre-aggregated
materialized views.

`peers` bool \| None  
A flag indicating if peer (sibling) marks are excluded when
cross-filtering (default `true`). If set, peer marks will not be
filtered by this interactor’s selection in cross-filtering setups.

`brush` [Brush](inspect_viz.interactor.qmd#brush) \| None  
CSS styles for the brush (SVG `rect`) element.

### interval_xy

Select a continuous 2D interval selection over the `x` and `y` scale
domains.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L91)

``` python
def interval_xy(
    target: Selection,
    xfield: str | None = None,
    yfield: str | None = None,
    pixel_size: float | None = None,
    peers: bool | None = None,
    brush: Brush | None = None,
) -> Interactor
```

`target` [Selection](inspect_viz.qmd#selection)  
The target selection. A clause of the form
`(xfield BETWEEN x1 AND x2) AND (yfield BETWEEN y1 AND y2)` is added for
the currently selected intervals.

`xfield` str \| None  
The name of the field (database column) over which the `x`-component of
the interval selection should be defined. If unspecified, the `x`
channel field of the first valid prior mark definition is used.

`yfield` str \| None  
The name of the field (database column) over which the `y`-component of
the interval selection should be defined. If unspecified, the `y`
channel field of the first valid prior mark definition is used.

`pixel_size` float \| None  
The size of an interative pixel (default `1`). Larger pixel sizes reduce
the brush resolution, which can reduce the size of pre-aggregated
materialized views.

`peers` bool \| None  
A flag indicating if peer (sibling) marks are excluded when
cross-filtering (default `true`). If set, peer marks will not be
filtered by this interactor’s selection in cross-filtering setups.

`brush` [Brush](inspect_viz.interactor.qmd#brush) \| None  
CSS styles for the brush (SVG `rect`) element.

### nearest_x

Select values from the mark closest to the pointer *x* location.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L227)

``` python
def nearest_x(
    target: Selection,
    channels: list[str] | None = None,
    fields: list[str] | None = None,
    max_radius: float | None = None,
) -> Interactor
```

`target` [Selection](inspect_viz.qmd#selection)  
The target selection. A clause of the form `field = value` is added for
the currently nearest value.

`channels` list\[str\] \| None  
The encoding channels whose domain values should be selected. For
example, a setting of `['color']` selects the data value backing the
color channel, whereas `['x', 'z']` selects both x and z channel domain
values. If unspecified, the selected channels default to match the
current pointer settings: a `nearestX` interactor selects the `['x']`
channels, while a `nearest` interactor selects the `['x', 'y']`
channels.

`fields` list\[str\] \| None  
The fields (database column names) to use in generated selection clause
predicates. If unspecified, the fields backing the selected *channels*
in the first valid prior mark definition are used by default.

`max_radius` float \| None  
The maximum radius of a nearest selection (default 40). Marks with
(x, y) coordinates outside this radius will not be selected as nearest
points.

### nearest_y

Select values from the mark closest to the pointer *y* location.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L253)

``` python
def nearest_y(
    target: Selection,
    channels: list[str] | None = None,
    fields: list[str] | None = None,
    max_radius: float | None = None,
) -> Interactor
```

`target` [Selection](inspect_viz.qmd#selection)  
The target selection. A clause of the form `field = value` is added for
the currently nearest value.

`channels` list\[str\] \| None  
The encoding channels whose domain values should be selected. For
example, a setting of `['color']` selects the data value backing the
color channel, whereas `['x', 'z']` selects both x and z channel domain
values. If unspecified, the selected channels default to match the
current pointer settings: a `nearestX` interactor selects the `['x']`
channels, while a `nearest` interactor selects the `['x', 'y']`
channels.

`fields` list\[str\] \| None  
The fields (database column names) to use in generated selection clause
predicates. If unspecified, the fields backing the selected *channels*
in the first valid prior mark definition are used by default.

`max_radius` float \| None  
The maximum radius of a nearest selection (default 40). Marks with
(x, y) coordinates outside this radius will not be selected as nearest
points.

### toggle

Select individal values.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L158)

``` python
def toggle(
    target: Selection,
    channels: list[str],
    peers: bool | None = None,
) -> Interactor
```

`target` [Selection](inspect_viz.qmd#selection)  
The target selection. A clause of the form
`(field = value1) OR (field = value2) ...` is added for the currently
selected values.

`channels` list\[str\]  
The encoding channels over which to select values. For a selected mark,
selection clauses will cover the backing data fields for each channel.

`peers` bool \| None  
A flag indicating if peer (sibling) marks are excluded when
cross-filtering (default `true`). If set, peer marks will not be
filtered by this interactor’s selection in cross-filtering setups.

### toggle_x

Select individal values in the `x` scale domain. Clicking or touching a
mark toggles its selection status.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L183)

``` python
def toggle_x(
    target: Selection,
    peers: bool | None = None,
) -> Interactor
```

`target` [Selection](inspect_viz.qmd#selection)  
The target selection. A clause of the form
`(field = value1) OR (field = value2) ...` is added for the currently
selected values.

`peers` bool \| None  
A flag indicating if peer (sibling) marks are excluded when
cross-filtering (default `true`). If set, peer marks will not be
filtered by this interactor’s selection in cross-filtering setups.

### toggle_y

Toggle interactor over the `"y"` encoding channel only.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L307)

``` python
def toggle_y(
    target: Selection,
    peers: bool | None = None,
) -> Interactor
```

`target` [Selection](inspect_viz.qmd#selection)  
The target selection. A clause of the form
`(field = value1) OR (field = value2) ...` is added for the currently
selected values.

`peers` bool \| None  
A flag indicating if peer (sibling) marks are excluded when
cross-filtering (default `true`). If set, peer marks will not be
filtered by this interactor’s selection in cross-filtering setups.

### toggle_color

Select individal values in the `color` scale domain. Clicking or
touching a mark toggles its selection status.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L205)

``` python
def toggle_color(
    target: Selection,
    peers: bool | None = None,
) -> Interactor
```

`target` [Selection](inspect_viz.qmd#selection)  
The target selection. A clause of the form
`(field = value1) OR (field = value2) ...` is added for the currently
selected values.

`peers` bool \| None  
A flag indicating if peer (sibling) marks are excluded when
cross-filtering (default `true`). If set, peer marks will not be
filtered by this interactor’s selection in cross-filtering setups.

### region

Select aspects of individual marks within a 2D range.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L279)

``` python
def region(
    target: Selection,
    channels: list[str],
    peers: bool | None = None,
    brush: Brush | None = None,
) -> Interactor
```

`target` [Selection](inspect_viz.qmd#selection)  
The target selection. A clause of the form
`(field = value1) OR (field = value2) ...` is added for the currently
selected values.

`channels` list\[str\]  
The encoding channels over which to select values (e.g. “x”, “y”,
“color”, etc.). For a selected mark, selection clauses will cover the
backing data fields for each channel.

`peers` bool \| None  
A flag indicating if peer (sibling) marks are excluded when
cross-filtering (default `true`). If set, peer marks will not be
filtered by this interactor’s selection in cross-filtering setups.

`brush` [Brush](inspect_viz.interactor.qmd#brush) \| None  
CSS styles for the brush (SVG `rect`) element.

### highlight

Highlight individual visualized data points based on a `Selection`.

Selected values keep their normal appearance. Unselected values are
deemphasized.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L17)

``` python
def highlight(
    by: Selection,
    opacity: float | None = None,
    fill_opacity: float | None = None,
    stroke_opacity: float | None = None,
    fill: str | None = None,
    stroke: str | None = None,
) -> Interactor
```

`by` [Selection](inspect_viz.qmd#selection)  
The input selection. Unselected marks are deemphasized.

`opacity` float \| None  
The overall opacity of deemphasized marks. By default the opacity is set
to 0.2.

`fill_opacity` float \| None  
The fill opacity of deemphasized marks. By default the fill opacity is
unchanged.

`stroke_opacity` float \| None  
The stroke opacity of deemphasized marks. By default the stroke opacity
is unchanged.

`fill` str \| None  
The fill color of deemphasized marks. By default the fill is unchanged.

`stroke` str \| None  
The stroke color of deemphasized marks. By default the stroke is
unchanged.

## Navigation

### pan

Pan a plot along both the `x` and `y` scales.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L328)

``` python
def pan(
    x: Selection | None = None,
    y: Selection | None = None,
    xfield: str | None = None,
    yfield: str | None = None,
) -> Interactor
```

`x` [Selection](inspect_viz.qmd#selection) \| None  
The output selection for the `x` domain. A clause of the form
`field BETWEEN x1 AND x2` is added for the current pan/zom interval
\[x1, x2\].

`y` [Selection](inspect_viz.qmd#selection) \| None  
The output selection for the `y` domain. A clause of the form
`field BETWEEN y1 AND y2` is added for the current pan/zom interval
\[y1, y2\].

`xfield` str \| None  
The name of the field (database column) over which the `x`-component of
the pan/zoom interval should be defined. If unspecified, the `x` channel
field of the first valid prior mark definition is used.

`yfield` str \| None  
The name of the field (database column) over which the `y`-component of
the pan/zoom interval should be defined. If unspecified, the `y` channel
field of the first valid prior mark definition is used.

### pan_x

Pan a plot along the `x` scale only.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L353)

``` python
def pan_x(
    x: Selection | None = None,
    y: Selection | None = None,
    xfield: str | None = None,
    yfield: str | None = None,
) -> Interactor
```

`x` [Selection](inspect_viz.qmd#selection) \| None  
The output selection for the `x` domain. A clause of the form
`field BETWEEN x1 AND x2` is added for the current pan/zom interval
\[x1, x2\].

`y` [Selection](inspect_viz.qmd#selection) \| None  
The output selection for the `y` domain. A clause of the form
`field BETWEEN y1 AND y2` is added for the current pan/zom interval
\[y1, y2\].

`xfield` str \| None  
The name of the field (database column) over which the `x`-component of
the pan/zoom interval should be defined. If unspecified, the `x` channel
field of the first valid prior mark definition is used.

`yfield` str \| None  
The name of the field (database column) over which the `y`-component of
the pan/zoom interval should be defined. If unspecified, the `y` channel
field of the first valid prior mark definition is used.

### pan_y

Pan a plot along the `y` scale only.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L378)

``` python
def pan_y(
    x: Selection | None = None,
    y: Selection | None = None,
    xfield: str | None = None,
    yfield: str | None = None,
) -> Interactor
```

`x` [Selection](inspect_viz.qmd#selection) \| None  
The output selection for the `x` domain. A clause of the form
`field BETWEEN x1 AND x2` is added for the current pan/zom interval
\[x1, x2\].

`y` [Selection](inspect_viz.qmd#selection) \| None  
The output selection for the `y` domain. A clause of the form
`field BETWEEN y1 AND y2` is added for the current pan/zom interval
\[y1, y2\].

`xfield` str \| None  
The name of the field (database column) over which the `x`-component of
the pan/zoom interval should be defined. If unspecified, the `x` channel
field of the first valid prior mark definition is used.

`yfield` str \| None  
The name of the field (database column) over which the `y`-component of
the pan/zoom interval should be defined. If unspecified, the `y` channel
field of the first valid prior mark definition is used.

### pan_zoom

Pan and zoom a plot along both the `x` and `y` scales.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L403)

``` python
def pan_zoom(
    x: Selection | None = None,
    y: Selection | None = None,
    xfield: str | None = None,
    yfield: str | None = None,
) -> Interactor
```

`x` [Selection](inspect_viz.qmd#selection) \| None  
The output selection for the `x` domain. A clause of the form
`field BETWEEN x1 AND x2` is added for the current pan/zom interval
\[x1, x2\].

`y` [Selection](inspect_viz.qmd#selection) \| None  
The output selection for the `y` domain. A clause of the form
`field BETWEEN y1 AND y2` is added for the current pan/zom interval
\[y1, y2\].

`xfield` str \| None  
The name of the field (database column) over which the `x`-component of
the pan/zoom interval should be defined. If unspecified, the `x` channel
field of the first valid prior mark definition is used.

`yfield` str \| None  
The name of the field (database column) over which the `y`-component of
the pan/zoom interval should be defined. If unspecified, the `y` channel
field of the first valid prior mark definition is used.

### pan_zoom_x

Pan and zoom a plot along the `x` scale only.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L428)

``` python
def pan_zoom_x(
    x: Selection | None = None,
    y: Selection | None = None,
    xfield: str | None = None,
    yfield: str | None = None,
) -> Interactor
```

`x` [Selection](inspect_viz.qmd#selection) \| None  
The output selection for the `x` domain. A clause of the form
`field BETWEEN x1 AND x2` is added for the current pan/zom interval
\[x1, x2\].

`y` [Selection](inspect_viz.qmd#selection) \| None  
The output selection for the `y` domain. A clause of the form
`field BETWEEN y1 AND y2` is added for the current pan/zom interval
\[y1, y2\].

`xfield` str \| None  
The name of the field (database column) over which the `x`-component of
the pan/zoom interval should be defined. If unspecified, the `x` channel
field of the first valid prior mark definition is used.

`yfield` str \| None  
The name of the field (database column) over which the `y`-component of
the pan/zoom interval should be defined. If unspecified, the `y` channel
field of the first valid prior mark definition is used.

### pan_zoom_y

Pan and zoom a plot along the `y` scale only.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L453)

``` python
def pan_zoom_y(
    x: Selection | None = None,
    y: Selection | None = None,
    xfield: str | None = None,
    yfield: str | None = None,
) -> Interactor
```

`x` [Selection](inspect_viz.qmd#selection) \| None  
The output selection for the `x` domain. A clause of the form
`field BETWEEN x1 AND x2` is added for the current pan/zom interval
\[x1, x2\].

`y` [Selection](inspect_viz.qmd#selection) \| None  
The output selection for the `y` domain. A clause of the form
`field BETWEEN y1 AND y2` is added for the current pan/zom interval
\[y1, y2\].

`xfield` str \| None  
The name of the field (database column) over which the `x`-component of
the pan/zoom interval should be defined. If unspecified, the `x` channel
field of the first valid prior mark definition is used.

`yfield` str \| None  
The name of the field (database column) over which the `y`-component of
the pan/zoom interval should be defined. If unspecified, the `y` channel
field of the first valid prior mark definition is used.

## Types

### Interactor

Interactors imbue plots with interactive behavior, such as selecting or
highlighting values, and panning or zooming the display.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_interactors.py#L9)

``` python
class Interactor(Component)
```

### Brush

Brush options.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/interactor/_brush.py#L6)

``` python
class Brush(TypedDict, total=False)
```

#### Attributes

`fill` str  
The fill color of the brush rectangle.

`fill_opacity` float  
The fill opacity of the brush rectangle.

`opacity` float  
The overall opacity of the brush rectangle.

`stroke` str  
The stroke color of the brush rectangle.

`stroke_dasharray` str  
The stroke dash array of the brush rectangle.

`stroke_opacity` float  
The stroke opacity of the brush rectangle.
