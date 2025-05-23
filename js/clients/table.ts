import { Param, Selection } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';
import { Table as MosaicTable } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-inputs@0.16.2/+esm';

export class Table extends MosaicTable {
    constructor(
        el: HTMLElement,
        table: string,
        filterBy: Selection,
        private readonly params_: Map<string, Param>
    ) {
        super({ element: el, filterBy, from: table });
        this.params_.forEach(value => {
            value.addEventListener('value', () => this.requestUpdate());
        });
    }
}
