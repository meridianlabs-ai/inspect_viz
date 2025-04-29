
import { RenderProps } from "@anywidget/types";

import { addSharedDF } from "./store";

interface SharedDFREcord {
	id: string
	buffer: DataView
}

function render({ model, el }: RenderProps<SharedDFREcord>) {

	const id = model.get("id");
	const buffer = model.get("buffer");
	const df = window.aq.fromArrow(
		new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength)
	);
	addSharedDF(id, df)

}

export default { render } ;
