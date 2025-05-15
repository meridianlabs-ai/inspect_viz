
import { RenderProps } from "@anywidget/types";

import { addSharedDF } from "./store";

const aq = await import("https://cdn.jsdelivr.net/npm/arquero@8.0.1/+esm");

import { addSharedDF as addShared } from "./coordinator";


interface SharedDFREcord {
	id: string
	buffer: DataView
}

function render({ model }: RenderProps<SharedDFREcord>) {

	const id = model.get("id");
	const buffer = model.get("buffer");
	const arrowBuffer = new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength)
	const df = aq.fromArrow(arrowBuffer);
	addSharedDF(id, df)

	setTimeout(async () => {
		await addShared(id, arrowBuffer)
	}, 100)

}

export default { render } ;
