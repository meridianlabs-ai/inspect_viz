import * as React from "react";
import { createRender, useModelState } from "@anywidget/react";

import * as aq from 'arquero';
import { addSharedDF } from "./store";

const render = createRender(() => {
	const [id] = useModelState<string>("id");
	const [buffer] = useModelState<DataView>("buffer");
	const df = aq.fromArrow(
		new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength)
	);
	addSharedDF(id, df)

	return (
		<div className="shared_df">
		</div>
	);
});

export default render;
