import {
    MosaicClient,
    Param,
    Selection,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';
import { SelectQuery } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm';

export abstract class VizClient extends MosaicClient {
    constructor(
        private readonly table_: string,
        filterBy: Selection,
        private readonly queries_: SelectQuery[],
        private readonly params_: Map<string, Param>
    ) {
        super(filterBy);
        this.params_.forEach(value => {
            value.addEventListener('value', () => this.requestUpdate());
        });
    }

    query(filter: any[] = []): SelectQuery {
        let query = SelectQuery.select('*').from(this.table_).where(filter);
        return VizClient.applyQueries(query, this.queries_);
    }

    static applyQueries(query: SelectQuery, queries: SelectQuery[]): SelectQuery {
        for (let q of queries) {
            query = q.clone().from(query);
        }
        return query;
    }
}
