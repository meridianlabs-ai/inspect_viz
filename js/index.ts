


import renderSharedDF from './shared_df'
import renderFigureView from './figure_view'

import type { RenderProps } from "@anywidget/types";

function render({ model, el, experimental }: RenderProps) {
    const componentType = model.get("component");

    switch (componentType) {
        case "SharedDF":
            renderSharedDF({ model, el, experimental });
            break;
        case "FigureView":
            renderFigureView({ model, el, experimental });
            break;
        default:
            throw new Error(`Unknown component type ${componentType}`);
    }
}

export default { render }
