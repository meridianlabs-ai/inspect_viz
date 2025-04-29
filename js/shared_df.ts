
import { RenderProps } from "@anywidget/types";

import { addSharedDF } from "./store";

const aq = await import("https://cdn.jsdelivr.net/npm/arquero@8.0.1/+esm");


interface SharedDFREcord {
	id: string
	buffer: DataView
}

function render({ model }: RenderProps<SharedDFREcord>) {

	

	const id = model.get("id");
	const buffer = model.get("buffer");
	const df = aq.fromArrow(
		new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength)
	);
	addSharedDF(id, df)

}

export default { render } ;
