import { AsyncDuckDBConnection } from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm';

import { wasmConnector } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

import { InstantiateContext } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm';

import { initDuckdb } from './duckdb';
import { sleep } from '../util/wait';

class VizContext extends InstantiateContext {
    private readonly tables_ = new Set<string>();

    constructor(private readonly conn_: AsyncDuckDBConnection) {
        super();
        this.coordinator.databaseConnector(wasmConnector({ connection: this.conn_ }));
    }

    async addData(id: string, buffer: Uint8Array) {
        // insert table into database
        await this.conn_?.insertArrowFromIPCStream(buffer, {
            name: id,
            create: true,
        });

        // add to list of tables
        this.tables_.add(id);
    }

    async waitForData(id: string) {
        // at startup we can't control the order of df producing and df consuming
        // widgets, so we may need to wait and retry for the data frame
        while (true) {
            if (this.tables_.has(id)) {
                return;
            } else {
                await sleep(100);
            }
        }
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
