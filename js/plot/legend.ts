import { readOptions } from './plot';

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

export const installLegendHandler = (specEl: HTMLElement) => {
    const legends = specEl.querySelectorAll('div.legend');
    for (const legend of legends) {
        const legendEl = legend as HTMLElement;
        const legendOptions = readOptions(legendEl);

        const anchor = legendOptions['_frame_anchor'] as FrameAnchor | undefined;
        const inset = resolveInset(
            legendOptions['_inset'],
            legendOptions['_inset_x'],
            legendOptions['_inset_y']
        );
        const background = legendOptions['_background'] as string | boolean | undefined;
        const border = legendOptions['_border'] as string | boolean | undefined;

        // Resolve the frame anchor into element styles on the
        // element and its parent
        resolveFrameAnchorStyles(
            { anchor, inset, background, border },
            legendEl,
            legendEl.parentElement!
        );
    }
};

const resolveInset = (
    inset: number | null,
    insetX: number | null,
    insetY: number | null
): [number, number] | undefined => {
    console.log({ inset, insetX, insetY });
    if (inset == null && insetX == null && insetY == null) {
        return undefined;
    }

    if (inset !== null && insetX === null && insetY === null) {
        return [Math.abs(inset), Math.abs(inset)];
    }

    return [Math.abs(insetX || 0), Math.abs(insetY || 0)];
};

const resolveFrameAnchorStyles = (
    options: {
        anchor?: FrameAnchor;
        inset?: [number, number];
        background?: string | boolean;
        border?: string | boolean;
    },
    legendEl: HTMLElement,
    parentEl: HTMLElement
): void => {
    if (options.anchor) {
        const anchor = options.anchor;
        parentEl.style.position = 'relative';

        // Resolve the background color
        if (options.background !== false) {
            legendEl.style.background =
                options.background === true ? 'white' : options.background || 'white';
        }

        // Resolve the border style
        if (options.border !== false) {
            const borderColor = options.border === true ? '#DDDDDD' : options.border || '#DDDDDD';
            legendEl.style.border = `1px solid ${borderColor}`;
        }

        legendEl.style.padding = '0.3em';
        legendEl.style.position = 'absolute';

        if (anchor === 'left' || anchor === 'top-left' || anchor === 'bottom-left') {
            legendEl.style.left = '0';
            if (anchor === 'left' && options.inset === undefined) {
                parentEl.style.paddingLeft = '100px';
            }
        }
        if (anchor === 'right' || anchor === 'top-right' || anchor === 'bottom-right') {
            legendEl.style.right = '0';
            if (anchor === 'right' && options.inset === undefined) {
                parentEl.style.paddingRight = '100px';
            }
        }

        if (anchor === 'top' || anchor === 'top-left' || anchor === 'top-right') {
            legendEl.style.top = '0';
            if (anchor === 'top' && options.inset === undefined) {
                legendEl.style.left = '50%';
                legendEl.style.transform = 'translateX(-50%)';
            }
            if (options.inset === undefined) {
                parentEl.style.paddingTop = '100px';
            }
        }
        if (anchor === 'bottom' || anchor === 'bottom-left' || anchor === 'bottom-right') {
            legendEl.style.bottom = '0';
            if (anchor === 'bottom' && options.inset === undefined) {
                legendEl.style.left = '50%';
                legendEl.style.transform = 'translateX(-50%)';
            }

            if (options.inset === undefined) {
                parentEl.style.paddingBottom = '100px';
            }
        }
    }

    if (options.inset) {
        const inset = options.inset;
        legendEl.style.margin = `${inset[1]}px ${inset[0]}px`;
    }
};
