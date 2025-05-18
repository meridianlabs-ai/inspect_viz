import type { RenderProps } from '@anywidget/types';

import { dataFrameCoordinator } from '../coordinator';

import { TableView } from '../clients/table_view';

interface TableRecord {
    table: string;
}

async function render({ model, el }: RenderProps<TableRecord>) {
    // unwrap widget parameters
    const table: string = model.get('table');

    // get the data frame
    const coordinator = await dataFrameCoordinator();
    const df = await coordinator.getDataFrame(table);

    // create and connect the table view
    const view = new TableView(el, table, df.selection);
    await coordinator.connectClient(table, view);
}

export default { render };
