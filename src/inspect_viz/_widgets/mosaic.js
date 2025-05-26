// js/widgets/mosaic.ts
import {
  parseSpec
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm";

// js/context/index.ts
import { wasmConnector } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import { InstantiateContext } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm";

// js/context/duckdb.ts
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
      console.log(
        `Table ${table} not yet available, trying again in ${interval}ms (error: ${err})`
      );
    }
    if (performance.now() - t0 > timeout) {
      throw new Error(`Timed out waiting for table "${table}"`);
    }
    await new Promise((r) => setTimeout(r, interval));
  }
}

// js/context/index.ts
var VizContext = class extends InstantiateContext {
  constructor(conn_) {
    super();
    this.conn_ = conn_;
    this.tables_ = /* @__PURE__ */ new Set();
    this.coordinator.databaseConnector(wasmConnector({ connection: this.conn_ }));
  }
  async insertTable(table, data) {
    await this.conn_?.insertArrowFromIPCStream(data, {
      name: table,
      create: true
    });
    this.tables_.add(table);
  }
  async waitForTable(table) {
    await waitForTable(this.conn_, table);
  }
};
var VIZ_CONTEXT_KEY = Symbol.for("@@inspect-viz-context");
async function vizContext() {
  const globalScope = typeof window !== "undefined" ? window : globalThis;
  if (!globalScope[VIZ_CONTEXT_KEY]) {
    globalScope[VIZ_CONTEXT_KEY] = (async () => {
      const duckdb = await initDuckdb();
      const conn = await duckdb.connect();
      return new VizContext(conn);
    })();
  }
  return globalScope[VIZ_CONTEXT_KEY];
}

// js/widgets/mosaic.ts
async function render({ model, el }) {
  const tables = model.get("tables") || {};
  const spec_json = model.get("spec");
  const ctx = await vizContext();
  for (const [tableName, base64Data] of Object.entries(tables)) {
    if (base64Data) {
      const binaryString = atob(base64Data);
      const bytes = new Uint8Array(binaryString.length);
      for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      await ctx.insertTable(tableName, bytes);
    } else {
      await ctx.waitForTable(tableName);
    }
  }
  const spec = JSON.parse(spec_json);
  const ast = parseSpec(spec);
  const domResult = await astToDOM(ast, ctx);
  el.appendChild(domResult.element);
}
var mosaic_default = { render };
async function astToDOM(ast, ctx) {
  for (const [name, node] of Object.entries(ast.params)) {
    if (!ctx.activeParams.has(name)) {
      const param = node.instantiate(ctx);
      ctx.activeParams.set(name, param);
    }
  }
  return {
    element: ast.root.instantiate(ctx),
    params: ctx.activeParams
  };
}
export {
  mosaic_default as default
};
