import { AsyncDuckDB, AsyncDuckDBConnection } from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.1-dev132.0/+esm';

import { MosaicClient, Coordinator } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.15.0/+esm'

import { initDuckdb } from './duckdb';

class SharedDFCoordinator {

    private duckdb_?: AsyncDuckDB;
    private conn_?: AsyncDuckDBConnection;
    private coordinator_?: Coordinator;

    async initialize() {
        const mosaic = await import("https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.15.0/+esm");
        this.duckdb_ = await initDuckdb();
        this.conn_ = await this.duckdb_.connect();
        this.coordinator_ = new mosaic.Coordinator();
        const connector = mosaic.wasmConnector( { connection: this.conn_ });
        this.coordinator_.databaseConnector(connector);
    }

    async addSharedDF(name: string, buffer: Uint8Array) {
        await this.conn_?.insertArrowFromIPCStream(buffer, { name: name });
    }

    connectClient(client: MosaicClient) {
        this.coordinator_?.connect(client);
    }
}


// get the global coordinators instance, ensuring we get the same 
// instance eval across different js bundles loaded into the page
const SHARED_DF_COORDINATOR_KEY = Symbol.for('@@shared-df-store')
async function sharedDFCoordinator(): Promise<SharedDFCoordinator> {
    const globalScope: any = typeof window !== 'undefined' ? window : globalThis
    if (!globalScope[SHARED_DF_COORDINATOR_KEY]) {
        const coordinator = new SharedDFCoordinator()
        await coordinator.initialize()
        globalScope[SHARED_DF_COORDINATOR_KEY] = coordinator;
    }
    return globalScope[SHARED_DF_COORDINATOR_KEY] as SharedDFCoordinator;
}

export async function addSharedDF(name: string, buffer: Uint8Array) {
    await (await sharedDFCoordinator()).addSharedDF(name, buffer);
}

export async function connectClient(client: MosaicClient) {
    (await sharedDFCoordinator()).connectClient(client);
}