import { RenderProps } from '@anywidget/types';

import { addTable } from '../coordinator';

interface SharedDFREcord {
    table: string;
    buffer: DataView;
}

async function render({ model }: RenderProps<SharedDFREcord>) {
    const table = model.get('table');
    const buffer = model.get('buffer');
    const arrowBuffer = new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength);

    await addTable(table, arrowBuffer);
}

export default { render };
