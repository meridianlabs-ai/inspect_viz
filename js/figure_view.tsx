import * as React from "react";
import { createRender, useModelState } from "@anywidget/react";

import Plotly from 'plotly.js-dist-min'


import { useSharedDF } from "./store";
import { bindTable } from "./util/binding";

import "./styles.css";

const render = createRender(() => {


	const [df_id] = useModelState<string>("df_id");
	const [figure_json] = useModelState<string>("figure_json");
	const figure = React.useMemo(() => JSON.parse(figure_json), [figure_json]);

	const plotRef = React.useRef<HTMLDivElement>(null)

	const { df } = useSharedDF(df_id)


	React.useEffect(() => {
		if (df !== undefined) {
			const data = bindTable(figure.data, df)
			Plotly.react(plotRef.current!, data, figure.layout, figure.config || {});
		}

	}, [figure, df])



	return (
		<div ref={plotRef} className="figure_view">

		</div>
	);
});

export default render;
