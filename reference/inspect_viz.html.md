# inspect_viz


## Core

### Data

Data source for visualizations.

Data sources can be created from any standard Python data frame
(e.g. Pandas, Polars, etc.) or from a path pointing to a data file in a
standard format (e.g. csv, parquet, etc.)

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/_core/data.py#L18)

``` python
class Data
```

#### Attributes

`columns` list\[str\]  
Column names for data source.

#### Methods

from_dataframe  
Create `Data` from a standard Python data frame (e.g. Pandas, Polars,
PyArrow, etc.).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/_core/data.py#L24)

``` python
@classmethod
def from_dataframe(cls, df: IntoDataFrame) -> "Data"
```

`df` IntoDataFrame  
Data frame to read.

from_file  
Create `Data` from a data file (e.g. csv, parquet, feather, etc.).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/_core/data.py#L33)

``` python
@classmethod
def from_file(cls, file: Union[str, PathLike[str]]) -> "Data"
```

`file` Union\[str, PathLike\[str\]\]  
File to read data from. Supported formats include csv, json, xslx,
parquet, feather, sas7bdat, dta, and fwf.

### Component

Data visualization component (input, plot, mark, table, layout, etc.).

Visualization components are Jupyter widgets that can be used in any
notebook or Jupyter based publishing system.

See the documentation on inputs, plots, marks, and interactors for
details on available components.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/_core/component.py#L47)

``` python
class Component(AnyWidget)
```

## Params

### Selection

Selection that can be filtered by inputs and other selections.

Selection types include:

- `Selection.intersect()` for intersecting clauses (logical “and”)
- `Selection.union()` for unionone clauses (logical “or”)
- `Selection.single()` for a single clause only
- `Selection.crossfilter()` for a cross-filtered intersection

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/_core/selection.py#L10)

``` python
class Selection(str)
```

#### Methods

intersect  
Create a new Selection instance with an intersect (conjunction)
resolution strategy.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/_core/selection.py#L27)

``` python
@classmethod
def intersect(
    cls,
    cross: bool = False,
    empty: bool = False,
    include: Union["Selection", list["Selection"]] | None = None,
) -> "Selection"
```

`cross` bool  
Boolean flag indicating cross-filtered resolution. If true, selection
clauses will not be applied to the clients they are associated with.

`empty` bool  
Boolean flag indicating if a lack of clauses should correspond to an
empty selection with no records. This setting determines the default
selection state.

`include` Union\[[Selection](inspect_viz.qmd#selection), list\[[Selection](inspect_viz.qmd#selection)\]\] \| None  
Upstream selections whose clauses should be included as part of the new
selection. Any clauses published to upstream selections will be relayed
to the new selection.

union  
Create a new Selection instance with a union (disjunction) resolution
strategy.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/_core/selection.py#L43)

``` python
@classmethod
def union(
    cls,
    cross: bool = False,
    empty: bool = False,
    include: Union["Selection", list["Selection"]] | None = None,
) -> "Selection"
```

`cross` bool  
Boolean flag indicating cross-filtered resolution. If true, selection
clauses will not be applied to the clients they are associated with.

`empty` bool  
Boolean flag indicating if a lack of clauses should correspond to an
empty selection with no records. This setting determines the default
selection state.

`include` Union\[[Selection](inspect_viz.qmd#selection), list\[[Selection](inspect_viz.qmd#selection)\]\] \| None  
Upstream selections whose clauses should be included as part of the new
selection. Any clauses published to upstream selections will be relayed
to the new selection.

single  
Create a new Selection instance with a singular resolution strategy that
keeps only the most recent selection clause.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/_core/selection.py#L59)

``` python
@classmethod
def single(
    cls,
    cross: bool = False,
    empty: bool = False,
    include: Union["Selection", list["Selection"]] | None = None,
) -> "Selection"
```

`cross` bool  
Boolean flag indicating cross-filtered resolution. If true, selection
clauses will not be applied to the clients they are associated with.

`empty` bool  
Boolean flag indicating if a lack of clauses should correspond to an
empty selection with no records. This setting determines the default
selection state.

`include` Union\[[Selection](inspect_viz.qmd#selection), list\[[Selection](inspect_viz.qmd#selection)\]\] \| None  
Upstream selections whose clauses should be included as part of the new
selection. Any clauses published to upstream selections will be relayed
to the new selection.

crossfilter  
Create a new Selection instance with a cross-filtered intersect
resolution strategy.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/_core/selection.py#L75)

``` python
@classmethod
def crossfilter(
    cls,
    empty: bool = False,
    include: Union["Selection", list["Selection"]] | None = None,
) -> "Selection"
```

`empty` bool  
Boolean flag indicating if a lack of clauses should correspond to an
empty selection with no records. This setting determines the default
selection state.

`include` Union\[[Selection](inspect_viz.qmd#selection), list\[[Selection](inspect_viz.qmd#selection)\]\] \| None  
Upstream selections whose clauses should be included as part of the new
selection. Any clauses published to upstream selections will be relayed
to the new selection.

### Param

Parameter that can be bound from inputs.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/_core/param.py#L16)

``` python
class Param(str)
```

#### Attributes

`id` str  
Unique id (automatically generated).

`default` [ParamValue](inspect_viz.qmd#paramvalue)  
Default value.

### ParamValue

Type alias for parameter values (scalar or sequence of scalars).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/_core/param.py#L10)

``` python
ParamValue: TypeAlias = (
    int | float | bool | str | datetime | Sequence[int | float | bool | str]
)
```

## Options

### options

Inspect Viz global options.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/_core/_options.py#L25)

``` python
options: Options = Options(output_format="auto")
```

### options_context

Context manager for temporarily overriding global options.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/_core/_options.py#L29)

``` python
@contextmanager
def options_context(**kwargs: Unpack[OptionsArgs]) -> Iterator[None]
```

`**kwargs` Unpack\[OptionsArgs\]  
Options to override within the context.

### Options

Inspect Viz global options.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/_core/_options.py#L12)

``` python
class Options(SimpleNamespace)
```

#### Attributes

`output_format` Literal\['auto', 'js', 'png'\]  
Output format for components.

Defaults to “auto”, which resolves to “js” (interactive plots and
tables) in all contexts except Quarto PDF output (which uses “png”).
Specify “png” to always write static PNG images instead (interactive
features will be disabled in this case).
