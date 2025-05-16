// js/coordinator/index.ts
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

// js/coordinator/index.ts
var TableCoordinator = class {
  constructor(conn_) {
    this.conn_ = conn_;
    this.coordinator_ = new Coordinator();
    this.coordinator_.databaseConnector(wasmConnector({ connection: this.conn_ }));
    this.selections_ = /* @__PURE__ */ new Map();
  }
  async addTable(table, buffer) {
    await this.conn_?.insertArrowFromIPCStream(buffer, {
      name: table,
      create: true
    });
    this.selections_.set(table, Selection.intersect());
  }
  async waitForTable(table) {
    await waitForTable(this.conn_, table);
  }
  tableSelection(table) {
    return this.selections_.get(table);
  }
  connectClient(client) {
    this.coordinator_?.connect(client);
  }
};
var TABLE_COORDINATOR_KEY = Symbol.for("@@table-coordinator");
async function tableCoordinator() {
  const globalScope = typeof window !== "undefined" ? window : globalThis;
  if (!globalScope[TABLE_COORDINATOR_KEY]) {
    globalScope[TABLE_COORDINATOR_KEY] = (async () => {
      const duckdb = await initDuckdb();
      const conn = await duckdb.connect();
      return new TableCoordinator(conn);
    })();
  }
  return globalScope[TABLE_COORDINATOR_KEY];
}
async function tableSelection(table) {
  return withTableCoordinator(table, async (coordinator) => {
    const selection = coordinator.tableSelection(table);
    if (selection === void 0) {
      throw new Error(`No table named ${table} found.`);
    }
    return selection;
  });
}
async function connectClient(table, client) {
  return withTableCoordinator(table, async (coordinator) => {
    coordinator.connectClient(client);
  });
}
async function withTableCoordinator(table, fn) {
  const coordinator = await tableCoordinator();
  await coordinator.waitForTable(table);
  return await fn(coordinator);
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
  const table = model.get("table");
  const selection = await tableSelection(table);
  const view = new TableView(el, table, selection);
  await connectClient(table, view);
}
var table_view_default = { render };
export {
  table_view_default as default
};
