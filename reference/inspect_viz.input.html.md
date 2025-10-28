# inspect_viz.input


### select

Select input.

Select inputs can be populated either from a database table (via the
`data` and `column` parameters) or from a static set of options (via the
`options` parameter).

Select inputs can produce either a single value or multiple values when
`multiple=True` is specified.

Select inputs have a `target` which is either a `Param` or `Selection`.
In the latter case, the `field` parameter determines the data column
name to use within generated selection clause predicates (defaulting to
`column`). If no `target` is specified then the data source’s selection
is used as the target.

The intitial selected value will be “All” when `target` is a `Selection`
(indicating select all records) and the param value when `target` is a
`Param`.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/43bc7cbad55804123a0150d2f5f083c28b44e0c1/src/inspect_viz/input/_select.py#L10)

``` python
def select(
    data: Data | None = None,
    *,
    filter_by: Selection | None = None,
    column: str | None = None,
    options: Sequence[str | bool | float]
    | Mapping[str, str | bool | float]
    | None = None,
    value: Literal["all", "auto"] | str | list[str] = "all",
    multiple: bool = False,
    target: Param | Selection | None = None,
    field: str | None = None,
    label: str | None = None,
    width: float | None = None,
) -> Component
```

`data` [Data](inspect_viz.qmd#data) \| None  
The data source (used in conjunction with the `column` parameter). If
`data` is not specified, you must provide explcit `options`.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data source indicated by the `data` parameter.

`column` str \| None  
The name of a column from which to pull options. The unique column
values are used as options. Used in conjunction with the `data`
parameter.

`options` Sequence\[str \| bool \| float\] \| Mapping\[str, str \| bool \| float\] \| None  
A `list` or `dict` of options (provide a `dict` if you want values to
map to alternate labels). Alternative to populating options from a
database column via `data` and `column`.

`value` Literal\['all', 'auto'\] \| str \| list\[str\]  
Initial value for selection. Pass “all” (the default) for no filtering,
“auto” to select the first element in the list, or value(s) for an
explicit initial selection. Applies only when `target` is a `Selection`
(as `Param` carries its own default value).

`multiple` bool  
Enable selection of multiple values (defaults to `False`)

`target` [Param](inspect_viz.qmd#param) \| [Selection](inspect_viz.qmd#selection) \| None  
A `Param` or `Selection` that this select input should update. For a
`Param`, the selected value is set to be the new param value. For a
`Selection`, a predicate of the form column = value will be added to the
selection.

`field` str \| None  
The data column name to use within generated selection clause
predicates. Defaults to the `column` parameter.

`label` str \| None  
A text label for the input. If unspecified, the column name (if
provided) will be used by default.

`width` float \| None  
Width in pixels (defaults to 150).

### slider

Select input widget.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/43bc7cbad55804123a0150d2f5f083c28b44e0c1/src/inspect_viz/input/_slider.py#L10)

``` python
def slider(
    data: Data | None = None,
    *,
    filter_by: Selection | None = None,
    label: str | None = None,
    column: str | None = None,
    field: str | None = None,
    target: Param | Selection | None = None,
    select: Literal["point", "interval"] | None = None,
    value: float | tuple[float, float] | None = None,
    min: float | None = None,
    max: float | None = None,
    step: float | None = None,
    width: float = 150,
) -> Component
```

`data` [Data](inspect_viz.qmd#data) \| None  
The data source for this widget. Used in conjunction with the `column`
property. The minimum and maximum values of the column determine the
slider range.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data source indicated by the `data` property.

`label` str \| None  
A text label for this input (optional).

`column` str \| None  
The name of a database column whose values determine the slider range.
Used in conjunction with the `data` property. The minimum and maximum
values of the column determine the slider range.

`field` str \| None  
The database column name to use within generated selection clause
predicates. Defaults to the `column` property.

`target` [Param](inspect_viz.qmd#param) \| [Selection](inspect_viz.qmd#selection) \| None  
A `Param` or `Selection` that this select input should update. For a
`Param`, the selected value is set to be the new param value. For a
`Selection`, a predicate that does an equality check (for
`select=="point"`) or range check (for `select=="interval"`).

`select` Literal\['point', 'interval'\] \| None  
The type of selection clause predicate to generate when `selection` is
specified. If `'point'` (the default for a single value), the selection
predicate is an equality check for the slider value. If `'interval'`
(the default for a pair of values), the predicate checks the slider
value interval.

`value` float \| tuple\[float, float\] \| None  
The initial slider value. Either a single numeric value or a tuple of
two values representing a range.

`min` float \| None  
The minumum slider value.

`max` float \| None  
The maximum slider value.

`step` float \| None  
The slider step, the amount to increment between consecutive values.

`width` float  
The width of the slider in screen pixels (defaults to 200)

### search

Text search input widget

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/43bc7cbad55804123a0150d2f5f083c28b44e0c1/src/inspect_viz/input/_search.py#L10)

``` python
def search(
    data: Data,
    *,
    filter_by: Selection | None = None,
    column: str | None = None,
    field: str | None = None,
    target: Param | Selection | None = None,
    type: Literal["contains", "prefix", "suffix", "regexp"] | None = None,
    label: str | None = None,
    placeholder: str | None = None,
    width: float | None = None,
) -> Component
```

`data` [Data](inspect_viz.qmd#data)  
The data source for input selections (used in conjunction with the
`column` property).

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data source indicated by the `data` property.

`column` str \| None  
TThe name of a database column from which to pull valid search results.
The unique column values are used as search autocomplete values. Used in
conjunction with the `data` property.

`field` str \| None  
The data column name to use within generated selection clause
predicates. Defaults to the `column` property.

`target` [Param](inspect_viz.qmd#param) \| [Selection](inspect_viz.qmd#selection) \| None  
A `Param` or `Selection` that this search box should update. For a
`Param`, the textbox value is set as the new param value. For a
`Selection`, a predicate based on the `type` option will be added to the
selection.

`type` Literal\['contains', 'prefix', 'suffix', 'regexp'\] \| None  
The type of text search query to perform. One of: - `"contains"`
(default): the query string may appear anywhere in the text -
`"prefix"`: the query string must appear at the start of the text -
`"suffix"`: the query string must appear at the end of the text -
`"regexp"`: the query string is a regular expression the text must match

`label` str \| None  
A text label for this input (optional).

`placeholder` str \| None  
Placeholder text for empty search box.

`width` float \| None  
Width in pixels (defaults to 150).

### checkbox

Checkbox.

Checkboxes have a `target` which is either a `Param` or `Selection`. In
the latter case, the `field` parameter determines the data column name
to use within generated selection clause predicates (defaulting to
`column`). If no `target` is specified then the data source’s selection
is used as the target.

The `values` tuple enables you to determine what value is communicated
to the target for checked and unchecked states (by default, this is
`True` and `False`).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/43bc7cbad55804123a0150d2f5f083c28b44e0c1/src/inspect_viz/input/_checkbox.py#L8)

``` python
def checkbox(
    data: Data | None = None,
    *,
    label: str | None = None,
    target: Param | Selection | None = None,
    field: str | None = None,
    checked: bool = False,
    values: tuple[str | float | bool | None, str | float | bool | None] = (True, False),
) -> Component
```

`data` [Data](inspect_viz.qmd#data) \| None  
The data source (required when specifying the `field` parameter to
target a data source selection).

`label` str \| None  
A text label for the input (required)

`target` [Param](inspect_viz.qmd#param) \| [Selection](inspect_viz.qmd#selection) \| None  
A `Param` or `Selection` that this checkbox should interact with (use
`values` to customize the values that are used in the `target`).

`field` str \| None  
The data column name to use within generated selection clause predicates
(required if `target` is not a `Param`).

`checked` bool  
Should the checkbox be in the checked state by default.

`values` tuple\[str \| float \| bool \| None, str \| float \| bool \| None\]  
What value is communicated to the target for checked and unchecked
states.

### radio_group

Radio group.

Radio groups can be populated either from a database table (via the
`data` and `column` parameters) or from a static set of options (via the
`options` parameter).

Radio groups have a `target` which is either a `Param` or `Selection`.
In the latter case, the `field` parameter determines the data column
name to use within generated selection clause predicates (defaulting to
`column`). If no `target` is specified then the data source’s selection
is used as the target.

The intitial selected value will be “All” when `target` is a `Selection`
(indicating select all records) and the param value when `target` is a
`Param`.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/43bc7cbad55804123a0150d2f5f083c28b44e0c1/src/inspect_viz/input/_radio_group.py#L8)

``` python
def radio_group(
    data: Data | None = None,
    *,
    column: str | None = None,
    options: Sequence[str | bool | float]
    | Mapping[str, str | bool | float]
    | None = None,
    target: Param | Selection | None = None,
    field: str | None = None,
    label: str | None = None,
    filter_by: Selection | None = None,
) -> Component
```

`data` [Data](inspect_viz.qmd#data) \| None  
The data source (used in conjunction with the `column` parameter). If
`data` is not specified, you must provide explcit `options`.

`column` str \| None  
The name of a column from which to pull options. The unique column
values are used as options. Used in conjunction with the `data`
parameter.

`options` Sequence\[str \| bool \| float\] \| Mapping\[str, str \| bool \| float\] \| None  
A `list` or `dict` of options (provide a `dict` if you want values to
map to alternate labels). Alternative to populating options from a
database column via `data` and `column`.

`target` [Param](inspect_viz.qmd#param) \| [Selection](inspect_viz.qmd#selection) \| None  
A `Param` or `Selection` that this radio group should update. For a
`Param`, the selected value is set to be the new param value. For a
`Selection`, a predicate of the form column = value will be added to the
selection.

`field` str \| None  
The data column name to use within generated selection clause
predicates. Defaults to the `column` parameter.

`label` str \| None  
A text label for the input. If unspecified, the column name (if
provided) will be used by default.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data source indicated by the `data` parameter.

### checkbox_group

Checkbox group.

Radio groups can be populated either from a database table (via the
`data` and `column` parameters) or from a static set of options (via the
`options` parameter).

Checkbox groups have a `target` which is either a `Param` or
`Selection`. In the latter case, the `field` parameter determines the
data column name to use within generated selection clause predicates
(defaulting to `column`). If no `target` is specified then the data
source’s selection is used as the target.

The intitial selected values will be empty when `target` is a
`Selection` (indicating select all records) and the param value(s) when
`target` is a `Param` (param values should be an array with one or more
checkbox values).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/43bc7cbad55804123a0150d2f5f083c28b44e0c1/src/inspect_viz/input/_checkbox_group.py#L8)

``` python
def checkbox_group(
    data: Data | None = None,
    *,
    column: str | None = None,
    options: Sequence[str | bool | float] | dict[str, str | bool | float] | None = None,
    target: Param | Selection | None = None,
    field: str | None = None,
    label: str | None = None,
    filter_by: Selection | None = None,
) -> Component
```

`data` [Data](inspect_viz.qmd#data) \| None  
The data source (used in conjunction with the `column` parameter). If
`data` is not specified, you must provide explcit `options`.

`column` str \| None  
The name of a column from which to pull options. The unique column
values are used as options. Used in conjunction with the `data`
parameter.

`options` Sequence\[str \| bool \| float\] \| dict\[str, str \| bool \| float\] \| None  
A `list` or `dict` of options (provide a `dict` if you want values to
map to alternate labels). Alternative to populating options from a
database column via `data` and `column`.

`target` [Param](inspect_viz.qmd#param) \| [Selection](inspect_viz.qmd#selection) \| None  
A `Param` or `Selection` that this radio group should update. For a
`Param`, the selected value is set to be the new param value. For a
`Selection`, a predicate of the form column IN (values) will be added to
the selection.

`field` str \| None  
The data column name to use within generated selection clause
predicates. Defaults to the `column` parameter.

`label` str \| None  
A text label for the input. If unspecified, the column name (if
provided) will be used by default.

`filter_by` [Selection](inspect_viz.qmd#selection) \| None  
A selection to filter the data source indicated by the `data` parameter.
