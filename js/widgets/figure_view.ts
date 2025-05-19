import type { RenderProps } from '@anywidget/types';

import { reactiveDFCoordinator } from '../coordinator';

import { FigureView, PlotlyAxisMappings, PlotlyFigure } from '../clients/figure_view';

interface FigureProps {
    df_id: string;
    figure: string;
    axis_mappings: string;
}

async function render({ model, el }: RenderProps<FigureProps>) {
    // unwrap the widget payload
    const df_id: string = model.get('df_id');
    const figure_json: string = model.get('figure');
    const figure: PlotlyFigure = JSON.parse(figure_json);
    const axis_mappings_json: string = model.get('axis_mappings');
    const axis_mappings: PlotlyAxisMappings = JSON.parse(axis_mappings_json);

    // get the data frame
    const coordinator = await reactiveDFCoordinator();
    const df = await coordinator.getReactiveDF(df_id);

    // create the view and connect it
    const view = new FigureView(el, figure, axis_mappings, df.table, df.selection, df.queries);
    await coordinator.connectClient(view);
}

export default { render };
