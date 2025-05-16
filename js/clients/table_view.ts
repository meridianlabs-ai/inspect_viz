import { Selection } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';
import { Table } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-inputs@0.16.2/+esm';

export class TableView extends Table {
    constructor(el: HTMLElement, table: string, filterBy?: Selection) {
        super({ element: el, filterBy, from: table });
    }
}
