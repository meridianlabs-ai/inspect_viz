# inspect_viz.table – Inspect Viz

### table

Tabular display of data.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/ed1e7276aa39950499a3a4914a9d41476ca808c5/src/inspect_viz/table/_table.py#L243)

``` python
def table(
    data: Data,
    *,
    columns: Sequence[str | Column] | None = None,
    filter_by: Selection | None = None,
    target: Selection | None = None,
    select: Literal[
        "hover",
        "single_row",
        "multiple_row",
        "single_checkbox",
        "multiple_checkbox",
        "none",
    ]
    | None = None,
    width: float | None = None,
    max_width: float | None = None,
    height: float | Literal["auto"] | None = None,
    header_height: float | None = None,
    row_height: float | None = None,
    sorting: bool | None = None,
    filtering: bool | Literal["header", "row"] | None = None,
    pagination: bool | Pagination | None = None,
    style: TableStyle | None = None,
) -> Component
```

`data` [Data](../reference/inspect_viz.html.md#data)  
The data source for the table.

`columns` Sequence\[str \| [Column](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#column)\] \| None  
A list of column names to include in the table grid. If unspecified, all table columns are included.

`filter_by` [Selection](../reference/inspect_viz.html.md#selection) \| None  
Selection to filter by (defaults to data source selection).

`target` [Selection](../reference/inspect_viz.html.md#selection) \| None  
The output selection. A selection clause of the form column IN (rows) will be added to the selection for each currently selected table row.

`select` Literal\['hover', 'single_row', 'multiple_row', 'single_checkbox', 'multiple_checkbox', 'none'\] \| None  
The type of selection to use for the table. Valid values are “hover”, “single_checkbox”, “multiple_checkbox”, “single_row”, “multiple_row”, and “none”. Defaults to “single_row”.

`width` float \| None  
The total width of the table widget, in pixels.

`max_width` float \| None  
The maximum width of the table widget, in pixels.

`height` float \| Literal\['auto'\] \| None  
Either the height of the table widget in pixels, or “auto”. If “auto”, the height of the table will fit the content within the table up to the 500px. Defaults to “auto”.

`header_height` float \| None  
The height of the table header, in pixels.

`row_height` float \| None  
The height of each table row, in pixels.

`sorting` bool \| None  
Set whether sorting columns is enabled.

`filtering` bool \| Literal\['header', 'row'\] \| None  
Enable filtering. If set to ‘header’ a filter button is shown in the table header. If set to ‘row’, a filter is shown in a row beneath the header.

`pagination` bool \| Pagination \| None  
Enable pagination. If set to True, default pagination settings are used. If set to a Pagination object, custom pagination settings are used.

`style` TableStyle \| None  
The style configuration for the table display.
