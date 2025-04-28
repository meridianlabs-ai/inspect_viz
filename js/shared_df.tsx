import * as React from "react";
import { createRender, useModelState } from "@anywidget/react";

const render = createRender(() => {


	const [id] = useModelState<string>("_id");
	console.log(id)

	const [df] = useModelState<DataView>("_df_bytes");




	console.log(df)

	return (
		<div className="shared_df">
		</div>
	);
});

export default { render };
