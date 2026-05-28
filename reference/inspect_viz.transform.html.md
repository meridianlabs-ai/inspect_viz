# inspect_viz.transform – Inspect Viz

## SQL

### sql

SQL transform for a column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_sql.py#L6)

``` python
def sql(sql: str, label: str | None = None) -> Transform
```

`sql` str  
A SQL expression string to derive a new column value. Embedded Param references, such as `f"{param} + 1"`, are supported. For expressions with aggregate functions, use [agg()](../reference/inspect_viz.transform.html.md#agg) instead.

`label` str \| None  
A label for this expression, for example to label a plot axis.

### agg

Aggregation transform for a column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_agg.py#L6)

``` python
def agg(agg: str, label: str | None = None) -> Transform
```

`agg` str  
A SQL expression string to calculate an aggregate value. Embedded Param references, such as `f"SUM({param} + 1)"`, are supported. For expressions without aggregate functions, use [sql()](../reference/inspect_viz.transform.html.md#sql) instead.”

`label` str \| None  
A label for this expression, for example to label a plot axis.

## Column

### column

Intpret a string or param-value as a column reference.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_column.py#L75)

``` python
def column(column: str | Param) -> Transform
```

`column` str \| [Param](../reference/inspect_viz.html.md#param)  
Column name or paramameter.

### bin

Bin a continuous variable into discrete intervals.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_column.py#L12)

``` python
def bin(
    bin: str | float | bool | Param | Sequence[str | float | bool | Param],
    interval: Literal[
        "date",
        "number",
        "millisecond",
        "second",
        "minute",
        "hour",
        "day",
        "month",
        "year",
    ]
    | None = None,
    step: float | None = None,
    steps: float | None = None,
    minstep: float | None = None,
    nice: bool | None = None,
    offset: float | None = None,
) -> Transform
```

`bin` str \| float \| bool \| [Param](../reference/inspect_viz.html.md#param) \| Sequence\[str \| float \| bool \| [Param](../reference/inspect_viz.html.md#param)\]  
specifies a data column or expression to bin. Both numerical and temporal (date/time) values are supported.

`interval` Literal\['date', 'number', 'millisecond', 'second', 'minute', 'hour', 'day', 'month', 'year'\] \| None  
The interval bin unit to use, typically used to indicate a date/time unit for binning temporal values, such as `hour`, `day`, or `month`. If `date`, the extent of data values is used to automatically select an interval for temporal data. The value `number` enforces normal numerical binning, even over temporal data. If unspecified, defaults to `number` for numerical data and `date` for temporal data.

`step` float \| None  
The step size to use between bins. When binning numerical values (or interval type `number`), this setting specifies the numerical step size. For data/time intervals, this indicates the number of steps of that unit, such as hours, days, or years.

`steps` float \| None  
The target number of binning steps to use. To accommodate human-friendly (“nice”) bin boundaries, the actual number of bins may diverge from this exact value. This option is ignored when step is specified.

`minstep` float \| None  
The minimum allowed bin step size (default 0) when performing numerical binning. For example, a setting of 1 prevents step sizes less than 1. This option is ignored when step is specified.

`nice` bool \| None  
A flag (default true) requesting “nice” human-friendly end points and step sizes when performing numerical binning. When step is specified, this option affects the binning end points (e.g., origin) only.

`offset` float \| None  
Offset for computed bins (default 0). For example, a value of 1 will result in using the next consecutive bin boundary.

### date_day

Transform a Date value to a day of the month for cyclic comparison.

Year and month values are collapsed to enable comparison over days only.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_column.py#L97)

``` python
def date_day(expr: str | Param) -> Transform
```

`expr` str \| [Param](../reference/inspect_viz.html.md#param)  
Expression or parameter.

### date_month

Transform a Date value to a month boundary for cyclic comparison.

Year values are collapsed to enable comparison over months only.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_column.py#L109)

``` python
def date_month(expr: str | Param) -> Transform
```

`expr` str \| [Param](../reference/inspect_viz.html.md#param)  
Expression or parameter.

### date_month_day

Map date/times to a month and day value, all within the same year for comparison.

The resulting value is still date-typed.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_column.py#L85)

``` python
def date_month_day(expr: str | Param) -> Transform
```

`expr` str \| [Param](../reference/inspect_viz.html.md#param)  
Expression or parameter.

### epoch_ms

Transform a Date value to epoch milliseconds.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_column.py#L121)

``` python
def epoch_ms(expr: str | Param) -> Transform
```

`expr` str \| [Param](../reference/inspect_viz.html.md#param)  
Expression or parameter.

## Aggregate

### avg

Compute the average (mean) value of the given column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L47)

``` python
def avg(
    col: TransformArg | None = None,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg \| None  
Column to compute the mean for.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### count

A count aggregate transform.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L63)

``` python
def count(
    col: TransformArg | None = None,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg \| None  
Compute the count of records in an aggregation group. If specified, only non-null expression values are counted. If omitted, all rows within a group are counted.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### sum

Compute the sum of the given column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L207)

``` python
def sum(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to compute the sum for.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### min

Compute the minimum value of the given column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L127)

``` python
def min(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to compute the minimum for.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### max

Compute the maximum value of the given column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L111)

``` python
def max(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to compute the maximum for.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### median

Compute the median value of the given column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L143)

``` python
def median(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to compute the median for.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### mode

Compute the mode value of the given column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L159)

``` python
def mode(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to compute the mode for.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### first

Return the first column value found in an aggregation group.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L79)

``` python
def first(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to get the first value from.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### last

Return the last column value found in an aggregation group.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L95)

``` python
def last(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to get the last value from.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### product

Compute the product of the given column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L175)

``` python
def product(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to compute the product for.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### quantile

Compute the quantile value of the given column at the provided probability threshold.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L271)

``` python
def quantile(
    col: TransformArg,
    threshold: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to compute the quantile for.

`threshold` TransformArg  
Probability threshold (e.g., 0.5 for median).

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### stddev

Compute the standard deviation of the given column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L191)

``` python
def stddev(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to compute the standard deviation for.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### stddev_pop

Compute the population standard deviation of the given column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L239)

``` python
def stddev_pop(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to compute the population standard deviation for.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### variance

Compute the sample variance of the given column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L223)

``` python
def variance(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to compute the variance for.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### var_pop

Compute the population variance of the given column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L255)

``` python
def var_pop(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to compute the population variance for.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### argmin

Find a value of the first column that minimizes the second column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L29)

``` python
def argmin(
    col1: TransformArg,
    col2: TransformArg,
    distinct: bool | None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col1` TransformArg  
Column to yield the value from.

`col2` TransformArg  
Column to check for minimum corresponding value of `col1`.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### argmax

Find a value of the first column that maximizes the second column.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_aggregate.py#L11)

``` python
def argmax(
    col1: TransformArg,
    col2: TransformArg,
    distinct: bool | None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col1` TransformArg  
Column to yield the value from.

`col2` TransformArg  
Column to check for maximum corresponding value of `col1`.

`distinct` bool \| None  
Aggregate distinct.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### ci_bounds

Compute a confidence interval boundary.

Returns a tuple of two [Transform](../reference/inspect_viz.transform.html.md#transform) objects corresponding to the lower and upper bounds of the confidence interval.

Specify the confidence interval either as:

1.  A `level` and `stderr` column (where a z-score for level will be offset from the `stderr`); or
2.  Explicit `lower` and `upper` columns which should already be on the desired scale (e.g., z\*stderr, bootstrap deltas, HDIs from bayesian posterior distributions, etc.).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_ci.py#L8)

``` python
def ci_bounds(
    score: str | Param,
    *,
    level: float | None = None,
    stderr: str | Param | None = None,
    lower: str | Param | None = None,
    upper: str | Param | None = None,
) -> tuple[Transform, Transform]
```

`score` str \| [Param](../reference/inspect_viz.html.md#param)  
Column name for score.

`level` float \| None  
Confidence level (e.g. 0.95)

`stderr` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
Column name for stderr.

`lower` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
Column name for lower bound.

`upper` str \| [Param](../reference/inspect_viz.html.md#param) \| None  
Column name for upper bound.

## Window

### row_number

Compute the 1-based row number over an ordered window partition.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_window.py#L25)

``` python
def row_number(**options: Unpack[WindowOptions]) -> Transform
```

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### rank

Compute the row rank over an ordered window partition.

Sorting ties result in gaps in the rank numbers (\[1, 1, 3, …\]).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_window.py#L35)

``` python
def rank(**options: Unpack[WindowOptions]) -> Transform
```

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### dense_rank

Compute the dense row rank (no gaps) over an ordered window partition.

Sorting ties do not result in gaps in the rank numbers ( \[1, 1, 2, …\]).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_window.py#L47)

``` python
def dense_rank(**options: Unpack[WindowOptions]) -> Transform
```

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### percent_rank

Compute the percetange rank over an ordered window partition.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_window.py#L59)

``` python
def percent_rank(**options: Unpack[WindowOptions]) -> Transform
```

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### cume_dist

Compute the cumulative distribution value over an ordered window partition.

Equals the number of partition rows preceding or peer with the current row, divided by the total number of partition rows.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_window.py#L69)

``` python
def cume_dist(**options: Unpack[WindowOptions]) -> Transform
```

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### n_tile

Compute an n-tile integer ranging from 1 to `num_buckets` dividing the partition as equally as possible.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_window.py#L81)

``` python
def n_tile(num_buckets: int, **options: Unpack[WindowOptions]) -> Transform
```

`num_buckets` int  
Number of buckets.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### lag

Compute lagging values in a column.

Returns the value at the row that is at `offset` rows (default `1`) before the current row within the window frame.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_window.py#L92)

``` python
def lag(
    col: TransformArg,
    offset: int = 1,
    default: TransformArg | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to take value from.

`offset` int  
Rows to offset.

`default` TransformArg \| None  
Default value if thre is no such row.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### lead

Compute leading values in a column.

Returns the value at the row that is at `offset` rows (default `1`) after the current row within the window frame.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_window.py#L112)

``` python
def lead(
    col: TransformArg,
    offset: int = 1,
    default: TransformArg | None = None,
    **options: Unpack[WindowOptions],
) -> Transform
```

`col` TransformArg  
Column to take value from.

`offset` int  
Rows to offset.

`default` TransformArg \| None  
Default value if thre is no such row.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### first_value

Get the first value of the given column in the current window frame.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_window.py#L132)

``` python
def first_value(col: TransformArg, **options: Unpack[WindowOptions]) -> Transform
```

`col` TransformArg  
Aggregate column to take first value from.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### last_value

Get the last value of the given column in the current window frame.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_window.py#L143)

``` python
def last_value(col: TransformArg, **options: Unpack[WindowOptions]) -> Transform
```

`col` TransformArg  
Aggregate column to take last value from.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

### nth_value

Get the nth value of the given column in the current window frame, counting from one.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_window.py#L154)

``` python
def nth_value(
    col: TransformArg, offset: int, **options: Unpack[WindowOptions]
) -> Transform
```

`col` TransformArg  
Aggregate column to take nth value from.

`offset` int  
Offset for the nth row.

`**options` Unpack\[[WindowOptions](../reference/inspect_viz.transform.html.md#windowoptions)\]  
Window transform options.

## Types

### Transform

Column transformation operation.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_transform.py#L7)

``` python
Transform: TypeAlias = dict[str, JsonValue]
```

### WindowOptions

Window transform options.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/transform/_window.py#L9)

``` python
class WindowOptions(TypedDict, total=False)
```

#### Attributes

`orderby` str \| [Param](../reference/inspect_viz.html.md#param) \| Sequence\[str \| [Param](../reference/inspect_viz.html.md#param)\]  
One or more expressions by which to sort a windowed version of this aggregate function.

`partitionby` str \| [Param](../reference/inspect_viz.html.md#param) \| Sequence\[str \| [Param](../reference/inspect_viz.html.md#param)\]  
One or more expressions by which to partition a windowed version of this aggregate function.

`rows` Sequence\[float \| None\] \| [Param](../reference/inspect_viz.html.md#param)  
window rows frame specification as an array or array-valued expression.

`range` Sequence\[float \| None\] \| [Param](../reference/inspect_viz.html.md#param)  
Window range frame specification as an array or array-valued expression.
