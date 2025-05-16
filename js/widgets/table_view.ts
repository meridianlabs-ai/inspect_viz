import type { RenderProps } from '@anywidget/types';

import { connectClient } from '../coordinator';

import { TableView } from '../clients/table_view';

interface TableRecord {
    table: string;
}

async function render({ model, el }: RenderProps<TableRecord>) {
    const table: string = model.get('table');
    const view = new TableView(table, el);
    await connectClient(table, view);
}

export default { render };
