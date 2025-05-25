// js/widgets/mosaic.ts
import {
  parseSpec
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm";

// js/coordinator/coodinator.ts
import {
  wasmConnector
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

// js/widgets/mosaic.ts
async function render({ model, el }) {
  const df_id = model.get("df_id");
  const df_buffer = model.get("df_buffer");
  const spec_json = model.get("spec");
  const coordinator = await vizCoordinator();
  if (df_id) {
    if (df_buffer && df_buffer.byteLength > 0) {
      const arrowBuffer = new Uint8Array(
        df_buffer.buffer,
        df_buffer.byteOffset,
        df_buffer.byteLength
      );
      await coordinator.addData(df_id, arrowBuffer);
    } else {
      await coordinator.waitForData(df_id);
    }
  }
  const spec = JSON.parse(spec_json);
  const ast = parseSpec(spec);
  const domResult = await astToDOM(ast, coordinator.getInstantiateContext());
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
