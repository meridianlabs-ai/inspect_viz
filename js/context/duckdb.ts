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
    const logger = new ConsoleLogger(LogLevel.WARNING);
    const db = new AsyncDuckDB(logger, worker);
    await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
    URL.revokeObjectURL(worker_url);

    return db;
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

        await new Promise(r => setTimeout(r, interval));
    }
}
