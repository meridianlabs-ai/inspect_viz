import type { RenderProps } from '@anywidget/types';

import {
    Spec,
    parseSpec,
    astToDOM,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm';

import { vizCoordinator } from '../coordinator';

interface SpecProps {
    df_id: string;
    spec: string;
}

// https://idl.uw.edu/mosaic/api/vgplot/plot.html

// https://github.com/uwdata/mosaic/blob/main/packages/spec/src/parse-spec.js
// https://github.com/uwdata/mosaic/blob/main/packages/spec/src/ast-to-dom.js

async function render({ model, el }: RenderProps<SpecProps>) {
    // unwrap widget parameters
    const df_id: string = model.get('df_id');
    const spec_json: string = model.get('spec');

    setTimeout(async () => {
        // get the context
        const coordinator = await vizCoordinator();
        // const ctx = coordinator.getInstantiateContext();
        await coordinator.waitForData(df_id);

        // create spec and parse it to an ast
        const spec: Spec = {
            params: {
                x: 'body_mass',
                y: 'flipper_length',
            },
            vconcat: [
                {
                    hconcat: [
                        {
                            input: 'menu',
                            label: 'Y',
                            options: ['body_mass', 'flipper_length', 'bill_depth', 'bill_length'],
                            as: '$y',
                        },
                        {
                            input: 'menu',
                            label: 'X',
                            options: ['body_mass', 'flipper_length', 'bill_depth', 'bill_length'],
                            as: '$x',
                        },
                    ],
                },
                {
                    vspace: 10,
                },
                {
                    hconcat: [
                        {
                            name: 'stroked',
                            plot: [
                                {
                                    mark: 'dot',
                                    data: {
                                        from: df_id,
                                    },
                                    x: {
                                        column: '$x',
                                    },
                                    y: {
                                        column: '$y',
                                    },
                                    stroke: 'species',
                                    symbol: 'species',
                                },
                            ],
                            grid: true,
                            xLabel: 'Body mass (g) →',
                            yLabel: '↑ Flipper length (mm)',
                        },
                        {
                            legend: 'symbol',
                            for: 'stroked',
                            columns: 1,
                        },
                    ],
                },
                {
                    vspace: 20,
                },
                {
                    hconcat: [
                        {
                            name: 'filled',
                            plot: [
                                {
                                    mark: 'dot',
                                    data: {
                                        from: df_id,
                                    },
                                    x: {
                                        column: '$x',
                                    },
                                    y: {
                                        column: '$y',
                                    },
                                    fill: 'species',
                                    symbol: 'species',
                                },
                            ],
                            grid: true,
                            xLabel: 'Body mass (g) →',
                            yLabel: '↑ Flipper length (mm)',
                        },
                        {
                            legend: 'symbol',
                            for: 'filled',
                            columns: 1,
                        },
                    ],
                },
            ],
        };

        const ast = parseSpec(spec);

        // create dom
        const { element, params } = await astToDOM(ast);
        el.appendChild(element);

        //await coordinator.connectClient(menu);
    }, 1000);
}

export default { render };
