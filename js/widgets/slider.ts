import type { RenderProps } from '@anywidget/types';

import { Slider } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-inputs@0.16.2/+esm';

import { vizCoordinator } from '../coordinator';

interface SliderProps {
    df_id: string;
    column: string;
    param: string;
    params: string;
}

async function render({ model, el }: RenderProps<SliderProps>) {
    // unwrap widget parameters
    const df_id: string = model.get('df_id');
    const column: string = model.get('column');
    const param: string = model.get('param');

    // get the data frame
    const coordinator = await vizCoordinator();
    await coordinator.waitForData(df_id);

    // add params
    coordinator.addParams(JSON.parse(model.get('params')));

    // initialize the slider and connect it
    const menu = new Slider({
        element: el,
        as: coordinator.getParam(param),
        from: df_id,
        column: column,
    });
    await coordinator.connectClient(menu);
}

export default { render };
