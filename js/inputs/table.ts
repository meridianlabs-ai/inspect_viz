import {
    clausePoints,
    FieldInfo,
    isSelection,
    queryFieldInfo,
    throttle,
    toDataColumns,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

import {
    and,
    asc,
    contains,
    desc,
    eq,
    ExprNode,
    FilterExpr,
    gt,
    gte,
    isNull,
    literal,
    lt,
    lte,
    neq,
    not,
    or,
    prefix,
    suffix,
    Query,
    SelectQuery,
    sql,
    column,
    avg,
    count,
    sum,
    argmax,
    mad,
    max,
    min,
    product,
    geomean,
    median,
    mode,
    variance,
    stddev,
    skewness,
    kurtosis,
    entropy,
    varPop,
    stddevPop,
    first,
    last,
    stringAgg,
    arrayAgg,
    argmin,
    quantile,
    corr,
    covarPop,
    regrIntercept,
    regrSlope,
    regrCount,
    regrR2,
    regrSXX,
    regrSYY,
    regrSXY,
    regrAvgX,
    regrAvgY,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm';

import {
    createGrid,
    GridOptions,
    ColDef,
    ModuleRegistry,
    AllCommunityModule,
    GridApi,
    themeBalham,
    FilterModel,
    TextFilterModel,
    NumberFilterModel,
    DateFilterModel,
    IMultiFilterModel,
    SetFilterModel,
    ICombinedSimpleModel,
    RowSelectionOptions,
} from 'https://cdn.jsdelivr.net/npm/ag-grid-community@33.3.2/+esm';

import * as d3Format from 'https://cdn.jsdelivr.net/npm/d3-format@3.1.0/+esm';
import * as d3TimeFormat from 'https://cdn.jsdelivr.net/npm/d3-time-format@4.1.0/+esm';
import { Input, InputOptions } from './input';
import { generateId } from '../util/id';
import { JSType } from '@uwdata/mosaic-core';
import { AggregateNode, ExprValue } from '@uwdata/mosaic-sql';

type Transform = Record<string, any>;

type Channel = string | Transform | boolean | number | undefined | Array<boolean | number>;

// A column which has been resolved with user provided information
type ResolvedColumn = ResolvedSimpleColumn | ResolvedLiteralColumn | ResolvedAggregateColumn;

// Resolved Column adds additional information to the Column type
// based upon the raw column specifiction provided by the user, including
// any aggregatinon behavior.
export interface BaseResolvedColumn extends Column {
    // The column name as it will be used in the query (e.g. the alias for the column)
    // This could be synthesized if this is an aggregation or literal.
    column_name: string;
}

// A column which contains one or more literal values
export interface ResolvedLiteralColumn extends BaseResolvedColumn {
    type: 'literal';
}

// A column which contains an aggregate expression
export interface ResolvedAggregateColumn extends BaseResolvedColumn {
    // The actual column name in the database
    column_id: string;

    // The aggregate expression and its arguments, if this column is an aggregation.
    agg_expr: string;
    agg_expr_args: ExprValue[];

    type: 'aggregate';
}
// A column which is a simple column reference in the database.
export interface ResolvedSimpleColumn extends BaseResolvedColumn {
    // The actual column name in the database
    column_id: string;
    type: 'column';
}

export interface Column {
    column: Channel;
    label?: string;
    align?: 'left' | 'right' | 'center' | 'justify';
    format?: string;
    sortable?: boolean;
    filterable?: boolean;
    width?: number;
    flex?: number;
    resizable?: boolean;
    min_width?: number;
    max_width?: number;
    auto_height?: boolean;
    wrap_text?: boolean;
    header_auto_height?: boolean;
    header_align?: 'left' | 'right' | 'center' | 'justify';
    header_wrap_text?: boolean;
}

export interface TableStyle {
    background_color?: string;
    foreground_color?: string;
    accent_color?: string;
    text_color?: string;
    header_text_color?: string;
    cell_text_color?: string;

    font_family?: string;
    header_font_family?: string;
    cell_font_family?: string;

    spacing?: number | string;

    border_color?: string;
    border_width?: number | string;
    border_radius?: number | string;

    selected_row_background_color?: string;
}

export interface TableOptions extends InputOptions {
    filter_by: any;
    from: string;
    columns?: Array<string | Column>;
    width?: number;
    height?: number;
    max_width?: number;
    pagination?: {
        page_size?: number | 'auto';
        page_size_selector?: number[] | boolean;
    };
    sorting?: boolean;
    filtering?: boolean | 'header' | 'row';
    row_height?: number;
    header_height?: number | 'auto';
    select?:
        | 'hover'
        | 'single_row'
        | 'multiple_row'
        | 'single_checkbox'
        | 'multiple_checkbox'
        | 'none';
    style?: TableStyle;
}

interface ColSortModel {
    colId: string;
    sort: 'asc' | 'desc' | null | undefined;
}

export class Table extends Input {
    private readonly id_: string;
    private columns_: ResolvedColumn[] | null = null;
    private columnsByName_: Record<string, ResolvedColumn> | null = null;
    private columnTypes_: Record<string, JSType> = {};
    private readonly height_: number | undefined;

    private readonly gridContainer_: HTMLDivElement;
    private grid_: GridApi | null = null;
    private gridOptions_: GridOptions;

    private currentRow_: number;
    private sortModel_: ColSortModel[] = [];
    private filterModel_: FilterModel = {};

    private data_: { numRows: number; columns: Record<string, Array<unknown>> } = {
        numRows: 0,
        columns: {},
    };

    constructor(protected readonly options_: TableOptions) {
        super(options_.filter_by);

        // register ag-grid modules
        ModuleRegistry.registerModules([AllCommunityModule]);

        // id
        this.id_ = generateId();

        // state
        this.currentRow_ = -1;

        // class decoration
        this.element.classList.add('inspect-viz-table');

        // height and width
        this.height_ = this.options_.height;
        if (typeof this.options_.width === 'number') {
            this.element.style.width = `${this.options_.width}px`;
        }
        if (this.options_.max_width) {
            this.element.style.maxWidth = `${this.options_.max_width}px`;
        }
        if (this.options_.height) {
            this.element.style.height = `${this.height_}px`;
        }

        if (this.options_.style) {
            // note that since these are CSS variables that we define
            // for adapting to Quarto themes, we need to use CSS
            // vars to override the variables
            if (this.options_.style?.background_color) {
                this.element.style.setProperty(
                    '--ag-background-color',
                    this.options_.style.background_color
                );
            }

            if (this.options_.style?.foreground_color) {
                this.element.style.setProperty(
                    '--ag-foreground-color',
                    this.options_.style.foreground_color
                );
            }

            if (this.options_.style?.accent_color) {
                this.element.style.setProperty(
                    '--ag-accent-color',
                    this.options_.style.accent_color
                );
            }
        }

        // create grid container
        this.gridContainer_ = document.createElement('div');
        this.gridContainer_.id = this.id_;
        this.gridContainer_.style.width = '100%';
        this.gridContainer_.style.height = '100%';
        this.element.appendChild(this.gridContainer_);

        // create grid options
        this.gridOptions_ = this.createGridOptions(this.options_);
    }

    // contribute a selection clause back to the target selection
    clause(rows: number[] = []) {
        const fields = this.getDatabaseColumns().map(column => column.column_id);

        const values = rows.map(row => {
            return fields.map(f => this.data_.columns[f][row]);
        });
        return clausePoints(fields, values, { source: this });
    }

    // mosaic calls this and initialization to let us fetch the schema
    // and do related setup
    async prepare() {
        // query available columns from the database
        const table = this.options_.from;
        const schema = await queryFieldInfo(this.coordinator!, [{ column: '*', table }]);

        // Resolve the columns using either the user provided columns or all
        // the fields in the schema
        const userColumns = this.options_.columns
            ? this.options_.columns
            : schema.map(f => f.column);
        this.columns_ = resolveColumns(userColumns);
        this.columnsByName_ = this.columns_.reduce(
            (acc, col) => {
                acc[col.column_name] = col;
                return acc;
            },
            {} as Record<string, ResolvedColumn>
        );

        // For each non-literal column, we need to resolve the type
        // Do this by using the schema query to get column types and use the
        // column type as the type (even for aggregate columns  )
        this.columns_
            .filter(c => c.type !== 'literal')
            .forEach(column => {
                const item = schema.find(s => s.column === column.column_id);
                if (item) {
                    this.columnTypes_[column.column_name] = item.type as JSType;
                }
            });

        // For literals, we need to determine their types based on the values provided.
        this.getLiteralColumns().forEach(c => {
            const colVal = c.column;
            if (Array.isArray(colVal)) {
                // Peek at the first element to determine the type
                const firstVal = colVal[0];
                const typeStr =
                    typeof firstVal === 'boolean'
                        ? 'boolean'
                        : typeof firstVal === 'number'
                          ? 'number'
                          : undefined;
                if (typeStr) {
                    this.columnTypes_[c.column_name] = typeStr as JSType;
                }
            } else if (typeof colVal === 'boolean') {
                this.columnTypes_[c.column_name] = 'boolean';
            } else if (typeof colVal === 'number') {
                this.columnTypes_[c.column_name] = 'number';
            }
        });

        // create column definitions for ag-grid
        const columnDefs: ColDef[] = this.columns_.map(column => {
            const t = this.columnTypes_[column.column_name];
            return this.createColumnDef(column.column_name, t);
        });
        this.gridOptions_.columnDefs = columnDefs;

        // create the grid
        this.grid_ = createGrid(this.gridContainer_, this.gridOptions_);
    }

    // mosaic calls this every time it needs to show data to find
    // out what query we want to run
    query(filter: FilterExpr[] = []) {
        const selectItems: Record<string, ExprNode | string> = {};
        const groupBy: string[] = [];
        let has_aggregate = false;

        // Go through each column and determine the select item
        // for the column. Some columns may not have items because
        // they are providing a literal or list of literals.
        for (const column of this.getDatabaseColumns()) {
            if (column.type === 'aggregate') {
                const item = aggregateExpression(column);
                selectItems[item[0]] = item[1];
                has_aggregate = true;
            } else if (column.type === 'column') {
                selectItems[column.column_id] = column.column_id;
                groupBy.push(column.column_id);
            }
        }

        // Select the columns
        let query = Query.from(this.options_.from).select(
            Object.keys(selectItems).length ? selectItems : '*'
        );

        // Group by non aggregated columns
        if (has_aggregate && groupBy.length > 0) {
            query.groupby(groupBy);
        }

        // apply the external filter
        query = query.where(...filter);

        // apply the filter model
        Object.keys(this.filterModel_).forEach(columnName => {
            if (!this.columnsByName_) {
                throw new Error('Columns not resolved yet. Please call prepare() first.');
            }

            const col = this.columnsByName_[columnName];
            if (col.type !== 'literal') {
                const useHaving = col?.type === 'aggregate';
                const filter = this.filterModel_[columnName] as SupportedFilter;
                const expression = filterExpression(columnName, filter, query);
                if (expression) {
                    if (useHaving) {
                        query.having(expression);
                    } else {
                        query = query.where(expression);
                    }
                }
            }
        });

        // Apply sorting
        if (this.sortModel_.length > 0) {
            this.sortModel_.forEach(sort => {
                if (!this.columnsByName_) {
                    throw new Error('Columns not resolved yet. Please call prepare() first.');
                }

                const col = this.columnsByName_[sort.colId];
                if (col.type !== 'literal') {
                    query = query.orderby(sort.sort === 'asc' ? asc(sort.colId) : desc(sort.colId));
                }
            });
        }

        return query;
    }

    // mosaic returns the results of the query() in this function.
    queryResult(data: any) {
        this.data_ = toDataColumns(data);
        return this;
    }

    // requests a client UI update (e.g. to reflect results from a query)
    update() {
        this.updateGrid(null);
        return this;
    }

    private updateGrid = throttle(async () => {
        if (!this.grid_) {
            return;
        }

        if (!this.columns_) {
            throw new Error('Columns not resolved yet. Please call prepare() first.');
        }

        // convert column-based data to row-based data for ag-grid
        const rowData: any[] = [];
        for (let i = 0; i < this.data_.numRows; i++) {
            const row: any = {};
            this.columns_.forEach(({ column_name, column }) => {
                if (Array.isArray(column)) {
                    const index = i % column.length;
                    row[column_name] = column[index];
                } else if (typeof column === 'boolean' || typeof column === 'number') {
                    row[column_name] = column;
                } else {
                    row[column_name] = this.data_.columns[column_name][i];
                }
            });

            rowData.push(row);
        }

        this.grid_.setGridOption('rowData', rowData);
    });

    private createGridOptions(options: TableOptions): GridOptions {
        const headerHeightPixels =
            typeof options.header_height === 'string' ? undefined : options.header_height;
        const hoverSelect = options.select === 'hover';
        const explicitSelection = resolveRowSelection(options);

        // Theme
        const gridTheme = themeBalham.withParams({
            textColor: this.options_.style?.text_color,
            headerTextColor:
                this.options_.style?.header_text_color || this.options_.style?.text_color,
            cellTextColor: this.options_.style?.cell_text_color,

            fontFamily: this.options_.style?.font_family,
            headerFontFamily:
                this.options_.style?.header_font_family || this.options_.style?.font_family,
            cellFontFamily:
                this.options_.style?.cell_font_family || this.options_.style?.font_family,

            spacing: this.options_.style?.spacing || 4,

            borderColor: this.options_.style?.border_color,
            borderRadius: this.options_.style?.border_radius,

            selectedRowBackgroundColor: this.options_.style?.selected_row_background_color,
        });

        // initialize grid options
        return {
            // always pass filter to allow server-side filtering
            pagination: !!options.pagination,
            paginationAutoPageSize:
                options.pagination?.page_size === 'auto' ||
                options.pagination?.page_size === undefined,
            paginationPageSizeSelector: options.pagination?.page_size_selector,
            paginationPageSize:
                typeof options.pagination?.page_size === 'number'
                    ? options.pagination.page_size
                    : undefined,
            animateRows: false,
            headerHeight: headerHeightPixels,
            rowHeight: options.row_height,
            columnDefs: [],
            rowData: [],
            rowSelection: explicitSelection,
            suppressCellFocus: true,
            enableCellTextSelection: true,
            theme: gridTheme,
            onFilterChanged: () => {
                // Capture the filter model for server-side use
                this.filterModel_ = this.grid_?.getFilterModel() || {};

                // Trigger server-side query
                this.requestQuery();
            },
            onSortChanged: () => {
                if (this.grid_) {
                    // make a sort model
                    const sortModel = this.grid_
                        .getColumnState()
                        .filter(col => col.sort)
                        .map(col => ({ colId: col.colId, sort: col.sort }));
                    this.sortModel_ = sortModel;

                    // requery using the new sort model
                    this.requestQuery();
                }
            },
            onSelectionChanged: event => {
                if (explicitSelection !== undefined && isSelection(this.options_.as)) {
                    if (event.selectedNodes) {
                        // Get the selected rows
                        const rowIndices = event.selectedNodes
                            .map(n => n.rowIndex)
                            .filter(n => n !== null);

                        // Update the selection clause in the target selection
                        this.options_.as.update(this.clause(rowIndices));
                    }
                }
            },
            onCellMouseOver: event => {
                if (hoverSelect && isSelection(this.options_.as)) {
                    const rowIndex = event.rowIndex;
                    if (
                        rowIndex !== undefined &&
                        rowIndex !== null &&
                        rowIndex !== this.currentRow_
                    ) {
                        this.currentRow_ = rowIndex;
                        this.options_.as.update(this.clause([rowIndex]));
                    }
                }
            },
            onCellMouseOut: () => {
                if (hoverSelect && isSelection(this.options_.as)) {
                    this.currentRow_ = -1;
                    this.options_.as.update(this.clause());
                }
            },
            onGridReady: () => {
                // When the grid is ready, we can update it with the initial data
                this.patchGrid();
            },
        };
    }

    private getLiteralColumns(): ResolvedLiteralColumn[] {
        if (!this.columns_) {
            throw new Error('Columns not resolved yet. Please call prepare() first.');
        }

        return this.columns_.filter(c => c.type === 'literal');
    }

    private getDatabaseColumns(): Array<ResolvedSimpleColumn | ResolvedAggregateColumn> {
        if (!this.columns_) {
            throw new Error('Columns not resolved yet. Please call prepare() first.');
        }

        return this.columns_.filter(c => c.type === 'column' || c.type === 'aggregate');
    }

    private createColumnDef(column_name: string, type: JSType): ColDef {
        if (!this.columnsByName_) {
            throw new Error('Columns not resolved yet. Please call prepare() first.');
        }

        const column = this.columnsByName_[column_name] || {};

        // Align, numbers right aligned by default
        const align = column.align || (type === 'number' ? 'right' : 'left');
        const headerAlignment = column.header_align;

        // Format string
        const formatter = formatterForType(type, column.format);

        // Sorting / filtering
        const sortable = this.options_.sorting !== false && column.sortable !== false;
        const filterable = this.options_.filtering !== false && column.filterable !== false;

        // Sizing
        const resizable = column.resizable !== false;

        // Min and max width
        const minWidth = column.min_width;
        const maxWidth = column.max_width;

        // auto height
        const autoHeight = column.auto_height;
        const autoHeaderHeight =
            this.options_.header_height === 'auto' && column.header_auto_height !== false;

        // wrap text
        const wrapText = column.wrap_text;
        const wrapHeaderText = column.header_wrap_text;

        // flex
        const flex = column.flex;

        // Disables client side sorting (used for non-literal columns
        // where the database can handle the sorting)
        const disableClientSort = (_valueA: unknown, _valueB: unknown) => {
            return 0;
        };

        // Position the filter below the header
        const colDef: ColDef = {
            field: column_name,
            headerName: column.label || column_name,
            headerClass: headerClasses(headerAlignment),
            cellStyle: { textAlign: align },
            comparator: column.type !== 'literal' ? disableClientSort : undefined,
            filter: !filterable ? false : filterForColumnType(type),
            flex,
            sortable,
            resizable,
            minWidth,
            maxWidth,
            autoHeight,
            autoHeaderHeight,
            wrapText,
            wrapHeaderText,
            floatingFilter: this.options_.filtering === 'row',
            // Disable column moving
            suppressMovable: true,
            valueFormatter: params => {
                // Format the value if a format is provided
                const value = params.value;
                if (formatter && value !== null && value !== undefined) {
                    return formatter(value);
                }
                return value;
            },
        };

        // Set columns widths, if explicitly provided
        // otherwise use flex to make all columns equal
        const width = column.width;
        if (width) {
            colDef.width = width;
        } else if (flex === undefined || flex === null) {
            colDef.flex = 1;
        }

        return colDef;
    }

    private patchGrid() {
        if (!this.grid_) {
            return;
        }

        const columns = this.grid_.getColumns();
        if (columns) {
            columns.forEach(async column => {
                if (!this.columnsByName_) {
                    throw new Error('Columns not resolved yet. Please call prepare() first.');
                }

                const colId = column.getColId();
                const filterInstance = await this.grid_!.getColumnFilterInstance(colId);
                const col = this.columnsByName_[colId];

                // This is a workaround to disable client side filtering so we can implement
                // filtering using the query method instead.
                //
                // Since literal columns aren't filtered in the database, we instead
                // use client side filtering for these
                if (
                    filterInstance &&
                    typeof filterInstance.doesFilterPass === 'function' &&
                    col.type !== 'literal'
                ) {
                    filterInstance.doesFilterPass = () => true;
                }
            });
        }
    }

    // all mosaic inputs implement this, not exactly sure what it does
    activate() {
        if (isSelection(this.options_.as)) {
            this.options_.as.activate(this.clause([]));
        }
    }
}

const resolveColumns = (columns: Array<string | Column>): ResolvedColumn[] => {
    let columnCount = 1;
    const incrementedColumnName = () => {
        return `col_${columnCount++}`;
    };

    return columns.map(col => {
        if (typeof col === 'string') {
            // Column is just a column id
            return {
                column_name: col,
                column_id: col,
                column: col,
                type: 'column',
            };
        } else if (typeof col === 'object' && col !== null) {
            // Column is an object (a Column), we need to parse the column
            // property to properly resolve it
            if (typeof col.column === 'string') {
                return {
                    ...col,
                    column_name: col.column,
                    column_id: col.column,
                    type: 'column',
                };
            } else if (typeof col.column === 'number') {
                // If the column is a number, treat it as an index
                // It has no column_id since it isn't in the database - we generate
                // a display alias for it
                return {
                    ...col,
                    column_name: incrementedColumnName(),
                    column: col.column,
                    type: 'literal',
                };
            } else if (typeof col.column === 'boolean') {
                // If the column is a boolean, treat it as a flag
                // It has no column_id since it isn't in the database - we generate
                // a display alias for it
                return {
                    ...col,
                    column_name: incrementedColumnName(),
                    column: col.column,
                    type: 'literal',
                };
            } else if (Array.isArray(col.column)) {
                // peek at the first element to determine the type
                if (col.column.length === 0) {
                    throw new Error('Empty array column is not supported');
                }
                return {
                    ...col,
                    column_name: incrementedColumnName(),
                    column: col.column,
                    type: 'literal',
                };
            } else if (typeof col.column === 'object') {
                const agg = Object.keys(col.column)[0];
                const targetColumn = col.column[agg];
                return {
                    ...col,
                    column_name: `${agg}_${targetColumn}`,
                    column_id: targetColumn,
                    agg_expr: agg,
                    agg_expr_args: [targetColumn],
                    type: 'aggregate',
                };
            } else {
                throw new Error('Unsupported column type: ' + typeof col.column);
            }
        } else {
            throw new Error(`Invalid column definition: ${col}`);
        }
    });
};

const headerClasses = (align?: 'left' | 'right' | 'center' | 'justify'): string[] | undefined => {
    if (!align) {
        return undefined;
    }
    return [`header-${align}`];
};

const resolveRowSelection = (options: TableOptions): RowSelectionOptions<any, any> | undefined => {
    if (options.select === 'hover') {
        return undefined;
    }

    const selectType = options.select || 'single_row';
    if (selectType.startsWith('single_')) {
        return {
            mode: 'singleRow',
            checkboxes: options.select === 'single_checkbox',
            enableClickSelection: options.select === 'single_row',
        };
    } else if (selectType.startsWith('multiple_')) {
        return {
            mode: 'multiRow',
            selectAll: 'filtered',
            checkboxes: options.select === 'multiple_checkbox',
        };
    } else {
        throw new Error('Invalid select option: ' + options.select);
    }
};

const filterForColumnType = (type: string): string => {
    // Select the proper filter type based on the column type
    switch (type) {
        case 'number':
        case 'integer':
        case 'float':
        case 'decimal':
            return 'agNumberColumnFilter';
        case 'date':
        case 'datetime':
        case 'timestamp':
            return 'agDateColumnFilter';
        case 'boolean':
            return 'agTextColumnFilter';
        default:
            return 'agTextColumnFilter';
    }
};

const formatterForType = (type: string, formatStr?: string) => {
    switch (type) {
        case 'integer':
            return d3Format.format(formatStr || ',');
        case 'number':
        case 'float':
            return d3Format.format(formatStr || ',.2~f');
        case 'decimal':
            return d3Format.format(formatStr || ',.4~f');
        case 'date':
            // ISO date format (2024-03-15)
            return d3TimeFormat.timeFormat(formatStr || '%Y-%m-%d');
        case 'datetime':
        case 'timestamp':
            // ISO datetime format
            return d3TimeFormat.timeFormat(formatStr || '%Y-%m-%d %H:%M:%S');
        case 'boolean':
        case 'string':
        default:
            return undefined;
    }
};

type BaseFilter =
    | TextFilterModel
    | NumberFilterModel
    | DateFilterModel
    | IMultiFilterModel
    | SetFilterModel;

type SupportedFilter = BaseFilter | ICombinedSimpleModel<BaseFilter>;

const filterExpression = (
    colId: string,
    filter: SupportedFilter,
    query: SelectQuery
): ExprNode | undefined => {
    if (isCombinedSimpleModel(filter)) {
        const operator = filter.operator === 'AND' ? and : or;
        const expressions = filter.conditions
            ?.map((f: any) => {
                return filterExpression(colId, f as SupportedFilter, query);
            })
            .filter(e => e !== undefined);
        if (expressions && expressions.length > 0) {
            return operator(...expressions);
        }
    } else if (isTextFilter(filter)) {
        return simpleExpression(colId, filter.type, filter.filter, undefined, true);
    } else if (isNumberFilter(filter)) {
        return simpleExpression(colId, filter.type, filter.filter);
    } else if (isMultiFilter(filter)) {
        const expr = filter.filterModels
            ?.map((f: any) => {
                return filterExpression(colId, f, query);
            })
            .filter(e => e !== undefined);
        if (expr && expr.length > 0) {
            return and(...expr);
        }
    } else if (isDateFilter(filter)) {
        return simpleExpression(colId, filter.type, filter.dateFrom, filter.dateTo || undefined);
    } else if (isSetFilter(filter)) {
        console.warn('Set filter not implemented');
    }
};

export const simpleExpression = (
    colId: string,
    type:
        | 'empty'
        | 'equals'
        | 'notEqual'
        | 'lessThan'
        | 'lessThanOrEqual'
        | 'greaterThan'
        | 'greaterThanOrEqual'
        | 'inRange'
        | 'contains'
        | 'notContains'
        | 'startsWith'
        | 'endsWith'
        | 'blank'
        | 'notBlank'
        | null
        | undefined,
    filter: string | number | null | undefined,
    filterTo: string | number | null | undefined = undefined,
    textColumn: boolean = false
): ExprNode | undefined => {
    switch (type) {
        case 'equals':
            return eq(colId, literal(filter));
        case 'notEqual':
            return neq(colId, literal(filter));
        case 'contains':
            if (textColumn) {
                return sql`${column(colId)} ILIKE ${literal('%' + filter + '%')}`;
            } else {
                return contains(colId, String(filter));
            }
        case 'notContains':
            return not(contains(colId, String(filter)));
        case 'blank':
            return isNull(colId);
        case 'notBlank':
            return not(isNull(colId));
        case 'startsWith':
            return prefix(colId, String(filter));
        case 'endsWith':
            return suffix(colId, String(filter));
        case 'greaterThan':
            return gt(colId, literal(filter));
        case 'lessThan':
            return lt(colId, literal(filter));
        case 'greaterThanOrEqual':
            return gte(colId, literal(filter));
        case 'lessThanOrEqual':
            return lte(colId, literal(filter));
        case 'inRange':
            if (filterTo !== undefined && filterTo !== null) {
                return (gte(colId, literal(filter)), lte(colId, literal(filterTo)));
            }
            break;
        default:
            console.warn(`Unsupported filter type: ${type}`);
    }
    return undefined;
};

const aggregateExpression = (
    c: ResolvedAggregateColumn
): [alias: string, aggregate: AggregateNode] => {
    const aggExpr = c.agg_expr;

    const firstArg = () => {
        if (c.agg_expr_args.length > 0) {
            return c.agg_expr_args[0];
        }
        throw new Error(`Aggregate expression ${aggExpr} requires at least one argument`);
    };

    const secondArg = () => {
        if (c.agg_expr_args.length > 1) {
            return c.agg_expr_args[1];
        }
        throw new Error(`Aggregate expression ${aggExpr} requires at least two arguments`);
    };

    const r = (val: AggregateNode): [alias: string, aggregate: AggregateNode] => {
        return [c.column_name, val];
    };

    switch (aggExpr) {
        case 'count':
            return r(count(firstArg()));
        case 'sum':
            return r(sum(firstArg()));
        case 'avg':
            return r(avg(firstArg()));
        case 'argmax':
            return r(argmax(firstArg(), secondArg()));
        case 'mad':
            return r(mad(firstArg()));
        case 'max':
            return r(max(firstArg()));
        case 'min':
            return r(min(firstArg()));
        case 'product':
            return r(product(firstArg()));
        case 'geomean':
            return r(geomean(firstArg()));
        case 'median':
            return r(median(firstArg()));
        case 'mode':
            return r(mode(firstArg()));
        case 'variance':
            return r(variance(firstArg()));
        case 'stddev':
            return r(stddev(firstArg()));
        case 'skewness':
            return r(skewness(firstArg()));
        case 'kurtosis':
            return r(kurtosis(firstArg()));
        case 'entropy':
            return r(entropy(firstArg()));
        case 'varPop':
            return r(varPop(firstArg()));
        case 'stddevPop':
            return r(stddevPop(firstArg()));
        case 'first':
            return r(first(firstArg()));
        case 'last':
            return r(last(firstArg()));
        case 'stringAgg':
            return r(stringAgg(firstArg()));
        case 'arrayAgg':
            return r(arrayAgg(firstArg()));
        case 'argmin':
            return r(argmin(firstArg(), secondArg()));
        case 'quantile':
            return r(quantile(firstArg(), secondArg()));
        case 'corr':
            return r(corr(firstArg(), secondArg()));
        case 'covarPop':
            return r(covarPop(firstArg(), secondArg()));
        case 'regrIntercept':
            return r(regrIntercept(firstArg(), secondArg()));
        case 'regrSlope':
            return r(regrSlope(firstArg(), secondArg()));
        case 'regrCount':
            return r(regrCount(firstArg(), secondArg()));
        case 'regrR2':
            return r(regrR2(firstArg(), secondArg()));
        case 'regrSXX':
            return r(regrSXX(firstArg(), secondArg()));
        case 'regrSYY':
            return r(regrSYY(firstArg(), secondArg()));
        case 'regrSXY':
            return r(regrSXY(firstArg(), secondArg()));
        case 'regrAvgX':
            return r(regrAvgX(firstArg(), secondArg()));
        case 'regrAvgY':
            return r(regrAvgY(firstArg(), secondArg()));
        default:
            throw new Error(`Unsupported aggregate expression: ${aggExpr}`);
    }
};

const isCombinedSimpleModel = (
    filter: any
): filter is ICombinedSimpleModel<TextFilterModel | NumberFilterModel> => {
    return (
        typeof filter === 'object' &&
        filter !== null &&
        'operator' in filter &&
        'conditions' in filter &&
        (filter.operator === 'AND' || filter.operator === 'OR') &&
        typeof filter.conditions === 'object'
    );
};

const isTextFilter = (filter: any): filter is TextFilterModel => {
    return filter?.filterType === 'text';
};

const isNumberFilter = (filter: any): filter is NumberFilterModel => {
    return filter?.filterType === 'number';
};

const isDateFilter = (filter: any): filter is DateFilterModel => {
    return filter?.filterType === 'date' || filter?.filterType === 'dateString';
};

const isMultiFilter = (filter: any): filter is IMultiFilterModel => {
    return filter?.filterType === 'multi' && 'filterModels' in filter;
};

const isSetFilter = (filter: any): filter is SetFilterModel => {
    return filter?.filterType === 'set';
};
