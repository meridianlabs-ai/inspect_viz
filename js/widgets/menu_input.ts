import type { RenderProps } from '@anywidget/types';

import { Menu } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-inputs@0.16.2/+esm';

import { dataFrameCoordinator } from '../coordinator';

interface MenuRecord {
    table: string;
    column: string;
}

async function render({ model, el }: RenderProps<MenuRecord>) {
    // unwrap widget parameters
    const table: string = model.get('table');
    const column: string = model.get('column');

    // get the data frame
    const coordinator = await dataFrameCoordinator();
    const df = await coordinator.getDataFrame(table);

    // initialize the menu and connect it
    const menu = new Menu({ element: el, as: df.selection, from: table, column });
    await coordinator.connectClient(table, menu);
}

export default { render };
