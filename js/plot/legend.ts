import { Spec } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm';
import { hasValue, readOptions, readPlotEl } from './plot';
import { throttle } from '../util/async';

interface LegendOptions {
    inset: number | null;
    insetX: number | null;
    insetY: number | null;
    frameAnchor: FrameAnchor | null;
    background: string | boolean | null;
    border: string | boolean | null;
}

interface ResolvedLegendOptions {
    inset: [number, number] | undefined;
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

const kInsetX = '_inset_x';
const kInsetY = '_inset_y';
const kInset = '_inset';
const kFrameAnchor = '_frame_anchor';
const kBackground = '_background';
const kBorder = '_border';

export const installLegendHandler = (specEl: HTMLElement, responsive: boolean) => {
    // If the spec element has already been configured, dispose of it
    const existingObserver = observedSpecs.get(specEl);
    if (existingObserver) {
        existingObserver.disconnect();
        observedSpecs.delete(specEl);
    }

    // Check if the spec element has a legend
    const hasLegend = specEl.querySelector('div.legend') !== null;
    if (!hasLegend) {
        // No legend found, so we don't need to do anything
        return;
    }

    // Configure the legend handler for this spec element
    configureLegendHandler(specEl, responsive);

    // Watch the spec element for svgs to be added
    // When they are added, attempt to connect our tooltip
    // handler
    const observer = new MutationObserver(() => {
        configureLegendHandler(specEl, responsive);
    });
    observer.observe(specEl, { childList: true, subtree: true });
    observedSpecs.set(specEl, observer);
};
const observedSpecs = new WeakMap<HTMLElement, MutationObserver>();

export function legendPaddingRegion(spec: Spec): {
    top: boolean;
    bottom: boolean;
    left: boolean;
    right: boolean;
} {
    // The regions that need padding
    const result = { top: false, bottom: false, left: false, right: false };

    // Find legends and see what the deal is with inset and frame anchor
    function visitLegends(obj: any): void {
        if (!obj || typeof obj !== 'object') return;

        // Check if this object has a "legend" key
        if ('legend' in obj) {
            const legendObj = obj;

            // Check if it has inset properties
            const hasInset = kInset in legendObj || kInsetX in legendObj || kInsetY in legendObj;

            if (!hasInset && kFrameAnchor in legendObj) {
                const frameAnchor = legendObj[kFrameAnchor] as string;

                // Map frame anchor to inset requirements
                switch (frameAnchor) {
                    case 'top':
                    case 'top-left':
                    case 'top-right':
                        result.top = true;
                        break;
                    case 'bottom':
                    case 'bottom-left':
                    case 'bottom-right':
                        result.bottom = true;
                        break;
                    case 'left':
                        result.left = true;
                        break;
                    case 'right':
                        result.right = true;
                        break;
                }
            }
        }

        // Recursively search through all object properties
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                visitLegends(obj[key]);
            }
        }

        // Handle arrays
        if (Array.isArray(obj)) {
            obj.forEach(item => visitLegends(item));
        }
    }

    visitLegends(spec);
    return result;
}

// Track which legends have been setup
// to avoid setting up multiple observers on the same SVG.
const configuredLegends = new WeakSet<Element>();
const specHandlers = new WeakMap<HTMLElement, ResizeObserver>();

const configureLegendHandler = (specEl: HTMLElement, responsive: boolean) => {
    // Find all the legend elements in the spec element
    const newLegends = Array.from(specEl.querySelectorAll('div.legend')).filter(
        legend => !configuredLegends.has(legend)
    );

    if (newLegends.every(legend => legend.childElementCount === 0)) {
        // Do nothing, these are just empty legends
        return;
    }

    const frameLegends: Record<string, HTMLElement[]> = groupLegendsByPosition(newLegends);

    // Dispose of any existing observer for this spec element
    const existingObserver = specHandlers.get(specEl);
    if (existingObserver) {
        existingObserver.disconnect();
        specHandlers.delete(specEl);
    }

    // Process each legend, applying styles
    const processLegends = throttle(() => {
        const legends = specEl.querySelectorAll('div.legend');
        legends.forEach(legend => {
            const legendEl = legend as HTMLElement;
            applyLegendStyles(legendEl);
        });
    }, 25);

    if (newLegends.length > 0) {
        // Move legends into their containers
        emplaceLegendContainers(frameLegends, specEl);

        // Note that this legend has been processed
        newLegends.forEach(legend => configuredLegends.add(legend));
    }
    // Process the legends immediately
    processLegends();

    // Watch the spec element and apply legend styles when the spec is resized
    if (responsive) {
        const observer = new ResizeObserver(() => {
            processLegends();
        });
        observer.observe(specEl);
        specHandlers.set(specEl, observer);
    }
};

const applyLegendStyles = (legendEl: HTMLElement): void => {
    // Read the legend options
    const options = readLegendOptions(legendEl);
    if (!options.frameAnchor) {
        return;
    }

    // Legend container parents
    const legendContainerEl = legendEl.parentElement as HTMLElement;
    const legendContainerParentEl = legendContainerEl.parentElement as HTMLElement;

    // Global configuration
    legendContainerParentEl.style.position = 'relative';
    legendContainerEl.style.padding = '0.3em';
    legendContainerEl.style.position = 'absolute';
    legendContainerEl.style.width = 'max-content';

    // Background and border
    applyBackground(legendContainerEl, options.background);
    applyBorder(legendContainerEl, options.border);

    // Compute the size of the legend and apply padding
    applyParentPadding(options, legendContainerEl, legendContainerParentEl);

    // Scale the legend as the plot changes size
    responsiveScaleLegend(options, legendEl, legendContainerEl);

    // Apply cursor styles if interactive
    applyCursorStyle(legendEl);
};

const applyBackground = (targetEl: HTMLElement, background: string | boolean | null): void => {
    if (background !== false) {
        targetEl.style.background = background === true ? 'white' : background || 'white';
    }
};

const applyBorder = (targetEl: HTMLElement, border: string | boolean | null): void => {
    if (border !== false) {
        const borderColor = border === true ? '#DDDDDD' : border || '#DDDDDD';
        targetEl.style.border = `1px solid ${borderColor}`;
    }
};

// Watch the legend and apply a cursor style if it has a selection
const applyCursorStyle = (legendEl: HTMLElement): void => {
    // If the legend already has a cursor observer, remove it
    const existingObserver = cursorObserver.get(legendEl);
    if (existingObserver) {
        existingObserver.disconnect();
        cursorObserver.delete(legendEl);
    }

    const applyPointer = () => {
        if (hasValue(legendEl, 'selection')) {
            const subContainerEl = legendEl.firstElementChild;
            (subContainerEl as HTMLElement).style.cursor = 'pointer';
        }
    };

    const observer = new MutationObserver(() => {
        applyPointer();
    });
    observer.observe(legendEl, { childList: true, subtree: true });
    applyPointer();

    cursorObserver.set(legendEl, observer);
};
const cursorObserver = new WeakMap<HTMLElement, MutationObserver>();

const applyParentPadding = (
    options: ResolvedLegendOptions,
    legendEl: HTMLElement,
    parentEl: HTMLElement
): void => {
    if (!options.inset) {
        // Watch for size changes
        const observer = new MutationObserver(() => {
            if (options.frameAnchor) {
                const newSize = legendEl.getBoundingClientRect();
                const parentConfig = kParentAnchorConfig[options.frameAnchor];
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
    options: ResolvedLegendOptions,
    legendEl: HTMLElement,
    legendContainerEl: HTMLElement
): void => {
    // Apply the anchor styles
    const anchor = options.frameAnchor || 'right';
    const config = kLegendAnchorConfig[anchor];
    Object.assign(legendContainerEl.style, config.position);
    if (config.centerTransform) {
        legendContainerEl.style.transform = 'translateX(-50%)';
    }

    // Find the plot element which owns the legend
    const plotEl = readPlotEl(legendEl);
    if (!plotEl || !plotEl.children || plotEl.childElementCount === 0) {
        return;
    }

    // The observed parent element
    const parentEl = plotEl.parentElement;
    if (!parentEl) {
        console.warn('No parent element found for the plot.');
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

    if (options.inset) {
        // Look through the plot to find rect of the plot
        // which excludes the axes, etc..
        const plotRect = findPlotRegionRect(plotEl);

        // Compute the inset based upon the y-grid and x-grid positions
        const yShift = config.transformOrigin?.startsWith('bottom')
            ? parentRect.bottom - plotRect.bottom
            : plotRect.top - parentRect.top;
        const xShift = config.transformOrigin?.endsWith('right')
            ? parentRect.right - plotRect.right
            : plotRect.left - parentRect.left;

        // substract the distance from the parent plot to the y-grid, if possible
        const yInset = options.inset[1] * scaleFactor + yShift;
        const xInset = options.inset[0] * scaleFactor + xShift;
        if (config.centerTransform) {
            styles.margin = `${yInset}px 0px`;
        } else {
            styles.margin = `${yInset}px ${xInset}px`;
        }
    }

    Object.assign(legendContainerEl.style, styles);
};

// Resolves the inset options into a tuple of [insetX, insetY] or undefined if no inset is specified.
const resolveOptions = (options: LegendOptions): ResolvedLegendOptions => {
    if (options.inset == null && options.insetX == null && options.insetY == null) {
        return {
            inset: undefined,
            frameAnchor: options.frameAnchor,
            background: options.background,
            border: options.border,
        };
    }

    let inset: [number, number] | undefined = undefined;
    if (options.inset !== null && options.insetX === null && options.insetY === null) {
        inset = [Math.abs(options.inset), Math.abs(options.inset)];
    } else if (options.insetX !== null || options.insetY !== null) {
        inset = [Math.abs(options.insetX || 0), Math.abs(options.insetY || 0)];
    }

    return {
        inset: inset,
        frameAnchor: options.frameAnchor,
        background: options.background,
        border: options.border,
    };
};

// Reads the legend options from the legend element's attributes.
const readLegendOptions = (legendEl: HTMLElement): ResolvedLegendOptions => {
    const optionsRaw = readOptions(legendEl);
    const options: LegendOptions = {
        inset: optionsRaw[kInset] as number | null,
        insetX: optionsRaw[kInsetX] as number | null,
        insetY: optionsRaw[kInsetY] as number | null,
        frameAnchor: optionsRaw[kFrameAnchor] as FrameAnchor | null,
        background: optionsRaw[kBackground] as string | boolean | null,
        border: optionsRaw[kBorder] as string | boolean | null,
    };
    return resolveOptions(options);
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

// The style information for the parent element based on the anchor position.
const kParentAnchorConfig: Record<FrameAnchor, { paddingType: string }> = {
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

// The style information for the legend element based on the anchor position.
const kLegendAnchorConfig: Record<
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

function emplaceLegendContainers(frameLegends: Record<string, HTMLElement[]>, specEl: HTMLElement) {
    for (const [positionKey, legendEls] of Object.entries(frameLegends)) {
        for (const legendEl of legendEls) {
            // Ensure there is a frame container for the legend container
            let containerEl: HTMLElement | null = specEl.querySelector(
                `div.legend-container.${positionKey}`
            ) as HTMLElement | null;
            if (containerEl === null) {
                // Create a new container element
                containerEl = document.createElement('div');
                containerEl.className = `legend-container ${positionKey}`;
                legendEl.parentElement!.insertBefore(containerEl, legendEl);
            }

            // Move the legend element into the container
            containerEl.appendChild(legendEl);
        }
    }
}

function groupLegendsByPosition(legends: Element[]): Record<string, HTMLElement[]> {
    const frameLegends: Record<string, HTMLElement[]> = {};
    for (const legend of Array.from(legends)) {
        // Find the element
        const legendEl = legend as HTMLElement;

        // read the legend options
        const options = readLegendOptions(legendEl);

        // Create a legend key (which encodes the anchor and inset to group
        // legends into buckets which share the same container position)
        const legendKey = `${options.frameAnchor}-${options.inset?.[0] || 0}-${options.inset?.[1] || 0}`;
        frameLegends[legendKey] = frameLegends[legendKey] || [];
        frameLegends[legendKey]!.push(legendEl);
    }
    return frameLegends;
}
