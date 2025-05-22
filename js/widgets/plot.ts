import type { RenderProps } from '@anywidget/types';

import { vizCoordinator } from '../coordinator';

interface PlotProps {
    df_id: string;
    plot: string;
    params: string;
}

async function render({ model, el }: RenderProps<PlotProps>) {
    // unwrap widget parameters
    const df_id: string = model.get('df_id');
    const plot_json: string = model.get('plot');
    const param_json: string = model.get('params');

    // get the data frame
    const coordinator = await vizCoordinator();
    const df = await coordinator.getDataFrame(df_id);

    //await coordinator.connectClient(menu);
}

export default { render };
