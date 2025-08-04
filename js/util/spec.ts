// Function that visits each plto in the spec and applies the provided function
export function visitPlot(obj: Object, fn: (plot: Object) => void): void {
    if (Array.isArray(obj)) {
        obj.flatMap(item => visitPlot(item, fn));
    } else if (typeof obj === 'object' && obj !== null) {
        if ('plot' in obj) {
            fn(obj);
        } else {
            Object.values(obj).flatMap(value => visitPlot(value, fn));
        }
    }
}
