// js/coordinator/duckdb.ts
async function initDuckdb() {
  const duckdb = await import("https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm");
  const JSDELIVR_BUNDLES = duckdb.getJsDelivrBundles();
  const bundle = await duckdb.selectBundle(JSDELIVR_BUNDLES);
  const worker_url = URL.createObjectURL(
    new Blob([`importScripts("${bundle.mainWorker}");`], { type: "text/javascript" })
  );
  const worker = new Worker(worker_url);
  const logger = new duckdb.ConsoleLogger();
  const db = new duckdb.AsyncDuckDB(logger, worker);
  await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
  URL.revokeObjectURL(worker_url);
  return db;
}

// js/coordinator/index.ts
var TableCoordinator = class {
  async initialize() {
    const mosaic = await import("https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm");
    this.duckdb_ = await initDuckdb();
    this.conn_ = await this.duckdb_?.connect();
    this.coordinator_ = new mosaic.Coordinator();
    this.coordinator_.databaseConnector(mosaic.wasmConnector({ connection: this.conn_ }));
  }
  async addTable(name, buffer) {
    await this.conn_?.insertArrowFromIPCStream(buffer, { name, create: true });
  }
  connectClient(client) {
    this.coordinator_?.connect(client);
  }
};
var TABLE_COORDINATOR_KEY = Symbol.for("@@table-coordinator");
async function tableCoordinator() {
  const globalScope = typeof window !== "undefined" ? window : globalThis;
  if (!globalScope[TABLE_COORDINATOR_KEY]) {
    console.log("creating coordinator");
    const coordinator = new TableCoordinator();
    await coordinator.initialize();
    globalScope[TABLE_COORDINATOR_KEY] = coordinator;
  }
  return globalScope[TABLE_COORDINATOR_KEY];
}
async function addTable(name, buffer) {
  console.log("adding table");
  const coordinator = await tableCoordinator();
  await coordinator.addTable(name, buffer);
  console.log("table added");
}

// js/shared_df.ts
async function render({ model }) {
  const id = model.get("id");
  const buffer = model.get("buffer");
  const arrowBuffer = new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength);
  await addTable(id, arrowBuffer);
}
var shared_df_default = { render };
export {
  shared_df_default as default
};
