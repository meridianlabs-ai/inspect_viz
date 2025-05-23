// js/coordinator/coodinator.ts
import {
  wasmConnector,
  Selection,
  Param
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import { InstantiateContext } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm";

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

// js/coordinator/dataframe.ts
var DataFrame = class {
  constructor(table, selection) {
    this.table = table;
    this.selection = selection;
  }
};

// js/util/wait.ts
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// js/coordinator/coodinator.ts
var VizCoordinator = class {
  constructor(conn_) {
    this.conn_ = conn_;
    this.dfs_ = /* @__PURE__ */ new Map();
    this.ctx_ = new InstantiateContext();
    this.ctx_.coordinator.databaseConnector(wasmConnector({ connection: this.conn_ }));
  }
  addParams(params) {
    for (const param of params) {
      this.addParam(param.id, param.default);
    }
  }
  getParams() {
    return this.ctx_.activeParams;
  }
  addParam(name, value) {
    if (!this.ctx_.activeParams.has(name)) {
      this.ctx_.activeParams.set(name, Param.value(value));
    }
    return this.ctx_.activeParams.get(name);
  }
  getParam(name) {
    return this.ctx_.activeParams.get(name);
  }
  async addDataFrame(id, buffer) {
    await this.conn_?.insertArrowFromIPCStream(buffer, {
      name: id,
      create: true
    });
    const df = new DataFrame(id, Selection.intersect());
    this.dfs_.set(id, df);
  }
  async getDataFrame(id) {
    while (true) {
      const df = this.dfs_.get(id);
      if (df) {
        return df;
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

// js/clients/table.ts
import { Table as MosaicTable } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-inputs@0.16.2/+esm";
var Table = class extends MosaicTable {
  constructor(el, table, filterBy, params_) {
    super({ element: el, filterBy, from: table });
    this.params_ = params_;
    this.params_.forEach((value) => {
      value.addEventListener("value", () => this.requestUpdate());
    });
  }
};

// js/widgets/table.ts
async function render({ model, el }) {
  const df_id = model.get("df_id");
  const coordinator = await vizCoordinator();
  const df = await coordinator.getDataFrame(df_id);
  coordinator.addParams(JSON.parse(model.get("params")));
  const view = new Table(el, df.table, df.selection, coordinator.getParams());
  await coordinator.connectClient(view);
}
var table_default = { render };
export {
  table_default as default
};
