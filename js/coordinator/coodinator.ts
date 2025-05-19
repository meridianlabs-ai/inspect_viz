import { AsyncDuckDBConnection } from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm';

import {
    MosaicClient,
    Coordinator,
    wasmConnector,
    Selection,
    Param,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

import { initDuckdb } from './duckdb';
import { MosaicQuery } from './query';
import { ReactiveDF } from './reactive_df';
import { sleep } from '../util/wait';
import { toSelectQuery } from './select';

class ReactiveDFCoordinator {
    private readonly coordinator_: Coordinator;
    private readonly dfs_ = new Map<string, ReactiveDF>();

    constructor(private readonly conn_: AsyncDuckDBConnection) {
        this.coordinator_ = new Coordinator();
        this.coordinator_.databaseConnector(wasmConnector({ connection: this.conn_ }));
    }

    async addReactiveDF(id: string, source_id: string, buffer: Uint8Array, queries: MosaicQuery[]) {
        // insert table into database if there is data
        if (buffer.length > 0) {
            await this.conn_?.insertArrowFromIPCStream(buffer, {
                name: id,
                create: true,
            });
        }

        // create params from queries
        const params = new Map<string, Param>();
        for (const query of queries) {
            for (const p of Object.values(query.parameters)) {
                params.set(p.name, Param.value(p.value));
            }
        }

        // convert to select queries
        const selectQueries = queries.map(toSelectQuery);

        // create and regsiter df
        this.dfs_.set(id, new ReactiveDF(source_id, Selection.intersect(), selectQueries, params));
    }

    async getReactiveDF(id: string) {
        // at startup we can't control the order of df producing and df consuming
        // widgets, so we may need to wait and retry for the data frame
        while (true) {
            const df = this.dfs_.get(id);
            if (df) {
                return df;
            } else {
                await sleep(100);
            }
        }
    }

    async connectClient(client: MosaicClient) {
        this.coordinator_.connect(client);
    }
}

// get the global coordinators instance, ensuring we get the same
// instance eval across different js bundles loaded into the page
const REACTIVE_DF_COORDINATOR_KEY = Symbol.for('@@reactive-df-coordinator');
async function reactiveDFCoordinator(): Promise<ReactiveDFCoordinator> {
    const globalScope: any = typeof window !== 'undefined' ? window : globalThis;
    if (!globalScope[REACTIVE_DF_COORDINATOR_KEY]) {
        globalScope[REACTIVE_DF_COORDINATOR_KEY] = (async () => {
            const duckdb = await initDuckdb();
            const conn = await duckdb.connect();
            return new ReactiveDFCoordinator(conn);
        })();
    }
    return globalScope[REACTIVE_DF_COORDINATOR_KEY] as Promise<ReactiveDFCoordinator>;
}

export { ReactiveDFCoordinator, reactiveDFCoordinator };
