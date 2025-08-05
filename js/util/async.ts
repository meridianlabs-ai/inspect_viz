export function sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Creates a throttled version of a function that only invokes the original function
 * at most once per every `wait` milliseconds. The throttled function will run as much
 * as it can, without ever going more than once per `wait` duration.
 */
export function throttle<T extends (...args: any[]) => any>(
    func: T,
    wait: number,
    options: { leading?: boolean; trailing?: boolean } = {}
): (...args: Parameters<T>) => ReturnType<T> {
    let context: any;
    let args: Parameters<T> | null;
    let result: ReturnType<T>;
    let timeout: ReturnType<typeof setTimeout> | null = null;
    let previous = 0;

    const later = function (): void {
        previous = options.leading === false ? 0 : Date.now();
        timeout = null;
        result = func.apply(context, args === null ? [] : args);
        if (!timeout) {
            context = null;
            args = null;
        }
    };

    return function (this: any, ...callArgs: Parameters<T>): ReturnType<T> {
        const now = Date.now();
        if (!previous && options.leading === false) {
            previous = now;
        }
        const remaining = wait - (now - previous);

        context = this;
        args = callArgs as unknown as Parameters<T>;

        if (remaining <= 0 || remaining > wait) {
            if (timeout) {
                clearTimeout(timeout);
                timeout = null;
            }
            previous = now;
            result = func.apply(context, args);
            if (!timeout) {
                context = null;
                args = null;
            }
        } else if (!timeout && options.trailing !== false) {
            timeout = setTimeout(later, remaining);
        }

        return result;
    };
}
