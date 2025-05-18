import type { RenderProps } from '@anywidget/types';

import { dataFrameCoordinator } from '../coordinator';

import { FigureView } from '../clients/figure_view';

interface FigureRecord {
    table: string;
    figure_json: string;
}

async function render({ model, el }: RenderProps<FigureRecord>) {
    // unwrap the widget payload
    const table: string = model.get('table');
    const figure_json: string = model.get('figure_json');
    const figure = JSON.parse(figure_json);

    // get the data frame
    const coordinator = await dataFrameCoordinator();
    const df = await coordinator.getDataFrame(table);

    // create the view and connect it
    const view = new FigureView(el, table, figure, df.selection);
    await coordinator.connectClient(table, view);
}

export default { render };
