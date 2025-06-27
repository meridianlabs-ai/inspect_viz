from typing import Literal

from pydantic import BaseModel, JsonValue

from inspect_viz._util.marshall import dict_remove_none

from .._core import Component, Data
from .._core.selection import Selection


class Column(BaseModel):
    """Column configuration options for table display.

    Args:
        name: The column name as it appears in the data source. This is required.
        label: The text label for the column header. If not specified, the column name is used.
        align: Text alignment for the column. Valid values are "left", "right",
            "center", and "justify". By default, numbers are right-aligned and other
            values are left-aligned.
        width: Column width in pixels.
        flex: The flex value of the table widget, used to determine how much space it
            should take relative to other widgets in a layout. If specified, width is
            ignored.
        sortable: Whether sorting is enabled for this column.
        filterable: Whether filtering is enabled for this column.
        resizable: Whether the column width can be adjusted by the user.
        min_width: Minimum column width in pixels.
        max_width: Maximum column width in pixels.
        format: Format string for column values. Use d3-format for numeric columns or
            d3-time-format for datetime columns.
        auto_height: Whether the column cell height is automatically adjusted based on
            content.
        wrap_text: Whether the column text is wrapped to fit within the cell.
        header_align: Text alignment for the column header. Valid values are "left",
            "right", "center", and "justify". By default, left aligned.
        header_auto_height: Whether the column header cell height is automatically
            adjusted based on content.
        header_wrap_text: Whether the column header text is wrapped to fit within the
            header cell.
    """

    name: str
    label: str | None = None
    align: Literal["left", "right", "center", "justify"] | None = None
    format: str | None = None
    width: float | None = None
    flex: float | None = None
    min_width: float | None = None
    max_width: float | None = None
    auto_height: bool | None = None
    sortable: bool | None = None
    filterable: bool | None = None
    resizable: bool | None = None
    wrap_text: bool | None = None
    header_align: Literal["left", "right", "center", "justify"] | None = None
    header_auto_height: bool | None = None
    header_wrap_text: bool | None = None


class Pagination(BaseModel):
    """Pagination configuration for table display.

    Args:
        page_size: Number of rows to load per page.
        page_size_selector: Determines if the page size selector is shown in the
            pagination panel or not. Set to a list of values to show the page size
            selector with custom list of possible page sizes. Set to true to show the
            page size selector with the default page sizes [20, 50, 100]. Set to false
            to hide the page size selector.
        auto_page_size: If true, the number of rows to load per page is automatically
            adjusted by the grid so each page shows enough rows to just fill the area
            designated for the grid. If false, paginationPageSize is used.
    """

    page_size: int | None = None
    page_size_selector: list[int] | bool | None = None
    auto_page_size: bool | None = None


def table(
    data: Data,
    filter_by: Selection | None = None,
    columns: list[str | Column] | None = None,
    target: Selection | None = None,
    width: float | None = None,
    max_width: float | None = None,
    height: float | None = None,
    sorting: bool | None = None,
    filtering: bool | Literal["header", "row"] | None = None,
    pagination: bool | Pagination | None = None,
    header_height: float | None = None,
    row_height: float | None = None,
    select: Literal[
        "hover",
        "single_row",
        "multiple_row",
        "single_checkbox",
        "multiple_checkbox",
        "none",
    ]
    | None = None,
    select_all_scope: Literal["all", "filtered", "currentPage"] | None = None,
) -> Component:
    """Tabular display of data.

    Args:

        data: The data source for the table.
        filter_by: Selection to filter by (defaults to data source selection).
        columns: A list of column names to include in the table grid. If unspecified,
            all table columns are included.
        target: The output selection. A selection clause of the form column IN (rows)
            will be added to the selection for each currently selected table row.
        select: The type of selection to use for the table. Valid values are "hover",
            "single_checkbox", "multiple_checkbox", "single_row", "multiple_row", and
            "none". Defaults to "hover".
        select_all_scope: If select 'multiple' is enabled, controls the scope of the
            select all option in the header. Valid values are 'all', 'filtered' or
            'currentPage'.
        column_options: A dictionary of column configuration options. The keys are
            column names and the values are dictionaries with column options.
        width: The total width of the table widget, in pixels.
        max_width: The maximum width of the table widget, in pixels.
        height: The height of the table widget, in pixels (defaults to 380).
        sorting: Set whether sorting columns is enabled.
        filtering: Enable filtering. If set to 'header' a filter button is shown in
            the table header. If set to 'row', a filter is shown in a row beneath the
            header.
        pagination: Enable pagination. If set to True, default pagination settings
            are used. If set to a Pagination object, custom pagination settings are
            used.
        header_height: The height of the table header, in pixels.
        row_height: The height of each table row, in pixels.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "input": "table",
            "from": data.table,
            "filter_by": filter_by or data.selection,
            "columns": [validate_column(data, c) for c in columns] if columns else None,
            "as": target,
            "width": width,
            "max_width": max_width,
            "height": height,
            "sorting": sorting,
            "filtering": filtering,
            "pagination": resolve_pagination(pagination),
            "header_height": header_height,
            "row_height": row_height,
            "select": select,
            "select_all_scope": select_all_scope,
        }
    )

    return Component(config=config)


def validate_column(data: Data | None, column: str | Column) -> str | Column:
    column_name = column.name if isinstance(column, Column) else column
    if data is not None:
        if column_name not in data.columns:
            raise ValueError(f"Column '{column}' was not found in the data source.")
    return column


def resolve_pagination(
    pagination: bool | Pagination | None = None,
) -> Pagination | None:
    """Resolve pagination configuration."""
    if isinstance(pagination, Pagination):
        return pagination
    if pagination is True:
        return Pagination()
    else:
        return None
