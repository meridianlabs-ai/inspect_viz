import * as React from "react";
import { createRender, useModelState } from "@anywidget/react";
import "./figure_view.css";

const render = createRender(() => {
	const [value, setValue] = useModelState<number>("value");
	return (
		<div className="figure_view">
			<button onClick={() => setValue(value + 1)}>
				count is {value}
			</button>
		</div>
	);
});

export default { render };
