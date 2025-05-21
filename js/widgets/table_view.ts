import type { RenderProps } from '@anywidget/types';

import { vizCoordinator } from '../coordinator';

import { TableView } from '../clients/table_view';

interface TableProps {
    df_id: string;
}

async function render({ model, el }: RenderProps<TableProps>) {
    // unwrap widget parameters
    const df_id: string = model.get('df_id');

    // get the data frame
    const coordinator = await vizCoordinator();
    const df = await coordinator.getDataFrame(df_id);

    // create and connect the table view
    const view = new TableView(el, df.table, df.selection, df.queries, df.params);
    await coordinator.connectClient(view);
}

export default { render };
