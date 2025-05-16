import type { RenderProps } from '@anywidget/types';

import { Menu } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-inputs@0.16.2/+esm';

import { connectClient, tableSelection } from '../coordinator';

interface MenuRecord {
    table: string;
    column: string;
}

async function render({ model, el }: RenderProps<MenuRecord>) {
    const table: string = model.get('table');
    const column: string = model.get('column');

    const selection = await tableSelection(table);

    const menu = new Menu({ element: el, as: selection, from: table, column });
    await connectClient(table, menu);
}

export default { render };
