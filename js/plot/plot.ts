export interface MarkData {
    type: string;
    channels?: [{ channel: string; value: any }];
}

export const readMarks = (plotEl: HTMLElement): MarkData[] => {
    // Read the value from the plot element
    const value = (plotEl as any).value;
    const marks = value ? value.marks || [] : [];
    return marks;
};

export const readOptions = (el: HTMLElement): Record<string, any> => {
    // Read the value from the element
    const value = (el as any).value;
    return value ? value.options || {} : {};
};

export const readPlotEl = (el: HTMLElement): HTMLElement | undefined => {
    // Read the value from the element
    const value = (el as any).value;
    const plot = value?.plot;
    if (plot) {
        return plot.element as HTMLElement;
    }
    return undefined;
};

export const hasValue = (el: HTMLElement, key: string): boolean => {
    const value = (el as any).value;
    return value ? !!value[key] || false : false;
};
