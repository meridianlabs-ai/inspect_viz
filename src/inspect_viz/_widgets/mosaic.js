// js/widgets/mosaic.ts
import {
  parseSpec
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm";
import { throttle } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";

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
async function waitForTable(conn, table, { interval = 250 } = {}) {
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
    await new Promise((r) => setTimeout(r, interval));
  }
}

// js/inputs/input.ts
import {
  coordinator,
  MosaicClient
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
function input(InputClass, ...params) {
  const input2 = new InputClass(...params);
  coordinator().connect(input2);
  return input2.element;
}
var Input = class extends MosaicClient {
  constructor(filterBy, element, className = "input") {
    super(filterBy);
    this.element = element || document.createElement("div");
    if (className) this.element.setAttribute("class", className);
    Object.defineProperty(this.element, "value", { value: this });
  }
  activate() {
  }
};

// js/inputs/radio.ts
var Radio = class extends Input {
  constructor(options) {
    super(options.filterBy, options.element);
    const strongEl = window.document.createElement("strong");
    strongEl.innerText = "STRONG";
    this.element.appendChild(strongEl);
  }
};

// js/inputs/index.ts
var CUSTOM_INPUTS = {
  radio: (options) => input(Radio, options)
};

// js/context/index.ts
var VizContext = class extends InstantiateContext {
  constructor(conn_, plotDefaults) {
    super({
      plotDefaults
    });
    this.conn_ = conn_;
    this.tables_ = /* @__PURE__ */ new Set();
    this.api = { ...this.api, ...CUSTOM_INPUTS };
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
async function vizContext(plotDefaults) {
  const globalScope = typeof window !== "undefined" ? window : globalThis;
  if (!globalScope[VIZ_CONTEXT_KEY]) {
    globalScope[VIZ_CONTEXT_KEY] = (async () => {
      const duckdb = await initDuckdb();
      const conn = await duckdb.connect();
      return new VizContext(conn, plotDefaults);
    })();
  }
  return globalScope[VIZ_CONTEXT_KEY];
}

// js/widgets/mosaic.ts
async function render({ model, el }) {
  const spec = JSON.parse(model.get("spec"));
  const plotDefaultsSpec = { plotDefaults: spec.plotDefaults, vspace: 0 };
  const plotDefaultsAst = parseSpec(plotDefaultsSpec);
  const ctx = await vizContext(plotDefaultsAst.plotDefaults);
  const tables = model.get("tables") || {};
  await syncTables(ctx, tables);
  const renderOptions = renderSetup(el);
  const inputs = new Set(
    ["menu", "search", "slider", "table"].concat(Object.keys(CUSTOM_INPUTS))
  );
  if (renderOptions.autoFillScrolling && isOutputSpec(spec)) {
    el.style.width = "100%";
    el.style.height = "400px";
  }
  const renderSpec = async () => {
    const targetSpec = renderOptions.autoFill ? responsiveSpec(spec, el) : spec;
    const ast = parseSpec(targetSpec, { inputs });
    const specEl = await astToDOM(ast, ctx);
    el.innerHTML = "";
    el.appendChild(specEl);
  };
  await renderSpec();
  if (renderOptions.autoFill) {
    const resizeObserver = new ResizeObserver(throttle(renderSpec));
    resizeObserver.observe(el);
    return () => {
      resizeObserver.disconnect();
    };
  }
}
async function syncTables(ctx, tables) {
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
}
function renderSetup(containerEl) {
  const widgetEl = containerEl.closest(".widget-subarea");
  if (widgetEl) {
    widgetEl.style.marginBottom = "0";
  }
  const autoFill = window.document.body.classList.contains("quarto-dashboard");
  const autoFillScrolling = autoFill && !window.document.body.classList.contains("dashboard-fill");
  return { autoFill, autoFillScrolling };
}
function responsiveSpec(spec, containerEl) {
  spec = structuredClone(spec);
  if ("plot" in spec) {
    const plot = spec.plot[0];
    if ("width" in plot && "height" in plot) {
      plot.width = containerEl.clientWidth;
      plot.height = containerEl.clientHeight;
    }
  } else if ("hconcat" in spec && spec.hconcat.length === 2) {
    const hconcat = spec.hconcat;
    const plot = "plot" in hconcat[0] ? hconcat[0] : "plot" in hconcat[1] ? hconcat[1] : void 0;
    if (plot) {
      plot.width = containerEl.clientWidth - 80;
      plot.height = containerEl.clientHeight;
    }
  } else if ("vconcat" in spec && spec.vconcat.length == 2) {
    const vconcat = spec.vconcat;
    const plot = "plot" in vconcat[0] ? vconcat[0] : "plot" in vconcat[1] ? vconcat[1] : void 0;
    if (plot) {
      plot.width = containerEl.clientWidth;
      plot.height = containerEl.clientHeight - 35;
    }
  }
  return spec;
}
function isOutputSpec(spec) {
  if ("plot" in spec) {
    return true;
  } else if ("input" in spec && spec.input === "table") {
    return true;
  } else if ("hconcat" in spec && spec.hconcat.length === 2 && ("plot" in spec.hconcat[0] || "plot" in spec.hconcat[1])) {
    return true;
  } else if ("vconcat" in spec && spec.vconcat.length === 2 && ("plot" in spec.vconcat[0] || "plot" in spec.vconcat[1])) {
    return true;
  } else {
    return false;
  }
}
async function astToDOM(ast, ctx) {
  for (const [name, node] of Object.entries(ast.params)) {
    if (!ctx.activeParams.has(name)) {
      const param = node.instantiate(ctx);
      ctx.activeParams.set(name, param);
    }
  }
  return ast.root.instantiate(ctx);
}
var mosaic_default = { render };
export {
  mosaic_default as default
};
