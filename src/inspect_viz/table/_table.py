from typing import Literal, Sequence, cast

from pydantic import BaseModel, JsonValue

from inspect_viz._util.marshall import dict_remove_none
from inspect_viz.mark._channel import Channel
from inspect_viz.transform._transform import Transform

from .._core import Component, Data
from .._core.selection import Selection


class Column(BaseModel):
    """Column configuration options for table display.

    Args:
        column: The column name as it appears in the data source. This is required.
        label: The text label for the column header. If not specified, the column name is used.
        align: Text alignment for the column. Valid values are "left", "right",
            "center", and "justify". By default, numbers are right-aligned and other
            values are left-aligned.
        format: Format string for column values. Use d3-format for numeric columns or
            d3-time-format for datetime columns.
        width: Column width in pixels.
        min_width: Minimum column width in pixels.
        max_width: Maximum column width in pixels.
        flex: The flex value of the table widget, used to determine how much space it
            should take relative to other widgets in a layout. If specified, width is
            ignored.
        auto_height: Whether the column cell height is automatically adjusted based on
            content.
        sortable: Whether sorting is enabled for this column.
        filterable: Whether filtering is enabled for this column.
        resizable: Whether the column width can be adjusted by the user.
        wrap_text: Whether the column text is wrapped to fit within the cell.
        header_align: Text alignment for the column header. Valid values are "left",
            "right", "center", and "justify". By default, left aligned.
        header_auto_height: Whether the column header cell height is automatically
            adjusted based on content.
        header_wrap_text: Whether the column header text is wrapped to fit within the
            header cell.
    """

    column: Channel
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

    def __init__(
        self,
        column: Channel,
        *,
        label: str | None = None,
        align: Literal["left", "right", "center", "justify"] | None = None,
        format: str | None = None,
        width: float | None = None,
        min_width: float | None = None,
        max_width: float | None = None,
        flex: float | None = None,
        auto_height: bool | None = None,
        sortable: bool | None = None,
        filterable: bool | None = None,
        resizable: bool | None = None,
        wrap_text: bool | None = None,
        header_align: Literal["left", "right", "center", "justify"] | None = None,
        header_auto_height: bool | None = None,
        header_wrap_text: bool | None = None,
    ):
        super().__init__(
            column=column,
            label=label,
            align=align,
            format=format,
            width=width,
            flex=flex,
            min_width=min_width,
            max_width=max_width,
            auto_height=auto_height,
            sortable=sortable,
            filterable=filterable,
            resizable=resizable,
            wrap_text=wrap_text,
            header_align=header_align,
            header_auto_height=header_auto_height,
            header_wrap_text=header_wrap_text,
        )


def column(
    column: Channel,
    *,
    label: str | None = None,
    align: Literal["left", "right", "center", "justify"] | None = None,
    format: str | None = None,
    width: float | None = None,
    min_width: float | None = None,
    max_width: float | None = None,
    flex: float | None = None,
    auto_height: bool | None = None,
    sortable: bool | None = None,
    filterable: bool | None = None,
    resizable: bool | None = None,
    wrap_text: bool | None = None,
    header_align: Literal["left", "right", "center", "justify"] | None = None,
    header_auto_height: bool | None = None,
    header_wrap_text: bool | None = None,
) -> Column:
    """Create a column configuration for table display.

    Args:
        column: The column name as it appears in the data source. This is required.
        label: The text label for the column header. If not specified, the column name is used.
        align: Text alignment for the column. Valid values are "left", "right",
            "center", and "justify". By default, numbers are right-aligned and other
            values are left-aligned.
        format: Format string for column values. Use d3-format for numeric columns or
            d3-time-format for datetime columns.
        width: Column width in pixels.
        min_width: Minimum column width in pixels.
        max_width: Maximum column width in pixels.
        flex: The flex value of the table widget, used to determine how much space it
            should take relative to other widgets in a layout. If specified, width is
            ignored.
        auto_height: Whether the column cell height is automatically adjusted based on
            content.
        sortable: Whether sorting is enabled for this column.
        filterable: Whether filtering is enabled for this column.
        resizable: Whether the column width can be adjusted by the user.
        wrap_text: Whether the column text is wrapped to fit within the cell.
        header_align: Text alignment for the column header. Valid values are "left",
            "right", "center", and "justify". By default, left aligned.
        header_auto_height: Whether the column header cell height is automatically
            adjusted based on content.
        header_wrap_text: Whether the column header text is wrapped to fit within the
            header cell.

    Returns:
        Column: A configured Column object.
    """
    return Column(
        column=column,
        label=label,
        align=align,
        format=format,
        width=width,
        min_width=min_width,
        max_width=max_width,
        flex=flex,
        auto_height=auto_height,
        sortable=sortable,
        filterable=filterable,
        resizable=resizable,
        wrap_text=wrap_text,
        header_align=header_align,
        header_auto_height=header_auto_height,
        header_wrap_text=header_wrap_text,
    )


class Pagination(BaseModel):
    """Pagination configuration for table display.

    Args:
        page_size: Number of rows to load per page, or "auto" to fit the number of
            rows in a page to the available space. Defaults to "auto".
        page_size_selector: Determines if the page size selector is shown in the
            pagination panel or not. Set to a list of values to show the page size
            selector with custom list of possible page sizes. Set to true to show the
            page size selector with the default page sizes [20, 50, 100]. Set to false
            to hide the page size selector.
    """

    page_size: int | Literal["auto"] | None = None
    page_size_selector: list[int] | bool | None = None

    def __init__(
        self,
        page_size: int | Literal["auto"] | None = None,
        *,
        page_size_selector: list[int] | bool | None = None,
    ):
        super().__init__(
            page_size=page_size,
            page_size_selector=page_size_selector,
        )


class TableStyle(BaseModel):
    """Style configuration for table display.

    Args:
        background_color: Background color for the table.
        foreground_color: Foreground color for the table.
        accent_color: Accent color for the table, used for highlights and
            other emphasis.
        text_color: Text color for the table.
        header_text_color: Text color for the table header.
        cell_text_color: Text color for the table cells.

        font_family: Font family for the table text.
        header_font_family: Font family for the table header text.
        cell_font_family: Font family for the table cell text.

        spacing: Spacing configuration for the table. Padding and margins throughout the table are automatically calculated based on this value.

        border_color: Border color for the table.
        border_width: Border width for the table.
        border_radius: Border radius for the table.

        selected_row_background_color: Background color for selected rows.
    """

    background_color: str | None = None
    foreground_color: str | None = None
    accent_color: str | None = None
    text_color: str | None = None
    header_text_color: str | None = None
    cell_text_color: str | None = None
    selected_row_background_color: str | None = None

    font_family: str | None = None
    header_font_family: str | None = None
    cell_font_family: str | None = None

    spacing: float | str | None = None

    border_color: str | None = None
    border_width: float | str | None = None
    border_radius: float | str | None = None


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
    height: float | None = None,
    header_height: float | None = None,
    row_height: float | None = None,
    sorting: bool | None = None,
    filtering: bool | Literal["header", "row"] | None = None,
    pagination: bool | Pagination | None = None,
    style: TableStyle | None = None,
) -> Component:
    """Tabular display of data.

    Args:
        data: The data source for the table.
        columns: A list of column names to include in the table grid. If unspecified,
            all table columns are included.
        filter_by: Selection to filter by (defaults to data source selection).
        target: The output selection. A selection clause of the form column IN (rows)
            will be added to the selection for each currently selected table row.
        select: The type of selection to use for the table. Valid values are "hover",
            "single_checkbox", "multiple_checkbox", "single_row", "multiple_row", and
            "none". Defaults to "single_row".
        width: The total width of the table widget, in pixels.
        max_width: The maximum width of the table widget, in pixels.
        height: The height of the table widget, in pixels (defaults to 300).
        header_height: The height of the table header, in pixels.
        row_height: The height of each table row, in pixels.
        sorting: Set whether sorting columns is enabled.
        filtering: Enable filtering. If set to 'header' a filter button is shown in
            the table header. If set to 'row', a filter is shown in a row beneath the
            header.
        pagination: Enable pagination. If set to True, default pagination settings
            are used. If set to a Pagination object, custom pagination settings are
            used.
        style: The style configuration for the table display.
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
            "style": style,
        }
    )

    return Component(config=config)


def validate_column(data: Data | None, column: str | Column) -> str | Column:
    if data is None:
        return column

    column_name: str | None = None
    if isinstance(column, Column):
        if isinstance(column.column, str):
            column_name = column.column
        elif isinstance(column.column, dict):
            column_name = cast(str, next(iter(column.column.values())))
    else:
        column_name = column

    if column_name is not None and column_name not in data.columns:
        raise ValueError(f"Column '{column_name}' was not found in the data source.")

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
