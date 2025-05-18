import { AsyncDuckDBConnection } from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm';

import {
    MosaicClient,
    Coordinator,
    wasmConnector,
    Param,
    Selection,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

import { initDuckdb, waitForTable } from './duckdb';
import { MosaicQuery } from './query';

class DataFrame {
    constructor(
        public readonly table: string,
        public readonly queries: MosaicQuery[],
        public readonly params: Record<string, Param>,
        public readonly selection: Selection
    ) {}
}

class DataFrameCoordinator {
    private readonly coordinator_: Coordinator;
    private readonly dfs_ = new Map<string, DataFrame>();

    constructor(private readonly conn_: AsyncDuckDBConnection) {
        this.coordinator_ = new Coordinator();
        this.coordinator_.databaseConnector(wasmConnector({ connection: this.conn_ }));
    }

    async addDataFrame(name: string, queries: MosaicQuery[], buffer: Uint8Array) {
        // insert table into database
        await this.conn_?.insertArrowFromIPCStream(buffer, {
            name,
            create: true,
        });

        // create df
        this.dfs_.set(name, new DataFrame(name, queries, {}, Selection.intersect()));
    }

    async getDataFrame(name: string) {
        await waitForTable(this.conn_, name);
        return this.dfs_.get(name)!;
    }

    async connectClient(dataframe: string, client: MosaicClient) {
        await waitForTable(this.conn_, dataframe);
        this.coordinator_.connect(client);
    }
}

// get the global coordinators instance, ensuring we get the same
// instance eval across different js bundles loaded into the page
const REACTIVE_DF_COORDINATOR_KEY = Symbol.for('@@reactive-df-coordinator');
async function dataFrameCoordinator(): Promise<DataFrameCoordinator> {
    const globalScope: any = typeof window !== 'undefined' ? window : globalThis;
    if (!globalScope[REACTIVE_DF_COORDINATOR_KEY]) {
        globalScope[REACTIVE_DF_COORDINATOR_KEY] = (async () => {
            const duckdb = await initDuckdb();
            const conn = await duckdb.connect();
            return new DataFrameCoordinator(conn);
        })();
    }
    return globalScope[REACTIVE_DF_COORDINATOR_KEY] as Promise<DataFrameCoordinator>;
}

export { DataFrame, DataFrameCoordinator, dataFrameCoordinator };
