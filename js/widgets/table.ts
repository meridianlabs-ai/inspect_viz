import type { RenderProps } from '@anywidget/types';

import { vizCoordinator } from '../coordinator';

import { Table } from '../clients/table';
import { Selection } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

interface TableProps {
    df_id: string;
    selection: string;
    params: string;
}

async function render({ model, el }: RenderProps<TableProps>) {
    // unwrap widget parameters
    const df_id: string = model.get('df_id');
    const selection: string = model.get('selection');

    // get the data frame
    const coordinator = await vizCoordinator();
    await coordinator.waitForData(df_id);

    // add params
    coordinator.addParams(JSON.parse(model.get('params')));

    // get selection param
    const sel = coordinator.getParam(selection);
    if (sel === undefined) {
        throw new Error('You must pass a selection to tables.');
    }

    // create and connect the table view
    const view = new Table(el, df_id, sel as Selection, coordinator.getParams());
    await coordinator.connectClient(view);
}

export default { render };
