import {
    MosaicClient,
    Selection,
    toDataColumns,
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
        for (const q of this.queries_) {
            query = q.from(query);
        }

        // return
        return query;
    }

    queryResult(data: any) {
        const columns = toDataColumns(data).columns as Record<string, ArrayLike<unknown>>;
        this.onQueryResult(columns);
        return this;
    }

    abstract onQueryResult(columns: Record<string, ArrayLike<unknown>>): void;
}
