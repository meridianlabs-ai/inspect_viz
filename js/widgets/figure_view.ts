import type { RenderProps } from '@anywidget/types';

import { dataFrameCoordinator } from '../coordinator';

import { FigureView } from '../clients/figure_view';

interface FigureProps {
    df_id: string;
    figure_json: string;
}

async function render({ model, el }: RenderProps<FigureProps>) {
    // unwrap the widget payload
    const df_id: string = model.get('df_id');
    const figure_json: string = model.get('figure_json');
    const figure = JSON.parse(figure_json);

    // get the data frame
    const coordinator = await dataFrameCoordinator();
    const df = await coordinator.getDataFrame(df_id);

    // create the view and connect it
    const view = new FigureView(el, df.table, figure, df.selection);
    await coordinator.connectClient(view);
}

export default { render };
