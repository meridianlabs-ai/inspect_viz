

const duckdb = await import('https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.1-dev132.0/+esm')


// import { Query } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.15.0/+esm'

// import { MosaicClient } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.15.0/+esm'

const JSDELIVR_BUNDLES = duckdb.getJsDelivrBundles();

const initDuckDB = async () => {
    // Select a bundle based on browser checks
    const bundle = await duckdb.selectBundle(JSDELIVR_BUNDLES);

    const worker_url = URL.createObjectURL(
    new Blob([`importScripts("${bundle.mainWorker!}");`], {type: 'text/javascript'})
    );

    // Instantiate the asynchronous version of DuckDB-wasm
    const worker = new Worker(worker_url);
    const logger = new duckdb.ConsoleLogger();
    const db = new duckdb.AsyncDuckDB(logger, worker);
    await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
    URL.revokeObjectURL(worker_url);
    console.log(await db.getVersion())
    
}

export { initDuckDB }
