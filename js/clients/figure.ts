import {
    Param,
    Selection,
    toDataColumns,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';
import { SelectQuery } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm';

import Plotly from 'https://esm.sh/plotly.js-dist-min@3.0.1';
import { VizClient } from './viz';

export interface PlotlyAxisMappings {
    x: string | null;
    y: string | null;
    z: string | null;
}

export interface PlotlyFigure {
    data: Plotly.Data[];
    layout?: Partial<Plotly.Layout>;
    config?: Partial<Plotly.Config>;
}

export class Figure extends VizClient {
    constructor(
        private readonly el_: HTMLElement,
        private readonly figure_: PlotlyFigure,
        private readonly axisMappings_: PlotlyAxisMappings,
        table: string,
        filterBy: Selection,
        queries: SelectQuery[],
        params: Map<string, Param>
    ) {
        super(table, filterBy, queries, params);
    }

    queryResult(data: any) {
        // resolve data
        const columns = toDataColumns(data).columns as Record<string, ArrayLike<unknown>>;
        const table = bindTable(this.figure_, this.axisMappings_, columns);

        console.log(this.figure_.data);
        console.log('---------');
        console.log(table);

        // resolve layout
        const layout = this.figure_.layout || {};
        layout.autosize = true;

        // resolve config
        const config = this.figure_.config || {};
        config.responsive = true;

        // render
        Plotly.react(this.el_, table, layout, config);
        return this;
    }
}

function bindTable(
    figure: PlotlyFigure,
    axisMappings: PlotlyAxisMappings,
    columns: Record<string, ArrayLike<unknown>>
): Plotly.Data[] {
    // don't mutate the passed traces
    const traces = structuredClone(figure.data);

    // Check if this is a multi-trace figure
    const isMultiTrace = traces.length > 1;

    // Early return for single-trace figures
    if (!isMultiTrace) {
        const trace = traces[0];
        const mapping = columnMapping(trace, Object.keys(columns), axisMappings);

        for (const [attr, col] of Object.entries(mapping)) {
            const arr = columns[col];
            if (arr) {
                setData(trace, attr.split('.'), arr);
            } else {
                console.warn(`Column "${col}" not found in table`);
            }
        }
        return traces;
    }

    // For multi-trace figures, we need to examine how traces are related to data

    // First, detect if this is a Plotly Express figure with specific properties
    const isPlotlyExpressFigure = detectPlotlyExpressFigure(traces);

    // Check for special cases like facets which have specific handling needs
    const hasFacets = detectFacetSubplots(traces, figure.layout);

    // Handle faceted figures specially since they keep all data in each trace but use different domains
    if (hasFacets) {
        // For faceted plots, each trace represents a different subplot but has all the data
        // We need to apply all data to each trace
        traces.forEach((trace: Plotly.Data) => {
            const mapping = columnMapping(trace, Object.keys(columns), axisMappings);
            for (const [attr, col] of Object.entries(mapping)) {
                const arr = columns[col];
                if (arr) {
                    setData(trace, attr.split('.'), arr);
                } else {
                    console.warn(`Column "${col}" not found in table`);
                }
            }
        });
        return traces;
    }

    // Try to identify categorical columns that might be used for trace separation
    const possibleCatColumns = findPossibleCategoricalColumns(traces, columns);

    // Group traces by type to handle different trace types with different strategies
    const tracesByType = groupTracesByType(traces);

    // For each trace, determine how to map the data
    traces.forEach((trace: Plotly.Data, _traceIndex: number) => {
        // Map the columns for this trace
        const mapping = columnMapping(trace, Object.keys(columns), axisMappings);

        // Try to determine which rows belong to this trace
        let indexArray: number[] | undefined = undefined;

        // Different approaches for trace filtering
        if (isPlotlyExpressFigure) {
            // For Plotly Express figures, use trace name and categorical columns
            indexArray = findIndicesForPlotlyExpressTrace(trace, possibleCatColumns, columns);
        }

        // If we couldn't get indices for a PE trace or this is a custom figure, try other approaches
        if (!indexArray) {
            const traceAny = trace as any;

            // First, try to use trace metadata directly if available
            if (getProp<any[]>(traceAny, '_index') !== undefined) {
                const indices = getProp<any[]>(traceAny, '_index');
                if (Array.isArray(indices)) {
                    indexArray = indices as number[];
                }
            }
            // Next, look for filter expression in the trace
            else if (getProp<string>(traceAny, '_filter') !== undefined) {
                const filterExpr = getProp<string>(traceAny, '_filter');
                if (typeof filterExpr === 'string') {
                    indexArray = applyFilterExpression(filterExpr, columns);
                }
            }
            // Try various other trace properties that might indicate data mapping
            else {
                indexArray = inferIndicesFromTraceProperties(trace, columns, possibleCatColumns);
            }
        }

        // If we're dealing with the same trace type repeated multiple times,
        // the traces may be split by categorical variable
        const traceType = getProp<string>(trace, 'type') || 'scatter';
        const tracesOfSameType = tracesByType[traceType] || [];

        if (!indexArray && tracesOfSameType.length > 1) {
            // We may need to split by index based on trace position
            const tracePosition = tracesOfSameType.indexOf(trace);
            if (tracePosition !== -1 && tracePosition < tracesOfSameType.length) {
                // Try splitting the data evenly among traces of the same type
                const dataLength = Object.values(columns)[0]?.length || 0;
                const chunkSize = Math.ceil(dataLength / tracesOfSameType.length);
                const startIdx = tracePosition * chunkSize;
                const endIdx = Math.min(startIdx + chunkSize, dataLength);
                indexArray = Array.from({ length: endIdx - startIdx }, (_, i) => startIdx + i);
            }
        }

        // Apply the data from columns to the trace
        for (const [attr, col] of Object.entries(mapping)) {
            const arr = columns[col];
            if (arr) {
                if (indexArray && indexArray.length > 0) {
                    // Filter the array to only include values at specified indices
                    const filteredArr = Array.from(arr).filter((_, i) => indexArray!.includes(i));
                    setData(trace, attr.split('.'), filteredArr);
                } else {
                    // No filtering required or unable to determine filtering logic,
                    // so use all data (falling back to original behavior)
                    setData(trace, attr.split('.'), arr);
                }
            } else {
                console.warn(`Column "${col}" not found in table`);
            }
        }
    });

    return traces;
}

function columnMapping(
    trace: Plotly.Data,
    cols: string[],
    axisMappings: PlotlyAxisMappings
): Record<string, string> {
    const map: Record<string, string> = {};
    const lc = cols.map(c => c.toLowerCase());

    for (const p of arrayProps(trace)) {
        const simple = p.split('.').pop()!.toLowerCase();
        const i = lc.indexOf(simple);
        if (i === -1) continue;

        const exists = p.split('.').reduce<unknown>((o, k) => (o as any)?.[k], trace) !== undefined;
        if (exists) map[p] = cols[i];
    }

    // fill x
    const needsX = !map.x && (!isOrientable(trace) || trace.orientation !== 'h');
    if (needsX && axisMappings.x) {
        map.x = axisMappings.x;
    }

    // fill y
    const needsY = !map.y && (isOrientable(trace) && trace.orientation === 'h' ? false : true);
    if (needsY && axisMappings.y) {
        map.y = axisMappings.y;
    }

    // optional z for 3-D traces
    const is3d = ['scatter3d', 'surface', 'mesh3d'].includes(trace.type ?? '');
    if (is3d && !map.z && axisMappings.z) {
        map.z = axisMappings.z;
    }

    return map;
}

function setData(trace: Plotly.Data, path: string[], val: unknown) {
    const last = path.pop()!;
    let cur = trace as Record<string, unknown>;
    for (const k of path) {
        if (cur[k] == null || typeof cur[k] !== 'object') cur[k] = {};
        cur = cur[k] as Record<string, unknown>;
    }
    cur[last] = val;
}

function arrayProps(obj: any, prefix = ''): string[] {
    return Object.entries(obj).flatMap(([k, v]) =>
        Array.isArray(v) || ArrayBuffer.isView(v)
            ? [`${prefix}${k}`]
            : typeof v === 'object' && v !== null
              ? arrayProps(v, `${prefix}${k}.`)
              : []
    );
}

interface OrientableTrace {
    orientation?: 'h' | 'v';
}

function isOrientable(t: Plotly.Data): t is Plotly.Data & OrientableTrace {
    return 'orientation' in t;
}

/**
 * Groups traces by their type for easier processing
 */
function groupTracesByType(traces: Plotly.Data[]): Record<string, Plotly.Data[]> {
    const result: Record<string, Plotly.Data[]> = {};

    traces.forEach(trace => {
        const type = trace.type || 'scatter'; // Default to scatter if no type specified
        if (!result[type]) {
            result[type] = [];
        }
        result[type].push(trace);
    });

    return result;
}

/**
 * Type-safe property accessor for Plotly trace objects
 * Allows accessing properties that might not be defined in all trace types
 */
function getProp<T>(obj: any, prop: string, defaultVal?: T): T | undefined {
    return obj && prop in obj ? obj[prop] : defaultVal;
}

/**
 * Detects if a figure is likely created with Plotly Express
 */
function detectPlotlyExpressFigure(traces: Plotly.Data[]): boolean {
    // Common characteristics of Plotly Express figures
    return traces.some(trace => {
        // Cast trace to any to safely access all properties
        const t = trace as any;

        // Plotly Express usually adds metadata to traces
        if (t._px !== undefined || t._plotlyExpressDefaults !== undefined) {
            return true;
        }

        // Often have standard legend groups or pattern matching for hover
        const legendgroup = getProp<string>(t, 'legendgroup');
        if (legendgroup && typeof legendgroup === 'string' && legendgroup.includes(':')) {
            return true;
        }

        // Specific trace naming patterns in newer versions
        const name = getProp<string | number>(t, 'name');
        if (name !== undefined && typeof name === 'string') {
            if (name.includes(' =') || name.match(/^[a-zA-Z_]+=[a-zA-Z0-9_]+$/)) {
                return true;
            }
        }

        return false;
    });
}

/**
 * Detects if a figure has facet subplots
 */
function detectFacetSubplots(traces: Plotly.Data[], layout?: Partial<Plotly.Layout>): boolean {
    // First check layout for facet grid properties
    if (layout) {
        // Check for grid structure in layout
        const hasGridStructure =
            layout.grid !== undefined ||
            Object.keys(layout).some(key => key.startsWith('xaxis') && key !== 'xaxis') ||
            Object.keys(layout).some(key => key.startsWith('yaxis') && key !== 'yaxis');

        if (hasGridStructure) return true;
    }

    // Then check traces for facet-specific properties
    return traces.some(trace => {
        // Safely check for subplot properties using our helper
        const xaxis = getProp<string>(trace, 'xaxis');
        const yaxis = getProp<string>(trace, 'yaxis');
        const hasSubplot = getProp<any>(trace as any, '_subplot') !== undefined;

        // Traces in facet plots often have specific subplot assignments
        return (
            (xaxis !== undefined && xaxis !== 'x') ||
            (yaxis !== undefined && yaxis !== 'y') ||
            // Some Plotly Express facet plots contain this meta information
            hasSubplot
        );
    });
}

/**
 * Find appropriate indices for a Plotly Express trace
 */
function findIndicesForPlotlyExpressTrace(
    trace: Plotly.Data,
    categoricalColumns: string[],
    columns: Record<string, ArrayLike<unknown>>
): number[] | undefined {
    const name = getProp<string | number>(trace, 'name');
    if (name === undefined) return undefined;

    // Try to match trace name against categorical column values
    for (const colName of categoricalColumns) {
        const colValues = columns[colName];
        if (!colValues) continue;

        // Try exact match (most common with categorical variables)
        const exactMatches = Array.from(colValues)
            .map((val, idx) => (val === name ? idx : -1))
            .filter(idx => idx !== -1);

        if (exactMatches.length > 0) {
            return exactMatches;
        }

        // Try more flexible matches based on common Plotly Express trace naming patterns
        // Ex: "species = setosa" or "species=setosa"
        if (typeof name === 'string' && name.includes('=')) {
            const parts = name.split('=').map(s => s.trim());
            if (parts.length === 2 && parts[0] === colName) {
                const targetValue = parts[1];
                const matches = Array.from(colValues)
                    .map((val, idx) => (String(val) === targetValue ? idx : -1))
                    .filter(idx => idx !== -1);

                if (matches.length > 0) {
                    return matches;
                }
            }
        }
    }

    // If we couldn't find a direct category match, try using the legendgroup
    const legendgroup = getProp<string>(trace, 'legendgroup');
    if (legendgroup) {
        for (const colName of categoricalColumns) {
            const colValues = columns[colName];
            if (!colValues) continue;

            // Check if legendgroup contains column name
            if (
                typeof legendgroup === 'string' &&
                legendgroup.includes(colName) &&
                legendgroup.includes(':')
            ) {
                // Extract the value part from formats like "species:setosa"
                const valueMatch = legendgroup.match(new RegExp(`${colName}:([^:]+)`));
                if (valueMatch && valueMatch[1]) {
                    const targetValue = valueMatch[1];

                    const matches = Array.from(colValues)
                        .map((val, idx) => (String(val) === targetValue ? idx : -1))
                        .filter(idx => idx !== -1);

                    if (matches.length > 0) {
                        return matches;
                    }
                }
            }
        }
    }

    return undefined;
}

/**
 * Apply a filter expression to get indices
 * (placeholder for potential future enhancement)
 */
function applyFilterExpression(
    filterExpr: string,
    columns: Record<string, ArrayLike<unknown>>
): number[] | undefined {
    // This is a placeholder for potential future enhancement
    // Implementing a full filter expression parser is complex

    // For now, we'll just handle simple cases with exact matches
    const matches = filterExpr.match(/(\w+)\s*==\s*["']?([^"']+)["']?/);
    if (matches && matches.length === 3) {
        const [_, colName, value] = matches;

        if (columns[colName]) {
            const colValues = columns[colName];
            return Array.from(colValues)
                .map((val, idx) => (String(val) === value ? idx : -1))
                .filter(idx => idx !== -1);
        }
    }

    return undefined;
}

/**
 * Try to infer indices by examining various trace properties
 */
function inferIndicesFromTraceProperties(
    trace: Plotly.Data,
    columns: Record<string, ArrayLike<unknown>>,
    categoricalColumns: string[]
): number[] | undefined {
    // Try to match trace name with categorical columns
    const name = getProp<string | number>(trace, 'name');
    if (name !== undefined) {
        // First check categorical columns directly
        for (const colName of categoricalColumns) {
            const colValues = columns[colName];
            if (!colValues) continue;

            const matches = Array.from(colValues)
                .map((val, idx) => (String(val) === String(name) ? idx : -1))
                .filter(idx => idx !== -1);

            if (matches.length > 0) {
                return matches;
            }
        }

        // Then check if the trace name contains a value in a key-value format
        if (typeof name === 'string' && name.includes('=')) {
            const parts = name.split('=').map(p => p.trim());
            if (parts.length === 2 && columns[parts[0]]) {
                const colValues = columns[parts[0]];
                const matches = Array.from(colValues)
                    .map((val, idx) => (String(val) === parts[1] ? idx : -1))
                    .filter(idx => idx !== -1);

                if (matches.length > 0) {
                    return matches;
                }
            }
        }
    }

    // Try working with marker colors or symbols if they're arrays
    const marker = getProp<any>(trace, 'marker');
    if (marker) {
        if (Array.isArray(marker.color)) {
            // Use non-null as a filter (for traces where missing values are nulls)
            const nonNullIndices = marker.color
                .map((val: any, idx: number) => (val != null ? idx : -1))
                .filter((idx: number) => idx !== -1);

            // Only use this method if it results in a meaningful subset
            if (
                nonNullIndices.length > 0 &&
                nonNullIndices.length < (Object.values(columns)[0]?.length || 0)
            ) {
                return nonNullIndices;
            }
        }

        if (Array.isArray(marker.symbol)) {
            // If symbols are categorical, use the specific symbol for this trace
            const symbolName = marker.symbol[0]; // Use first symbol as representative
            if (symbolName && typeof symbolName === 'string') {
                const nonNullIndices = marker.symbol
                    .map((val: any, idx: number) => (val === symbolName ? idx : -1))
                    .filter((idx: number) => idx !== -1);

                if (nonNullIndices.length > 0) {
                    return nonNullIndices;
                }
            }
        }
    }

    // Try working with line properties for line charts
    const line = getProp<any>(trace, 'line');
    if (line) {
        if (Array.isArray(line.color)) {
            const nonNullIndices = line.color
                .map((val: any, idx: number) => (val != null ? idx : -1))
                .filter((idx: number) => idx !== -1);

            if (
                nonNullIndices.length > 0 &&
                nonNullIndices.length < (Object.values(columns)[0]?.length || 0)
            ) {
                return nonNullIndices;
            }
        }

        if (Array.isArray(line.dash)) {
            const dashStyle = line.dash[0];
            if (dashStyle) {
                const matchingIndices = line.dash
                    .map((val: any, idx: number) => (val === dashStyle ? idx : -1))
                    .filter((idx: number) => idx !== -1);

                if (matchingIndices.length > 0) {
                    return matchingIndices;
                }
            }
        }
    }

    // If we have a legendgroup, it might contain filtering information
    const legendgroup = getProp<string>(trace, 'legendgroup');
    if (legendgroup && typeof legendgroup === 'string') {
        // Check for patterns like "columnName:value"
        const lgParts = legendgroup.split(':');
        if (lgParts.length >= 2 && columns[lgParts[0]]) {
            const colValues = columns[lgParts[0]];
            const matches = Array.from(colValues)
                .map((val, idx) => (String(val) === lgParts[1] ? idx : -1))
                .filter(idx => idx !== -1);

            if (matches.length > 0) {
                return matches;
            }
        }
    }

    return undefined;
}

/**
 * Identifies potential categorical columns that might have been used for trace separation
 * by examining trace names and data columns
 */
function findPossibleCategoricalColumns(
    traces: Plotly.Data[],
    columns: Record<string, ArrayLike<unknown>>
): string[] {
    const categoricalColumns: string[] = [];

    // Safely extract trace names using our helper function
    const traceNames: (string | number)[] = [];
    traces.forEach(trace => {
        const name = getProp<string | number>(trace, 'name');
        if (name !== undefined) traceNames.push(name);
    });

    // If we don't have trace names, we can't identify categorical columns
    if (traceNames.length === 0) return [];

    // Check each column to see if it might be categorical
    for (const [colName, colValues] of Object.entries(columns)) {
        if (!colValues || colValues.length === 0) continue;

        // Convert column values to an array
        const values = Array.from(colValues);

        // Skip if all values are numbers (except for numerical categories)
        const allNumbers = values.every(val => typeof val === 'number');
        if (allNumbers) {
            // Check if these could be numerical categories by seeing if trace names match any values
            const matchesAnyTraceName = traceNames.some(name => {
                // For type safety, check using some() instead of includes()
                if (typeof name === 'string') {
                    return values.some(val => val === Number(name));
                } else {
                    return values.some(val => val === name);
                }
            });

            if (!matchesAnyTraceName) continue;
        }

        // Skip columns with too many unique values (>= 50% of total rows)
        // as they're unlikely to be categorical
        const uniqueValues = new Set(values);
        if (uniqueValues.size >= values.length * 0.5 && uniqueValues.size > 10) continue;

        // Check if any trace name is in this column
        const matchesTraceName = traceNames.some(name => values.some(val => val === name));

        // Also check if trace legendgroups match any column values
        const legendGroups: string[] = [];
        traces.forEach(trace => {
            const legendgroup = getProp<string>(trace, 'legendgroup');
            if (legendgroup) legendGroups.push(legendgroup);
        });

        const matchesLegendGroup = legendGroups.some(group =>
            values.some(val => String(val) === group)
        );

        if (matchesTraceName || matchesLegendGroup) {
            categoricalColumns.push(colName);
        } else {
            // If we don't have direct matches, check if this column has few unique values
            // which might indicate it's a categorical variable
            if (
                uniqueValues.size <= 25 &&
                uniqueValues.size > 0 &&
                uniqueValues.size < values.length * 0.25
            ) {
                categoricalColumns.push(colName);
            }
        }
    }

    return categoricalColumns;
}
