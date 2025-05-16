import type { RenderProps } from '@anywidget/types';

import { connectClient, tableSelection } from '../coordinator';

import { TableView } from '../clients/table_view';

interface TableRecord {
    table: string;
}

async function render({ model, el }: RenderProps<TableRecord>) {
    const table: string = model.get('table');

    const selection = await tableSelection(table);
    const view = new TableView(el, table, selection);
    await connectClient(table, view);
}

export default { render };
