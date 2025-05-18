import { RenderProps } from '@anywidget/types';

import { addTable } from '../coordinator';

interface ReactiveDFRecord {
    table: string;
    buffer: DataView;
    queries: string;
}

async function render({ model }: RenderProps<ReactiveDFRecord>) {
    const table = model.get('table');
    const buffer = model.get('buffer');
    const arrowBuffer = new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength);

    await addTable(table, arrowBuffer);
}

export default { render };
