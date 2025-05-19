import { Selection } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';
import { Table } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-inputs@0.16.2/+esm';
import { SelectQuery } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm';
import { VizClient } from './viz_client';

export class TableView extends Table {
    constructor(
        el: HTMLElement,
        table: string,
        filterBy: Selection,
        private readonly queries_: SelectQuery[]
    ) {
        super({ element: el, filterBy, from: table });
    }

    query(filter?: any[]): SelectQuery {
        let query = super.query(filter);
        return VizClient.applyQueries(query, this.queries_);
    }
}
