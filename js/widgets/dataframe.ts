import { RenderProps } from '@anywidget/types';

import { vizCoordinator } from '../coordinator';
import { MosaicQuery } from '../coordinator/query';
import { ParamDef } from '../coordinator/param';

interface DataFrameProps {
    id: string;
    source_id: string;
    buffer: DataView;
    params: string;
    queries: string;
}

async function render({ model, el }: RenderProps<DataFrameProps>) {
    // unwrap widget parameters
    const id = model.get('id');
    const source_id = model.get('source_id');
    const buffer = model.get('buffer');
    const queries = model.get('queries');
    const dfQueries: MosaicQuery[] = queries ? JSON.parse(queries) : [];

    // mark cell output div hidden for layout
    setTimeout(() => {
        const elCellOutput = el.closest('.cell-output') as HTMLDivElement | undefined;
        if (elCellOutput) {
            elCellOutput.style.display = 'none';
        }
    }, 100);

    // register data frame
    const coordinator = await vizCoordinator();
    const arrowBuffer = new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength);
    await coordinator.addDataFrame(id, source_id, arrowBuffer, dfQueries);

    // add params
    coordinator.addParams(JSON.parse(model.get('params')));
}

export default { render };
