import type { RenderProps } from '@anywidget/types';

import {
    Spec,
    SpecNode,
    parseSpec,
    InstantiateContext,
    ASTNode,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm';

import { vizContext } from '../context';

interface MosaicProps {
    table: string;
    data?: DataView;
    spec: string;
}

async function render({ model, el }: RenderProps<MosaicProps>) {
    // unwrap widget parameters
    const table: string = model.get('table');
    const data = model.get('data');
    const spec_json: string = model.get('spec');

    // get context
    const ctx = await vizContext();

    // handle data if necessary
    if (table) {
        // actual data buffer to insert
        if (data && data.byteLength > 0) {
            const arrowBuffer = new Uint8Array(data.buffer, data.byteOffset, data.byteLength);
            await ctx.insertTable(table, arrowBuffer);
            // just wait for the data to be available
        } else {
            await ctx.waitForTable(table);
        }
    }

    // render spec
    const spec: Spec = JSON.parse(spec_json);
    const ast = parseSpec(spec);

    // create dom
    const domResult = await astToDOM(ast, ctx);
    el.appendChild(domResult.element);
}

export default { render };

async function astToDOM(ast: SpecNode, ctx: InstantiateContext) {
    // process param/selection definitions
    // skip definitions with names already defined
    for (const [name, node] of Object.entries(ast.params)) {
        if (!ctx.activeParams.has(name)) {
            const param = (node as ASTNode).instantiate(ctx);
            ctx.activeParams.set(name, param);
        }
    }

    return {
        element: ast.root.instantiate(ctx),
        params: ctx.activeParams,
    };
}
