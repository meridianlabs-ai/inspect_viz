import svgPathParser from 'https://cdn.jsdelivr.net/npm/svg-path-parser@1.1.0/+esm';
import tippy, { Placement } from 'https://cdn.jsdelivr.net/npm/tippy.js@6.3.7/+esm';
import { isLinkableUrl } from '../util/url';
import { readMarks } from './plot';

const HIDDEN_USER_CHANNEL = '_user_channels';

export const replaceTooltipImpl = (specEl: HTMLElement) => {
    // Check if SVG already exists
    configureSpecSvgTooltips(specEl);

    // Watch the spec element for svgs to be added
    // When they are added, attempt to connect our tooltip
    // handler
    const observer = new MutationObserver(() => {
        configureSpecSvgTooltips(specEl);
    });
    observer.observe(specEl, { childList: true, subtree: true });
};

// Track which SVGs have been setup
// to avoid setting up multiple observers on the same SVG.
const configuredSvgs = new WeakSet<SVGSVGElement>();

const configureSpecSvgTooltips = (specEl: HTMLElement) => {
    const childSvgEls = specEl.querySelectorAll('svg');
    childSvgEls.forEach(svgEl => {
        if (svgEl && !configuredSvgs.has(svgEl)) {
            setupTooltipObserver(svgEl, specEl);
            configuredSvgs.add(svgEl);
            return;
        }
    });
};

let tooltipInstance: any | undefined = undefined;
let tooltipSpecEl: HTMLElement | undefined = undefined;

function initializeTooltip(specEl: HTMLElement) {
    // Initialize tippy for this spec element if not already done.
    if (!tooltipInstance || tooltipSpecEl !== specEl) {
        // Destroy the old tooltip instance if it exists
        if (tooltipInstance) {
            tooltipInstance.destroy();
        }

        // recreate the tooltip instance for the specEl
        tooltipInstance = tippy(specEl, {
            trigger: 'manual',
            theme: 'inspect',
            interactive: true,
            // One instance serves every widget on the page, so mount it on
            // the body: inside specEl (the default for interactive tooltips)
            // it would inherit that widget's transforms, clipping and
            // visibility.
            appendTo: () => document.body,
        });

        // Note which specEl we're tracking
        tooltipSpecEl = specEl;
    }
}

function hideTooltip() {
    try {
        tooltipInstance.hide();
    } catch {
        // Sometimes tippy throws a null ref related to this. No idea why.
    } finally {
        window.removeEventListener('scroll', hideTooltip);
    }
}

function maybeHideTooltip() {
    if (!tooltipInstance.popper.matches(':hover')) {
        hideTooltip();
    }
}

function showTooltip() {
    try {
        tooltipInstance.show();
        window.addEventListener('scroll', hideTooltip, { once: true });
    } catch {
        // Soemtimes tippy throws a null ref related to this. No idea why.
    }
}

const setupTooltipObserver = (svgEl: SVGSVGElement, specEl: HTMLElement) => {
    // Initialize tippy for this spec element if not already done.
    initializeTooltip(specEl);

    // Watch the SVG for childList mutations and inspect the tip element
    // whenever it changes.
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            if (mutation.type === 'childList') {
                const tipElements = svgEl.querySelectorAll('g[aria-label="tip"]');

                // Hide all the tip elements
                for (const tipElement of tipElements) {
                    const tipContainerEl = tipElement as SVGGElement;
                    tipContainerEl.style.display = 'none';
                }

                // Find the tip element that is currently visible
                let tipEl = undefined;
                let tipContainerEl: SVGGElement | undefined = undefined;
                for (const tipElement of tipElements) {
                    const searchElement = tipElement as SVGGElement;

                    // Find the path element within the tip container (the path )
                    const pathEl = searchElement.querySelector('path');
                    const pathElParent = pathEl?.parentElement as SVGGElement | null;
                    if (pathElParent) {
                        tipEl = pathElParent;
                        tipContainerEl = searchElement;
                        break;
                    }
                }

                // If the tip container is empty, the tooltip has been dismissed
                // hide the tooltip
                if (!tipEl || !tipContainerEl) {
                    maybeHideTooltip();
                } else {
                    // Look for channels
                    const userChannels = readUserChannels(svgEl);
                    const userKeys = userChannels ? Object.keys(userChannels) : undefined;

                    // Find the tip container and parse it to determine how the tooltips
                    // are configured and what is being displayed.
                    const parsed = parseSVGTooltip(tipContainerEl, tipEl);

                    const tooltips = distillTooltips(parsed, userKeys);

                    // Convert the SVG point to screen coordinates
                    const svgPoint = svgEl.createSVGPoint();
                    svgPoint.x = parsed.transform?.x || 0;
                    svgPoint.y = parsed.transform?.y || 0;

                    const screenPoint = svgPoint.matrixTransform(svgEl.getScreenCTM()!);

                    // Position the tooltip
                    const centerX = screenPoint.x;
                    const centerY = screenPoint.y;

                    // Configure tippy to display the HTML tooltip
                    tooltipInstance.setProps({
                        placement:
                            parsed.placement !== 'middle' ? parsed.placement || 'top' : 'top',
                        getReferenceClientRect: () => {
                            return {
                                width: 0,
                                height: 0,
                                top: centerY,
                                bottom: centerY,
                                left: centerX,
                                right: centerX,
                                x: centerX,
                                y: centerY,
                                toJSON: () => {},
                            } as DOMRect;
                        },
                        arrow: parsed.placement !== 'middle',
                        offset: parsed.placement === 'middle' ? [0, 0] : undefined,
                        popperOptions:
                            // Special handling for middle placement, which isn't a supported
                            // tippy placement
                            parsed.placement === 'middle'
                                ? {
                                      modifiers: [
                                          {
                                              name: 'preventOverflow',
                                              enabled: false,
                                          },
                                          {
                                              name: 'flip',
                                              enabled: false,
                                          },
                                          {
                                              name: 'customMiddle',
                                              enabled: true,
                                              phase: 'main',
                                              fn: ({ state }: any) => {
                                                  // Center the popover at the reference point
                                                  state.modifiersData.popperOffsets.x =
                                                      centerX - state.rects.popper.width / 2;
                                                  state.modifiersData.popperOffsets.y =
                                                      centerY - state.rects.popper.height / 2;
                                              },
                                          },
                                      ],
                                  }
                                : undefined,
                    });

                    // Create the tooltip content
                    const contentEl = document.createElement('div');
                    contentEl.classList.add('inspect-tip-container');
                    let count = 0;
                    for (const row of tooltips) {
                        // The row
                        const rowEl = document.createElement('div');
                        rowEl.className = 'inspect-tip-row';
                        contentEl.appendChild(rowEl);

                        // The key
                        const keyEl = document.createElement('div');
                        keyEl.className = 'inspect-tip-key';
                        keyEl.append(document.createTextNode(row.key));

                        // The value
                        const valueEl = document.createElement('div');
                        valueEl.className = 'inspect-tip-value';

                        if (row.href) {
                            const linkEl = document.createElement('a');
                            linkEl.href = row.href;
                            linkEl.target = '_blank';
                            linkEl.rel = 'noopener noreferrer';
                            linkEl.className = 'inspect-tip-link';
                            linkEl.textContent = row.value;
                            valueEl.appendChild(linkEl);
                        } else {
                            valueEl.append(document.createTextNode(row.value));
                        }

                        // Add a color, if provided
                        if (row.color) {
                            const colorEl = document.createElement('span');
                            colorEl.className = 'inspect-tip-color';
                            colorEl.style.backgroundColor = row.color;
                            valueEl.append(colorEl);
                        }

                        rowEl.appendChild(keyEl);
                        rowEl.appendChild(valueEl);
                        count++;
                    }

                    // Show the tooltip
                    tooltipInstance.setContent(contentEl);
                    showTooltip();
                }
            }
        });
    });

    observer.observe(svgEl, {
        childList: true,
        subtree: true,
    });
};

interface TooltipRow {
    key: string;
    value: string;
    href?: string;
    color?: string;
}

interface ParsedTooltip {
    transform?: {
        x: number;
        y: number;
    };
    values: Array<TooltipRow>;
    placement?: Placement | 'middle';
}

const parseTransform = (el: HTMLElement | SVGGElement): { x: number; y: number } | undefined => {
    // Parse the transform attribute to capture the position
    // offset (relative to SVG element)
    const transformVal = el.getAttribute('transform');
    if (transformVal) {
        const match = transformVal.match(/translate\(([^)]+)\)/);
        if (match) {
            const [x, y] = match[1].split(',').map(Number);
            return { x, y };
        }
    }
    return undefined;
};

const parseSVGTooltip = (tipContainerEl: SVGElement, tipEl: SVGGElement): ParsedTooltip => {
    const result: ParsedTooltip = { values: [] };

    // Parse the child spans
    const tspanEls = tipEl.querySelectorAll('tspan');
    tspanEls.forEach(tspan => {
        let key = undefined;
        let value = undefined;
        let color = undefined;
        tspan.childNodes.forEach(node => {
            if (node.nodeName === 'tspan') {
                // Nested tspan, either key or color
                const colorAttr = (node as Element).getAttribute('fill');
                if (colorAttr) {
                    color = colorAttr;
                } else {
                    key = node.textContent?.trim();
                }
            } else if (node.nodeName === '#text') {
                // Bare text nodes are a key
                value = node.textContent?.trim();
            }
        });

        if (key !== undefined && value !== undefined) {
            if (isLinkableUrl(value)) {
                result.values.push({ key, value: 'Link', href: value, color });
            } else {
                result.values.push({ key, value, color });
            }
        }
    });

    // Parse the path to determine the arrow direction
    const pathEl = tipEl.querySelector('path');
    if (pathEl) {
        const pathData = pathEl.getAttribute('d');
        if (pathData) {
            result.placement = parseArrowDirection(pathData);
        }

        // Walk the transforms to compute the position
        const transforms = getTransformsBetween(pathEl, tipContainerEl);
        if (transforms.length > 0) {
            result.transform = transforms.reduce(
                (acc, transform) => {
                    acc.x += transform.x;
                    acc.y += transform.y;
                    return acc;
                },
                { x: 0, y: 0 }
            );
        }
    }

    return result;
};

function distillTooltips(parsed: ParsedTooltip, userKeys?: string[]) {
    // There is no user customization, pass through
    if (!userKeys) {
        return parsed.values;
    }

    // There are user values, only show what
    // is explicitly included
    const userValues = parsed.values
        .filter(row => {
            return userKeys.includes(row.key);
        })
        .map(row => row.value);

    const filteredRows = parsed.values.filter(row => {
        // Never show the internal channel
        if (row.key === HIDDEN_USER_CHANNEL) {
            return false;
        }

        // Next show any internal channels
        if (row.key.startsWith('_')) {
            return false;
        }

        // Include all user keys
        if (userKeys.includes(row.key)) {
            return true;
        }

        // Ignore values that have already been displayed as a user labeled values
        if (userValues.includes(row.value)) {
            return false;
        }

        return false;
    });
    return filteredRows;
}

function readUserChannels(svgEl: SVGSVGElement) {
    const plotEl = svgEl.parentElement;
    if (plotEl) {
        const marks = readMarks(plotEl);
        for (const mark of marks) {
            const markChannels = mark.channels || [];
            const markChannelNames = markChannels.map((c: any) => c.channel);
            // This is a mark with a tip
            if (markChannelNames.includes('tip')) {
                // Read the user channels
                const userChannels = markChannels.find(
                    (c: any) => c.channel === HIDDEN_USER_CHANNEL
                );

                const userChannelsValue = userChannels?.value;
                if (userChannelsValue) {
                    const parsedChannels = JSON.parse(userChannelsValue) as Record<string, string>;
                    return parsedChannels;
                }
            }
        }
    }
    return undefined;
}

function getTransformsBetween(
    pathElement: HTMLElement | SVGElement,
    containerElement: HTMLElement | SVGElement
) {
    const transforms = [];
    let current = pathElement.parentElement;

    while (current) {
        const transform = parseTransform(current);
        if (transform) {
            transforms.unshift(transform);
        }
        if (current !== containerElement) {
            current = current.parentElement;
        } else {
            break;
        }
    }

    return transforms;
}

const parseArrowPosition = (a: number, b: number): 'start' | 'center' | 'end' => {
    if (a < b) {
        return 'end';
    } else if (a > b) {
        return 'start';
    } else {
        return 'center';
    }
};

const parseArrowDirection = (pathData: string): Placement | 'middle' => {
    const parsed = svgPathParser.parseSVG(pathData);
    if (parsed.length < 3) {
        return 'top';
    }

    const moveTo = parsed[0];
    if (moveTo.code !== 'M') {
        console.warn('Expected moveto command (M) in path data, found:', moveTo);
        return 'top';
    }

    if (moveTo.x !== 0 && moveTo.y !== 0) {
        return 'middle';
    }

    const lineTo = parsed[1];
    if (lineTo.code !== 'l') {
        console.warn('Expected lineto command (l) in path data, found:', lineTo);
        return 'top';
    }

    const firstEdgeLineTo = parsed[2];
    if (firstEdgeLineTo.code !== 'h' && firstEdgeLineTo.code !== 'v') {
        console.warn(
            'Expected horizontal (h) or vertical (v) line command after move, found:',
            firstEdgeLineTo
        );
        return 'top';
    }

    const lastEdgeLineTo = parsed[parsed.length - 2];
    if (lastEdgeLineTo.code !== 'h' && lastEdgeLineTo.code !== 'v') {
        console.warn(
            'Expected horizontal (h) or vertical (v) line command before close, found:',
            lastEdgeLineTo
        );
        return 'top';
    }

    // first determine the direction of the arrow
    const x = lineTo.x;
    const y = lineTo.y;

    let arrowDirection: 'top' | 'bottom' | 'left' | 'right' = 'top';
    if (x > 0 && y > 0) {
        arrowDirection = 'bottom';
    } else if (x < 0 && y < 0) {
        if (firstEdgeLineTo.code === 'h') {
            arrowDirection = 'bottom';
        } else {
            arrowDirection = 'left';
        }
    } else if (x > 0 && y < 0) {
        if (firstEdgeLineTo.code === 'h') {
            arrowDirection = 'top';
        } else {
            arrowDirection = 'right';
        }
    } else if (x < 0 && y > 0) {
        arrowDirection = 'bottom';
    } else {
        console.warn(
            'Could not determine arrow direction from path data, returning default placement: top'
        );
    }

    // Next determine the placement within the svg (start, center, end)
    let arrowPosition: 'start' | 'center' | 'end' = 'center';
    if (firstEdgeLineTo.code === 'h') {
        arrowPosition = parseArrowPosition(firstEdgeLineTo.x, lastEdgeLineTo.x);
    } else {
        arrowPosition = parseArrowPosition(firstEdgeLineTo.y, lastEdgeLineTo.y);
    }

    // Finalize the placement based on direction and position
    if (arrowPosition === 'center') {
        return arrowDirection as Placement;
    } else {
        return `${arrowDirection}-${arrowPosition}` as Placement;
    }
};
