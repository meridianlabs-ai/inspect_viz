import type { RenderProps } from '@anywidget/types';

import {
    Spec,
    SpecNode,
    parseSpec,
    InstantiateContext,
    ASTNode,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm';

import { throttle } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

import { vizContext } from '../context';

interface MosaicProps {
    tables: Record<string, string>;
    spec: string;
}

async function render({ model, el }: RenderProps<MosaicProps>) {
    // unwrap widget parameters
    const tables: Record<string, string> = model.get('tables') || {};
    const spec_json: string = model.get('spec');

    // get context
    const ctx = await vizContext();

    // handle tables
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

    // mosaic widgets already have sufficient margin/padding so override
    // any host prescribed bottom margin.
    const widgetEl = el.closest('.widget-subarea') as HTMLElement | undefined;
    if (widgetEl) {
        widgetEl.style.marginBottom = '0';
    }

    // render spec according to container size
    const spec: Spec = JSON.parse(spec_json);
    const renderSpec = async () => {
        const sizedSpec = sizeToContainer(spec, el);
        const ast = parseSpec(sizedSpec);
        const { element } = await astToDOM(ast, ctx);
        el.innerHTML = '';
        el.appendChild(element);
    };
    await renderSpec();

    // re-render on container size changed
    const resizeObserver = new ResizeObserver(throttle(renderSpec));
    resizeObserver.observe(el);

    // cleanup resize observer on disconnect
    return () => {
        resizeObserver.disconnect();
    };
}

export default { render };

async function astToDOM(ast: SpecNode, ctx: InstantiateContext) {
    // process param/selection definitions
    for (const [name, node] of Object.entries(ast.params)) {
        // skip definitions with names already defined
        if (!ctx.activeParams.has(name)) {
            const param = (node as ASTNode).instantiate(ctx);
            ctx.activeParams.set(name, param);
        }
    }

    // instantiate and return root context + params
    return {
        element: ast.root.instantiate(ctx),
        params: ctx.activeParams,
    };
}

function sizeToContainer(spec: Spec, containerEl: HTMLElement): Spec {
    spec = structuredClone(spec);
    if ('plot' in spec) {
        const plot = spec.plot[0];
        if ('width' in plot && 'height' in plot) {
            plot.width = containerEl.clientWidth;
            plot.height = containerEl.clientHeight;
        }
    } else if ('hconcat' in spec) {
        const hconcat = spec.hconcat;
        if ('plot' in hconcat[0]) {
            hconcat[0].width = containerEl.clientWidth;
            hconcat[0].height = containerEl.clientHeight;
        }
    } else if ('vconcat' in spec) {
        const vconcat = spec.vconcat;
        if ('plot' in vconcat[0]) {
            vconcat[0].width = containerEl.clientWidth;
            vconcat[0].height = containerEl.clientHeight;
        }
    }
    return spec;
}
