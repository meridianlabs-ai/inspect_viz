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
import { CUSTOM_INPUTS } from '../inputs';

interface MosaicProps {
    tables: Record<string, string>;
    spec: string;
}

async function render({ model, el }: RenderProps<MosaicProps>) {
    // get the spec and parse it for plot defaults
    const spec: Spec = JSON.parse(model.get('spec'));
    const plotDefaultsSpec = { plotDefaults: spec.plotDefaults, vspace: 0 } as Spec;
    const plotDefaultsAst = parseSpec(plotDefaultsSpec);

    // initialize context
    const ctx = await vizContext(plotDefaultsAst.plotDefaults);

    // insert/wait for tables to be ready
    const tables: Record<string, string> = model.get('tables') || {};
    await syncTables(ctx, tables);

    // render mosaic spec
    const renderOptions = renderSetup(el);
    const inputs = new Set(
        ['menu', 'search', 'slider', 'table'].concat(Object.keys(CUSTOM_INPUTS))
    );
    if (renderOptions.autoFillScrolling && isOutputSpec(spec)) {
        el.style.width = '100%';
        el.style.height = '400px';
    }
    const renderSpec = async () => {
        const targetSpec = renderOptions.autoFill ? responsiveSpec(spec, el) : spec;
        const ast = parseSpec(targetSpec, { inputs });
        const specEl = await astToDOM(ast, ctx);
        el.innerHTML = '';
        el.appendChild(specEl);
    };
    await renderSpec();

    // if we are doing auto-fill then re-render when size changes
    if (renderOptions.autoFill) {
        // re-render on container size changed
        const resizeObserver = new ResizeObserver(throttle(renderSpec));
        resizeObserver.observe(el);

        // cleanup resize observer on disconnect
        return () => {
            resizeObserver.disconnect();
        };
    }
}

// insert/wait for tables to be ready
async function syncTables(ctx: VizContext, tables: Record<string, string>) {
    for (const [tableName, base64Data] of Object.entries(tables)) {
        if (base64Data) {
            // decode base64 to bytes
            const binaryString = atob(base64Data);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }

            // insert table into context
            await ctx.insertTable(tableName, bytes);
        } else {
            // wait for table if no data provided
            await ctx.waitForTable(tableName);
        }
    }
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

// TODO: multiple plots
function responsiveSpec(spec: Spec, containerEl: HTMLElement): Spec {
    spec = structuredClone(spec);
    if ('plot' in spec) {
        const plot = spec.plot[0];
        if ('width' in plot && 'height' in plot) {
            plot.width = containerEl.clientWidth;
            plot.height = containerEl.clientHeight;
        }
    } else if ('hconcat' in spec && spec.hconcat.length === 2) {
        const hconcat = spec.hconcat;
        const plot =
            'plot' in hconcat[0] ? hconcat[0] : 'plot' in hconcat[1] ? hconcat[1] : undefined;
        if (plot) {
            // TODO: better dynamic sizing for legend
            plot.width = containerEl.clientWidth - 80;
            plot.height = containerEl.clientHeight;
        }
    } else if ('vconcat' in spec && spec.vconcat.length == 2) {
        const vconcat = spec.vconcat;
        const plot =
            'plot' in vconcat[0] ? vconcat[0] : 'plot' in vconcat[1] ? vconcat[1] : undefined;
        if (plot) {
            // TODO: Is the legend always 35 pixels high
            plot.width = containerEl.clientWidth;
            plot.height = containerEl.clientHeight - 35;
        }
    }
    return spec;
}

function isOutputSpec(spec: Spec) {
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

async function astToDOM(ast: SpecNode, ctx: InstantiateContext) {
    // process param/selection definitions
    for (const [name, node] of Object.entries(ast.params)) {
        // skip definitions with names already defined
        if (!ctx.activeParams.has(name)) {
            const param = (node as ASTNode).instantiate(ctx);
            ctx.activeParams.set(name, param);
        }
    }

    // instantiate and return element
    return ast.root.instantiate(ctx);
}

export default { render };
