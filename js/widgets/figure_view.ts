import type { RenderProps } from '@anywidget/types';

import { dataFrameCoordinator, toSelectQuery } from '../coordinator';

import { FigureView } from '../clients/figure_view';
import { SelectQuery } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm';

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

    // it keep getting the first one by id, need a new id but need original table

    // build sub-queries
    const queries: SelectQuery[] = df.queries.map(toSelectQuery);

    // create the view and connect it
    const view = new FigureView(el, figure, df.table, df.selection, queries);
    await coordinator.connectClient(view);
}

export default { render };
