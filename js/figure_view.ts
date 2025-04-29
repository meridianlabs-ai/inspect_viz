
import type { RenderProps } from "@anywidget/types";

import { getSharedDF } from "./store";
import { bindTable } from "./util/binding";

const Plotly = (await import(
	"https://esm.sh/plotly.js-dist-min@3.0.1"
)).default;

import "./figure_view.css";

interface FigureRecord {
	df_id: string
	figure_json: string
}

function render({ model, el }: RenderProps<FigureRecord>) {

	const df_id: string = model.get("df_id");
	const figure_json: string = model.get("figure_json");
	const figure = JSON.parse(figure_json)

	setTimeout(() => {
		const df  = getSharedDF(df_id)
		if (df) {
			const data = bindTable(figure.data, df.computed);
			Plotly.react(el, data, figure.layout, figure.config || {});
		}
	}, 1000)
	

}

export default { render } ;

