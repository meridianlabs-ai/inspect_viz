import {
    MosaicClient,
    Selection,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';
import { SelectQuery } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm';

export abstract class VizClient extends MosaicClient {
    constructor(
        private readonly table_: string,
        filterBy: Selection,
        private readonly queries_: SelectQuery[]
    ) {
        super(filterBy);
    }

    query(filter: any[] = []): SelectQuery {
        // run the main query
        let query = SelectQuery.select('*').from(this.table_).where(filter);

        // run any subqueries
        return VizClient.applyQueries(query, this.queries_);
    }

    static applyQueries(query: SelectQuery, queries: SelectQuery[]): SelectQuery {
        for (const q of queries) {
            query = q.clone().from(query);
        }
        return query;
    }
}
