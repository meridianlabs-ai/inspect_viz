import type { RenderProps } from '@anywidget/types';

import { Menu } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-inputs@0.16.2/+esm';

import { dataFrameCoordinator } from '../coordinator';

interface MenuProps {
    df_id: string;
    column: string;
}

async function render({ model, el }: RenderProps<MenuProps>) {
    // unwrap widget parameters
    const df_id: string = model.get('df_id');
    const column: string = model.get('column');

    // get the data frame
    const coordinator = await dataFrameCoordinator();
    const df = await coordinator.getDataFrame(df_id);

    // initialize the menu and connect it
    const menu = new Menu({
        element: el,
        as: df.selection,
        from: df.table,
        column: column,
    });
    await coordinator.connectClient(menu);
}

export default { render };
