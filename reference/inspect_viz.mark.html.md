# inspect_viz.mark


## Basic

### dot

A dot mark that draws circles, or other symbols, as in a scatterplot.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_dot.py#L15)

``` python
def dot(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    z: Channel | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    filter_by: Selection | None = None,
    rotate: Channel | float | Param | None = None,
    symbol: ChannelSpec | Param | Symbol | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
Horizontal position channel specifying the dot’s center.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel specifying the dot’s center.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series.

`r` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The radius of dots; either a channel or constant. When a number, it is
interpreted as a constant radius in pixels. Otherwise it is interpreted
as a channel, typically bound to the *r* channel, which defaults to the
*sqrt* type for proportional symbols. The radius defaults to 4.5 pixels
when using the **symbol** channel, and otherwise 3 pixels. Dots with a
nonpositive radius are not drawn.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`rotate` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle of dots in degrees clockwise; either a channel or a
constant. When a number, it is interpreted as a constant; otherwise it
is interpreted as a channel. Defaults to 0°, pointing up.

`symbol` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| [Symbol](inspect_viz.mark.qmd#symbol) \| None  
Categorical column to bind symbols to or CSS color string.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor specifies defaults for **x** and **y** based on the
plot’s frame; it may be one of the four sides (*top*, *right*, *bottom*,
*left*), one of the four corners (*top-left*, *top-right*,
*bottom-right*, *bottom-left*), or the *middle* of the frame.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### dot_x

A horizontal dot mark that draws circles, or other symbols.

Like dot, except that **y** defaults to the identity function, assuming
that *data* = \[*y₀*, *y₁*, *y₂*, …\].

If an **interval** is specified, such as *day*, **y** is transformed to
the middle of the interval.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_dot.py#L62)

``` python
def dot_x(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelIntervalSpec | None = None,
    z: Channel | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    interval: Interval | None = None,
    filter_by: Selection | None = None,
    rotate: Channel | float | Param | None = None,
    symbol: ChannelSpec | Param | Symbol | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel specifying the dot’s center.

`y` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| None  
The vertical position of the dot’s center,typically bound to the *y*
scale.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series.

`r` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The radius of dots; either a channel or constant. When a number, it is
interpreted as a constant radius in pixels. Otherwise it is interpreted
as a channel, typically bound to the *r* channel, which defaults to the
*sqrt* type for proportional symbols. The radius defaults to 4.5 pixels
when using the **symbol** channel, and otherwise 3 pixels. Dots with a
nonpositive radius are not drawn.

`interval` Interval \| None  
An interval (such as *day* or a number), to transform **y** values to
the middle of the interval.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`rotate` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle of dots in degrees clockwise; either a channel or a
constant. When a number, it is interpreted as a constant; otherwise it
is interpreted as a channel. Defaults to 0°, pointing up.

`symbol` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| [Symbol](inspect_viz.mark.qmd#symbol) \| None  
Categorical column to bind symbols to or CSS color string.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor specifies defaults for **x** and **y** based on the
plot’s frame; it may be one of the four sides (*top*, *right*, *bottom*,
*left*), one of the four corners (*top-left*, *top-right*,
*bottom-right*, *bottom-left*), or the *middle* of the frame.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### dot_y

A vertical dot mark that draws circles, or other symbols.

Like dot, except that **x** defaults to the identity function, assuming
that *data* = \[*x₀*, *x₁*, *x₂*, …\].

If an **interval** is specified, such as *day*, **x** is transformed to
the middle of the interval.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_dot.py#L117)

``` python
def dot_y(
    data: Data,
    y: ChannelSpec | Param,
    x: ChannelIntervalSpec | None = None,
    z: Channel | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    interval: Interval | None = None,
    filter_by: Selection | None = None,
    rotate: Channel | float | Param | None = None,
    symbol: ChannelSpec | Param | Symbol | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel specifying the dot’s center.

`x` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| None  
The horizontal position of the dot’s center, typically bound to the *x*
scale.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series.

`r` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The radius of dots; either a channel or constant. When a number, it is
interpreted as a constant radius in pixels. Otherwise it is interpreted
as a channel, typically bound to the *r* channel, which defaults to the
*sqrt* type for proportional symbols. The radius defaults to 4.5 pixels
when using the **symbol** channel, and otherwise 3 pixels. Dots with a
nonpositive radius are not drawn.

`interval` Interval \| None  
An interval (such as *day* or a number), to transform **x** values to
the middle of the interval.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`rotate` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle of dots in degrees clockwise; either a channel or a
constant. When a number, it is interpreted as a constant; otherwise it
is interpreted as a channel. Defaults to 0°, pointing up.

`symbol` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| [Symbol](inspect_viz.mark.qmd#symbol) \| None  
Categorical column to bind symbols to or CSS color string.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor specifies defaults for **x** and **y** based on the
plot’s frame; it may be one of the four sides (*top*, *right*, *bottom*,
*left*), one of the four corners (*top-left*, *top-right*,
*bottom-right*, *bottom-left*), or the *middle* of the frame.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### circle

A circle mark that draws circles as in a scatterplot.

Like dot, but with the symbol fixed to be a circle.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_dot.py#L172)

``` python
def circle(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    z: ChannelSpec | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    filter_by: Selection | None = None,
    rotate: ChannelSpec | float | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
Horizontal position channel specifying the circle’s center.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel specifying the circle’s center.

`z` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series.

`r` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The radius of circles; either a channel or constant. When a number, it
is interpreted as a constant radius in pixels. Otherwise it is
interpreted as a channel, typically bound to the *r* channel, which
defaults to the *sqrt* type for proportional symbols. The radius
defaults to 3 pixels. Circles with a nonpositive radius are not drawn.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`rotate` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle of circles in degrees clockwise; either a channel or
a constant. When a number, it is interpreted as a constant; otherwise it
is interpreted as a channel. Defaults to 0°, pointing up.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor specifies defaults for **x** and **y** based on the
plot’s frame; it may be one of the four sides (*top*, *right*, *bottom*,
*left*), one of the four corners (*top-left*, *top-right*,
*bottom-right*, *bottom-left*), or the *middle* of the frame.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### hexagon

A hexagon mark that draws hexagons as in a scatterplot.

Like dot, but with the symbol fixed to be a hexagon.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_dot.py#L218)

``` python
def hexagon(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    z: ChannelSpec | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    filter_by: Selection | None = None,
    rotate: ChannelSpec | float | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
Horizontal position channel specifying the hexagon’s center.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel specifying the hexagon’s center.

`z` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series.

`r` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The radius of hexagons; either a channel or constant. When a number, it
is interpreted as a constant radius in pixels. Otherwise it is
interpreted as a channel, typically bound to the *r* channel, which
defaults to the *sqrt* type for proportional symbols. The radius
defaults to 4.5 pixels. Hexagons with a nonpositive radius are not
drawn.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`rotate` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle of hexagons in degrees clockwise; either a channel or
a constant. When a number, it is interpreted as a constant; otherwise it
is interpreted as a channel. Defaults to 0°, pointing up.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor specifies defaults for **x** and **y** based on the
plot’s frame; it may be one of the four sides (*top*, *right*, *bottom*,
*left*), one of the four corners (*top-left*, *top-right*,
*bottom-right*, *bottom-left*), or the *middle* of the frame.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### line

A line mark that connects control points.

Points along the line are connected in input order. If there are
multiple series via the **z**, **fill**, or **stroke** channel, series
are drawn in input order such that the last series is drawn on top.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_line.py#L15)

``` python
def line(
    data: Data | None = None,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data) \| None  
The data source for the mark. If None, x and y must be provided as
sequences.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The required horizontal position channel, typically bound to the *x*
scale. When data is None, must be a sequence of x-coordinates.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The required vertical position channel, typically bound to the *y*
scale. When data is None, must be a sequence of y-coordinates.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series. When data is
None, can be a sequence of z-values.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for marker_start, marker_mid, and
marker_end.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the starting point of a line segment.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for any middle (interior) points of a line segment.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the ending point of a line segment.

`curve` [Curve](inspect_viz.mark.qmd#curve) \| [Param](inspect_viz.qmd#param) \| None  
The curve (interpolation) method for connecting adjacent points.

`tension` float \| [Param](inspect_viz.qmd#param) \| None  
The tension option for bundle, cardinal and Catmull-Rom splines.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### line_x

A horizontal line mark that connects control points.

Like line, except that **y** defaults to the zero-based index of the
data \[0, 1, 2, …\].

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_line.py#L67)

``` python
def line_x(
    data: Data | None = None,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data) \| None  
The data source for the mark. If None, x must be provided as a sequence.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The required horizontal position channel, typically bound to the *x*
scale. When data is None, must be a sequence of x-coordinates.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale;
defaults to the zero-based index of the data \[0, 1, 2, …\].

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series. When data is
None, can be a sequence of z-values.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for marker_start, marker_mid, and
marker_end.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the starting point of a line segment.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for any middle (interior) points of a line segment.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the ending point of a line segment.

`curve` [Curve](inspect_viz.mark.qmd#curve) \| [Param](inspect_viz.qmd#param) \| None  
The curve (interpolation) method for connecting adjacent points.

`tension` float \| [Param](inspect_viz.qmd#param) \| None  
The tension option for bundle, cardinal and Catmull-Rom splines.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### line_y

A vertical line mark that connects control points.

Like line, except that **x** defaults to the zero-based index of the
data \[0, 1, 2, …\].

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_line.py#L119)

``` python
def line_y(
    data: Data | None = None,
    y: ChannelSpec | Param | None = None,
    x: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data) \| None  
The data source for the mark. If None, y must be provided as a sequence.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The required vertical position channel, typically bound to the *y*
scale. When data is None, must be a sequence of y-coordinates.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale;
defaults to the zero-based index of the data \[0, 1, 2, …\].

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series. When data is
None, can be a sequence of z-values.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for marker_start, marker_mid, and
marker_end.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the starting point of a line segment.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for any middle (interior) points of a line segment.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the ending point of a line segment.

`curve` [Curve](inspect_viz.mark.qmd#curve) \| [Param](inspect_viz.qmd#param) \| None  
The curve (interpolation) method for connecting adjacent points.

`tension` float \| [Param](inspect_viz.qmd#param) \| None  
The tension option for bundle, cardinal and Catmull-Rom splines.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### area

An area mark defined by a baseline (*x1*, *y1*) and a topline (*x2*,
*y2*).

The **x1** and **y1** channels specify the area’s baseline; the **x2**
and **y2** channels specify the area’s topline. Both the baseline and
topline are typically bound to the same scales as their respective
dimensions.

If **x2** is not specified, it defaults to **x1**. If **y2** is not
specified, it defaults to **y1**. Typically either **x2** or **y2** is
unspecified, creating either a horizontal or vertical area.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_area.py#L14)

``` python
def area(
    data: Data,
    x1: ChannelSpec | Param,
    y1: ChannelSpec | Param,
    x2: ChannelSpec | Param | None = None,
    y2: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    curve: Curve | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The required primary (starting, often left) horizontal position channel,
representing the area’s baseline, typically bound to the *x* scale.

`y1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The required primary (starting, often bottom) vertical position channel,
representing the area’s baseline, typically bound to the *y* scale.

`x2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The optional secondary (ending, often right) horizontal position
channel, representing the area’s topline, typically bound to the *x*
scale; if not specified, **x1** is used.

`y2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The optional secondary (ending, often top) vertical position channel,
representing the area’s topline, typically bound to the *y* scale; if
not specified, **y1** is used.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into (possibly stacked)
series to be drawn as separate areas; defaults to **fill** if a channel,
or **stroke** if a channel.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`offset` Literal\['center', 'normalize', 'wiggle'\] \| [Param](inspect_viz.qmd#param) \| None  
After stacking, an optional **offset** can be applied to translate and
scale stacks, say to produce a streamgraph; defaults to null for a zero
baseline (**y** = 0 for stackY, and **x** = 0 for stackX). If the
*wiggle* offset is used, the default **order** changes to *inside-out*.

`order` Literal\['value', 'x', 'y', 'z', 'sum', 'appearance', 'inside-out'\] \| str \| Sequence\[float \| bool\] \| [Param](inspect_viz.qmd#param) \| None  
The order in which stacks are layered; one of: - null (default) for
input order - a named stack order method such as *inside-out* or *sum* -
a field name, for natural order of the corresponding values - a function
of data, for natural order of the corresponding values - an array of
explicit **z** values in the desired order

If the *wiggle* **offset** is used, as for a streamgraph, the default
changes to *inside-out*.

`curve` [Curve](inspect_viz.mark.qmd#curve) \| [Param](inspect_viz.qmd#param) \| None  
The curve (interpolation) method for connecting adjacent points.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### area_x

A horizontal area mark.

The **x** channel specifies the area’s length (or width); it is
typically bound to the *x* scale. The **y** channel specifies the area’s
vertical position; it is typically bound to the *y* scale and defaults
to the zero-based index of the data \[0, 1, 2, …\].

If neither **x1** nor **x2** is specified, an implicit stackX transform
is applied and **x** defaults to the identity function, assuming that
*data* = \[*x₀*, *x₁*, *x₂*, …\]. Otherwise, if only one of **x1** or
**x2** is specified, the other defaults to **x**, which defaults to
zero.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_area.py#L74)

``` python
def area_x(
    data: Data,
    x: ChannelSpec | Param,
    x1: ChannelSpec | Param | None = None,
    x2: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    curve: Curve | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position (or length) channel, typically bound to the *x*
scale. If neither **x1** nor **x2** is specified, an implicit stackX
transform is applied and **x** defaults to the identity function,
assuming that *data* = \[*x₀*, *x₁*, *x₂*, …\]. Otherwise, if only one
of **x1** or **x2** is specified, the other defaults to **x**, which
defaults to zero.

`x1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The required primary (starting, often left) horizontal position channel,
representing the area’s baseline, typically bound to the *x* scale. For
areaX, setting this option disables the implicit stackX transform.

`x2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The optional secondary (ending, often right) horizontal position
channel, representing the area’s topline, typically bound to the *x*
scale; if not specified, **x1** is used. For areaX, setting this option
disables the implicit stackX transform.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale;
defaults to the zero-based index of the data \[0, 1, 2, …\].

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into (possibly stacked)
series to be drawn as separate areas; defaults to **fill** if a channel,
or **stroke** if a channel.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`offset` Literal\['center', 'normalize', 'wiggle'\] \| [Param](inspect_viz.qmd#param) \| None  
After stacking, an optional **offset** can be applied to translate and
scale stacks, say to produce a streamgraph; defaults to null for a zero
baseline (**y** = 0 for stackY, and **x** = 0 for stackX). If the
*wiggle* offset is used, the default **order** changes to *inside-out*.

`order` Literal\['value', 'x', 'y', 'z', 'sum', 'appearance', 'inside-out'\] \| str \| Sequence\[float \| bool\] \| [Param](inspect_viz.qmd#param) \| None  
The order in which stacks are layered; one of:

- null (default) for input order
- a named stack order method such as *inside-out* or *sum*
- a field name, for natural order of the corresponding values
- a function of data, for natural order of the corresponding values
- an array of explicit **z** values in the desired order

If the *wiggle* **offset** is used, as for a streamgraph, the default
changes to *inside-out*.

`curve` [Curve](inspect_viz.mark.qmd#curve) \| [Param](inspect_viz.qmd#param) \| None  
The curve (interpolation) method for connecting adjacent points.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### area_y

A vertical area mark.

The **y** channel specifies the area’s height (or length); it is
typically bound to the *y* scale. The **x** channel specifies the area’s
horizontal position; it is typically bound to the *x* scale and defaults
to the zero-based index of the data \[0, 1, 2, …\].

If neither **y1** nor **y2** is specified, an implicit stackY transform
is applied and **y** defaults to the identity function, assuming that
*data* = \[*y₀*, *y₁*, *y₂*, …\]. Otherwise, if only one of **y1** or
**y2** is specified, the other defaults to **y**, which defaults to
zero.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_area.py#L135)

``` python
def area_y(
    data: Data,
    y: ChannelSpec | Param,
    y1: ChannelSpec | Param | None = None,
    y2: ChannelSpec | Param | None = None,
    x: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    curve: Curve | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position (or length) channel, typically bound to the *y*
scale. If neither **y1** nor **y2** is specified, an implicit stackY
transform is applied and **y** defaults to the identity function,
assuming that *data* = \[*y₀*, *y₁*, *y₂*, …\]. Otherwise, if only one
of **y1** or **y2** is specified, the other defaults to **y**, which
defaults to zero.

`y1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The required primary (starting, often bottom) vertical position channel,
representing the area’s baseline, typically bound to the *y* scale. For
areaY, setting this option disables the implicit stackY transform.

`y2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The optional secondary (ending, often top) vertical position channel,
representing the area’s topline, typically bound to the *y* scale; if
not specified, **y1** is used. For areaY, setting this option disables
the implicit stackY transform.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale;
defaults to the zero-based index of the data \[0, 1, 2, …\].

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into (possibly stacked)
series to be drawn as separate areas; defaults to **fill** if a channel,
or **stroke** if a channel.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`offset` Literal\['center', 'normalize', 'wiggle'\] \| [Param](inspect_viz.qmd#param) \| None  
After stacking, an optional **offset** can be applied to translate and
scale stacks, say to produce a streamgraph; defaults to null for a zero
baseline (**y** = 0 for stackY, and **x** = 0 for stackX). If the
*wiggle* offset is used, the default **order** changes to *inside-out*.

`order` Literal\['value', 'x', 'y', 'z', 'sum', 'appearance', 'inside-out'\] \| str \| Sequence\[float \| bool\] \| [Param](inspect_viz.qmd#param) \| None  
The order in which stacks are layered; one of:

- null (default) for input order
- a named stack order method such as *inside-out* or *sum*
- a field name, for natural order of the corresponding values
- a function of data, for natural order of the corresponding values
- an array of explicit **z** values in the desired order

If the *wiggle* **offset** is used, as for a streamgraph, the default
changes to *inside-out*.

`curve` [Curve](inspect_viz.mark.qmd#curve) \| [Param](inspect_viz.qmd#param) \| None  
The curve (interpolation) method for connecting adjacent points.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### bar_x

A horizontal bar mark.

The required *x* values should be quantitative or temporal, and the
optional *y* values should be ordinal.

If neither **x1** nor **x2** nor **interval** is specified, an implicit
stackX transform is applied and **x** defaults to the identity function,
assuming that *data* = \[*x₀*, *x₁*, *x₂*, …\]. Otherwise if an
**interval** is specified, then **x1** and **x2** are derived from
**x**, representing the lower and upper bound of the containing
interval, respectively. Otherwise, if only one of **x1** or **x2** is
specified, the other defaults to **x**, which defaults to zero.

The optional **y** ordinal channel specifies the vertical position; it
is typically bound to the *y* scale, which must be a *band* scale. If
the **y** channel is not specified, the bar will span the vertical
extent of the plot’s frame.

If *y* is quantitative, use the rectX mark instead. If *x* is ordinal,
use the cell mark instead.”

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_bar.py#L14)

``` python
def bar_x(
    data: Data,
    x: ChannelIntervalSpec | Param,
    x1: ChannelSpec | Param | None = None,
    x2: ChannelSpec | Param | None = None,
    y: ChannelIntervalSpec | Param | None = None,
    interval: Interval | None = None,
    filter_by: Selection | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    z: Channel | Param | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: str | float | Param | None = None,
    ry: str | float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position (or length/width) channel, typically bound to
the *x* scale. If neither **x1** nor **x2** nor **interval** is
specified, an implicit stackX transform is applied and **x** defaults to
the identity function, assuming that *data* = \[*x₀*, *x₁*, *x₂*, …\].
Otherwise if an **interval** is specified, then **x1** and **x2** are
derived from **x**, representing the lower and upper bound of the
containing interval, respectively. Otherwise, if only one of **x1** or
**x2** is specified, the other defaults to **x**, which defaults to
zero.

`x1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The required primary (starting, often left) horizontal position channel,
typically bound to the *x* scale. Setting this option disables the
implicit stackX transform. If *x* represents ordinal values, use a cell
mark instead.

`x2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The required secondary (ending, often right) horizontal position
channel, typically bound to the *x* scale. Setting this option disables
the implicit stackX transform. If *x* represents ordinal values, use a
cell mark instead.

`y` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| [Param](inspect_viz.qmd#param) \| None  
The optional vertical position of the bar; a ordinal channel typically
bound to the *y* scale. If not specified, the bar spans the vertical
extent of the frame; otherwise the *y* scale must be a *band* scale. If
*y* represents quantitative or temporal values, use a rectX mark
instead.

`interval` Interval \| None  
How to convert a continuous value (**x** for barX, or **y** for barY)
into an interval (**x1** and **x2** for barX, or **y1** and **y2** for
barY); one of:

- a named time interval such as *day* (for date intervals)
- a number (for number intervals), defining intervals at integer
  multiples of *n*

Setting this option disables the implicit stack transform (stackX for
barX, or stackY for barY).

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`offset` Literal\['center', 'normalize', 'wiggle'\] \| [Param](inspect_viz.qmd#param) \| None  
After stacking, an optional **offset** can be applied to translate and
scale stacks, say to produce a streamgraph; defaults to null for a zero
baseline (**y** = 0 for stackY, and **x** = 0 for stackX). If the
*wiggle* offset is used, the default **order** changes to *inside-out*.

`order` Literal\['value', 'x', 'y', 'z', 'sum', 'appearance', 'inside-out'\] \| str \| Sequence\[float \| bool\] \| [Param](inspect_viz.qmd#param) \| None  
The order in which stacks are layered; one of:

- null (default) for input order
- a named stack order method such as *inside-out* or *sum*
- a field name, for natural order of the corresponding values
- a function of data, for natural order of the corresponding values
- an array of explicit **z** values in the desired order

If the *wiggle* **offset** is used, as for a streamgraph, the default
changes to *inside-out*.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
The **z** channel defines the series of each value in the stack. Used
when the **order** is *sum*, *appearance*, *inside-out*, or an explicit
array of **z** values.

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for all four insets.

`inset_top` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the top edge by the specified number of pixels. A positive value
insets towards the bottom edge (reducing effective area), while a
negative value insets away from the bottom edge (increasing it).

`inset_right` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the right edge by the specified number of pixels. A positive
value insets towards the left edge (reducing effective area), while a
negative value insets away from the left edge (increasing it).

`inset_bottom` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the bottom edge by the specified number of pixels. A positive
value insets towards the top edge (reducing effective area), while a
negative value insets away from the top edge (increasing it).

`inset_left` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the left edge by the specified number of pixels. A positive value
insets towards the right edge (reducing effective area), while a
negative value insets away from the right edge (increasing it).

`rx` str \| float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner
[*x*-radius](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/rx),
either in pixels or as a percentage of the rect width. If **rx** is not
specified, it defaults to **ry** if present, and otherwise draws square
corners.

`ry` str \| float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner \[*y*-radius\]\[\], either in pixels or as a
percentage of the rect height. If **ry** is not specified, it defaults
to **rx** if present, and otherwise draws square corners.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### bar_y

A vertical bar mark.

The required *y* values should be quantitative or temporal, and the
optional *x* values should be ordinal.

If neither **y1** nor **y2** nor **interval** is specified, an implicit
stackY transform is applied and **y** defaults to the identity function,
assuming that *data* = \[*y₀*, *y₁*, *y₂*, …\]. Otherwise if an
**interval** is specified, then **y1** and **y2** are derived from
**y**, representing the lower and upper bound of the containing
interval, respectively. Otherwise, if only one of **y1** or **y2** is
specified, the other defaults to **y**, which defaults to zero.

The optional **x** ordinal channel specifies the horizontal position; it
is typically bound to the *x* scale, which must be a *band* scale. If
the **x** channel is not specified, the bar will span the horizontal
extent of the plot’s frame.

If *x* is quantitative, use the rectY mark instead. If *y* is ordinal,
use the cell mark instead.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_bar.py#L105)

``` python
def bar_y(
    data: Data,
    y: ChannelSpec | Param,
    y1: ChannelSpec | Param | None = None,
    y2: ChannelSpec | Param | None = None,
    x: ChannelSpec | Param | None = None,
    interval: Interval | None = None,
    filter_by: Selection | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    z: Channel | Param | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: str | float | Param | None = None,
    ry: str | float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position (or length/height) channel, typically bound to the
*y* scale. If neither **y1** nor **y2** nor **interval** is specified,
an implicit stackY transform is applied and **y** defaults to the
identity function, assuming that *data* = \[*y₀*, *y₁*, *y₂*, …\].
Otherwise if an **interval** is specified, then **y1** and **y2** are
derived from **y**, representing the lower and upper bound of the
containing interval, respectively. Otherwise, if only one of **y1** or
**y2** is specified, the other defaults to **y**, which defaults to
zero.

`y1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The required primary (starting, often bottom) vertical position channel,
typically bound to the *y* scale. Setting this option disables the
implicit stackY transform. If *y* represents ordinal values, use a cell
mark instead.

`y2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The required secondary (ending, often top) vertical position channel,
typically bound to the *y* scale. Setting this option disables the
implicit stackY transform. If *y* represents ordinal values, use a cell
mark instead.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The optional horizontal position of the bar; a ordinal channel typically
bound to the *x* scale. If not specified, the bar spans the horizontal
extent of the frame; otherwise the *x* scale must be a *band* scale. If
*x* represents quantitative or temporal values, use a rectY mark
instead.

`interval` Interval \| None  
How to convert a continuous value (**x** for barX, or **y** for barY)
into an interval (**x1** and **x2** for barX, or **y1** and **y2** for
barY); one of:

- a named time interval such as *day* (for date intervals)
- a number (for number intervals), defining intervals at integer
  multiples of *n*

Setting this option disables the implicit stack transform (stackX for
barX, or stackY for barY).

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`offset` Literal\['center', 'normalize', 'wiggle'\] \| [Param](inspect_viz.qmd#param) \| None  
After stacking, an optional **offset** can be applied to translate and
scale stacks, say to produce a streamgraph; defaults to null for a zero
baseline (**y** = 0 for stackY, and **x** = 0 for stackX). If the
*wiggle* offset is used, the default **order** changes to *inside-out*.

`order` Literal\['value', 'x', 'y', 'z', 'sum', 'appearance', 'inside-out'\] \| str \| Sequence\[float \| bool\] \| [Param](inspect_viz.qmd#param) \| None  
The order in which stacks are layered; one of:

- null (default) for input order
- a named stack order method such as *inside-out* or *sum*
- a field name, for natural order of the corresponding values
- a function of data, for natural order of the corresponding values
- an array of explicit **z** values in the desired order

If the *wiggle* **offset** is used, as for a streamgraph, the default
changes to *inside-out*.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
The **z** channel defines the series of each value in the stack. Used
when the **order** is *sum*, *appearance*, *inside-out*, or an explicit
array of **z** values.

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for all four insets.

`inset_top` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the top edge by the specified number of pixels. A positive value
insets towards the bottom edge (reducing effective area), while a
negative value insets away from the bottom edge (increasing it).

`inset_right` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the right edge by the specified number of pixels. A positive
value insets towards the left edge (reducing effective area), while a
negative value insets away from the left edge (increasing it).

`inset_bottom` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the bottom edge by the specified number of pixels. A positive
value insets towards the top edge (reducing effective area), while a
negative value insets away from the top edge (increasing it).

`inset_left` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the left edge by the specified number of pixels. A positive value
insets towards the right edge (reducing effective area), while a
negative value insets away from the right edge (increasing it).

`rx` str \| float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner
[*x*-radius](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/rx),
either in pixels or as a percentage of the rect width. If **rx** is not
specified, it defaults to **ry** if present, and otherwise draws square
corners.

`ry` str \| float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner \[*y*-radius\]\[\], either in pixels or as a
percentage of the rect height. If **ry** is not specified, it defaults
to **rx** if present, and otherwise draws square corners.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### heatmap

Create a heatmap mark for density visualization with optimized defaults.

The heatmap mark is essentially a raster mark with different default
options optimized for density visualization. It bins spatial data into a
raster grid and applies kernel density smoothing to create smooth
density surfaces from point data.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_raster.py#L79)

``` python
def heatmap(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    filter_by: Selection | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    pixel_size: float | Param | None = None,
    pad: float | Param | None = None,
    interpolate: Interpolate | Param | None = None,
    bandwidth: float | Param | None = None,
    image_rendering: str | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel, typically bound to the *x* scale.
Domain values are binned into a grid with *width* horizontal bins.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel, typically bound to the *y* scale. Domain
values are binned into a grid with *height* vertical bins.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`width` float \| [Param](inspect_viz.qmd#param) \| None  
The width (number of columns) of the grid, in actual pixels.

`height` float \| [Param](inspect_viz.qmd#param) \| None  
The height (number of rows) of the grid, in actual pixels.

`pixel_size` float \| [Param](inspect_viz.qmd#param) \| None  
The effective screen size of a raster pixel, used to determine the
height and width of the raster from the frame’s dimensions; defaults to
1.

`pad` float \| [Param](inspect_viz.qmd#param) \| None  
The bin padding, one of 1 (default) to include extra padding for the
final bin, or 0 to make the bins flush with the maximum domain value.

`interpolate` [Interpolate](inspect_viz.mark.qmd#interpolate) \| [Param](inspect_viz.qmd#param) \| None  
The spatial interpolation method; one of: - *none* - do not perform
interpolation (the default) - *linear* - apply proportional linear
interpolation across adjacent bins - *nearest* - assign each pixel to
the closest sample’s value (Voronoi diagram) - *barycentric* - apply
barycentric interpolation over the Delaunay triangulation -
*random-walk* - apply a random walk from each pixel

`bandwidth` float \| [Param](inspect_viz.qmd#param) \| None  
The kernel density bandwidth for smoothing, in pixels; defaults to 20.

`image_rendering` str \| [Param](inspect_viz.qmd#param) \| None  
The image-rendering attribute; defaults to *auto* (bilinear). May be set
to *pixelated* to disable bilinear interpolation for a sharper image.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

## Statistical

### density

Create a 2D density mark that shows smoothed point cloud densities.

The density mark bins the data, counts the number of records that fall
into each bin, and smooths the resulting counts, then plots the smoothed
distribution, by default using a circular dot mark. The density mark
calculates density values that can be mapped to encoding channels such
as fill or r using the special field name “density”.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_density.py#L17)

``` python
def density(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    type: Literal["dot", "circle", "hexagon", "cell", "text"] | Param | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    pixel_size: float | Param | None = None,
    pad: float | Param | None = None,
    bandwidth: float | Param | None = None,
    interpolate: Interpolate | Param | None = None,
    symbol: Symbol | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    rotate: Channel | float | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    styles: TextStyles | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel, typically bound to the *x* scale.
Domain values are binned into a grid with *width* horizontal bins.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel, typically bound to the *y* scale. Domain
values are binned into a grid with *height* vertical bins.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`type` Literal\['dot', 'circle', 'hexagon', 'cell', 'text'\] \| [Param](inspect_viz.qmd#param) \| None  
The base mark type to use for rendering; defaults to “dot”.

`width` float \| [Param](inspect_viz.qmd#param) \| None  
The number of horizontal bins for density calculation.

`height` float \| [Param](inspect_viz.qmd#param) \| None  
The number of vertical bins for density calculation.

`pixel_size` float \| [Param](inspect_viz.qmd#param) \| None  
The size of each pixel for the grid, in data units.

`pad` float \| [Param](inspect_viz.qmd#param) \| None  
The bin padding, one of 1 (default) to include extra padding for the
final bin, or 0 to make the bins flush with the maximum domain value.

`bandwidth` float \| [Param](inspect_viz.qmd#param) \| None  
The kernel density bandwidth for smoothing, in pixels.

`interpolate` [Interpolate](inspect_viz.mark.qmd#interpolate) \| [Param](inspect_viz.qmd#param) \| None  
The spatial interpolation method; one of: - *none* - do not perform
interpolation (the default) - *linear* - apply proportional linear
interpolation across adjacent bins - *nearest* - assign each pixel to
the closest sample’s value (Voronoi diagram) - *barycentric* - apply
barycentric interpolation over the Delaunay triangulation -
*random-walk* - apply a random walk from each pixel

`symbol` [Symbol](inspect_viz.mark.qmd#symbol) \| [Param](inspect_viz.qmd#param) \| None  
The symbol type for dots; defaults to “circle”.

`r` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The radius channel, typically bound to the *radius* scale.

`rotate` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle in degrees clockwise.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor position for legend placement.

`styles` [TextStyles](inspect_viz.mark.qmd#textstyles) \| None  
Text styles to apply.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### density_x

A densityX mark that visualizes smoothed point cloud densities along the
**x** dimension.

The mark bins the data, counts the number of records that fall into each
bin, smooths the resulting counts, and then plots the smoothed
distribution, by default using an areaX mark.

Set the *type* property to use a different base mark type.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_density.py#L100)

``` python
def density_x(
    data: Data,
    y: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    type: Literal["areaX", "lineX", "dotX", "textX"] | Param | None = None,
    stack: bool | Param | None = None,
    bandwidth: float | Param | None = None,
    bins: float | Param | None = None,
    normalize: bool | Literal["max", "sum", "none"] | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale;
defaults to the zero-based index of the data \[0, 1, 2, …\].

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`type` Literal\['areaX', 'lineX', 'dotX', 'textX'\] \| [Param](inspect_viz.qmd#param) \| None  
The basic mark type to use to render 1D density values. Defaults to an
areaX mark; lineX, dotX, and textX marks are also supported.

`stack` bool \| [Param](inspect_viz.qmd#param) \| None  
Flag indicating if densities should be stacked. Defaults to `False`.

`bandwidth` float \| [Param](inspect_viz.qmd#param) \| None  
The kernel density bandwidth for smoothing, in pixels.

`bins` float \| [Param](inspect_viz.qmd#param) \| None  
The number of bins over which to discretize the data prior to smoothing.
Defaults to 1024.

`normalize` bool \| Literal\['max', 'sum', 'none'\] \| [Param](inspect_viz.qmd#param) \| None  
Normalization method for density estimates. If `False` or `'none'` (the
default), the density estimates are smoothed weighted counts. If `True`
or `'sum'`, density estimates are divided by the sum of the total point
mass. If `'max'`, estimates are divided by the maximum smoothed value.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### density_y

A densityY mark that visualizes smoothed point cloud densities along the
**y** dimension.

The mark bins the data, counts the number of records that fall into each
bin, smooths the resulting counts, and then plots the smoothed
distribution, by default using an areaY mark.

Set the *type* property to use a different base mark type.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_density.py#L156)

``` python
def density_y(
    data: Data,
    x: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    type: Literal["areaY", "lineY", "dotY", "circle", "hexagon", "textY"]
    | Param
    | None = None,
    stack: bool | Param | None = None,
    bandwidth: float | Param | None = None,
    bins: float | Param | None = None,
    normalize: bool | Literal["max", "sum", "none"] | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale;
defaults to the zero-based index of the data \[0, 1, 2, …\].

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`type` Literal\['areaY', 'lineY', 'dotY', 'circle', 'hexagon', 'textY'\] \| [Param](inspect_viz.qmd#param) \| None  
The basic mark type to use to render 1D density values. Defaults to an
areaY mark; lineY, dotY, circle, hexagon, and textY marks are also
supported.

`stack` bool \| [Param](inspect_viz.qmd#param) \| None  
Flag indicating if densities should be stacked. Defaults to `False`.

`bandwidth` float \| [Param](inspect_viz.qmd#param) \| None  
The kernel density bandwidth for smoothing, in pixels.

`bins` float \| [Param](inspect_viz.qmd#param) \| None  
The number of bins over which to discretize the data prior to smoothing.
Defaults to 1024.

`normalize` bool \| Literal\['max', 'sum', 'none'\] \| [Param](inspect_viz.qmd#param) \| None  
Normalization method for density estimates. If `False` or `'none'` (the
default), the density estimates are smoothed weighted counts. If `True`
or `'sum'`, density estimates are divided by the sum of the total point
mass. If `'max'`, estimates are divided by the maximum smoothed value.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### contour

Create a contour mark that draws contour lines of equal value.

The contour mark creates isolines showing contours of equal value. It
bins the given data into a 2D grid, computes density estimates, and
draws contour lines at specified threshold levels. The contour mark is
useful for visualizing the density or distribution of 2D point data.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_contour.py#L14)

``` python
def contour(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    filter_by: Selection | None = None,
    thresholds: float | list[float] | Param | None = None,
    bandwidth: float | Param | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    pixel_size: float | Param | None = None,
    pad: float | Param | None = None,
    interpolate: Interpolate | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel, typically bound to the *x* scale.
Domain values are binned into a grid with *width* horizontal bins.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel, typically bound to the *y* scale. Domain
values are binned into a grid with *height* vertical bins.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`thresholds` float \| list\[float\] \| [Param](inspect_viz.qmd#param) \| None  
The number of contour thresholds to subdivide the domain into discrete
level sets; defaults to 10. Can be a count or an array of threshold
values.

`bandwidth` float \| [Param](inspect_viz.qmd#param) \| None  
The kernel density bandwidth for smoothing, in pixels.

`width` float \| [Param](inspect_viz.qmd#param) \| None  
The width (number of columns) of the grid, in actual pixels.

`height` float \| [Param](inspect_viz.qmd#param) \| None  
The height (number of rows) of the grid, in actual pixels.

`pixel_size` float \| [Param](inspect_viz.qmd#param) \| None  
The effective screen size of a raster pixel, used to determine the
height and width of the raster from the frame’s dimensions; defaults to
1.

`pad` float \| [Param](inspect_viz.qmd#param) \| None  
The bin padding, one of 1 (default) to include extra padding for the
final bin, or 0 to make the bins flush with the maximum domain value.

`interpolate` [Interpolate](inspect_viz.mark.qmd#interpolate) \| [Param](inspect_viz.qmd#param) \| None  
The spatial interpolation method; one of: - *none* - do not perform
interpolation (the default) - *linear* - apply proportional linear
interpolation across adjacent bins - *nearest* - assign each pixel to
the closest sample’s value (Voronoi diagram) - *barycentric* - apply
barycentric interpolation over the Delaunay triangulation -
*random-walk* - apply a random walk from each pixel

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### regression_y

A vertical regression mark.

The regressionY mark draws a regression line with optional confidence
bands showing the relationship between variables. The x variable is the
independent variable and y is the dependent variable.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_regression.py#L13)

``` python
def regression_y(
    data: Data,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    ci: float | Param | None = None,
    precision: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The independent variable horizontal position channel (defaults to
zero-based index).

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The dependent variable vertical position channel (defaults to identity
function).

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series, producing
independent regressions for each group.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`ci` float \| [Param](inspect_viz.qmd#param) \| None  
The confidence interval in (0, 1), or 0 to hide bands; defaults to 0.95.

`precision` float \| [Param](inspect_viz.qmd#param) \| None  
The distance in pixels between samples of the confidence band; defaults
to 4.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### error_bar_x

A horizontal error bar mark.

The errorBarX mark draws horizontal error bars showing confidence
intervals or uncertainty around data points. The error bars extend
horizontally from the central value.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_error_bar.py#L14)

``` python
def error_bar_x(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param | None = None,
    ci: float | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The dependent variable horizontal position channel (required).

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The independent variable vertical position channel (optional).

`ci` float \| [Param](inspect_viz.qmd#param) \| None  
The confidence interval in (0, 1); defaults to 0.95.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at all positions along the error bar.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the start of the error bar.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the middle of the error bar.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the end of the error bar.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### error_bar_y

A vertical error bar mark.

The errorBarY mark draws vertical error bars showing confidence
intervals or uncertainty around data points. The error bars extend
vertically from the central value.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_error_bar.py#L62)

``` python
def error_bar_y(
    data: Data,
    y: ChannelSpec | Param,
    x: ChannelSpec | Param | None = None,
    ci: float | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The dependent variable vertical position channel (required).

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The independent variable horizontal position channel (optional).

`ci` float \| [Param](inspect_viz.qmd#param) \| None  
The confidence interval in (0, 1); defaults to 0.95.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at all positions along the error bar.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the start of the error bar.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the middle of the error bar.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the end of the error bar.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

## Grid

### cell

A cell mark that draws axis-aligned rectangles for categorical data.

Cells are typically used to create heatmaps and other grid-based
visualizations where both x and y represent categorical or ordinal data.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_cell.py#L13)

``` python
def cell(
    data: Data,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    filter_by: Selection | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for all four insets.

`inset_top` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the top edge by the specified number of pixels.

`inset_right` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the right edge by the specified number of pixels.

`inset_bottom` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the bottom edge by the specified number of pixels.

`inset_left` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the left edge by the specified number of pixels.

`rx` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner x-radius, either in pixels or as a percentage of the
cell width.

`ry` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner y-radius, either in pixels or as a percentage of the
cell height.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### cell_x

A cellX mark that draws axis-aligned rectangles with ordinal
positioning.

The *x* values should be ordinal (categories), and the optional *y*
values should also be ordinal.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_cell.py#L67)

``` python
def cell_x(
    data: Data,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    filter_by: Selection | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for all four insets.

`inset_top` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the top edge by the specified number of pixels.

`inset_right` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the right edge by the specified number of pixels.

`inset_bottom` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the bottom edge by the specified number of pixels.

`inset_left` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the left edge by the specified number of pixels.

`rx` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner x-radius, either in pixels or as a percentage of the
cell width.

`ry` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner y-radius, either in pixels or as a percentage of the
cell height.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### cell_y

A cellY mark that draws axis-aligned rectangles with ordinal
positioning.

The *y* values should be ordinal (categories), and the optional *x*
values should also be ordinal.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_cell.py#L120)

``` python
def cell_y(
    data: Data,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    filter_by: Selection | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for all four insets.

`inset_top` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the top edge by the specified number of pixels.

`inset_right` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the right edge by the specified number of pixels.

`inset_bottom` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the bottom edge by the specified number of pixels.

`inset_left` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the left edge by the specified number of pixels.

`rx` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner x-radius, either in pixels or as a percentage of the
cell width.

`ry` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner y-radius, either in pixels or as a percentage of the
cell height.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### grid_x

A horizontal grid mark.

The gridX mark draws horizontal grid lines across the plot area. It is
primarily used for adding visual reference lines along the x-axis.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_grid.py#L14)

``` python
def grid_x(
    x: ChannelSpec | Param | None = None,
    y: ChannelIntervalSpec | None = None,
    y1: ChannelSpec | Param | None = None,
    y2: ChannelSpec | Param | None = None,
    interval: Interval | None = None,
    anchor: str | Param | None = None,
    color: ChannelSpec | str | Param | None = None,
    ticks: int | Sequence[Any] | Param | None = None,
    tick_spacing: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| None  
Shorthand for specifying both the primary and secondary vertical
position of the tick as the bounds of the containing interval; can only
be used in conjunction with the **interval** option.

`y1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The primary (starting, often bottom) vertical position of the grid line.

`y2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The secondary (ending, often top) vertical position of the grid line.

`interval` Interval \| None  
How to convert a continuous value into an interval.

`anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The side of the frame on which to place the grid (*top* or *bottom*).

`color` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| str \| [Param](inspect_viz.qmd#param) \| None  
Shorthand for setting both fill and stroke color.

`ticks` int \| Sequence\[Any\] \| [Param](inspect_viz.qmd#param) \| None  
The desired number of ticks, or an array of tick values, or null to
disable ticks.

`tick_spacing` float \| [Param](inspect_viz.qmd#param) \| None  
The desired spacing between ticks in pixels.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions` (including stroke, stroke_width,
stroke_opacity, stroke_dasharray).

### grid_y

A vertical grid mark.

The gridY mark draws vertical grid lines across the plot area. It is
primarily used for adding visual reference lines along the y-axis.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_grid.py#L60)

``` python
def grid_y(
    y: ChannelSpec | Param | None = None,
    x: ChannelIntervalSpec | None = None,
    x1: ChannelSpec | Param | None = None,
    x2: ChannelSpec | Param | None = None,
    interval: Interval | None = None,
    anchor: str | Param | None = None,
    color: ChannelSpec | str | Param | None = None,
    ticks: int | Sequence[Any] | Param | None = None,
    tick_spacing: float | Param | None = None,
    inset_left: float | Param | None = None,
    inset_right: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`x` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| None  
Shorthand for specifying both the primary and secondary horizontal
position of the tick as the bounds of the containing interval; can only
be used in conjunction with the **interval** option.

`x1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The primary (starting, often left) horizontal position of the grid line.

`x2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The secondary (ending, often right) horizontal position of the grid
line.

`interval` Interval \| None  
How to convert a continuous value into an interval.

`anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The side of the frame on which to place the grid (*left* or *right*).

`color` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| str \| [Param](inspect_viz.qmd#param) \| None  
Shorthand for setting both fill and stroke color.

`ticks` int \| Sequence\[Any\] \| [Param](inspect_viz.qmd#param) \| None  
The desired number of ticks, or an array of tick values, or null to
disable ticks.

`tick_spacing` float \| [Param](inspect_viz.qmd#param) \| None  
The desired spacing between ticks in pixels.

`inset_left` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the left edge by the specified number of pixels.

`inset_right` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the right edge by the specified number of pixels.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions` (including stroke, stroke_width,
stroke_opacity, stroke_dasharray).

### grid_fx

A horizontal facet grid mark.

The gridFx mark draws horizontal grid lines for faceted plots. It is
primarily used for adding visual reference lines along the fx-axis in
faceted visualizations.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_grid.py#L112)

``` python
def grid_fx(
    x: ChannelSpec | Param | None = None,
    y1: ChannelSpec | Param | None = None,
    y2: ChannelSpec | Param | None = None,
    interval: Interval | None = None,
    anchor: str | Param | None = None,
    color: ChannelSpec | str | Param | None = None,
    ticks: int | Sequence[Any] | Param | None = None,
    tick_spacing: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`y1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The primary (starting, often bottom) vertical position of the grid line.

`y2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The secondary (ending, often top) vertical position of the grid line.

`interval` Interval \| None  
How to convert a continuous value into an interval.

`anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The side of the frame on which to place the grid (*top* or *bottom*).

`color` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| str \| [Param](inspect_viz.qmd#param) \| None  
Shorthand for setting both fill and stroke color.

`ticks` int \| Sequence\[Any\] \| [Param](inspect_viz.qmd#param) \| None  
The desired number of ticks, or an array of tick values, or null to
disable ticks.

`tick_spacing` float \| [Param](inspect_viz.qmd#param) \| None  
The desired spacing between ticks in pixels.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions` (including stroke, stroke_width,
stroke_opacity, stroke_dasharray).

### grid_fy

A vertical facet grid mark.

The gridFy mark draws vertical grid lines for faceted plots. It is
primarily used for adding visual reference lines along the fy-axis in
faceted visualizations.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_grid.py#L155)

``` python
def grid_fy(
    y: ChannelSpec | Param | None = None,
    x1: ChannelSpec | Param | None = None,
    x2: ChannelSpec | Param | None = None,
    interval: Interval | None = None,
    anchor: str | Param | None = None,
    color: ChannelSpec | str | Param | None = None,
    ticks: int | Sequence[Any] | Param | None = None,
    tick_spacing: float | Param | None = None,
    inset_left: float | Param | None = None,
    inset_right: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`x1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The primary (starting, often left) horizontal position of the grid line.

`x2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The secondary (ending, often right) horizontal position of the grid
line.

`interval` Interval \| None  
How to convert a continuous value into an interval.

`anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The side of the frame on which to place the grid (*left* or *right*).

`color` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| str \| [Param](inspect_viz.qmd#param) \| None  
Shorthand for setting both fill and stroke color.

`ticks` int \| Sequence\[Any\] \| [Param](inspect_viz.qmd#param) \| None  
The desired number of ticks, or an array of tick values, or null to
disable ticks.

`tick_spacing` float \| [Param](inspect_viz.qmd#param) \| None  
The desired spacing between ticks in pixels.

`inset_left` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the left edge by the specified number of pixels.

`inset_right` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the right edge by the specified number of pixels.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions` (including stroke, stroke_width,
stroke_opacity, stroke_dasharray).

### hexbin

Create a hexbin mark for hexagonal binning of point data.

The hexbin mark bins two-dimensional point data into hexagonal bins and
displays aggregated values for each bin. This is useful for visualizing
density patterns in large datasets and for creating hexagonal heatmaps.

The mark creates a hexagonal grid and counts or aggregates data points
within each hexagon, then renders the results using the specified mark
type.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_hexbin.py#L15)

``` python
def hexbin(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    bin_width: float | Param | None = None,
    type: Literal["hexagon", "dot", "text"] | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    rotate: ChannelSpec | float | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    styles: TextStyles | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel, typically bound to the *x* scale.
Specifies the data to be binned horizontally.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel, typically bound to the *y* scale.
Specifies the data to be binned vertically.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
How to subdivide bins. Defaults to the *fill* channel, if any, or the
*stroke* channel, if any. If null, bins will not be subdivided.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`bin_width` float \| [Param](inspect_viz.qmd#param) \| None  
The distance between centers of neighboring hexagons, in pixels;
defaults to 20.

`type` Literal\['hexagon', 'dot', 'text'\] \| [Param](inspect_viz.qmd#param) \| None  
The basic mark type to use for hex-binned values. Defaults to a hexagon
mark; dot and text marks are also supported.

`r` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The radius of dots or hexagons; either a channel or constant.

`rotate` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle in degrees clockwise.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor position for legend placement.

`styles` [TextStyles](inspect_viz.mark.qmd#textstyles) \| None  
Text styles to apply when using text mark type.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### hexgrid

Create a hexgrid mark that displays a hexagonal grid overlay.

The hexgrid mark creates a hexagonal grid pattern, typically used as a
background or reference grid for hexbin visualizations. This is a
decoration mark that shows the underlying hexagonal structure without
requiring data.

The hexgrid mark is designed to complement hexbin marks by showing the
grid structure. It’s a stroke-only mark where fill is not supported.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_hexgrid.py#L11)

``` python
def hexgrid(
    bin_width: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`bin_width` float \| [Param](inspect_viz.qmd#param) \| None  
The distance between centers of neighboring hexagons, in pixels;
defaults to 20. Should match the bin_width of any corresponding hexbin
mark for proper alignment.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions. Note that this is a
stroke-only mark, so fill options will not be effective.

### waffle_x

A waffleX mark that creates horizontal waffle charts.

Waffle charts are a form of unit chart where data is represented as a
grid of small squares or rectangles, useful for showing part-to-whole
relationships and making proportions more tangible.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_waffle.py#L14)

``` python
def waffle_x(
    data: Data,
    x: ChannelIntervalSpec | Param,
    x1: ChannelSpec | Param | None = None,
    x2: ChannelSpec | Param | None = None,
    y: ChannelIntervalSpec | Param | None = None,
    z: ChannelSpec | Param | None = None,
    filter_by: Selection | None = None,
    multiple: float | Param | None = None,
    unit: float | Param | None = None,
    gap: float | Param | None = None,
    round: bool | Param | None = None,
    interval: Interval | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel, typically bound to the *x* scale.

`x1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The starting horizontal position channel, typically bound to the *x*
scale.

`x2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The ending horizontal position channel, typically bound to the *x*
scale.

`y` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`z` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The **z** channel defines the series of each value in the stack.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`multiple` float \| [Param](inspect_viz.qmd#param) \| None  
The number of units per tile; defaults to 1.

`unit` float \| [Param](inspect_viz.qmd#param) \| None  
The size of each unit in the waffle; defaults to 1.

`gap` float \| [Param](inspect_viz.qmd#param) \| None  
The gap between waffle units; defaults to 1.

`round` bool \| [Param](inspect_viz.qmd#param) \| None  
Whether to round values to the nearest unit; defaults to false.

`interval` Interval \| None  
How to convert a continuous value into an interval.

`offset` Literal\['center', 'normalize', 'wiggle'\] \| [Param](inspect_viz.qmd#param) \| None  
After stacking, an optional **offset** can be applied to translate and
scale stacks.

`order` Literal\['value', 'x', 'y', 'z', 'sum', 'appearance', 'inside-out'\] \| str \| Sequence\[float \| bool\] \| [Param](inspect_viz.qmd#param) \| None  
The order in which stacks are layered.

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for all four insets.

`inset_top` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the top edge by the specified number of pixels.

`inset_right` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the right edge by the specified number of pixels.

`inset_bottom` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the bottom edge by the specified number of pixels.

`inset_left` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the left edge by the specified number of pixels.

`rx` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner x-radius, either in pixels or as a percentage.

`ry` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner y-radius, either in pixels or as a percentage.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### waffle_y

A waffleY mark that creates vertical waffle charts.

Waffle charts are a form of unit chart where data is represented as a
grid of small squares or rectangles, useful for showing part-to-whole
relationships and making proportions more tangible.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_waffle.py#L103)

``` python
def waffle_y(
    data: Data,
    y: ChannelSpec | Param,
    y1: ChannelSpec | Param | None = None,
    y2: ChannelSpec | Param | None = None,
    x: ChannelSpec | Param | None = None,
    z: ChannelSpec | Param | None = None,
    filter_by: Selection | None = None,
    multiple: float | Param | None = None,
    unit: float | Param | None = None,
    gap: float | Param | None = None,
    round: bool | Param | None = None,
    interval: Interval | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel, typically bound to the *y* scale.

`y1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The starting vertical position channel, typically bound to the *y*
scale.

`y2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The ending vertical position channel, typically bound to the *y* scale.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`z` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The **z** channel defines the series of each value in the stack.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`multiple` float \| [Param](inspect_viz.qmd#param) \| None  
The number of units per tile; defaults to 1.

`unit` float \| [Param](inspect_viz.qmd#param) \| None  
The size of each unit in the waffle; defaults to 1.

`gap` float \| [Param](inspect_viz.qmd#param) \| None  
The gap between waffle units; defaults to 1.

`round` bool \| [Param](inspect_viz.qmd#param) \| None  
Whether to round values to the nearest unit; defaults to false.

`interval` Interval \| None  
How to convert a continuous value into an interval.

`offset` Literal\['center', 'normalize', 'wiggle'\] \| [Param](inspect_viz.qmd#param) \| None  
After stacking, an optional **offset** can be applied to translate and
scale stacks.

`order` Literal\['value', 'x', 'y', 'z', 'sum', 'appearance', 'inside-out'\] \| str \| Sequence\[float \| bool\] \| [Param](inspect_viz.qmd#param) \| None  
The order in which stacks are layered.

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for all four insets.

`inset_top` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the top edge by the specified number of pixels.

`inset_right` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the right edge by the specified number of pixels.

`inset_bottom` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the bottom edge by the specified number of pixels.

`inset_left` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the left edge by the specified number of pixels.

`rx` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner x-radius, either in pixels or as a percentage.

`ry` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner y-radius, either in pixels or as a percentage.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

## Specialized

### raster

Create a raster mark for spatial samples with optional interpolation and
smoothing.

The raster mark bins spatial data into a raster grid and optionally
applies spatial interpolation and kernel density smoothing. The raster
mark is useful for visualizing continuous spatial phenomena from
discrete sample points.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_raster.py#L14)

``` python
def raster(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    filter_by: Selection | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    pixel_size: float | Param | None = None,
    pad: float | Param | None = None,
    interpolate: Interpolate | Param | None = None,
    bandwidth: float | Param | None = None,
    image_rendering: str | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel, typically bound to the *x* scale.
Domain values are binned into a grid with *width* horizontal bins.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel, typically bound to the *y* scale. Domain
values are binned into a grid with *height* vertical bins.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`width` float \| [Param](inspect_viz.qmd#param) \| None  
The width (number of columns) of the grid, in actual pixels.

`height` float \| [Param](inspect_viz.qmd#param) \| None  
The height (number of rows) of the grid, in actual pixels.

`pixel_size` float \| [Param](inspect_viz.qmd#param) \| None  
The effective screen size of a raster pixel, used to determine the
height and width of the raster from the frame’s dimensions; defaults to
1.

`pad` float \| [Param](inspect_viz.qmd#param) \| None  
The bin padding, one of 1 (default) to include extra padding for the
final bin, or 0 to make the bins flush with the maximum domain value.

`interpolate` [Interpolate](inspect_viz.mark.qmd#interpolate) \| [Param](inspect_viz.qmd#param) \| None  
The spatial interpolation method; one of: - *none* - do not perform
interpolation (the default) - *linear* - apply proportional linear
interpolation across adjacent bins - *nearest* - assign each pixel to
the closest sample’s value (Voronoi diagram) - *barycentric* - apply
barycentric interpolation over the Delaunay triangulation -
*random-walk* - apply a random walk from each pixel

`bandwidth` float \| [Param](inspect_viz.qmd#param) \| None  
The kernel density bandwidth for smoothing, in pixels.

`image_rendering` str \| [Param](inspect_viz.qmd#param) \| None  
The image-rendering attribute; defaults to *auto* (bilinear). May be set
to *pixelated* to disable bilinear interpolation for a sharper image.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### raster_tile

Create an experimental raster tile mark with tiling and prefetching for
scalable rasters.

The rasterTile mark is an experimental version of the raster mark that
supports tiling and prefetching for better performance with large
datasets. It provides scalable raster visualization with efficient
memory usage.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_raster.py#L144)

``` python
def raster_tile(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    filter_by: Selection | None = None,
    origin: list[float] | Param | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    pixel_size: float | Param | None = None,
    pad: float | Param | None = None,
    interpolate: Interpolate | Param | None = None,
    bandwidth: float | Param | None = None,
    image_rendering: str | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel, typically bound to the *x* scale.
Domain values are binned into a grid with *width* horizontal bins.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel, typically bound to the *y* scale. Domain
values are binned into a grid with *height* vertical bins.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`origin` list\[float\] \| [Param](inspect_viz.qmd#param) \| None  
The coordinates of the tile origin in the x and y data domains; defaults
to \[0, 0\].

`width` float \| [Param](inspect_viz.qmd#param) \| None  
The width (number of columns) of the grid, in actual pixels.

`height` float \| [Param](inspect_viz.qmd#param) \| None  
The height (number of rows) of the grid, in actual pixels.

`pixel_size` float \| [Param](inspect_viz.qmd#param) \| None  
The effective screen size of a raster pixel, used to determine the
height and width of the raster from the frame’s dimensions; defaults to
1.

`pad` float \| [Param](inspect_viz.qmd#param) \| None  
The bin padding, one of 1 (default) to include extra padding for the
final bin, or 0 to make the bins flush with the maximum domain value.

`interpolate` [Interpolate](inspect_viz.mark.qmd#interpolate) \| [Param](inspect_viz.qmd#param) \| None  
The spatial interpolation method; one of: - *none* - do not perform
interpolation (the default) - *linear* - apply proportional linear
interpolation across adjacent bins - *nearest* - assign each pixel to
the closest sample’s value (Voronoi diagram) - *barycentric* - apply
barycentric interpolation over the Delaunay triangulation -
*random-walk* - apply a random walk from each pixel

`bandwidth` float \| [Param](inspect_viz.qmd#param) \| None  
The kernel density bandwidth for smoothing, in pixels.

`image_rendering` str \| [Param](inspect_viz.qmd#param) \| None  
The image-rendering attribute; defaults to *auto* (bilinear). May be set
to *pixelated* to disable bilinear interpolation for a sharper image.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### vector

A vector mark that draws arrows or other directional shapes.

Vectors are typically used to represent direction and magnitude in data,
such as wind vectors, force fields, or gradients.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_vector.py#L14)

``` python
def vector(
    data: Data,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    filter_by: Selection | None = None,
    length: ChannelSpec | float | Param | None = None,
    rotate: Channel | float | Param | None = None,
    shape: Literal["arrow", "spike"] | Param | None = None,
    anchor: Literal["start", "middle", "end"] | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`r` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The radius or magnitude channel; either a constant or a channel.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`length` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The length of the vector; either a constant or a channel.

`rotate` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle in degrees clockwise; either a constant or a channel.

`shape` Literal\['arrow', 'spike'\] \| [Param](inspect_viz.qmd#param) \| None  
The shape of the vector; one of “arrow” or “spike”.

`anchor` Literal\['start', 'middle', 'end'\] \| [Param](inspect_viz.qmd#param) \| None  
The anchor position; one of “start”, “middle”, or “end”.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor position for legend placement.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### vector_x

A vectorX mark that draws horizontal directional vectors.

VectorX marks are oriented primarily along the x-axis and are useful for
showing horizontal flow or direction.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_vector.py#L65)

``` python
def vector_x(
    data: Data,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    filter_by: Selection | None = None,
    length: ChannelSpec | float | Param | None = None,
    rotate: Channel | float | Param | None = None,
    shape: Literal["arrow", "spike"] | Param | None = None,
    anchor: Literal["start", "middle", "end"] | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`r` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The radius or magnitude channel; either a constant or a channel.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`length` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The length of the vector; either a constant or a channel.

`rotate` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle in degrees clockwise; either a constant or a channel.

`shape` Literal\['arrow', 'spike'\] \| [Param](inspect_viz.qmd#param) \| None  
The shape of the vector; one of “arrow” or “spike”.

`anchor` Literal\['start', 'middle', 'end'\] \| [Param](inspect_viz.qmd#param) \| None  
The anchor position; one of “start”, “middle”, or “end”.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor position for legend placement.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### vector_y

A vectorY mark that draws vertical directional vectors.

VectorY marks are oriented primarily along the y-axis and are useful for
showing vertical flow or direction.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_vector.py#L116)

``` python
def vector_y(
    data: Data,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    filter_by: Selection | None = None,
    length: ChannelSpec | float | Param | None = None,
    rotate: Channel | float | Param | None = None,
    shape: Literal["arrow", "spike"] | Param | None = None,
    anchor: Literal["start", "middle", "end"] | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`r` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The radius or magnitude channel; either a constant or a channel.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`length` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The length of the vector; either a constant or a channel.

`rotate` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle in degrees clockwise; either a constant or a channel.

`shape` Literal\['arrow', 'spike'\] \| [Param](inspect_viz.qmd#param) \| None  
The shape of the vector; one of “arrow” or “spike”.

`anchor` Literal\['start', 'middle', 'end'\] \| [Param](inspect_viz.qmd#param) \| None  
The anchor position; one of “start”, “middle”, or “end”.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor position for legend placement.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### spike

A spike mark that draws spike-shaped directional indicators.

Spikes are a specialized type of vector that typically appear as thin
lines or needles, useful for showing precise directional data or
impulses.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_vector.py#L167)

``` python
def spike(
    data: Data,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    length: ChannelSpec | float | Param | None = None,
    rotate: Channel | float | Param | None = None,
    shape: Literal["arrow", "spike"] | Param | None = None,
    anchor: Literal["start", "middle", "end"] | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    filter_by: Selection | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`r` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The radius or magnitude channel; either a constant or a channel.

`length` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The length of the spike; either a constant or a channel.

`rotate` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle in degrees clockwise; either a constant or a channel.

`shape` Literal\['arrow', 'spike'\] \| [Param](inspect_viz.qmd#param) \| None  
The shape of the spike; one of “arrow” or “spike”.

`anchor` Literal\['start', 'middle', 'end'\] \| [Param](inspect_viz.qmd#param) \| None  
The anchor position; one of “start”, “middle”, or “end”.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor position for legend placement.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### arrow

An arrow mark.

The arrow mark draws arrows between two points, with customizable
arrowheads and curved paths. It is useful for indicating direction,
flow, or relationships between data points.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_arrow.py#L13)

``` python
def arrow(
    data: Data,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    x1: ChannelSpec | Param | None = None,
    y1: ChannelSpec | Param | None = None,
    x2: ChannelSpec | Param | None = None,
    y2: ChannelSpec | Param | None = None,
    filter_by: Selection | None = None,
    bend: float | bool | Param | None = None,
    head_angle: float | Param | None = None,
    head_length: float | Param | None = None,
    inset: float | Param | None = None,
    inset_start: float | Param | None = None,
    inset_end: float | Param | None = None,
    sweep: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, shorthand for both x1 and x2.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, shorthand for both y1 and y2.

`x1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The starting horizontal position of the arrow.

`y1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The starting vertical position of the arrow.

`x2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The ending horizontal position of the arrow.

`y2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The ending vertical position of the arrow.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`bend` float \| bool \| [Param](inspect_viz.qmd#param) \| None  
The angle between straight line and outgoing tangent (±90°, use True for
22.5°).

`head_angle` float \| [Param](inspect_viz.qmd#param) \| None  
How pointy the arrowhead is in degrees (0°-180°, defaults to 60°).

`head_length` float \| [Param](inspect_viz.qmd#param) \| None  
Size of arrowhead relative to stroke width.

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Shorthand for both inset_start and inset_end.

`inset_start` float \| [Param](inspect_viz.qmd#param) \| None  
Starting inset in pixels (defaults to 0).

`inset_end` float \| [Param](inspect_viz.qmd#param) \| None  
Ending inset in pixels (defaults to 0).

`sweep` float \| [Param](inspect_viz.qmd#param) \| None  
Sweep order (1=clockwise, -1=anticlockwise, 0=no bend).

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### link

Create a link mark that draws line segments between pairs of points.

The link mark connects pairs of points with line segments. It supports
both simple positioning using x and y (which serve as shorthand for
x1/x2 and y1/y2), and explicit positioning using x1/y1 and x2/y2
coordinates for full control over link endpoints.

For vertical links, specify **x** (or **x1** and **x2**) for the
horizontal position and **y1** and **y2** for the vertical endpoints.
For horizontal links, specify **y** (or **y1** and **y2**) for the
vertical position and **x1** and **x2** for the horizontal endpoints.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_link.py#L14)

``` python
def link(
    data: Data,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    x1: ChannelSpec | Param | None = None,
    y1: ChannelSpec | Param | None = None,
    x2: ChannelSpec | Param | None = None,
    y2: ChannelSpec | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position for vertical links; shorthand for x1 and x2.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position for horizontal links; shorthand for y1 and y2.

`x1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The starting horizontal position; also sets default for x2.

`y1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The starting vertical position; also sets default for y2.

`x2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The ending horizontal position; also sets default for x1.

`y2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The ending vertical position; also sets default for y1.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for marker_start, marker_mid, and
marker_end.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the starting point of a line segment.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for any middle (interior) points of a line segment.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the ending point of a line segment.

`curve` [Curve](inspect_viz.mark.qmd#curve) \| [Param](inspect_viz.qmd#param) \| None  
The curve interpolation method for connecting adjacent points.
Recommended for links: *linear*, *step*, *step-after*, *step-before*,
*bump-x*, *bump-y*.

`tension` float \| [Param](inspect_viz.qmd#param) \| None  
The tension option only has an effect on bundle, cardinal and
Catmull–Rom splines.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### delaunay_link

Create a Delaunay link mark that draws links for each edge of the
Delaunay triangulation.

The delaunayLink mark computes the Delaunay triangulation of the data
and draws a line segment for each edge of the triangulation. This is
useful for visualizing spatial relationships and adjacencies in
scattered point data.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_delaunay.py#L14)

``` python
def delaunay_link(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel, typically bound to the *y* scale.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping to produce multiple (possibly
overlapping) triangulations.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for marker_start, marker_mid, and
marker_end.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the starting point of a line segment.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for any middle (interior) points of a line segment.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the ending point of a line segment.

`curve` [Curve](inspect_viz.mark.qmd#curve) \| [Param](inspect_viz.qmd#param) \| None  
The curve interpolation method; defaults to *linear*.

`tension` float \| [Param](inspect_viz.qmd#param) \| None  
The tension option only has an effect on bundle, cardinal and
Catmull–Rom splines.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### delaunay_mesh

Create a Delaunay mesh mark that draws a mesh of the Delaunay
triangulation.

The delaunayMesh mark computes the Delaunay triangulation of the data
and draws filled triangular polygons for each triangle in the
triangulation. This creates a continuous mesh surface useful for spatial
interpolation and surface visualization.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_delaunay.py#L70)

``` python
def delaunay_mesh(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel, typically bound to the *y* scale.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping to produce multiple (possibly
overlapping) triangulations.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for marker_start, marker_mid, and
marker_end.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the starting point of a line segment.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for any middle (interior) points of a line segment.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the ending point of a line segment.

`curve` [Curve](inspect_viz.mark.qmd#curve) \| [Param](inspect_viz.qmd#param) \| None  
The curve interpolation method; defaults to *linear*.

`tension` float \| [Param](inspect_viz.qmd#param) \| None  
The tension option only has an effect on bundle, cardinal and
Catmull–Rom splines.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### voronoi

Create a Voronoi mark that draws polygons for each cell of the Voronoi
tessellation.

The voronoi mark computes the Voronoi tessellation (also known as
Thiessen polygons) of the data points and draws filled polygons for each
cell. Each cell contains all points that are closer to the cell’s
generator point than to any other generator.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_delaunay.py#L182)

``` python
def voronoi(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel, typically bound to the *y* scale.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping to produce multiple
tessellations.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for marker_start, marker_mid, and
marker_end.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the starting point of a line segment.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for any middle (interior) points of a line segment.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the ending point of a line segment.

`curve` [Curve](inspect_viz.mark.qmd#curve) \| [Param](inspect_viz.qmd#param) \| None  
The curve interpolation method; defaults to *linear*.

`tension` float \| [Param](inspect_viz.qmd#param) \| None  
The tension option only has an effect on bundle, cardinal and
Catmull–Rom splines.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### voronoi_mesh

Create a Voronoi mesh mark that draws a mesh for the cell boundaries of
the Voronoi tessellation.

The voronoiMesh mark computes the Voronoi tessellation of the data
points and draws line segments for the boundaries between cells. This
creates a mesh of cell edges useful for visualizing the spatial
partitioning without filled polygons.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_delaunay.py#L237)

``` python
def voronoi_mesh(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel, typically bound to the *y* scale.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping to produce multiple
tessellations.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for marker_start, marker_mid, and
marker_end.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the starting point of a line segment.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for any middle (interior) points of a line segment.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the ending point of a line segment.

`curve` [Curve](inspect_viz.mark.qmd#curve) \| [Param](inspect_viz.qmd#param) \| None  
The curve interpolation method; defaults to *linear*.

`tension` float \| [Param](inspect_viz.qmd#param) \| None  
The tension option only has an effect on bundle, cardinal and
Catmull–Rom splines.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### hull

Create a hull mark that draws a convex hull around points.

The hull mark computes the convex hull of the data points and draws a
polygon representing the smallest convex shape that contains all the
points. This is useful for showing the overall extent or boundary of a
point cloud.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_delaunay.py#L126)

``` python
def hull(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    curve: Curve | Param | None = None,
    tension: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel, typically bound to the *y* scale.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping to produce multiple hulls;
defaults to fill or stroke channel if not specified.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for marker_start, marker_mid, and
marker_end.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the starting point of a line segment.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for any middle (interior) points of a line segment.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker for the ending point of a line segment.

`curve` [Curve](inspect_viz.mark.qmd#curve) \| [Param](inspect_viz.qmd#param) \| None  
The curve interpolation method; defaults to *linear*.

`tension` float \| [Param](inspect_viz.qmd#param) \| None  
The tension option only has an effect on bundle, cardinal and
Catmull–Rom splines.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### dense_line

Create a dense line mark that plots line densities rather than point
densities.

The denseLine mark forms a binned raster grid and “draws” straight lines
into it, creating a density visualization of line segments rather than
individual points. This is useful for visualizing the density of linear
features, trajectories, or paths in spatial data.

The mark bins the data into a 2D grid and renders density values as a
raster image. Unlike traditional line marks that use curve
interpolation, dense lines operate on a pixel grid to accumulate line
density information.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_dense.py#L14)

``` python
def dense_line(
    data: Data,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    bandwidth: float | Param | None = None,
    normalize: bool | Param | None = None,
    interpolate: Interpolate | Param | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    pixel_size: float | Param | None = None,
    pad: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.
Domain values are binned into a grid with *width* horizontal bins.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale. Domain
values are binned into a grid with *height* vertical bins.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An ordinal channel for grouping data into series to be drawn as separate
lines.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`bandwidth` float \| [Param](inspect_viz.qmd#param) \| None  
The kernel density bandwidth for smoothing, in pixels.

`normalize` bool \| [Param](inspect_viz.qmd#param) \| None  
Flag to perform approximate arc length normalization of line segments to
prevent artifacts due to overcounting steep lines; defaults to True.

`interpolate` [Interpolate](inspect_viz.mark.qmd#interpolate) \| [Param](inspect_viz.qmd#param) \| None  
The spatial interpolation method; one of: - *none* - do not perform
interpolation (the default) - *linear* - apply proportional linear
interpolation across adjacent bins - *nearest* - assign each pixel to
the closest sample’s value (Voronoi diagram) - *barycentric* - apply
barycentric interpolation over the Delaunay triangulation -
*random-walk* - apply a random walk from each pixel

`width` float \| [Param](inspect_viz.qmd#param) \| None  
The width (number of columns) of the grid, in actual pixels.

`height` float \| [Param](inspect_viz.qmd#param) \| None  
The height (number of rows) of the grid, in actual pixels.

`pixel_size` float \| [Param](inspect_viz.qmd#param) \| None  
The effective screen size of a raster pixel, used to determine the
height and width of the raster from the frame’s dimensions; defaults to
1.

`pad` float \| [Param](inspect_viz.qmd#param) \| None  
The bin padding, one of 1 (default) to include extra padding for the
final bin, or 0 to make the bins flush with the maximum domain value.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions. Note that fill and fillOpacity
can use the special value “density” to map computed density values to
visual properties.

## Decoration

### title

Create a plot title mark.

Adds a title at the top of the plot frame.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_title.py#L29)

``` python
def title(
    title: str,
    margin_top: int = 15,
    font_size: float | None = 16,
    font_family: str | None = None,
    font_weight: float | None = None,
) -> Title
```

`title` str  
Title text.

`margin_top` int  
Top margin fot title (defaults to 10 pixels). You may need to increase
this if there are facet labels on the x-axis that the title needs to be
placed above.

`font_size` float \| None  
The font size in pixels (defaults to 14)

`font_family` str \| None  
The font-family (defaults to the plot’s font family, which is typically
*system-ui*”)

`font_weight` float \| None  
The font weight (defaults to the plot’s font weight, which is typically
400.”

### frame

Create a frame mark that draws a rectangular outline around the plot
area.

The frame mark draws a rectangular border around the plot’s frame area.
By default, it draws a complete rectangular outline, but when an anchor
is specified, it draws only a line on the given side (ignoring rx, ry,
fill, and fillOpacity).

The frame mark is commonly used for visual separation of facets,
providing backgrounds for plot areas, or creating borders around
visualizations.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_frame.py#L11)

``` python
def frame(
    anchor: Literal["top", "right", "bottom", "left"] | Param | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: str | float | Param | None = None,
    ry: str | float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`anchor` Literal\['top', 'right', 'bottom', 'left'\] \| [Param](inspect_viz.qmd#param) \| None  
Controls how the frame is drawn. If null (default), draws a complete
rectangular outline. If specified, draws a line only on the given side
(*top*, *right*, *bottom*, or *left*), ignoring rx, ry, fill, and
fillOpacity.

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for all four insets.

`inset_top` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the top edge by the specified number of pixels. A positive value
insets towards the bottom edge (reducing effective area), while a
negative value insets away from the bottom edge (increasing it).

`inset_right` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the right edge by the specified number of pixels. A positive
value insets towards the left edge (reducing effective area), while a
negative value insets away from the left edge (increasing it).

`inset_bottom` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the bottom edge by the specified number of pixels. A positive
value insets towards the top edge (reducing effective area), while a
negative value insets away from the top edge (increasing it).

`inset_left` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the left edge by the specified number of pixels. A positive value
insets towards the right edge (reducing effective area), while a
negative value insets away from the right edge (increasing it).

`rx` str \| float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner x-radius, either in pixels or as a percentage of the
frame width. If rx is not specified, it defaults to ry if present, and
otherwise draws square corners.

`ry` str \| float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner y-radius, either in pixels or as a percentage of the
frame height. If ry is not specified, it defaults to rx if present, and
otherwise draws square corners.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### axis_x

A horizontal axis mark.

The axisX mark draws a horizontal axis at the bottom or top of the plot
(or both). It is primarily used for displaying scales and reference
lines along the x-axis.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_axis.py#L16)

``` python
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
) -> Mark
```

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`interval` Interval \| None  
How to convert a continuous value into an interval.

`text` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The text channel for tick labels.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor specifies defaults for **x** and **y** based on the
plot’s frame.

`line_anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The line anchor controls how text is aligned relative to its anchor
point.

`rotate` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle of the axis in degrees clockwise.

`text_stroke` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The stroke color for text labels.

`text_stroke_opacity` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The stroke opacity for text labels.

`text_stroke_width` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The stroke width for text labels.

`styles` [TextStyles](inspect_viz.mark.qmd#textstyles) \| None  
`TextStyles` to apply to axis text.

`anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The side of the frame on which to place the axis (*top* or *bottom*).

`color` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| str \| [Param](inspect_viz.qmd#param) \| None  
Shorthand for setting both fill and stroke color.

`ticks` int \| Sequence\[Any\] \| [Param](inspect_viz.qmd#param) \| None  
The desired number of ticks, or an array of tick values, or null to
disable ticks.

`tick_spacing` float \| [Param](inspect_viz.qmd#param) \| None  
The desired spacing between ticks in pixels.

`tick_size` float \| [Param](inspect_viz.qmd#param) \| None  
The length of tick marks in pixels.

`tick_padding` float \| [Param](inspect_viz.qmd#param) \| None  
The distance between the tick mark and its label in pixels.

`tick_format` str \| [Param](inspect_viz.qmd#param) \| None  
A d3-format string for formatting tick labels.

`tick_rotate` float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle of tick labels in degrees clockwise.

`label` str \| [Param](inspect_viz.qmd#param) \| None  
The axis label text.

`label_offset` float \| [Param](inspect_viz.qmd#param) \| None  
The distance between the axis and its label in pixels.

`label_anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The label anchor position.

`label_arrow` str \| bool \| [Param](inspect_viz.qmd#param) \| None  
Whether to show an arrow on the axis label.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### axis_y

A vertical axis mark.

The axisY mark draws a vertical axis at the left or right of the plot
(or both). It is primarily used for displaying scales and reference
lines along the y-axis.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_axis.py#L101)

``` python
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
) -> Mark
```

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`interval` Interval \| None  
How to convert a continuous value into an interval.

`text` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The text channel for tick labels.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor specifies defaults for **x** and **y** based on the
plot’s frame.

`line_anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The line anchor controls how text is aligned relative to its anchor
point.

`rotate` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle of the axis in degrees clockwise.

`text_stroke` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The stroke color for text labels.

`text_stroke_opacity` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The stroke opacity for text labels.

`text_stroke_width` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The stroke width for text labels.

`styles` [TextStyles](inspect_viz.mark.qmd#textstyles) \| None  
`TextStyles` to apply to axis text.

`anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The side of the frame on which to place the axis (*left* or *right*).

`color` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| str \| [Param](inspect_viz.qmd#param) \| None  
Shorthand for setting both fill and stroke color.

`ticks` int \| Sequence\[Any\] \| [Param](inspect_viz.qmd#param) \| None  
The desired number of ticks, or an array of tick values, or null to
disable ticks.

`tick_spacing` float \| [Param](inspect_viz.qmd#param) \| None  
The desired spacing between ticks in pixels.

`tick_size` float \| [Param](inspect_viz.qmd#param) \| None  
The length of tick marks in pixels.

`tick_padding` float \| [Param](inspect_viz.qmd#param) \| None  
The distance between the tick mark and its label in pixels.

`tick_format` str \| [Param](inspect_viz.qmd#param) \| None  
A d3-format string for formatting tick labels.

`tick_rotate` float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle of tick labels in degrees clockwise.

`label` str \| [Param](inspect_viz.qmd#param) \| None  
The axis label text.

`label_offset` float \| [Param](inspect_viz.qmd#param) \| None  
The distance between the axis and its label in pixels.

`label_anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The label anchor position.

`label_arrow` str \| bool \| [Param](inspect_viz.qmd#param) \| None  
Whether to show an arrow on the axis label.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### axis_fx

A horizontal facet axis mark.

The axisFx mark draws a horizontal axis for faceted plots. It is
primarily used for displaying scales and reference lines along the
fx-axis in faceted visualizations.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_axis.py#L186)

``` python
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
) -> Mark
```

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`interval` Interval \| None  
How to convert a continuous value into an interval.

`text` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The text channel for tick labels.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor specifies defaults for **x** and **y** based on the
plot’s frame.

`line_anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The line anchor controls how text is aligned relative to its anchor
point.

`rotate` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle of the axis in degrees clockwise.

`text_stroke` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The stroke color for text labels.

`text_stroke_opacity` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The stroke opacity for text labels.

`text_stroke_width` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The stroke width for text labels.

`styles` [TextStyles](inspect_viz.mark.qmd#textstyles) \| None  
`TextStyles` to apply to axis text.

`anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The side of the frame on which to place the axis (*top* or *bottom*).

`color` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| str \| [Param](inspect_viz.qmd#param) \| None  
Shorthand for setting both fill and stroke color.

`ticks` int \| Sequence\[Any\] \| [Param](inspect_viz.qmd#param) \| None  
The desired number of ticks, or an array of tick values, or null to
disable ticks.

`tick_spacing` float \| [Param](inspect_viz.qmd#param) \| None  
The desired spacing between ticks in pixels.

`tick_size` float \| [Param](inspect_viz.qmd#param) \| None  
The length of tick marks in pixels.

`tick_padding` float \| [Param](inspect_viz.qmd#param) \| None  
The distance between the tick mark and its label in pixels.

`tick_format` str \| [Param](inspect_viz.qmd#param) \| None  
A d3-format string for formatting tick labels.

`tick_rotate` float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle of tick labels in degrees clockwise.

`label` str \| [Param](inspect_viz.qmd#param) \| None  
The axis label text.

`label_offset` float \| [Param](inspect_viz.qmd#param) \| None  
The distance between the axis and its label in pixels.

`label_anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The label anchor position.

`label_arrow` str \| bool \| [Param](inspect_viz.qmd#param) \| None  
Whether to show an arrow on the axis label.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### axis_fy

A vertical facet axis mark.

The axisFy mark draws a vertical axis for faceted plots. It is primarily
used for displaying scales and reference lines along the fy-axis in
faceted visualizations.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_axis.py#L271)

``` python
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
) -> Mark
```

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`interval` Interval \| None  
How to convert a continuous value into an interval.

`text` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The text channel for tick labels.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor specifies defaults for **x** and **y** based on the
plot’s frame.

`line_anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The line anchor controls how text is aligned relative to its anchor
point.

`rotate` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle of the axis in degrees clockwise.

`text_stroke` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The stroke color for text labels.

`text_stroke_opacity` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The stroke opacity for text labels.

`text_stroke_width` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The stroke width for text labels.

`styles` [TextStyles](inspect_viz.mark.qmd#textstyles) \| None  
`TextStyles` to apply to axis text.

`anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The side of the frame on which to place the axis (*left* or *right*).

`color` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| str \| [Param](inspect_viz.qmd#param) \| None  
Shorthand for setting both fill and stroke color.

`ticks` int \| Sequence\[Any\] \| [Param](inspect_viz.qmd#param) \| None  
The desired number of ticks, or an array of tick values, or null to
disable ticks.

`tick_spacing` float \| [Param](inspect_viz.qmd#param) \| None  
The desired spacing between ticks in pixels.

`tick_size` float \| [Param](inspect_viz.qmd#param) \| None  
The length of tick marks in pixels.

`tick_padding` float \| [Param](inspect_viz.qmd#param) \| None  
The distance between the tick mark and its label in pixels.

`tick_format` str \| [Param](inspect_viz.qmd#param) \| None  
A d3-format string for formatting tick labels.

`tick_rotate` float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle of tick labels in degrees clockwise.

`label` str \| [Param](inspect_viz.qmd#param) \| None  
The axis label text.

`label_offset` float \| [Param](inspect_viz.qmd#param) \| None  
The distance between the axis and its label in pixels.

`label_anchor` str \| [Param](inspect_viz.qmd#param) \| None  
The label anchor position.

`label_arrow` str \| bool \| [Param](inspect_viz.qmd#param) \| None  
Whether to show an arrow on the axis label.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### rule_x

A ruleX mark that draws horizontal rule lines.

RuleX marks are horizontal lines that span the full extent of the plot
area, typically used for reference lines, grid lines, or highlighting
specific values.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_rule.py#L15)

``` python
def rule_x(
    data: Data | None = None,
    x: ChannelSpec | Param | None = None,
    y: ChannelIntervalSpec | Param | None = None,
    y1: ChannelSpec | Param | None = None,
    y2: ChannelSpec | Param | None = None,
    filter_by: Selection | None = None,
    interval: Interval | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    inset: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data) \| None  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`y1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The primary (starting, often bottom) vertical position of the tick; a
channel bound to the *y* scale.

`y2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The secondary (ending, often top) vertical position of the tick; a
channel bound to the *y* scale.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`interval` Interval \| None  
How to convert a continuous value into an interval.

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at all positions along the rule.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the start of the rule.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the middle of the rule.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the end of the rule.

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Set top and bottom insets.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### rule_y

A ruleY mark that draws vertical rule lines.

RuleY marks are vertical lines that span the full extent of the plot
area, typically used for reference lines, grid lines, or highlighting
specific values.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_rule.py#L72)

``` python
def rule_y(
    data: Data | None = None,
    y: ChannelSpec | Param | None = None,
    x: ChannelIntervalSpec | Param | None = None,
    x1: ChannelSpec | Param | None = None,
    x2: ChannelSpec | Param | None = None,
    filter_by: Selection | None = None,
    interval: Interval | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    inset: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data) \| None  
The data source for the mark.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`x` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`x1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The primary (starting, often left) horizontal position of the tick; a
channel bound to the *x* scale.

`x2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The secondary (ending, often right) horizontal position of the tick; a
channel bound to the *x* scale.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`interval` Interval \| None  
How to convert a continuous value into an interval.

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at all positions along the rule.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the start of the rule.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the middle of the rule.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the end of the rule.

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Set left and right insets.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### tick_x

A tickX mark that draws horizontal tick marks.

TickX marks are horizontal lines typically used for marking positions
along the x-axis or creating horizontal reference lines.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_tick.py#L15)

``` python
def tick_x(
    data: Data,
    x: ChannelSpec | Param,
    y: ChannelSpec | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at all positions along the tick.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the start of the tick.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the middle of the tick.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the end of the tick.

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for top and bottom insets.

`inset_top` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the top edge by the specified number of pixels.

`inset_bottom` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the bottom edge by the specified number of pixels.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### tick_y

A tickY mark that draws vertical tick marks.

TickY marks are vertical lines typically used for marking positions
along the y-axis or creating vertical reference lines.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_tick.py#L69)

``` python
def tick_y(
    data: Data,
    y: ChannelSpec | Param,
    x: ChannelSpec | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    inset: float | Param | None = None,
    inset_left: float | Param | None = None,
    inset_right: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel, typically bound to the *y* scale.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`marker` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at all positions along the tick.

`marker_start` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the start of the tick.

`marker_mid` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the middle of the tick.

`marker_end` [Marker](inspect_viz.mark.qmd#marker) \| bool \| [Param](inspect_viz.qmd#param) \| None  
The marker symbol to use at the end of the tick.

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for left and right insets.

`inset_left` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the left edge by the specified number of pixels.

`inset_right` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the right edge by the specified number of pixels.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### rect

A rect mark that draws axis-aligned rectangles.

Both *x* and *y* should be quantitative or temporal; rect does not
perform grouping, so use rectX or rectY for ordinal data.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_rect.py#L15)

``` python
def rect(
    data: Data,
    x: ChannelIntervalSpec | Param | None = None,
    x1: ChannelSpec | Param | None = None,
    x2: ChannelSpec | Param | None = None,
    y: ChannelIntervalSpec | Param | None = None,
    y1: ChannelSpec | Param | None = None,
    y2: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    interval: Interval | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`x1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The starting horizontal position channel, typically bound to the *x*
scale.

`x2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The ending horizontal position channel, typically bound to the *x*
scale.

`y` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`y1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The starting vertical position channel, typically bound to the *y*
scale.

`y2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The ending vertical position channel, typically bound to the *y* scale.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
The **z** channel defines the series of each value in the stack

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`interval` Interval \| None  
How to convert a continuous value into an interval; one of: - a named
time interval such as *day* (for date intervals) - a number (for number
intervals), defining intervals at integer multiples of *n*

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for all four insets.

`inset_top` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the top edge by the specified number of pixels.

`inset_right` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the right edge by the specified number of pixels.

`inset_bottom` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the bottom edge by the specified number of pixels.

`inset_left` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the left edge by the specified number of pixels.

`rx` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner x-radius, either in pixels or as a percentage of the
rect width.

`ry` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner y-radius, either in pixels or as a percentage of the
rect height.

`offset` Literal\['center', 'normalize', 'wiggle'\] \| [Param](inspect_viz.qmd#param) \| None  
After stacking, an optional **offset** can be applied to translate and
scale stacks.

`order` Literal\['value', 'x', 'y', 'z', 'sum', 'appearance', 'inside-out'\] \| str \| Sequence\[float \| bool\] \| [Param](inspect_viz.qmd#param) \| None  
The order in which stacks are layered; one of: - null (default) for
input order - a named stack order method such as *inside-out* or *sum* -
a field name, for natural order of the corresponding values - a function
of data, for natural order of the corresponding values - an array of
explicit **z** values in the desired order.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### rect_x

A rectX mark that draws axis-aligned rectangles.

The *x* values should be quantitative or temporal, and the optional *y*
values should be ordinal.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_rect.py#L104)

``` python
def rect_x(
    data: Data,
    x: ChannelSpec | Param | None = None,
    x1: ChannelSpec | Param | None = None,
    x2: ChannelSpec | Param | None = None,
    y: ChannelIntervalSpec | Param | None = None,
    y1: ChannelSpec | Param | None = None,
    y2: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    interval: Interval | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`x1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The starting horizontal position channel, typically bound to the *x*
scale.

`x2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The ending horizontal position channel, typically bound to the *x*
scale.

`y` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`y1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The starting vertical position channel, typically bound to the *y*
scale.

`y2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The ending vertical position channel, typically bound to the *y* scale.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
The **z** channel defines the series of each value in the stack.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`interval` Interval \| None  
How to convert a continuous value into an interval; one of: - a named
time interval such as *day* (for date intervals) - a number (for number
intervals), defining intervals at integer multiples of *n*

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for all four insets.

`inset_top` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the top edge by the specified number of pixels.

`inset_right` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the right edge by the specified number of pixels.

`inset_bottom` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the bottom edge by the specified number of pixels.

`inset_left` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the left edge by the specified number of pixels.

`rx` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner x-radius, either in pixels or as a percentage of the
rect width.

`ry` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner y-radius, either in pixels or as a percentage of the
rect height.

`offset` Literal\['center', 'normalize', 'wiggle'\] \| [Param](inspect_viz.qmd#param) \| None  
After stacking, an optional **offset** can be applied to translate and
scale stacks.

`order` Literal\['value', 'x', 'y', 'z', 'sum', 'appearance', 'inside-out'\] \| str \| Sequence\[float \| bool\] \| [Param](inspect_viz.qmd#param) \| None  
The order in which stacks are layered; one of: - null (default) for
input order - a named stack order method such as *inside-out* or *sum* -
a field name, for natural order of the corresponding values - a function
of data, for natural order of the corresponding values - an array of
explicit **z** values in the desired order

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### rect_y

A rectY mark that draws axis-aligned rectangles.

The *y* values should be quantitative or temporal, and the optional *x*
values should be ordinal.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_rect.py#L192)

``` python
def rect_y(
    data: Data,
    x: ChannelIntervalSpec | Param | None = None,
    x1: ChannelSpec | Param | None = None,
    x2: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    y1: ChannelSpec | Param | None = None,
    y2: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    interval: Interval | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: float | Param | None = None,
    ry: float | Param | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`x1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The starting horizontal position channel, typically bound to the *x*
scale.

`x2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The ending horizontal position channel, typically bound to the *x*
scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`y1` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The starting vertical position channel, typically bound to the *y*
scale.

`y2` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The ending vertical position channel, typically bound to the *y* scale.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
The **z** channel defines the series of each value in the stack.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data.

`interval` Interval \| None  
How to convert a continuous value into an interval; one of: - a named
time interval such as *day* (for date intervals) - a number (for number
intervals), defining intervals at integer multiples of *n*

`inset` float \| [Param](inspect_viz.qmd#param) \| None  
Shorthand to set the same default for all four insets.

`inset_top` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the top edge by the specified number of pixels.

`inset_right` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the right edge by the specified number of pixels.

`inset_bottom` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the bottom edge by the specified number of pixels.

`inset_left` float \| [Param](inspect_viz.qmd#param) \| None  
Insets the left edge by the specified number of pixels.

`rx` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner x-radius, either in pixels or as a percentage of the
rect width.

`ry` float \| [Param](inspect_viz.qmd#param) \| None  
The rounded corner y-radius, either in pixels or as a percentage of the
rect height.

`offset` Literal\['center', 'normalize', 'wiggle'\] \| [Param](inspect_viz.qmd#param) \| None  
After stacking, an optional **offset** can be applied to translate and
scale stacks.

`order` Literal\['value', 'x', 'y', 'z', 'sum', 'appearance', 'inside-out'\] \| str \| Sequence\[float \| bool\] \| [Param](inspect_viz.qmd#param) \| None  
The order in which stacks are layered; one of: - null (default) for
input order - a named stack order method such as *inside-out* or *sum* -
a field name, for natural order of the corresponding values - a function
of data, for natural order of the corresponding values - an array of
explicit **z** values in the desired order

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

### text

A text mark that displays textual labels.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_text.py#L18)

``` python
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
) -> Mark
```

`data` [Data](inspect_viz.qmd#data) \| None  
The data source for the mark (not required if not binding `text` to a
column). If None, any of x, y, z, text can be provided as sequences.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel specifying the text’s anchor point,
typically bound to the *x* scale. When data is None, can be a sequence
of x-coordinates.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel specifying the text’s anchor point,
typically bound to the *y* scale. When data is None, can be a sequence
of y-coordinates.

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series. When data is
None, can be a sequence of z-values.

`text` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
The text contents channel, possibly with line breaks (, , or . When data
is None, can be a sequence of text values. To place a single piece of
text specify the text as a string\[\] (e.g. `["My Text"]`).

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor specifies defaults for **x** and **y**, along with
**textAnchor** and **lineAnchor**, based on the plot’s frame; it may be
one of the four sides (*top*, *right*, *bottom*, *left*), one of the
four corners (*top-left*, *top-right*, *bottom-right*, *bottom-left*),
or the *middle* of the frame.

`line_anchor` [LineAnchor](inspect_viz.mark.qmd#lineanchor) \| [Param](inspect_viz.qmd#param) \| None  
The line anchor controls how text is aligned (typically vertically)
relative to its anchor point; it is one of *top*, *bottom*, or *middle*.
If the frame anchor is *top*, *top-left*, or *top-right*, the default
line anchor is *top*; if the frame anchor is *bottom*, *bottom-right*,
or *bottom-left*, the default is *bottom*; otherwise it is *middle*.

`rotate` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle in degrees clockwise; a constant or a channel;
defaults to 0°. When a number, it is interpreted as a constant;
otherwise it is interpreted as a channel.

`styles` [TextStyles](inspect_viz.mark.qmd#textstyles) \| None  
`TextStyles` to apply.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### text_x

A horizontal text mark that displays textual labels.

Like text, except that **y** defaults to the zero-based index of the
data \[0, 1, 2, …\].

If an **interval** is specified, such as *day*, **y** is transformed to
the middle of the interval.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_text.py#L65)

``` python
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
) -> Mark
```

`data` [Data](inspect_viz.qmd#data) \| None  
The data source for the mark. If None, any of x, y, z, text can be
provided as sequences.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The horizontal position channel specifying the text’s anchor point,
typically bound to the *x* scale. When data is None, can be a sequence
of x-coordinates.

`y` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel specifying the text’s anchor point,
typically bound to the *y* scale; defaults to the zero-based index of
the data \[0, 1, 2, …\].

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series. When data is
None, can be a sequence of z-values.

`text` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
The text contents channel, possibly with line breaks (, , or . When data
is None, can be a sequence of text values. If not specified, defaults to
the zero-based index \[0, 1, 2, …\].

`interval` Interval \| [Param](inspect_viz.qmd#param) \| None  
An interval (such as *day* or a number), to transform **y** values to
the middle of the interval.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor specifies defaults for **x** and **y**, along with
**textAnchor** and **lineAnchor**, based on the plot’s frame; it may be
one of the four sides (*top*, *right*, *bottom*, *left*), one of the
four corners (*top-left*, *top-right*, *bottom-right*, *bottom-left*),
or the *middle* of the frame.

`line_anchor` [LineAnchor](inspect_viz.mark.qmd#lineanchor) \| [Param](inspect_viz.qmd#param) \| None  
The line anchor controls how text is aligned (typically vertically)
relative to its anchor point; it is one of *top*, *bottom*, or *middle*.
If the frame anchor is *top*, *top-left*, or *top-right*, the default
line anchor is *top*; if the frame anchor is *bottom*, *bottom-right*,
or *bottom-left*, the default is *bottom*; otherwise it is *middle*.

`rotate` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle in degrees clockwise; a constant or a channel;
defaults to 0°. When a number, it is interpreted as a constant;
otherwise it is interpreted as a channel.

`styles` [TextStyles](inspect_viz.mark.qmd#textstyles) \| None  
`TextStyles` to apply.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### text_y

A vertical text mark that displays textual labels.

Like text, except that **x** defaults to the zero-based index of the
data \[0, 1, 2, …\].

If an **interval** is specified, such as *day*, **x** is transformed to
the middle of the interval.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_text.py#L119)

``` python
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
) -> Mark
```

`data` [Data](inspect_viz.qmd#data) \| None  
The data source for the mark. If None, any of x, y, z, text can be
provided as sequences.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
The vertical position channel specifying the text’s anchor point,
typically bound to the *y* scale. When data is None, can be a sequence
of y-coordinates.

`x` [ChannelIntervalSpec](inspect_viz.mark.qmd#channelintervalspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel specifying the text’s anchor point,
typically bound to the *x* scale; defaults to the zero-based index of
the data \[0, 1, 2, …\].

`z` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
An optional ordinal channel for grouping data into series. When data is
None, can be a sequence of z-values.

`text` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
The text contents channel, possibly with line breaks (, , or . When data
is None, can be a sequence of text values. If not specified, defaults to
the zero-based index \[0, 1, 2, …\].

`interval` Interval \| [Param](inspect_viz.qmd#param) \| None  
An interval (such as *day* or a number), to transform **x** values to
the middle of the interval.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor specifies defaults for **x** and **y**, along with
**textAnchor** and **lineAnchor**, based on the plot’s frame; it may be
one of the four sides (*top*, *right*, *bottom*, *left*), one of the
four corners (*top-left*, *top-right*, *bottom-right*, *bottom-left*),
or the *middle* of the frame.

`line_anchor` [LineAnchor](inspect_viz.mark.qmd#lineanchor) \| [Param](inspect_viz.qmd#param) \| None  
The line anchor controls how text is aligned (typically vertically)
relative to its anchor point; it is one of *top*, *bottom*, or *middle*.
If the frame anchor is *top*, *top-left*, or *top-right*, the default
line anchor is *top*; if the frame anchor is *bottom*, *bottom-right*,
or *bottom-left*, the default is *bottom*; otherwise it is *middle*.

`rotate` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle in degrees clockwise; a constant or a channel;
defaults to 0°. When a number, it is interpreted as a constant;
otherwise it is interpreted as a channel.

`styles` [TextStyles](inspect_viz.mark.qmd#textstyles) \| None  
`TextStyles` to apply.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional `MarkOptions`.

### image

Create an image mark for displaying images in visualizations.

The image mark displays raster images (PNG, JPEG, etc.) at specified
positions and sizes. Images can be positioned using x/y coordinates,
sized with width/height, and styled with various options including
aspect ratio preservation and rendering modes.

This mark is useful for: - Adding logos, icons, or other imagery to
visualizations - Creating image-based scatter plots or dashboards -
Displaying photographs or other raster content within plots

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_image.py#L15)

``` python
def image(
    data: Data,
    x: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    filter_by: Selection | None = None,
    width: Channel | float | Param | None = None,
    height: Channel | float | Param | None = None,
    r: Channel | float | Param | None = None,
    rotate: Channel | float | Param | None = None,
    src: Channel | str | Param | None = None,
    preserve_aspect_ratio: str | Param | None = None,
    cross_origin: str | Param | None = None,
    frame_anchor: FrameAnchor | Param | None = None,
    image_rendering: str | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The horizontal position channel, typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param) \| None  
The vertical position channel, typically bound to the *y* scale.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`width` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The image width in pixels. When a number, it is interpreted as a
constant; otherwise it is interpreted as a channel. Defaults to 16 if
neither width nor height are set.

`height` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The image height in pixels. When a number, it is interpreted as a
constant; otherwise it is interpreted as a channel. Defaults to 16 if
neither width nor height are set.

`r` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The image clip radius for circular images. If null (default), images are
not clipped; when a number, it is interpreted as a constant in pixels;
otherwise it is interpreted as a channel.

`rotate` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param) \| None  
The rotation angle in degrees clockwise.

`src` [Channel](inspect_viz.mark.qmd#channel) \| str \| [Param](inspect_viz.qmd#param) \| None  
The required image URL (or relative path). If a string that starts with
a dot, slash, or URL protocol it is assumed to be a constant; otherwise
it is interpreted as a channel.

`preserve_aspect_ratio` str \| [Param](inspect_viz.qmd#param) \| None  
The image aspect ratio; defaults to “xMidYMid meet”. To crop the image
instead of scaling it to fit, use “xMidYMid slice”.

`cross_origin` str \| [Param](inspect_viz.qmd#param) \| None  
The cross-origin behavior for loading images from external domains.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param) \| None  
The frame anchor position for legend placement.

`image_rendering` str \| [Param](inspect_viz.qmd#param) \| None  
The image-rendering attribute; defaults to “auto” (bilinear). May be set
to “pixelated” to disable bilinear interpolation for a sharper image.

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions.

## Geographic

### geo

Create a geo mark for rendering geographic data.

The geo mark renders geographic data, typically GeoJSON objects, with
support for map projections and geographic styling. It’s designed for
displaying geographic features like countries, states, cities, or any
spatial geometry.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_geo.py#L13)

``` python
def geo(
    data: Data,
    geometry: Channel | Param | None = None,
    r: ChannelSpec | float | Param | None = None,
    filter_by: Selection | None = None,
    **options: Unpack[MarkOptions],
) -> Mark
```

`data` [Data](inspect_viz.qmd#data)  
The data source for the mark.

`geometry` [Channel](inspect_viz.mark.qmd#channel) \| [Param](inspect_viz.qmd#param) \| None  
A channel for the geometry to render; defaults to identity, assuming
data is a GeoJSON object or iterable of GeoJSON objects. Supports
various geographic data types and transformations.

`r` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| float \| [Param](inspect_viz.qmd#param) \| None  
The radius channel for point geometries, typically bound to the *radius*
scale.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
Selection to filter by (defaults to data source selection).

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Additional mark options from MarkOptions. Note that clip can be set to
“sphere” for projection-aware clipping when using spherical projections.

### graticule

Create a graticule mark that renders a global coordinate grid.

The graticule mark renders a 10° global graticule (coordinate grid)
showing lines of longitude and latitude. This provides a reference grid
for geographic visualizations and helps users understand the projection
and scale.

This mark is particularly useful for: - Adding coordinate reference
lines to world maps - Showing distortion in map projections - Providing
spatial reference for geographic data

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_geo.py#L77)

``` python
def graticule(
    **options: Unpack[MarkOptions],
) -> Mark
```

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Options from MarkOptions. Note that this mark is designed for use with
spherical projections only.

### sphere

Create a sphere mark that renders the outline of the projection sphere.

The sphere mark renders the outline of the sphere on the projection’s
plane. This is typically used with spherical projections to show the
boundary of the projected world. The sphere mark automatically generates
the appropriate geometry for the current projection.

This mark is particularly useful for: - Adding a border around world
maps with spherical projections - Showing the extent of the projection -
Creating a background for geographic visualizations

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_geo.py#L52)

``` python
def sphere(
    **options: Unpack[MarkOptions],
) -> Mark
```

`**options` Unpack\[[MarkOptions](inspect_viz.mark.qmd#markoptions)\]  
Options from MarkOptions. Note that this mark is designed for use with
spherical projections only.

## Types

### Mark

Plot mark (create marks using mark functions, e.g. `dot()`, `bar_x()`,
etc.).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_mark.py#L15)

``` python
class Mark(Component)
```

### MarkOptions

Shared options for all marks.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_options.py#L8)

``` python
class MarkOptions(TypedDict, total=False)
```

#### Attributes

`filter` [Channel](inspect_viz.mark.qmd#channel)  
Applies a transform to filter the mark’s index according to the given
channel values; only truthy values are retained.

`select` Literal\['first', 'last', 'maxX', 'maxY', 'minX', 'minY', 'nearest', 'nearestX', 'nearestY'\]  
Applies a filter transform after data is loaded to highlight selected
values only. For example, `first` and `last` select the first or last
values of series only (using the *z* channel to separate series).
Meanwhile, `nearestX` and `nearestY` select the point nearest to the
pointer along the *x* or *y* channel dimension. Unlike Mosaic
selections, a mark level *select* is internal to the mark only, and does
not populate a param or selection value to be shared across clients.

`reverse` bool \| [Param](inspect_viz.qmd#param)  
Applies a transform to reverse the order of the mark’s index, say for
reverse input order.

`sort` SortOrder  
Sort order for a plot mark’s index.

`fx` [Channel](inspect_viz.mark.qmd#channel)  
The horizontal facet position channel, for mark-level faceting, bound to
the *fx* scale

`fy` [Channel](inspect_viz.mark.qmd#channel)  
The vertical facet position channel, for mark-level faceting, bound to
the *fy* scale.

`facet` Literal\['auto', 'include', 'exclude', 'super'\] \| bool \| None \| [Param](inspect_viz.qmd#param)  
Whether to enable or disable faceting.

- *auto* (default) - automatically determine if this mark should be
  faceted
- *include* (or `True`) - draw the subset of the mark’s data in the
  current facet
- *exclude* - draw the subset of the mark’s data *not* in the current
  facet
- *super* - draw this mark in a single frame that covers all facets
- null (or `False`) - repeat this mark’s data across all facets (*i.e.*,
  no faceting)

When a mark uses *super* faceting, it is not allowed to use position
scales (*x*, *y*, *fx*, or *fy*); *super* faceting is intended for
decorations, such as labels and legends.

When top-level faceting is used, the default *auto* setting is
equivalent to *include* when the mark data is strictly equal to the
top-level facet data; otherwise it is equivalent to null. When the
*include* or *exclude* facet mode is chosen, the mark data must be
parallel to the top-level facet data: the data must have the same length
and order. If the data are not parallel, then the wrong data may be
shown in each facet. The default *auto* therefore requires strict
equality for safety, and using the facet data as mark data is
recommended when using the *exclude* facet mode.

When mark-level faceting is used, the default *auto* setting is
equivalent to *include*: the mark will be faceted if either the **fx**
or **fy** channel option (or both) is specified. The null or false
option will disable faceting, while *exclude* draws the subset of the
mark’s data *not* in the current facet.

`facet_anchor` Literal\['top', 'right', 'bottom', 'left', 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'top-empty', 'right-empty', 'bottom-empty', 'left-empty', 'empty'\] \| None \| [Param](inspect_viz.qmd#param)  
How to place the mark with respect to facets.

- `None` (default for most marks) - display the mark in each non-empty
  facet
- *top*, *right*, *bottom*, or *left* - display the mark only in facets
  on the given side
- *top-empty*, *right-empty*, *bottom-empty*, or *left-empty* (default
  for axis marks) - display the mark only in facets that have empty
  space on the given side: either the margin, or an empty facet
- *empty* - display the mark in empty facets only

`margin` float \| [Param](inspect_viz.qmd#param)  
Shorthand to set the same default for all four mark margins.

`margin_top` float \| [Param](inspect_viz.qmd#param)  
The mark’s top margin.

`margin_right` float \| [Param](inspect_viz.qmd#param)  
The mark’s right margin.

`margin_bottom` float \| [Param](inspect_viz.qmd#param)  
The mark’s bottom margin.

`margin_left` float \| [Param](inspect_viz.qmd#param)  
The mark’s left margin.

`aria_description` str \| [Param](inspect_viz.qmd#param)  
ARIA description
(<https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-description>).

`aria_hidden` str \| [Param](inspect_viz.qmd#param)  
ARIA hidden
(<https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-hidden>).

`aria_label` [Channel](inspect_viz.mark.qmd#channel)  
ARIA label
(<https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-label/>).

`pointer_events` str \| [Param](inspect_viz.qmd#param)  
Pointer events
(<https://developer.mozilla.org/en-US/docs/Web/CSS/pointer-events>).

`title` [Channel](inspect_viz.mark.qmd#channel)  
The title; a channel specifying accessible, short textual descriptions
as strings (possibly with newlines). If the `tip` option is specified,
the title will be displayed with an interactive tooltip instead of using
the SVG title element.

`tip` Union\[bool, [TipPointer](inspect_viz.mark.qmd#tippointer), [TipOptions](inspect_viz.mark.qmd#tipoptions), [Param](inspect_viz.qmd#param)\]  
Whether to generate a tooltip for this mark, and any tip options.

`channels` dict\[str, str\]  
Additional named channels, for example to include in a tooltip.

Consists of (channel name, data field name) key-value pairs.

`clip` Literal\['frame', 'sphere'\] \| bool \| None \| [Param](inspect_viz.qmd#param)  
How to clip the mark.

- *frame* or `True` - clip to the plot’s frame (inner area)
- *sphere* - clip to the projected sphere (*e.g.*, front hemisphere)
- `None` or `False` - do not clip

The *sphere* clip option requires a geographic projection.

`dx` float \| [Param](inspect_viz.qmd#param)  
The horizontal offset in pixels; a constant option. On low-density
screens, an additional 0.5px offset may be applied for crisp edges.

`dy` float \| [Param](inspect_viz.qmd#param)  
The vertical offset in pixels; a constant option. On low-density
screens, an additional 0.5px offset may be applied for crisp edges.

`fill` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
A constant CSS color string, or a channel typically bound to the *color*
scale. If all channel values are valid CSS colors, by default the
channel will not be bound to the *color* scale, interpreting the colors
literally.

`fill_opacity` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
A constant number between 0 and 1, or a channel typically bound to the
*opacity* scale. If all channel values are numbers in \[0, 1\], by
default the channel will not be bound to the *opacity* scale,
interpreting the opacities literally.

`stroke` [ChannelSpec](inspect_viz.mark.qmd#channelspec) \| [Param](inspect_viz.qmd#param)  
A constant CSS color string, or a channel typically bound to the *color*
scale. If all channel values are valid CSS colors, by default the
channel will not be bound to the *color* scale, interpreting the colors
literally.

`stroke_dasharray` str \| float \| [Param](inspect_viz.qmd#param)  
A constant number indicating the length in pixels of alternating dashes
and gaps, or a constant string of numbers separated by spaces or commas
(*e.g.*, *10 2* for dashes of 10 pixels separated by gaps of 2 pixels),
or *none* (the default) for no dashing.

`stroke_dashoffset` str \| float \| [Param](inspect_viz.qmd#param)  
A constant indicating the offset in pixels of the first dash along the
stroke; defaults to zero.

`stroke_linecap` str \| [Param](inspect_viz.qmd#param)  
A constant specifying how to cap stroked paths, such as *butt*, *round*,
or *square*
(<https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linecap>).

`stroke_linejoin` str \| [Param](inspect_viz.qmd#param)  
A constant specifying how to join stroked paths, such as *bevel*,
*miter*, *miter-clip*, or *round*
(<https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linejoin>)

`stroke_miterlimit` float \| [Param](inspect_viz.qmd#param)  
A constant number specifying how to limit the length of *miter* joins on
stroked paths.

`stroke_opacity` [ChannelSpec](inspect_viz.mark.qmd#channelspec)  
A constant between 0 and 1, or a channel typically bound to the
*opacity* scale. If all channel values are numbers in \[0, 1\], by
default the channel will not be bound to the *opacity* scale,
interpreting the opacities literally.

`stroke_width` [ChannelSpec](inspect_viz.mark.qmd#channelspec)  
A constant number in pixels, or a channel.

`opacity` [ChannelSpec](inspect_viz.mark.qmd#channelspec)  
A constant between 0 and 1, or a channel typically bound to the
*opacity* scale. If all channel values are numbers in \[0, 1\], by
default the channel will not be bound to the *opacity* scale,
interpreting the opacities literally. For faster rendering, prefer the
**stroke_opacity** or **fill_opacity** option.

`mix_blend_mode` str \| [Param](inspect_viz.qmd#param)  
A constant string specifying how to blend content such as *multiply*
(<https://developer.mozilla.org/en-US/docs/Web/CSS/filter>).

`image_filter` str \| [Param](inspect_viz.qmd#param)  
A constant string used to adjust the rendering of images, such as
*blur(5px)* (<https://developer.mozilla.org/en-US/docs/Web/CSS/filter>).

`paint_order` str \| [Param](inspect_viz.qmd#param)  
A constant string specifying the order in which the \* **fill**,
**stroke**, and any markers are drawn; defaults to *normal*, which draws
the fill, then stroke, then markers; defaults to *stroke* for the text
mark to create a “halo” around text to improve legibility.

`shape_rendering` str \| [Param](inspect_viz.qmd#param)  
A constant string such as *crispEdges*
(<https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/shape-rendering>).

`href` [Channel](inspect_viz.mark.qmd#channel)  
a channel specifying URLs for clickable links. May be used in
conjunction with the **target** option to open links in another window.

`target` str \| [Param](inspect_viz.qmd#param)  
A constant string specifying the target window (\_e.g. \*\_blank\*) for
clickable links; used in conjunction with the **href** option
(<https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/target>).

`shift_overlapping_text` bool \| [Param](inspect_viz.qmd#param)  
Whether to shift overlapping text marks to avoid collisions; defaults to
`False`. If `True`, text marks will be shifted to avoid collisions with
other text marks, but not with other marks.

### Marks

Set of marks to add to a plot.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_mark.py#L74)

``` python
Marks: TypeAlias = Mark | Sequence[Mark | Sequence[Mark]]
```

### Title

Plot title mark.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_title.py#L8)

``` python
class Title(Mark)
```

### Channel

Data channel for visualization.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_channel.py#L42)

``` python
Channel: TypeAlias = (
    str | Transform | Sequence[int | float | bool | str] | int | float | bool | None
)
```

### ChannelSpec

Data channel spec for visualization.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_channel.py#L80)

``` python
ChannelSpec: TypeAlias = Channel | ChannelWithScale
```

### ChannelIntervalSpec

In some contexts, when specifying a mark channel’s value, you can
provide a {value, interval} object to specify an associated interval.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_channel.py#L100)

``` python
ChannelIntervalSpec: TypeAlias = ChannelSpec | ChannelWithInterval
```

### ChannelWithInterval

Channel with associated interval.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_channel.py#L93)

``` python
class ChannelWithInterval(TypedDict)
```

### ChannelWithScale

Channel with label and scale to override the scale that would normally
be associated with the channel.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_channel.py#L56)

``` python
class ChannelWithScale(TypedDict)
```

### ChannelName

Known channel names.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_channel.py#L7)

``` python
ChannelName: TypeAlias = Literal[
    "ariaLabel",
    "fill",
    "fillOpacity",
    "fontSize",
    "fx",
    "fy",
    "geometry",
    "height",
    "href",
    "length",
    "opacity",
    "path",
    "r",
    "rotate",
    "src",
    "stroke",
    "strokeOpacity",
    "strokeWidth",
    "symbol",
    "text",
    "title",
    "weight",
    "width",
    "x",
    "x1",
    "x2",
    "y",
    "y1",
    "y2",
    "z",
]
```

### TipOptions

Options for the tip mark.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_options.py#L214)

``` python
class TipOptions(TypedDict, total=False)
```

#### Attributes

`pointer` [TipPointer](inspect_viz.mark.qmd#tippointer)  
The pointer mode for the tip (x, y, or xy)

`x` [ChannelSpec](inspect_viz.mark.qmd#channelspec)  
The horizontal position channel specifying the tip’s anchor, typically
bound to the *x* scale.

`x1` [ChannelSpec](inspect_viz.mark.qmd#channelspec)  
The starting horizontal position channel specifying the tip’s anchor,
typically bound to the *x* scale.

`x2` [ChannelSpec](inspect_viz.mark.qmd#channelspec)  
The ending horizontal position channel specifying the tip’s anchor,
typically bound to the *x* scale.

`y` [ChannelSpec](inspect_viz.mark.qmd#channelspec)  
The vertical position channel specifying the tip’s anchor, typically
bound to the *y* scale.

`y1` [ChannelSpec](inspect_viz.mark.qmd#channelspec)  
The starting vertical position channel specifying the tip’s anchor,
typically bound to the *y* scale.

`y2` [ChannelSpec](inspect_viz.mark.qmd#channelspec)  
The ending vertical position channel specifying the tip’s anchor,
typically bound to the *y* scale.

`frame_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param)  
The frame anchor specifies defaults for **x** and **y** based on the
plot’s frame.

It may be one of the four sides (*top*, *right*, *bottom*, *left*), one
of the four corners (*top-left*, *top-right*, *bottom-right*,
*bottom-left*), or the *middle* of the frame.

`anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param)  
The tip anchor specifies how to orient the tip box relative to its
anchor position.

The tip anchor refers to the part of the tip box that is attached to the
anchor point. For example, the *top-left* anchor places the top-left
corner of tip box near the anchor position, hence placing the tip box
below and to the right of the anchor position.

`preferred_anchor` [FrameAnchor](inspect_viz.mark.qmd#frameanchor) \| [Param](inspect_viz.qmd#param)  
If an explicit tip anchor is not specified, an anchor is chosen
automatically such that the tip fits within the plot’s frame. If the
preferred anchor fits, it is chosen.

`format` dict\[[ChannelName](inspect_viz.mark.qmd#channelname), bool \| str \| [Param](inspect_viz.qmd#param)\]  
How channel values are formatted for display.

If a format is a string, it is interpreted as a (UTC) time format for
temporal channels, and otherwise a number format.

### TipPointer

The pointer mode for the tip; corresponds to pointerX, pointerY, and
pointer.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_options.py#L210)

``` python
TipPointer: TypeAlias = Literal["x", "y", "xy"]
```

### Curve

The curve (interpolation) method for connecting adjacent points.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_types.py#L7)

``` python
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
```

### Symbol

Symbol type for dot or density plot.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_types.py#L45)

``` python
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
```

### Marker

Symbols used as plot markers.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_types.py#L76)

``` python
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
```

### Interpolate

The spatial interpolation method.

- *none* - do not perform interpolation (the default)
- *linear* - apply proportional linear interpolation across adjacent
  bins
- *nearest* - assign each pixel to the closest sample’s value (Voronoi
  diagram)
- *barycentric* - apply barycentric interpolation over the Delaunay
  triangulation
- *random-walk* - apply a random walk from each pixel

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_types.py#L32)

``` python
Interpolate: TypeAlias = Literal[
    "none", "linear", "nearest", "barycentric", "random-walk"
]
```

### FrameAnchor

Defaults for **x** and **y** based on the plot’s frame.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_types.py#L63)

``` python
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
```

### LineAnchor

The line anchor controls how text is aligned (typically vertically)
relative to its anchor point.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_types.py#L112)

``` python
LineAnchor = Literal["top", "bottom", "middle"]
```

### TextOverflow

How to truncate (or wrap) lines of text longer than the given
**line_width**; one of:

- null (default) preserve overflowing characters (and wrap if needed);
- *clip* or *clip-end* remove characters from the end;
- *clip-start* remove characters from the start;
- *ellipsis* or *ellipsis-end* replace characters from the end with an
  ellipsis (…);
- *ellipsis-start* replace characters from the start with an ellipsis
  (…);
- *ellipsis-middle* replace characters from the middle with an ellipsis
  (…).

If no **title** was specified, if text requires truncation, a title
containing the non-truncated text will be implicitly added.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_types.py#L89)

``` python
TextOverflow: TypeAlias = (
    Literal[
        "clip",
        "ellipsis",
        "clip-start",
        "clip-end",
        "ellipsis-start",
        "ellipsis-middle",
        "ellipsis-end",
    ]
    | None
)
```

### TextStyles

Text styling options.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/mark/_types.py#L116)

``` python
class TextStyles(TypedDict, total=False)
```

#### Attributes

`text_anchor` Literal\['start', 'middle', 'end'\] \| [Param](inspect_viz.qmd#param)  
The text anchor controls how text is aligned (typically horizontally)
relative to its anchor point; it is one of *start*, *end*, or *middle*.
If the frame anchor is *left*, *top-left*, or *bottom-left*, the default
text anchor is *start*; if the frame anchor is *right*, *top-right*, or
*bottom-right*, the default is *end*; otherwise it is *middle*.

`line_height` float \| [Param](inspect_viz.qmd#param)  
The line height in ems; defaults to 1. The line height affects the
(typically vertical) separation between adjacent baselines of text, as
well as the separation between the text and its anchor point.

`line_width` float \| [Param](inspect_viz.qmd#param)  
The line width in ems (e.g., 10 for about 20 characters); defaults to
infinity, disabling wrapping and clipping. If **text_overflow** is null,
lines will be wrapped at the specified length. If a line is split at a
soft hyphen (­), a hyphen (-) will be displayed at the end of the line.
If **text_overflow** is not null, lines will be clipped according to the
given strategy.

`text_overflow` [TextOverflow](inspect_viz.mark.qmd#textoverflow) \| [Param](inspect_viz.qmd#param)  
Text overflow behavior.

`monospace` bool \| [Param](inspect_viz.qmd#param)  
If `True`, changes the default **font_family** to *monospace*, and uses
simplified monospaced text metrics calculations.

`font_family` str \| [Param](inspect_viz.qmd#param)  
The font-family; a constant; defaults to the plot’s font family, which
is typically *system-ui*

`font_size` [Channel](inspect_viz.mark.qmd#channel) \| float \| [Param](inspect_viz.qmd#param)  
The font size in pixels; either a constant or a channel; defaults to the
plot’s font size, which is typically 10. When a number, it is
interpreted as a constant; otherwise it is interpreted as a channel.

`font_variant` str \| [Param](inspect_viz.qmd#param)  
The font variant; a constant; if the **text** channel contains numbers
or dates, defaults to *tabular-nums* to facilitate comparing numbers;
otherwise defaults to the plot’s font style, which is typically
*normal*.

`font_weight` float \| [Param](inspect_viz.qmd#param)  
The font weight; a constant; defaults to the plot’s font weight, which
is typically *normal*.
