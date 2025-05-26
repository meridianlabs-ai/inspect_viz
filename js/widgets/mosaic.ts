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

    // render spec
    const spec: Spec = JSON.parse(spec_json);
    const ast = parseSpec(spec);

    // create dom
    const domResult = await astToDOM(ast, ctx);

    // append it
    el.appendChild(domResult.element);

    const plot = domResult.element.querySelector('.plot') as HTMLElement;
    if (plot) {
        plot.style.width = '100%';
        plot.style.height = 'auto';
        const svgs = await waitForSvgs(plot);
        svgs.forEach((svg: SVGElement) => {
            svg.removeAttribute('width');
            svg.removeAttribute('height');
            svg.style.width = '100%';
            svg.style.height = 'auto';
        });
    }
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

function waitForSvgs(
    element: HTMLElement,
    timeout: number = 5000
): Promise<NodeListOf<SVGElement>> {
    return new Promise((resolve, reject) => {
        const existingSvgs = element.querySelectorAll<SVGElement>('svg');
        if (existingSvgs.length > 0) {
            resolve(existingSvgs);
            return;
        }

        const observer = new MutationObserver((_mutations: MutationRecord[]) => {
            const svgs = element.querySelectorAll<SVGElement>('svg');
            if (svgs.length > 0) {
                observer.disconnect();
                clearTimeout(timeoutId);
                resolve(svgs);
            }
        });

        const timeoutId = setTimeout(() => {
            observer.disconnect();
            reject(new Error('SVGs not found within timeout'));
        }, timeout);

        observer.observe(element, {
            childList: true,
            subtree: true,
        });
    });
}
