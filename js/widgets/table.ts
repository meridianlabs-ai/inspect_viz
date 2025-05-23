import type { RenderProps } from '@anywidget/types';

import { vizCoordinator } from '../coordinator';

import { Table } from '../clients/table';

interface TableProps {
    df_id: string;
    params: string;
}

async function render({ model, el }: RenderProps<TableProps>) {
    // unwrap widget parameters
    const df_id: string = model.get('df_id');

    // get the data frame
    const coordinator = await vizCoordinator();
    const df = await coordinator.getData(df_id);

    // add params
    coordinator.addParams(JSON.parse(model.get('params')));

    // create and connect the table view
    const view = new Table(el, df.table, df.selection, coordinator.getParams());
    await coordinator.connectClient(view);
}

export default { render };
