import { AsyncDuckDBConnection } from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm';

import { decodeIPC } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

import { InstantiateContext } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm';

import { INPUTS } from '../inputs';
import { initDuckdb, waitForTable } from './duckdb';
import { ErrorInfo, initializeErrorHandling } from '../util/errors.js';
import { sleep } from '../util/async.js';

// The DuckDB database. Documents that opt in share one (see `runtimeScope`);
// each document still has its own VizContext, so its coordinator, params,
// selections and inputs are built in its own window.
interface Runtime {
    conn: AsyncDuckDBConnection;
    worker: Worker;
    // each table's insert, awaited by every document that needs the table
    tables: Map<string, Promise<void>>;
    insert: (table: string, data: Uint8Array) => Promise<void>;
    runQuery: (sql: string) => Promise<Uint8Array>;
}

class VizContext extends InstantiateContext {
    private unhandledErrors_: ErrorInfo[] = [];

    constructor(
        private readonly runtime_: Runtime,
        plotDefaults: any[]
    ) {
        super({ plotDefaults });
        this.api = { ...this.api, ...INPUTS };
        this.coordinator.databaseConnector({
            query: (query: { type?: string; sql: string }) => this.query(query),
        });
    }

    // mosaic-core's wasmConnector, except that the result bytes are viewed
    // through this window's Uint8Array: the decoder's instanceof check fails
    // on bytes created in the window that owns the database
    private async query(query: { type?: string; sql: string }) {
        const bytes = await this.runtime_.runQuery(query.sql);
        const local = new Uint8Array(bytes.buffer, bytes.byteOffset, bytes.byteLength);
        return query.type === 'exec'
            ? undefined
            : query.type === 'arrow'
              ? decodeIPC(local)
              : decodeIPC(local).toArray();
    }

    async insertTable(table: string, data: Uint8Array) {
        // just wait for it if we already have it
        const pending = this.runtime_.tables.get(table);
        if (pending) {
            await pending;
            return;
        }

        // insert table into database; a failed insert is retried by the next caller
        const insert = this.runtime_.insert(table, data);
        this.runtime_.tables.set(table, insert);
        try {
            await insert;
        } catch (error) {
            this.runtime_.tables.delete(table);
            throw error;
        }
    }

    async waitForTable(table: string) {
        await waitForTable(this.runtime_.conn, table);
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
     *
     * Polls at 25ms (vs the 100ms used by `collectUnhandledError`) because
     * the success-case latency between Mosaic populating a div and us
     * noticing is on the user-perceived critical path.
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
            await sleep(25);
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
const RUNTIME_KEY = Symbol.for('@@inspect-viz-runtime');
const SHARED_CONTEXT_ATTR = 'data-iv-shared-context';

// The window that holds the database: this one, or with the shared-context
// attribute on <html>, the topmost same-origin ancestor so that same-origin
// iframes share one DuckDB runtime. The first document to start the
// database owns its worker, which dies with that document.
function runtimeScope(): Window | typeof globalThis {
    if (typeof window === 'undefined') {
        return globalThis;
    }
    if (!document.documentElement.hasAttribute(SHARED_CONTEXT_ATTR)) {
        return window;
    }
    let scope: Window = window;
    try {
        while (scope.parent !== scope && scope.parent.document) {
            scope = scope.parent;
        }
    } catch {
        // a cross-origin parent or a detached frame throws: stop at the last same-origin window
    }
    return scope;
}

async function initRuntime(): Promise<Runtime> {
    const { db, worker } = await initDuckdb();
    const conn = await db.connect();
    const insert = async (table: string, data: Uint8Array) => {
        await conn.insertArrowFromIPCStream(data, { name: table, create: true });
    };
    // Arrow IPC bytes straight from the bindings, as mosaic-core's wasmConnector does
    const runQuery = (sql: string) =>
        conn.useUnsafe((bindings, handle) => bindings.runQuery(handle, sql));
    return { conn, worker, tables: new Map<string, Promise<void>>(), insert, runQuery };
}

async function vizContext(plotDefaults: any[]): Promise<VizContext> {
    const globalScope: any = typeof window !== 'undefined' ? window : globalThis;
    if (!globalScope[VIZ_CONTEXT_KEY]) {
        const scope: any = runtimeScope();
        if (!scope[RUNTIME_KEY]) {
            const runtime = initRuntime();
            scope[RUNTIME_KEY] = runtime;
            const forget = () => {
                if (scope[RUNTIME_KEY] === runtime) {
                    delete scope[RUNTIME_KEY];
                }
            };
            // a failed start is retried by the next document
            runtime.catch(forget);
            // the worker dies with this document: let later documents start afresh
            globalScope.addEventListener?.('pagehide', (event: PageTransitionEvent) => {
                if (!event.persisted) {
                    forget();
                }
            });
        }
        globalScope[VIZ_CONTEXT_KEY] = (async () => {
            const runtime = (await scope[RUNTIME_KEY]) as Runtime;
            const ctx = new VizContext(runtime, plotDefaults);
            initializeErrorHandling(ctx, runtime.worker);
            return ctx;
        })();
    }
    return globalScope[VIZ_CONTEXT_KEY] as Promise<VizContext>;
}

export { VizContext, vizContext };
