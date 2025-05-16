import type { RenderProps } from '@anywidget/types';

import { connectClient } from '../coordinator';

import { FigureView } from '../clients/figure_view';

interface FigureRecord {
    table: string;
    figure_json: string;
}

async function render({ model, el }: RenderProps<FigureRecord>) {
    const table: string = model.get('table');
    const figure_json: string = model.get('figure_json');
    const figure = JSON.parse(figure_json);
    const view = new FigureView(table, figure, el);
    await connectClient(table, view);
}

export default { render };
