import type { RenderProps } from '@anywidget/types';

import {
    Spec,
    SpecNode,
    parseSpec,
    InstantiateContext,
    ASTNode,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm';

import { throttle } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

import { VizContext, vizContext } from '../context';
import { INPUTS } from '../inputs';
import { errorInfo, errorAsHTML, displayRenderError } from '../util/errors';
import { isNotebook } from '../util/platform';
import { TableOptions } from '../inputs/table';
import { replaceTooltipImpl as installPlotTooltips } from '../plot/tooltips';
import { installTextCollisionHandler } from '../plot/text-collision';
import { applyTickFormatting } from '../plot/ticks';
import { installLegendHandler, legendPaddingRegion } from '../plot/legend';

interface MosaicProps {
    // Each value is either a DataView (inline binary-buffer transport) or a
    // URL string pointing to a pre-written immutable `.arrow` asset.
    tables: Record<string, DataView | string>;
    spec: string;
}

async function render({ model, el }: RenderProps<MosaicProps>) {
    // get the spec and parse it for plot defaults
    const spec: Spec = JSON.parse(model.get('spec'));
    const plotDefaultsSpec = { plotDefaults: spec.plotDefaults, vspace: 0 } as Spec;
    const plotDefaultsAst = parseSpec(plotDefaultsSpec);

    // initialize context
    const ctx = await vizContext(plotDefaultsAst.plotDefaults);

    // handle tick formatting
    applyTickFormatting(spec);

    // insert/wait for tables to be ready
    const tables: Record<string, DataView | string> =
        model.get('tables') || {};
    try {
        await syncTables(ctx, tables);
    } catch (e: unknown) {
        console.error(e);
        el.innerHTML = errorAsHTML(errorInfo(e));
        return;
    }

    // render mosaic spec
    el.classList.add('mosaic-widget');
    const renderOptions = renderSetup(el);
    const inputs = new Set(Object.keys(INPUTS));
    if (renderOptions.autoFillScrolling && isPlotSpec(spec)) {
        el.style.width = '100%';
        el.style.height = '400px';
    }
    if (renderOptions.autoFill && isTableSpec(spec)) {
        // if we are auto-filling a table spec, then remove any padding from the card body
        // as the table will fill the entire space (this is basically in a quarto dashboard card)
        const card = el.closest('.card-body') as HTMLElement | null;
        if (card) {
            card.style.padding = '0';
        }
    }
    const renderSpec = async () => {
        try {
            ctx.clearUnhandledErrors();
            const targetSpec = renderOptions.autoFill ? responsiveSpec(spec, el) : spec;
            const ast = parseSpec(targetSpec, { inputs });
            const specEl = (await astToDOM(ast, ctx)) as HTMLElement;
            el.innerHTML = '';
            el.appendChild(specEl);

            // For plots, replace the tooltip implementation with
            // our own implementation
            installPlotTooltips(specEl);

            // For plots, install the text collision handler which
            // will adjust text labels to avoid collisions
            installTextCollisionHandler(specEl);

            // install legend handlers
            installLegendHandler(specEl, !renderOptions.autoFill);

            await displayUnhandledErrors(ctx, el);
        } catch (e: unknown) {
            console.error(e);
            const error = errorInfo(e);
            el.innerHTML = errorAsHTML(error);
        }
    };
    await renderSpec();

    // if we are doing auto-fill then re-render when size changes
    if (renderOptions.autoFill && !isInputSpec(spec)) {
        let lastContainerWidth = el.clientWidth;
        let lastContainerHeight = el.clientHeight;

        // re-render on container size changed
        const resizeObserver = new ResizeObserver(
            throttle(async () => {
                if (
                    lastContainerWidth !== el.clientWidth ||
                    lastContainerHeight !== el.clientHeight
                ) {
                    lastContainerWidth = el.clientWidth;
                    lastContainerHeight = el.clientHeight;
                    renderSpec();
                }
            })
        );
        resizeObserver.observe(el);

        // cleanup resize observer on disconnect
        return () => {
            resizeObserver.disconnect();
        };
    }
}

// Named Cache API store for immutable `.arrow` assets. URLs are
// content-addressed so cache entries never go stale; persists across reloads
// within the origin. Browsers may evict under storage pressure — a miss just
// re-fetches, so it is safe.
const SITE_DATA_CACHE = 'site_data/v1';

async function fetchCachedBytes(url: string): Promise<Uint8Array> {
    // `caches` is unavailable in a few older/embedded contexts — fall back
    // cleanly to a normal fetch in that case.
    const supportsCache = typeof caches !== 'undefined';
    let resp: Response | undefined;
    let cache: Cache | undefined;
    if (supportsCache) {
        try {
            cache = await caches.open(SITE_DATA_CACHE);
            resp = await cache.match(url);
        } catch {
            // ignore — fall through to network fetch
        }
    }
    if (!resp) {
        resp = await fetch(url, { cache: 'force-cache' });
        if (!resp.ok) {
            throw new Error(`fetch ${url}: ${resp.status} ${resp.statusText}`);
        }
        if (cache) {
            try {
                await cache.put(url, resp.clone());
            } catch {
                // storage full, cross-origin, etc. — not fatal
            }
        }
    }
    return new Uint8Array(await resp.arrayBuffer());
}

// insert/wait for tables to be ready; fetches for one widget run in parallel
async function syncTables(
    ctx: VizContext,
    tables: Record<string, DataView | string>
) {
    await Promise.all(
        Object.entries(tables).map(async ([tableName, val]) => {
            if (typeof val === 'string') {
                if (val.length === 0) {
                    // sibling widget is shipping the data; wait for it
                    await ctx.waitForTable(tableName);
                    return;
                }
                const bytes = await fetchCachedBytes(val);
                await ctx.insertTable(tableName, bytes);
            } else if (val && val.byteLength > 0) {
                // inline binary-buffer path: wrap DataView as a Uint8Array (no copy)
                const bytes = new Uint8Array(
                    val.buffer,
                    val.byteOffset,
                    val.byteLength
                );
                await ctx.insertTable(tableName, bytes);
            } else {
                // empty buffer → another widget is shipping the data
                await ctx.waitForTable(tableName);
            }
        })
    );
}

interface RenderOptions {
    autoFill: boolean;
    autoFillScrolling: boolean;
}

function renderSetup(containerEl: HTMLElement): RenderOptions {
    // mosaic widgets already have sufficient margin/padding so override
    // any host prescribed bottom margin.
    const widgetEl = containerEl.closest('.widget-subarea') as HTMLElement | undefined;
    if (widgetEl) {
        widgetEl.style.marginBottom = '0';
    }

    // detect whether we should be auto-filling our container
    const autoFill = window.document.body.classList.contains('quarto-dashboard');

    // detect whether we are in a scrolling layout w/ auto-fill (so we need to provide element heights)
    const autoFillScrolling =
        autoFill && !window.document.body.classList.contains('dashboard-fill');

    return { autoFill, autoFillScrolling };
}

// TODO: Why is the stupid null error

// if this is a single plot (w/ optional legend) in an hconcat or vconcat,
// then give it dynamic sizing (more complex layouts don't get auto-sized)
function responsiveSpec(spec: Spec, containerEl: HTMLElement): Spec {
    const kLegendWidth = 80; // best guess estimate
    const kLegendHeight = 35; // best guess estimate

    const paddingRegion = legendPaddingRegion(spec);
    const horizontalPadding = paddingRegion.left || paddingRegion.right ? kLegendWidth : 0;
    const verticalPadding = paddingRegion.top || paddingRegion.bottom ? kLegendHeight : 0;

    spec = structuredClone(spec);
    if ('input' in spec && spec.input === 'table') {
        const table = spec;
        // disable max-width for table inputs
        (table as unknown as TableOptions).auto_filling = true;
    } else if ('hconcat' in spec && spec.hconcat.length == 1) {
        // standalone plot
        const hconcat = spec.hconcat;
        const plot = 'plot' in hconcat[0] ? hconcat[0] : null;
        if (plot) {
            plot.width = containerEl.clientWidth - (hconcat.length > 1 ? horizontalPadding : 0);
            plot.height = containerEl.clientHeight;
        }
    } else if ('hconcat' in spec && spec.hconcat.length == 2) {
        // plot with horizontal legend
        const hconcat = spec.hconcat;
        const plot =
            'plot' in hconcat[0] && 'legend' in hconcat[1]
                ? hconcat[0]
                : 'plot' in hconcat[1] && 'legend' in hconcat[0]
                  ? hconcat[1]
                  : undefined;
        if (plot) {
            plot.width =
                containerEl.clientWidth - (spec.hconcat.length > 1 ? horizontalPadding : 0);
            plot.height = containerEl.clientHeight;
        }
    } else if ('vconcat' in spec && spec.vconcat.length == 2) {
        // plot with vertical legend
        const vconcat = spec.vconcat;
        const plot =
            'plot' in vconcat[0] && 'legend' in vconcat[1]
                ? vconcat[0]
                : 'plot' in vconcat[1] && 'legend' in vconcat[0]
                  ? vconcat[1]
                  : undefined;
        if (plot) {
            plot.width = containerEl.clientWidth;
            plot.height =
                containerEl.clientHeight - (spec.vconcat.length > 1 ? verticalPadding : 0);
        }
    }
    return spec;
}

function isPlotSpec(spec: Spec) {
    if ('plot' in spec) {
        return true;
    } else if ('input' in spec && spec.input === 'table') {
        return true;
    } else if (
        'hconcat' in spec &&
        spec.hconcat.length === 2 &&
        ('plot' in spec.hconcat[0] || 'plot' in spec.hconcat[1])
    ) {
        return true;
    } else if (
        'vconcat' in spec &&
        spec.vconcat.length === 2 &&
        ('plot' in spec.vconcat[0] || 'plot' in spec.vconcat[1])
    ) {
        return true;
    } else {
        return false;
    }
}

function isInputSpec(spec: Spec) {
    return 'input' in spec && spec.input !== 'table';
}

function isTableSpec(spec: Spec) {
    return 'input' in spec && spec.input === 'table';
}

async function astToDOM(ast: SpecNode, ctx: InstantiateContext) {
    // process param/selection definitions
    for (const [name, node] of Object.entries(ast.params)) {
        // define the parameter if it doesn't exist or if we are in a notebook
        // (as in a notebook we are losing the prior cell so we want to reset the selection)
        if (!ctx.activeParams.has(name) || isNotebook()) {
            const param = (node as ASTNode).instantiate(ctx);
            ctx.activeParams.set(name, param);
        }
    }

    // instantiate and return element
    return ast.root.instantiate(ctx);
}

async function displayUnhandledErrors(ctx: VizContext, widgetEl: HTMLElement) {
    // empty plot divs indicate a possible unhandled error: poll for an
    // unhandled error per div, but short-circuit as soon as the div
    // populates (the common case — Mosaic's async query resolved). All
    // empty divs share a single 1s budget via Promise.all.
    const emptyPlotDivs = widgetEl.querySelectorAll('div.plot:empty');
    await Promise.all(
        Array.from(emptyPlotDivs).map(async (emptyDiv) => {
            const error = await ctx.collectUnhandledErrorUntil(
                () => emptyDiv.children.length > 0
            );
            if (error) {
                displayRenderError(error, emptyDiv as HTMLElement);
            }
        })
    );
}

export default { render };
