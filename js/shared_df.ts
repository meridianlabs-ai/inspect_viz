
import { RenderProps } from "@anywidget/types";

import { addTable } from "./coordinator";


interface SharedDFREcord {
	id: string
	buffer: DataView
}

async function render({ model }: RenderProps<SharedDFREcord>) {

	const id = model.get("id");
	const buffer = model.get("buffer");
	const arrowBuffer = new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength)

	await addTable(id, arrowBuffer)
}

export default { render } ;
