import { Spec } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm';
import * as d3TimeFormat from 'https://cdn.jsdelivr.net/npm/d3-time-format@4.1.0/+esm';
import { visitPlot } from '../util/spec';

export const applyTickFormatting = (spec: Spec) => {
    // If the user specifies that they are formatting a timestamp
    // then convert the value to a date format and apply the d3 time format

    visitPlot(spec, (plot: Object) => {
        // if we have a plot, then we need to set the plot defaults
        if ('xTickFormat' in plot) {
            const format = plot.xTickFormat;
            if (typeof format === 'string') {
                processTickFormat(plot, 'xTickFormat');
                processTickFormat(plot, 'yTickFormat');
            }
        }
    });
};

const processTickFormat = (obj: Record<string, any>, formatKey: string): void => {
    // if we have a plot, then we need to set the plot defaults
    if (formatKey in obj) {
        const format = obj[formatKey];
        if (typeof format === 'string') {
            // If this is a d3 time format, then take over and process the values

            // If the format is a date string, cooerce it to a date
            if (isD3TimeFormat(format)) {
                obj[formatKey] = (val: any) => {
                    // Coerce the value to a date
                    if (typeof val === 'number') {
                        const d = new Date(val);
                        return d3TimeFormat.timeFormat(format)(d);
                    } else {
                        return d3TimeFormat.timeFormat(format)(val);
                    }
                };
            }
        }
    }
};

const isD3TimeFormat = (format: string): boolean => {
    // We know this is a format string, so just look to see
    // if there are date specific specifiers in the string
    return /%[aAbBcdefHIjLmMpqQsSuUVwWxXyYzZ%]/.test(format);
};
