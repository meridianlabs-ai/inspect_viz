import type { RenderProps } from '@anywidget/types';

import {
    Spec,
    parseSpec,
    astToDOM,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm';

import { vizCoordinator } from '../coordinator';

interface PlotProps {
    df_id: string;
    plot: string;
    params: string;
}

// https://idl.uw.edu/mosaic/api/vgplot/plot.html

// https://github.com/uwdata/mosaic/blob/main/packages/spec/src/parse-spec.js
// https://github.com/uwdata/mosaic/blob/main/packages/spec/src/ast-to-dom.js

async function render({ model, el }: RenderProps<PlotProps>) {
    // unwrap widget parameters
    const df_id: string = model.get('df_id');
    const plot_json: string = model.get('plot');

    setTimeout(async () => {
        // get the context
        const coordinator = await vizCoordinator();
        const df = await coordinator.getData(df_id);
        const ctx = coordinator.getInstantiateContext();

        // add params
        coordinator.addParams(JSON.parse(model.get('params')));

        // create spec
        const spec: Spec = JSON.parse(plot_json);
        const ast = parseSpec(spec);

        // create dom
        const { element, params } = await astToDOM(ast, {
            api: ctx.api,
            plotDefaults: ctx.plotDefaults,
            params: ctx.activeParams,
            baseURL: ctx.baseURL,
        });
        el.appendChild(element);

        //await coordinator.connectClient(menu);
    }, 1000);
}

export default { render };
