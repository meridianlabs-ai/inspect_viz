import { AsyncDuckDBConnection } from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm';

import {
    MosaicClient,
    Coordinator,
    wasmConnector,
    Selection,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

import { initDuckdb, waitForTable } from './duckdb';

class TableCoordinator {
    private readonly coordinator_: Coordinator;
    private readonly selections_: Map<string, Selection>;

    constructor(private readonly conn_: AsyncDuckDBConnection) {
        this.coordinator_ = new Coordinator();
        this.coordinator_.databaseConnector(wasmConnector({ connection: this.conn_ }));
        this.selections_ = new Map<string, Selection>();
    }

    async addTable(table: string, buffer: Uint8Array) {
        // insert table into database
        await this.conn_?.insertArrowFromIPCStream(buffer, {
            name: table,
            create: true,
        });
        // track selection for table
        this.selections_.set(table, Selection.intersect());
    }

    async waitForTable(table: string) {
        await waitForTable(this.conn_, table);
    }

    tableSelection(table: string) {
        return this.selections_.get(table);
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

export async function addTable(table: string, buffer: Uint8Array) {
    const coordinator = await tableCoordinator();
    await coordinator.addTable(table, buffer);
}

export async function tableSelection(table: string) {
    return withTableCoordinator<Selection>(table, async (coordinator: TableCoordinator) => {
        const selection = coordinator.tableSelection(table);
        if (selection === undefined) {
            throw new Error(`No table named ${table} found.`);
        }
        return selection;
    });
}

export async function connectClient(table: string, client: MosaicClient) {
    return withTableCoordinator(table, async (coordinator: TableCoordinator) => {
        coordinator.connectClient(client);
    });
}

async function withTableCoordinator<T = void>(
    table: string,
    fn: (coordinator: TableCoordinator) => Promise<T>
) {
    const coordinator = await tableCoordinator();
    await coordinator.waitForTable(table);
    return await fn(coordinator);
}
