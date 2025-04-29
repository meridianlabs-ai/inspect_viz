


import renderSharedDF from './shared_df'
import renderFigureView from './figure_view'

import type { AnyModel, Experimental } from "@anywidget/types";
type RenderArgs = {
    model: AnyModel;
    el: HTMLElement;
    experimental: Experimental
}

function render({ model, el, experimental }: RenderArgs) {
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
