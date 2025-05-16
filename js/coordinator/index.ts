import {
    AsyncDuckDB,
    AsyncDuckDBConnection,
} from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm';

import {
    MosaicClient,
    Coordinator,
    wasmConnector,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

import { initDuckdb, waitForTable } from './duckdb';

class TableCoordinator {
    private readonly coordinator_: Coordinator;

    constructor(private readonly conn_: AsyncDuckDBConnection) {
        this.coordinator_ = new Coordinator();
        this.coordinator_.databaseConnector(wasmConnector({ connection: this.conn_ }));
    }

    async addTable(table: string, buffer: Uint8Array) {
        await this.conn_?.insertArrowFromIPCStream(buffer, {
            name: table,
            create: true,
        });
    }

    async waitForTable(table: string) {
        await waitForTable(this.conn_, table);
    }

    connectClient(client: MosaicClient) {
        this.coordinator_?.connect(client);
    }
}

// get the global coordinators instance, ensuring we get the same
// instance eval across different js bundles loaded into the page
const TABLE_COORDINATOR_KEY = Symbol.for('@@table-coordinator');
async function tableCoordinator(): Promise<TableCoordinator> {
    const globalScope: any = typeof window !== 'undefined' ? window : globalThis;
    if (!globalScope[TABLE_COORDINATOR_KEY]) {
        globalScope[TABLE_COORDINATOR_KEY] = (async () => {
            const duckdb = await initDuckdb();
            const conn = await duckdb.connect();
            return new TableCoordinator(conn);
        })();
    }
    return globalScope[TABLE_COORDINATOR_KEY] as Promise<TableCoordinator>;
}

export async function addTable(name: string, buffer: Uint8Array) {
    const coordinator = await tableCoordinator();
    await coordinator.addTable(name, buffer);
}

export async function connectClient(table: string, client: MosaicClient) {
    const coordinator = await tableCoordinator();
    await coordinator.waitForTable(table);
    coordinator.connectClient(client);
}
