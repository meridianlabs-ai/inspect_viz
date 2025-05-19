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
    private readonly params_ = new Map<string, Param>();

    constructor(private readonly conn_: AsyncDuckDBConnection) {
        this.coordinator_ = new Coordinator();
        this.coordinator_.databaseConnector(wasmConnector({ connection: this.conn_ }));
    }

    addParam(name: string, value: number | boolean | string): Param {
        if (!this.params_.has(name)) {
            this.params_.set(name, Param.value(value));
        }
        return this.params_.get(name)!;
    }

    getParam(name: string): Param | undefined {
        return this.params_.get(name);
    }

    async addReactiveDF(id: string, source_id: string, buffer: Uint8Array, queries: MosaicQuery[]) {
        // insert table into database if there is data
        if (buffer.length > 0) {
            await this.conn_?.insertArrowFromIPCStream(buffer, {
                name: id,
                create: true,
            });
        }

        // extract parameters from queries and register them
        const params = new Map<string, Param>();
        for (const query of queries) {
            for (const p of Object.values(query.parameters)) {
                params.set(p.name, this.addParam(p.name, p.value));
            }
        }

        // create and register df
        const df = new ReactiveDF(
            source_id,
            Selection.intersect(),
            queries.map(q => toSelectQuery(q, params)),
            params
        );
        this.dfs_.set(id, df);
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
