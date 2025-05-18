import { RenderProps } from '@anywidget/types';

import { dataFrameCoordinator } from '../coordinator';

interface ReactiveDFProps {
    id: string;
    buffer: DataView;
    queries: string;
}

async function render({ model }: RenderProps<ReactiveDFProps>) {
    // unwrap widget parameters
    const id = model.get('id');
    const buffer = model.get('buffer');

    // register data frame
    const coordinator = await dataFrameCoordinator();
    const arrowBuffer = new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength);
    await coordinator.addDataFrame(id, arrowBuffer, []);
}

export default { render };
