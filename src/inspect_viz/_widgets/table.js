// js/coordinator/coodinator.ts
import {
  wasmConnector
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import {
  InstantiateContext
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm";

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
  const logger = new ConsoleLogger(LogLevel.INFO);
  const db = new AsyncDuckDB(logger, worker);
  await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
  URL.revokeObjectURL(worker_url);
  return db;
}

// js/util/wait.ts
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// js/coordinator/coodinator.ts
var VizCoordinator = class {
  constructor(conn_) {
    this.conn_ = conn_;
    this.tables_ = /* @__PURE__ */ new Set();
    this.ctx_ = new InstantiateContext();
    this.ctx_.coordinator.databaseConnector(wasmConnector({ connection: this.conn_ }));
  }
  getParams() {
    return this.ctx_.activeParams;
  }
  getParam(name) {
    return this.ctx_.activeParams.get(name);
  }
  async addData(id, buffer) {
    await this.conn_?.insertArrowFromIPCStream(buffer, {
      name: id,
      create: true
    });
    this.tables_.add(id);
  }
  async waitForData(id) {
    while (true) {
      if (this.tables_.has(id)) {
        return;
      } else {
        await sleep(100);
      }
    }
  }
  getInstantiateContext() {
    return this.ctx_;
  }
  async connectClient(client) {
    this.ctx_.coordinator.connect(client);
  }
};
var VIZ_COORDINATOR_KEY = Symbol.for("@@inspect-viz-coordinator");
async function vizCoordinator() {
  const globalScope = typeof window !== "undefined" ? window : globalThis;
  if (!globalScope[VIZ_COORDINATOR_KEY]) {
    globalScope[VIZ_COORDINATOR_KEY] = (async () => {
      const duckdb = await initDuckdb();
      const conn = await duckdb.connect();
      return new VizCoordinator(conn);
    })();
  }
  return globalScope[VIZ_COORDINATOR_KEY];
}

// js/widgets/table.ts
import { Table } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-inputs@0.16.2/+esm";
async function render({ model, el }) {
  const df_id = model.get("df_id");
  const selection = model.get("selection");
  const coordinator = await vizCoordinator();
  await coordinator.waitForData(df_id);
  const sel = coordinator.getParam(selection);
  if (sel === void 0) {
    throw new Error("You must pass a selection to tables.");
  }
  const view = new Table({ element: el, from: df_id, filterBy: sel });
  await coordinator.connectClient(view);
}
var table_default = { render };
export {
  table_default as default
};
