import { AsyncDuckDB, AsyncDuckDBConnection } from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm';

import { MosaicClient, Coordinator, wasmConnector } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm'

import { initDuckdb } from './duckdb';


class TableCoordinator {

    private readonly coordinator_: Coordinator;

    constructor(private readonly conn_: AsyncDuckDBConnection) {
        this.coordinator_  = new Coordinator()
        this.coordinator_.databaseConnector(wasmConnector({ connection: this.conn_ }));
    }
   

    async addTable(table: string, buffer: Uint8Array) {
        await this.conn_?.insertArrowFromIPCStream(buffer, { name: table , create: true });
    }

    connectClient(client: MosaicClient) {
        this.coordinator_?.connect(client);
    }
}


// get the global coordinators instance, ensuring we get the same 
// instance eval across different js bundles loaded into the page
const TABLE_COORDINATOR_KEY = Symbol.for('@@table-coordinator')
async function tableCoordinator(): Promise<TableCoordinator> {
    const globalScope: any = typeof window !== 'undefined' ? window : globalThis
    if (!globalScope[TABLE_COORDINATOR_KEY]) {
        const duckdb = await initDuckdb();
        const conn = await duckdb.connect();
        const coordinator = new TableCoordinator(conn)
        globalScope[TABLE_COORDINATOR_KEY] = coordinator;
    }
    return globalScope[TABLE_COORDINATOR_KEY] as TableCoordinator;
}

export async function addTable(name: string, buffer: Uint8Array) {
    const coordinator = await tableCoordinator();
    await coordinator.addTable(name, buffer);
}


export async function connectClient(client: MosaicClient) {
    const coordinator = await tableCoordinator();
    coordinator.connectClient(client)
}