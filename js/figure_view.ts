
import type { RenderProps } from "@anywidget/types";

import { MosaicClient, toDataColumns } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import { Query } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm";

import { connectClient } from "./coordinator";

import Plotly from "https://esm.sh/plotly.js-dist-min@3.0.1"



import "./figure_view.css";
import { bindTable } from "./util/binding";

interface FigureRecord {
	df_id: string
	figure_json: string
}

export class FigureView extends MosaicClient {
	constructor(
		private readonly df_id_: string, 
		private readonly figure_: any,
		private readonly el_: HTMLElement
	) {
		super()
	}

	query(_filter?: any): any {
		return Query.select("*").from(this.df_id_)
	}

	queryResult(data: any) {
		const columns = toDataColumns(data).columns as Record<string,ArrayLike<unknown>>;
		const table = bindTable(this.figure_.data, columns);
		Plotly.react(this.el_, table, this.figure_.layout, this.figure_.config || {});
		return this;
	}


}


async function render({ model, el }: RenderProps<FigureRecord>) {

	const df_id: string = model.get("df_id");
	const figure_json: string = model.get("figure_json");
	const figure = JSON.parse(figure_json)

	const fv = new FigureView(df_id, figure, el)

	setTimeout(async () => {
		console.log("connecting client")
		await connectClient(fv)
	}, 1000)
	

}

export default { render } ;

