import * as React from "react";
import { createRender, useModelState } from "@anywidget/react";
import { useState } from "react";


import Plotly from 'plotly.js-dist-min'

import "./figure_view.css";

const render = createRender(() => {

	const [value, setValue] = useState<number>(20)

	// const [df_id] = useModelState<number>("df_id");

	const [figure_json] = useModelState<string>("figure_json");
	const figure = React.useMemo(() => JSON.parse(figure_json), [figure_json]);

	const plotRef = React.useRef(null)

	React.useEffect(() => {

		Plotly.react(plotRef.current!, figure.data, figure.layout, figure.config || {});


	}, [figure])



	return (
		<div ref={plotRef} className="figure_view">

		</div>
	);
});

export default { render };
