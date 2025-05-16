
import { getJsDelivrBundles, selectBundle, AsyncDuckDB, ConsoleLogger } from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm'

export async function initDuckdb() {

    const JSDELIVR_BUNDLES = getJsDelivrBundles();

    // Select a bundle based on browser checks
    const bundle = await selectBundle(JSDELIVR_BUNDLES);

    const worker_url = URL.createObjectURL(
    new Blob([`importScripts("${bundle.mainWorker!}");`], {type: 'text/javascript'})
    );

    // Instantiate the asynchronous version of DuckDB-wasm
    const worker = new Worker(worker_url);
    const logger = new ConsoleLogger();
    const db = new AsyncDuckDB(logger, worker);
    await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
    URL.revokeObjectURL(worker_url);
    
    return db;
}

