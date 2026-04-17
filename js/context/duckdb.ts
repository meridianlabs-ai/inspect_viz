import {
    getJsDelivrBundles,
    selectBundle,
    AsyncDuckDB,
    ConsoleLogger,
    AsyncDuckDBConnection,
    LogLevel,
} from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm';
import { sleep } from '../util/async';

// IndexedDB-backed cache for the compiled DuckDB-WASM module. Keyed by the
// wasm URL (which includes the version), so bumping DuckDB-WASM invalidates
// the cache automatically. Content is a `WebAssembly.Module`, which is
// structured-cloneable in modern browsers — repeat visits skip the ~500ms
// compile entirely.
const WASM_CACHE_DB = 'inspect-viz';
const WASM_CACHE_STORE = 'wasm-modules';

function openWasmCacheDb(): Promise<IDBDatabase> {
    return new Promise<IDBDatabase>((resolve, reject) => {
        // Some sandboxed contexts (notably `file://` in Playwright) let
        // indexedDB.open() hang forever — neither onsuccess nor onerror
        // ever fires — which would deadlock our init. Cap it at 1 s and
        // fall through to the no-cache path.
        const timer = setTimeout(
            () => reject(new Error('indexedDB.open timeout')),
            1000
        );
        const req = indexedDB.open(WASM_CACHE_DB, 1);
        req.onupgradeneeded = () =>
            req.result.createObjectStore(WASM_CACHE_STORE);
        req.onsuccess = () => {
            clearTimeout(timer);
            resolve(req.result);
        };
        req.onerror = () => {
            clearTimeout(timer);
            reject(req.error);
        };
    });
}

function idbGet<T>(db: IDBDatabase, key: string): Promise<T | undefined> {
    return new Promise<T | undefined>((resolve, reject) => {
        const req = db
            .transaction(WASM_CACHE_STORE, 'readonly')
            .objectStore(WASM_CACHE_STORE)
            .get(key);
        req.onsuccess = () => resolve(req.result as T | undefined);
        req.onerror = () => reject(req.error);
    });
}

function idbPut(db: IDBDatabase, key: string, value: unknown): Promise<void> {
    return new Promise<void>((resolve, reject) => {
        const tx = db.transaction(WASM_CACHE_STORE, 'readwrite');
        tx.objectStore(WASM_CACHE_STORE).put(value, key);
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
    });
}

function withTimeout<T>(p: Promise<T>, ms: number, label: string): Promise<T> {
    return Promise.race([
        p,
        new Promise<T>((_, reject) =>
            setTimeout(() => reject(new Error(`${label} timeout`)), ms)
        ),
    ]);
}

// Origins where IndexedDB is unreliable — notably `file://` (as used by
// Playwright for headless PNG rendering) can have IDB requests that hang
// with no error callback. Skip the cache there and go straight to
// fetch+compile so the render path can never deadlock on IDB.
function idbAvailable(): boolean {
    try {
        const proto = typeof location !== 'undefined' ? location.protocol : '';
        if (proto === 'file:') return false;
        return typeof indexedDB !== 'undefined';
    } catch {
        return false;
    }
}

async function getOrCompileWasmModule(url: string): Promise<WebAssembly.Module> {
    // Cache lookup is best-effort; time-box each step and fall through to
    // fetch + compile on any hiccup.
    let db: IDBDatabase | undefined;
    if (idbAvailable()) {
        try {
            db = await withTimeout(openWasmCacheDb(), 1000, 'IDB open');
            const cached = await withTimeout(
                idbGet<WebAssembly.Module>(db, url),
                1000,
                'IDB get'
            );
            if (cached) return cached;
        } catch {
            // IDB unavailable / slow / broken — fall through
        }
    }

    // compileStreaming wants `Content-Type: application/wasm`; if a server
    // doesn't serve that, fall back to buffer + compile.
    const resp = await fetch(url);
    let mod: WebAssembly.Module;
    try {
        mod = await WebAssembly.compileStreaming(resp.clone());
    } catch {
        mod = await WebAssembly.compile(await resp.arrayBuffer());
    }

    // Fire-and-forget the cache write. If it hangs or errors, we don't care —
    // the module is already compiled and ready to return.
    if (db) {
        withTimeout(idbPut(db, url, mod), 2000, 'IDB put').catch(() => {
            /* quota / structured-clone / hung — non-fatal */
        });
    }
    return mod;
}

export async function initDuckdb() {
    const JSDELIVR_BUNDLES = getJsDelivrBundles();

    // Select a bundle based on browser checks
    const bundle = await selectBundle(JSDELIVR_BUNDLES);

    const worker_url = URL.createObjectURL(
        new Blob([`importScripts("${bundle.mainWorker!}");`], {
            type: 'text/javascript',
        })
    );

    // Instantiate the asynchronous version of DuckDB-wasm
    const worker = new Worker(worker_url);
    const logger = new ConsoleLogger(LogLevel.WARNING);
    const db = new AsyncDuckDB(logger, worker);

    if (idbAvailable()) {
        // http(s) origin: compile on the main thread so we can cache the
        // compiled WebAssembly.Module in IndexedDB across visits. Repeat
        // visits skip the ~500ms compile entirely.
        try {
            const mainModule = await getOrCompileWasmModule(bundle.mainModule);
            await db.instantiate(
                mainModule as unknown as string,
                bundle.pthreadWorker
            );
            URL.revokeObjectURL(worker_url);
            return { db, worker };
        } catch {
            // If the main-thread path fails unexpectedly, fall through to
            // the stock URL-based init so we never regress.
        }
    }

    // file:// / Playwright / no-IDB fallback: let DuckDB-WASM fetch + compile
    // the wasm inside its worker as it always has. No compile caching, but
    // guaranteed to work.
    await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
    URL.revokeObjectURL(worker_url);
    return { db, worker };
}

export async function waitForTable(
    conn: AsyncDuckDBConnection,
    table: string,
    { interval = 250 } = {}
) {
    while (true) {
        try {
            const res = await conn.query(
                `SELECT 1
           FROM information_schema.tables
         WHERE table_schema = 'main'
           AND table_name   = '${table}'
         LIMIT 1`
            );

            if (res.numRows) return; // success ✨
        } catch (err) {
            console.log(
                `Table ${table} not yet available, trying again in ${interval}ms (error: ${err})`
            );
        }

        await sleep(interval);
    }
}
