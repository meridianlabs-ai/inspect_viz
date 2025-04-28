import * as React from "react";
import { createRender, useModelState } from "@anywidget/react";

import * as aq from 'arquero';

const render = createRender(() => {


	const [id] = useModelState<string>("id");
	console.log(id)

	const [buffer] = useModelState<DataView>("buffer");

	const df = aq.fromArrow(
		new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength)
	);


	console.log(df)

	return (
		<div className="shared_df">
		</div>
	);
});

export default { render };
