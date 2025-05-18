import { RenderProps } from '@anywidget/types';

import { dataFrameCoordinator } from '../coordinator';
import { MosaicQuery } from '../coordinator/query';

interface ReactiveDFProps {
    id: string;
    source_id: string;
    buffer: DataView;
    queries: string;
}

async function render({ model }: RenderProps<ReactiveDFProps>) {
    // unwrap widget parameters
    const id = model.get('id');
    const source_id = model.get('source_id');
    const buffer = model.get('buffer');
    const queries = model.get('queries');
    const dfQueries: MosaicQuery[] = queries ? JSON.parse(queries) : [];

    // register data frame
    const coordinator = await dataFrameCoordinator();
    const arrowBuffer = new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength);
    await coordinator.addDataFrame(id, source_id, arrowBuffer, dfQueries);
}

export default { render };
