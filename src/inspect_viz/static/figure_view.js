// js/coordinator/coodinator.ts
import {
  Coordinator,
  wasmConnector,
  Selection,
  Param
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

// js/coordinator/dataframe.ts
var DataFrame = class {
  constructor(table, queries, params, selection) {
    this.table = table;
    this.queries = queries;
    this.params = params;
    this.selection = selection;
  }
};

// js/coordinator/coodinator.ts
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
    const params = /* @__PURE__ */ new Map();
    for (const query of queries) {
      for (const p of Object.values(query.parameters)) {
        params.set(p.name, Param.value(p.value));
      }
    }
    this.dfs_.set(id, new DataFrame(id, queries, params, Selection.intersect()));
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

// js/clients/figure_view.ts
import {
  MosaicClient as MosaicClient2,
  toDataColumns
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import { SelectQuery } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm";
import Plotly from "https://esm.sh/plotly.js-dist-min@3.0.1";
var FigureView = class extends MosaicClient2 {
  constructor(el_, table_, figure_, filterBy) {
    super(filterBy);
    this.el_ = el_;
    this.table_ = table_;
    this.figure_ = figure_;
  }
  query(filter = []) {
    return SelectQuery.select("*").from(this.table_).where(filter);
  }
  queryResult(data) {
    const columns = toDataColumns(data).columns;
    const table = bindTable(this.figure_.data, columns);
    Plotly.react(this.el_, table, this.figure_.layout, this.figure_.config);
    return this;
  }
};
function bindTable(traces, columns) {
  traces = structuredClone(traces);
  traces.forEach((trace) => {
    const mapping = columnMapping(trace, Object.keys(columns));
    for (const [attr, col] of Object.entries(mapping)) {
      const arr = columns[col];
      if (arr) {
        setData(trace, attr.split("."), arr);
      } else {
        console.warn(`Column "${col}" not found in table`);
      }
    }
  });
  return traces;
}
function columnMapping(trace, cols) {
  const map = {};
  const lc = cols.map((c) => c.toLowerCase());
  for (const p of arrayProps(trace)) {
    const simple = p.split(".").pop().toLowerCase();
    const i2 = lc.indexOf(simple);
    if (i2 === -1) continue;
    const exists = p.split(".").reduce((o, k) => o?.[k], trace) !== void 0;
    if (exists) map[p] = cols[i2];
  }
  const used = new Set(Object.values(map));
  const unused = cols.filter((c) => !used.has(c));
  let i = 0;
  const needsX = !map.x && (!isOrientable(trace) || trace.orientation !== "h");
  const needsY = !map.y && (isOrientable(trace) && trace.orientation === "h" ? false : true);
  if (needsX && unused[i]) {
    map.x = unused[i++];
  }
  if (needsY && unused[i]) {
    map.y = unused[i++];
  }
  const is3d = ["scatter3d", "surface", "mesh3d"].includes(trace.type ?? "");
  if (is3d && !map.z && unused[i]) {
    map.z = unused[i++];
  }
  return map;
}
function setData(trace, path, val) {
  const last = path.pop();
  let cur = trace;
  for (const k of path) {
    if (cur[k] == null || typeof cur[k] !== "object") cur[k] = {};
    cur = cur[k];
  }
  cur[last] = val;
}
function arrayProps(obj, prefix = "") {
  return Object.entries(obj).flatMap(
    ([k, v]) => Array.isArray(v) || ArrayBuffer.isView(v) ? [`${prefix}${k}`] : typeof v === "object" && v !== null ? arrayProps(v, `${prefix}${k}.`) : []
  );
}
function isOrientable(t) {
  return "orientation" in t;
}

// js/widgets/figure_view.ts
async function render({ model, el }) {
  const df_id = model.get("df_id");
  const figure_json = model.get("figure_json");
  const figure = JSON.parse(figure_json);
  const coordinator = await dataFrameCoordinator();
  const df = await coordinator.getDataFrame(df_id);
  const view = new FigureView(el, df.table, figure, df.selection);
  await coordinator.connectClient(view);
}
var figure_view_default = { render };
export {
  figure_view_default as default
};
