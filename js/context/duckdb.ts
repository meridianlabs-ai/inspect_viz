import {
    getJsDelivrBundles,
    selectBundle,
    AsyncDuckDB,
    ConsoleLogger,
    AsyncDuckDBConnection,
    LogLevel,
} from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm';

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
    const logger = new ConsoleLogger(LogLevel.INFO);
    const db = new AsyncDuckDB(logger, worker);
    await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
    URL.revokeObjectURL(worker_url);

    return db;
}

export async function waitForTable(
    conn: AsyncDuckDBConnection,
    table: string,
    { timeout = 10_000, interval = 250 } = {}
) {
    const t0 = performance.now();

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
            /* Table or even the database file may not be ready yet.
         Ignore the error and keep polling. */
        }

        if (performance.now() - t0 > timeout) {
            throw new Error(`Timed out waiting for table "${table}"`);
        }
        await new Promise(r => setTimeout(r, interval));
    }
}
