import { RenderProps } from '@anywidget/types';

import { vizCoordinator } from '../coordinator';

interface DataFrameProps {
    id: string;
    buffer: DataView;
    params: string;
}

async function render({ model, el }: RenderProps<DataFrameProps>) {
    // unwrap widget parameters
    const id = model.get('id');
    const buffer = model.get('buffer');

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
    await coordinator.addDataFrame(id, arrowBuffer);

    // add params
    coordinator.addParams(JSON.parse(model.get('params')));
}

export default { render };
