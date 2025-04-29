
import { RenderProps } from "@anywidget/types";

import { addSharedDF } from "./store";

function render({ model, el }: RenderProps) {

	const id: string = model.get("id");
	const buffer: DataView = model.get("buffer");
	const df = window.aq.fromArrow(
		new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength)
	);
	addSharedDF(id, df)

}

export default render;
