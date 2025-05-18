// js/coordinator/coodinator.ts
import {
  Coordinator,
  wasmConnector,
  Selection
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";

// js/coordinator/duckdb.ts
import {
  getJsDelivrBundles,
  selectBundle,
  AsyncDuckDB,
  ConsoleLogger,
  LogLevel
} from "https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm";
async function initDuckdb() {
  const JSDELIVR_BUNDLES = getJsDelivrBundles();
  const bundle = await selectBundle(JSDELIVR_BUNDLES);
  const worker_url = URL.createObjectURL(
    new Blob([`importScripts("${bundle.mainWorker}");`], {
      type: "text/javascript"
    })
  );
  const worker = new Worker(worker_url);
  const logger = new ConsoleLogger(LogLevel.WARNING);
  const db = new AsyncDuckDB(logger, worker);
  await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
  URL.revokeObjectURL(worker_url);
  return db;
}
async function waitForTable(conn, table, { timeout = 1e4, interval = 250 } = {}) {
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
      if (res.numRows) return;
    } catch (err) {
    }
    if (performance.now() - t0 > timeout) {
      throw new Error(`Timed out waiting for table "${table}"`);
    }
    await new Promise((r) => setTimeout(r, interval));
  }
}

// js/coordinator/coodinator.ts
var DataFrame = class {
  constructor(table, queries, params, selection) {
    this.table = table;
    this.queries = queries;
    this.params = params;
    this.selection = selection;
  }
};
var DataFrameCoordinator = class {
  constructor(conn_) {
    this.conn_ = conn_;
    this.dfs_ = /* @__PURE__ */ new Map();
    this.coordinator_ = new Coordinator();
    this.coordinator_.databaseConnector(wasmConnector({ connection: this.conn_ }));
  }
  async addDataFrame(id, buffer, queries) {
    await this.conn_?.insertArrowFromIPCStream(buffer, {
      name: id,
      create: true
    });
    this.dfs_.set(id, new DataFrame(id, queries, {}, Selection.intersect()));
  }
  async getDataFrame(id) {
    await waitForTable(this.conn_, id);
    return this.dfs_.get(id);
  }
  async connectClient(client) {
    this.coordinator_.connect(client);
  }
};
var REACTIVE_DF_COORDINATOR_KEY = Symbol.for("@@reactive-df-coordinator");
async function dataFrameCoordinator() {
  const globalScope = typeof window !== "undefined" ? window : globalThis;
  if (!globalScope[REACTIVE_DF_COORDINATOR_KEY]) {
    globalScope[REACTIVE_DF_COORDINATOR_KEY] = (async () => {
      const duckdb = await initDuckdb();
      const conn = await duckdb.connect();
      return new DataFrameCoordinator(conn);
    })();
  }
  return globalScope[REACTIVE_DF_COORDINATOR_KEY];
}

// js/clients/table_view.ts
import { Table } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-inputs@0.16.2/+esm";
var TableView = class extends Table {
  constructor(el, table, filterBy) {
    super({ element: el, filterBy, from: table });
  }
};

// js/widgets/table_view.ts
async function render({ model, el }) {
  const df_id = model.get("df_id");
  const coordinator = await dataFrameCoordinator();
  const df = await coordinator.getDataFrame(df_id);
  const view = new TableView(el, df.table, df.selection);
  await coordinator.connectClient(view);
}
var table_view_default = { render };
export {
  table_view_default as default
};
