import type { RenderProps } from '@anywidget/types';

import {
    Spec,
    SpecNode,
    parseSpec,
    InstantiateContext,
    ASTNode,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm';

import { vizCoordinator } from '../coordinator';

interface SpecProps {
    df_id: string;
    df_buffer?: DataView;
    spec: string;
}

async function render({ model, el }: RenderProps<SpecProps>) {
    // unwrap widget parameters
    const df_id: string = model.get('df_id');
    const df_buffer = model.get('df_buffer');
    const spec_json: string = model.get('spec');

    // get coordinator
    const coordinator = await vizCoordinator();

    // add data if necessary (alternatively wait for it)
    if (df_buffer && df_buffer.byteLength > 0) {
        const arrowBuffer = new Uint8Array(
            df_buffer.buffer,
            df_buffer.byteOffset,
            df_buffer.byteLength
        );
        await coordinator.addData(df_id, arrowBuffer);
    } else {
        await coordinator.waitForData(df_id);
    }

    // render spec
    const spec: Spec = JSON.parse(spec_json);
    const ast = parseSpec(spec);

    // create dom
    const domResult = await astToDOM(ast, coordinator.getInstantiateContext());
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
