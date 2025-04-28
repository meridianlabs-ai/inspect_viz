import * as React from "react";
import { createRender, useModelState } from "@anywidget/react";

import * as aq from 'arquero';

const render = createRender(() => {


	const [id] = useModelState<string>("_id");
	console.log(id)

	const [df_bytes] = useModelState<DataView>("_df_bytes");

	const dt = aq.fromArrow(new Uint8Array(df_bytes.buffer, df_bytes.byteOffset, df_bytes.byteLength));


	console.log(dt)

	return (
		<div className="shared_df">
		</div>
	);
});

export default { render };
