import { throttle } from '../util/async';
import { readOptions, readPlotEl } from './plot';

interface LegendOptions {
    inset: number | null;
    insetX: number | null;
    insetY: number | null;
    frameAnchor: FrameAnchor | null;
    background: string | boolean | null;
    border: string | boolean | null;
}

type FrameAnchor =
    | 'middle'
    | 'top-left'
    | 'top'
    | 'top-right'
    | 'right'
    | 'bottom-right'
    | 'bottom'
    | 'bottom-left'
    | 'left';

// TODO: If the the legend is interactive, update the mouse cursor to pointed on hover
// TODO: Position multiple legends appropriately

export const installLegendHandler = (specEl: HTMLElement) => {
    const legends = specEl.querySelectorAll('div.legend');
    for (const legend of Array.from(legends)) {
        // Find the element
        const legendEl = legend as HTMLElement;

        // read the legend options
        const options = readLegendOptions(legendEl);

        // Resolve the frame anchor into element styles on the
        // element and its parent
        applyLegendStyles(options, legendEl, legendEl.parentElement!);
    }
};

const applyLegendStyles = (
    options: LegendOptions,
    legendEl: HTMLElement,
    parentEl: HTMLElement
): void => {
    if (!options.frameAnchor) return;

    // Global configuration
    parentEl.style.position = 'relative';
    legendEl.style.padding = '0.3em';
    legendEl.style.position = 'absolute';

    // Background and border
    applyBackground(legendEl, options.background);
    applyBorder(legendEl, options.border);

    // Scale the legand as the plot changes size
    const plotEl = readPlotEl(legendEl);
    responsiveScaleLegend(options, legendEl, plotEl);

    // Compute the size of the legend and apply padding
    applyParentPadding(options, legendEl, parentEl);
};

const applyBackground = (legendEl: HTMLElement, background: string | boolean | null): void => {
    if (background !== false) {
        legendEl.style.background = background === true ? 'white' : background || 'white';
    }
};

const applyBorder = (legendEl: HTMLElement, border: string | boolean | null): void => {
    if (border !== false) {
        const borderColor = border === true ? '#DDDDDD' : border || '#DDDDDD';
        legendEl.style.border = `1px solid ${borderColor}`;
    }
};

const applyParentPadding = (
    options: LegendOptions,
    legendEl: HTMLElement,
    parentEl: HTMLElement
): void => {
    if (!isInset(options)) {
        // Watch for size changes
        const observer = new MutationObserver(() => {
            if (options.frameAnchor) {
                const newSize = legendEl.getBoundingClientRect();
                const parentConfig = kParentConfig[options.frameAnchor];
                const useHeight =
                    parentConfig.paddingType === 'paddingTop' ||
                    parentConfig.paddingType === 'paddingBottom';

                (parentEl.style as any)[parentConfig.paddingType] = useHeight
                    ? newSize.height + 'px'
                    : newSize.width + 'px';
            }
        });

        observer.observe(legendEl, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['style', 'class'],
        });
    }
};

const responsiveScaleLegend = (
    options: LegendOptions,
    legendEl: HTMLElement,
    plotEl?: HTMLElement
): void => {
    // Apply the anchor styles
    const anchor = options.frameAnchor || 'right';
    const config = kAnchorConfig[anchor];
    Object.assign(legendEl.style, config.position);
    if (config.centerTransform) {
        legendEl.style.transform = 'translateX(-50%)';
    }

    // Monitor the plot and responsive scale the size and position
    // of the legend
    if (plotEl && plotEl.parentElement) {
        // Throttle + only apply changes when scale factor changes
        let lastScaleFactor: number | null = null;

        const resizeObserver = new ResizeObserver(
            throttle(entries => {
                for (let entry of entries) {
                    if (!plotEl.children || plotEl.childElementCount === 0) {
                        return;
                    }

                    // The observed parent element
                    const parentEl = entry.target as HTMLElement;

                    // Find the x and y grid elements (we'll position the legend relative to these)
                    const yGridEl = plotEl.querySelector('g[aria-label="y-grid"]');
                    const xGridEl = plotEl.querySelector('g[aria-label="x-grid"]');
                    if (!yGridEl || !xGridEl) {
                        console.warn('Missing y-grid or x-grid elements in the plot.');
                        return;
                    }

                    // This assumes that the first child of the plot element is the SVG element
                    // itself. Verify this:
                    const svgEl = plotEl.children[0] as HTMLElement;
                    if (svgEl.tagName !== 'svg') {
                        console.warn('The first child of the plot element is not an SVG element.');
                        return;
                    }

                    // Read the width
                    const baseWidth = svgEl.getAttribute('width');
                    if (!baseWidth) {
                        console.warn('Plot element does not have a width attribute.');
                        return;
                    }

                    // Compute the scale factor based the based with vs the actual width
                    const parentRect = parentEl.getBoundingClientRect();
                    const actualWidth = parentRect.width;
                    const scaleFactor = actualWidth / parseFloat(baseWidth);

                    // Don't bother resizing if the scale factor hasn't changed much
                    if (
                        lastScaleFactor !== null &&
                        Math.abs(scaleFactor - lastScaleFactor) < 0.001
                    ) {
                        return;
                    }
                    lastScaleFactor = scaleFactor;

                    requestAnimationFrame(() => {
                        // Accumulate any styles
                        const styles: Partial<CSSStyleDeclaration> = {};

                        // Set the transform origin to maintain a stable position
                        if (config.transformOrigin) {
                            styles.transformOrigin = config.transformOrigin;
                        }
                        if (config.centerTransform) {
                            styles.transform = `translateX(-50%) scale(${scaleFactor})`;
                        } else {
                            styles.transform = `scale(${scaleFactor})`;
                        }

                        const inset = resolveInset(options);
                        if (inset) {
                            // Look through the plot to find rect of the plot
                            // which excludes the axes, etc..
                            const plotRect = findPlotRegionRect(plotEl);
                            console.log({ plotRect, parentRect });

                            // Compute the inset based upon the y-grid and x-grid positions
                            const yShift = config.transformOrigin?.startsWith('bottom')
                                ? parentRect.bottom - plotRect.bottom
                                : plotRect.top - parentRect.top;
                            const xShift = config.transformOrigin?.endsWith('right')
                                ? parentRect.right - plotRect.right
                                : plotRect.left - parentRect.left;

                            console.log({ xShift, yShift, inset });

                            // substract the distance from the parent plot to the y-grid, if possible
                            const yInset = inset[1] * scaleFactor + yShift;
                            const xInset = inset[0] * scaleFactor + xShift;
                            if (config.centerTransform) {
                                styles.margin = `${yInset}px 0px`;
                            } else {
                                styles.margin = `${yInset}px ${xInset}px`;
                            }
                        }

                        Object.assign(legendEl.style, styles);
                    });
                }
            }, 16)
        );

        resizeObserver.observe(plotEl.parentElement);
    }
};

const isInset = (options: LegendOptions): boolean => {
    return options.inset !== null || options.insetX !== null || options.insetY !== null;
};

const resolveInset = (options: LegendOptions): [number, number] | undefined => {
    if (options.inset == null && options.insetX == null && options.insetY == null) {
        return undefined;
    }

    if (options.inset !== null && options.insetX === null && options.insetY === null) {
        return [Math.abs(options.inset), Math.abs(options.inset)];
    }

    return [Math.abs(options.insetX || 0), Math.abs(options.insetY || 0)];
};

const readLegendOptions = (legendEl: HTMLElement): LegendOptions => {
    const options = readOptions(legendEl);
    return {
        inset: options['_inset'] as number | null,
        insetX: options['_inset_x'] as number | null,
        insetY: options['_inset_y'] as number | null,
        frameAnchor: options['_frame_anchor'] as FrameAnchor | null,
        background: options['_background'] as string | boolean | null,
        border: options['_border'] as string | boolean | null,
    };
};

const kParentConfig: Record<FrameAnchor, { paddingType: string }> = {
    'top-left': { paddingType: 'paddingLeft' },
    top: { paddingType: 'paddingTop' },
    'top-right': { paddingType: 'paddingRight' },
    right: { paddingType: 'paddingRight' },
    'bottom-right': { paddingType: 'paddingRight' },
    bottom: { paddingType: 'paddingBottom' },
    'bottom-left': { paddingType: 'paddingLeft' },
    left: { paddingType: 'paddingLeft' },
    middle: { paddingType: '' },
};

const kAnchorConfig: Record<
    FrameAnchor,
    {
        position: { [key: string]: string };
        parentPadding?: string;
        centerTransform?: boolean;
        transformOrigin?: string;
    }
> = {
    'top-left': { position: { top: '0', left: '0' }, transformOrigin: 'top left' },
    top: {
        position: { top: '0', left: '50%' },
        centerTransform: true,
        transformOrigin: 'top center',
    },
    'top-right': { position: { top: '0', right: '0' }, transformOrigin: 'top right' },
    right: {
        position: { right: '0', transformOrigin: 'center right' },
    },
    'bottom-right': { position: { bottom: '0', right: '0' }, transformOrigin: 'bottom right' },
    bottom: {
        position: { bottom: '0', left: '50%' },
        centerTransform: true,
        transformOrigin: 'bottom center',
    },
    'bottom-left': { position: { bottom: '0', left: '0' }, transformOrigin: 'bottom left' },
    left: {
        position: { left: '0' },
        transformOrigin: 'center left',
    },
    middle: { position: {} },
};

// Roots around in the plot to guess the internal dimensions based upon
// the bounding rectangle of the plot element and the position of elements
// within it.
const findPlotRegionRect = (plotEl: HTMLElement): DOMRect => {
    const plotRect = plotEl.getBoundingClientRect();

    const yLabel = plotEl.querySelector('g[aria-label="y-axis label"]');
    const top = yLabel ? yLabel.getBoundingClientRect().bottom : plotRect.top;

    const yTicks = plotEl.querySelector('g[aria-label="y-axis tick"]');
    const left = yTicks ? yTicks.getBoundingClientRect().right : plotRect.left;

    const right = plotRect.right;

    let bottom = plotRect.bottom;
    const xTicks = plotEl.querySelector('g[aria-label="x-axis tick"]');
    if (xTicks) {
        const xRect = xTicks.getBoundingClientRect();
        bottom = xRect.top;
    } else {
        const xLabel = plotEl.querySelector('g[aria-label="x-axis label"]');
        if (xLabel) {
            bottom = xLabel.getBoundingClientRect().top;
        }
    }
    return new DOMRect(left, top, right - left, bottom - top);
};
