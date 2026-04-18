import { AsyncDuckDBConnection } from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm';

import { wasmConnector } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

import { InstantiateContext } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm';

import { INPUTS } from '../inputs';
import { initDuckdb, waitForTable } from './duckdb';
import { ErrorInfo, initializeErrorHandling } from '../util/errors.js';
import { sleep } from '../util/async.js';

class VizContext extends InstantiateContext {
    private readonly tables_ = new Set<string>();
    private unhandledErrors_: ErrorInfo[] = [];

    constructor(
        private readonly conn_: AsyncDuckDBConnection,
        plotDefaults: any[]
    ) {
        super({ plotDefaults });
        this.api = { ...this.api, ...INPUTS };
        this.coordinator.databaseConnector(wasmConnector({ connection: this.conn_ }));
    }

    async insertTable(table: string, data: Uint8Array) {
        // just wait for it if we already have it
        if (this.tables_.has(table)) {
            await this.waitForTable(table);
            return;
        }

        // add to list of tables
        this.tables_.add(table);

        // insert table into database
        await this.conn_?.insertArrowFromIPCStream(data, {
            name: table,
            create: true,
        });
    }

    async waitForTable(table: string) {
        await waitForTable(this.conn_, table);
    }

    recordUnhandledError(error: ErrorInfo) {
        this.unhandledErrors_.push(error);
    }

    async collectUnhandledError(wait: number = 1000): Promise<ErrorInfo | undefined> {
        const startTime = Date.now();
        while (Date.now() - startTime < wait) {
            if (this.unhandledErrors_.length > 0) {
                return this.unhandledErrors_.shift();
            }
            await sleep(100);
        }
        return undefined;
    }

    /**
     * Like `collectUnhandledError`, but exits early when `isResolved()` becomes
     * true — used by the per-empty-plot error display so a successful render
     * doesn't keep us polling for an error that won't arrive.
     */
    async collectUnhandledErrorUntil(
        isResolved: () => boolean,
        wait: number = 1000
    ): Promise<ErrorInfo | undefined> {
        const startTime = Date.now();
        // Order matters: check the predicate first so a div that's already
        // populated returns immediately on the first iteration.
        while (Date.now() - startTime < wait) {
            if (isResolved()) return undefined;
            if (this.unhandledErrors_.length > 0) {
                return this.unhandledErrors_.shift();
            }
            await sleep(100);
        }
        return undefined;
    }

    clearUnhandledErrors() {
        this.unhandledErrors_ = [];
    }
}

// get the global context instance, ensuring we get the same
// instance eval across different js bundles loaded into the page
const VIZ_CONTEXT_KEY = Symbol.for('@@inspect-viz-context');
async function vizContext(plotDefaults: any[]): Promise<VizContext> {
    const globalScope: any = typeof window !== 'undefined' ? window : globalThis;
    if (!globalScope[VIZ_CONTEXT_KEY]) {
        globalScope[VIZ_CONTEXT_KEY] = (async () => {
            const { db, worker } = await initDuckdb();
            const conn = await db.connect();
            const ctx = new VizContext(conn, plotDefaults);
            initializeErrorHandling(ctx, worker);
            return ctx;
        })();
    }
    return globalScope[VIZ_CONTEXT_KEY] as Promise<VizContext>;
}

export { VizContext, vizContext };
