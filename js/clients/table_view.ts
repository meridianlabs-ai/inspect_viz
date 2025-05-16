import { Table } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-inputs@0.16.2/+esm';

export class TableView extends Table {
    constructor(table: string, el: HTMLElement) {
        super({ element: el, from: table });
    }
}
