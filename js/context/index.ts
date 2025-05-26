import { AsyncDuckDBConnection } from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm';

import { wasmConnector } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

import { InstantiateContext } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm';

import { initDuckdb, waitForTable } from './duckdb';

class VizContext extends InstantiateContext {
    private readonly tables_ = new Set<string>();

    constructor(private readonly conn_: AsyncDuckDBConnection) {
        super();
        this.coordinator.databaseConnector(wasmConnector({ connection: this.conn_ }));
    }

    async insertTable(table: string, data: Uint8Array) {
        // insert table into database
        await this.conn_?.insertArrowFromIPCStream(data, {
            name: table,
            create: true,
        });

        // add to list of tables
        this.tables_.add(table);
    }

    async waitForTable(table: string) {
        await waitForTable(this.conn_, table);
    }
}

// get the global context instance, ensuring we get the same
// instance eval across different js bundles loaded into the page
const VIZ_CONTEXT_KEY = Symbol.for('@@inspect-viz-context');
async function vizContext(): Promise<VizContext> {
    const globalScope: any = typeof window !== 'undefined' ? window : globalThis;
    if (!globalScope[VIZ_CONTEXT_KEY]) {
        globalScope[VIZ_CONTEXT_KEY] = (async () => {
            const duckdb = await initDuckdb();
            const conn = await duckdb.connect();
            return new VizContext(conn);
        })();
    }
    return globalScope[VIZ_CONTEXT_KEY] as Promise<VizContext>;
}

export { VizContext, vizContext };
