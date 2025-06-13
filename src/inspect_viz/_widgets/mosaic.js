// js/widgets/mosaic.ts
import {
  parseSpec
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm";
import { throttle } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";

// js/context/index.ts
import { wasmConnector } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import { InstantiateContext } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm";

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

// js/util/modal.ts
var Modal = class _Modal {
  static {
    this.modalCSSInjected = false;
  }
  static show(options) {
    const { title = "Error", friendlyMessage, technicalMessage } = options;
    _Modal.ensureModalCSS();
    const modal = _Modal.createModal(friendlyMessage, technicalMessage, title);
    document.body.appendChild(modal);
    modal.offsetHeight;
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        modal.classList.add("inspect-viz-modal-show");
        _Modal.focusModal(modal);
      });
    });
  }
  static ensureModalCSS() {
    if (_Modal.modalCSSInjected || document.getElementById("inspect-viz-modal-css")) {
      return;
    }
    const style = document.createElement("style");
    style.id = "inspect-viz-modal-css";
    style.textContent = `
            .inspect-viz-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: flex-start;
                justify-content: center;
                padding-top: 60px;
                z-index: 10000;
                opacity: 0;
                visibility: hidden;
                transition: opacity 0.3s, visibility 0.3s;
            }
            
            .inspect-viz-modal-show {
                opacity: 1;
                visibility: visible;
            }
            
            .inspect-viz-modal-content {
                background: white;
                border-radius: 8px;
                padding: 24px;
                min-width: 600px;
                max-width: min(90vw, 1000px);
                width: auto;
                max-height: calc(100vh - 120px);
                overflow-y: auto;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
                position: relative;
                transform: translateY(-20px);
                transition: transform 0.3s ease-out;
            }
            
            .inspect-viz-modal-show .inspect-viz-modal-content {
                transform: translateY(0);
            }
            
            .inspect-viz-modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 16px;
                padding-bottom: 12px;
                border-bottom: 1px solid #e0e0e0;
            }

            .inspect-viz-modal-header h2 {
                border-bottom: none;
                padding-bottom: 0;
            }
            
            .inspect-viz-modal-title {
                font-size: 18px;
                font-weight: 600;
                color: #d32f2f;
                margin: 0;
                display: flex;
                align-items: center;
            }
            
            .inspect-viz-modal-icon {
                width: 20px;
                height: 20px;
                margin-right: 8px;
                fill: currentColor;
            }
            
            .inspect-viz-modal-close {
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
                padding: 0;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 4px;
                color: #666;
            }
            
            .inspect-viz-modal-close:hover {
                background: #f5f5f5;
            }
            
            .inspect-viz-modal-close:focus {
                outline: 2px solid #1976d2;
                outline-offset: 2px;
            }
            
            .inspect-viz-modal-body {
                margin-bottom: 20px;
            }
            
            .inspect-viz-modal-message {
                font-size: 14px;
                line-height: 1.5;
                color: #333;
                margin-bottom: 16px;
            }
            
            .inspect-viz-modal-details {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
            
            .inspect-viz-modal-details summary {
                padding: 8px 12px;
                cursor: pointer;
                font-size: 13px;
                color: #666;
                background: #f8f9fa;
                border-radius: 4px 4px 0 0;
            }
            
            .inspect-viz-modal-details summary:hover {
                background: #e9ecef;
            }
            
            .inspect-viz-modal-details[open] summary {
                border-bottom: 1px solid #e0e0e0;
                border-radius: 4px 4px 0 0;
            }
            
            .inspect-viz-modal-details pre {
                margin: 0;
                padding: 12px;
                font-size: 12px;
                background: #f8f9fa;
                border-radius: 0 0 4px 4px;
                overflow-x: hidden;
                overflow-y: auto;
                color: #666;
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
                white-space: pre-wrap;
                word-break: break-all;
                overflow-wrap: break-word;
                max-width: 100%;
                box-sizing: border-box;
            }
            
            .inspect-viz-modal-footer {
                text-align: right;
            }
            
            .inspect-viz-modal-button {
                background: #1976d2;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                font-family: inherit;
            }
            
            .inspect-viz-modal-button:hover {
                background: #1565c0;
            }
            
            .inspect-viz-modal-button:focus {
                outline: 2px solid #1976d2;
                outline-offset: 2px;
            }
            
            @media (max-width: 768px) {
                .inspect-viz-modal {
                    padding-top: 20px;
                }
                
                .inspect-viz-modal-content {
                    margin: 0 20px;
                    min-width: auto;
                    width: auto;
                    max-height: calc(100vh - 40px);
                }
            }
            
            @media (prefers-reduced-motion: reduce) {
                .inspect-viz-modal {
                    transition: none;
                }
            }
        `;
    document.head.appendChild(style);
    _Modal.modalCSSInjected = true;
  }
  static createModal(friendlyMessage, technicalMessage, title) {
    const modalHtml = `
            <div class="inspect-viz-modal" role="dialog" aria-labelledby="inspect-viz-modal-title" aria-modal="true">
                <div class="inspect-viz-modal-content">
                    <div class="inspect-viz-modal-header">
                        <h2 class="inspect-viz-modal-title" id="inspect-viz-modal-title">
                            <svg class="inspect-viz-modal-icon" viewBox="0 0 24 24">
                                <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
                            </svg>
                            ${_Modal.escapeHtml(title)}
                        </h2>
                        <button class="inspect-viz-modal-close" aria-label="Close dialog">\xD7</button>
                    </div>
                    <div class="inspect-viz-modal-body">
                        <div class="inspect-viz-modal-message">${_Modal.escapeHtml(friendlyMessage)}</div>
                        <details class="inspect-viz-modal-details">
                            <summary>Technical Details</summary>
                            <pre>${_Modal.escapeHtml(technicalMessage)}</pre>
                        </details>
                    </div>
                    <div class="inspect-viz-modal-footer">
                        <button class="inspect-viz-modal-button">Close</button>
                    </div>
                </div>
            </div>
        `;
    const div = document.createElement("div");
    div.innerHTML = modalHtml;
    const modal = div.firstElementChild;
    const closeButton = modal.querySelector(".inspect-viz-modal-close");
    const closeFooterButton = modal.querySelector(".inspect-viz-modal-button");
    const backdrop = modal;
    const closeModal = () => {
      modal.classList.remove("inspect-viz-modal-show");
      setTimeout(() => {
        if (modal.parentNode) {
          modal.parentNode.removeChild(modal);
        }
      }, 300);
    };
    closeButton?.addEventListener("click", closeModal);
    closeFooterButton?.addEventListener("click", closeModal);
    backdrop.addEventListener("click", (e) => {
      if (e.target === backdrop) {
        closeModal();
      }
    });
    const handleKeyDown = (e) => {
      if (e.key === "Escape") {
        closeModal();
        document.removeEventListener("keydown", handleKeyDown);
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return modal;
  }
  static focusModal(modal) {
    const closeButton = modal.querySelector(".inspect-viz-modal-close");
    if (closeButton) {
      closeButton.focus();
    }
  }
  static escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
};

// js/util/errors.ts
function initializeErrorHandling() {
  const errorHandler = new ErrorHandler();
  window.addEventListener("error", (event) => {
    const error = event.error;
    if (error) {
      const errorMessage = error.message || error.toString();
      const isSQL = isSQLError(errorMessage);
      errorHandler.handleError(errorMessage, isSQL);
    }
  });
  window.addEventListener("unhandledrejection", (event) => {
    const error = event.reason;
    let errorMessage = "";
    if (error instanceof Error) {
      errorMessage = error.message;
    } else if (typeof error === "string") {
      errorMessage = error;
    } else {
      errorMessage = String(error);
    }
    const isSQL = isSQLError(errorMessage);
    errorHandler.handleError(errorMessage, isSQL);
    event.preventDefault();
  });
}
function isSQLError(message) {
  const sqlErrorIndicators = [
    "Binder Error",
    'column "',
    'table "',
    "syntax error",
    "type mismatch",
    "division by zero",
    "conversion error",
    "SQL",
    "DuckDB"
  ];
  return sqlErrorIndicators.some(
    (indicator) => message.toLowerCase().includes(indicator.toLowerCase())
  );
}
var ErrorHandler = class {
  constructor() {
    this.lastErrorTime = 0;
    this.ERROR_THROTTLE_MS = 2e3;
  }
  // Prevent spam
  handleError(errorMessage, isSQLError2 = false) {
    const now = Date.now();
    if (now - this.lastErrorTime < this.ERROR_THROTTLE_MS) return;
    this.lastErrorTime = now;
    const friendlyError = isSQLError2 ? this.translateSqlError(errorMessage) : "An unexpected error occurred in the application.";
    const errorTitle = isSQLError2 ? "Query Error" : "Application Error";
    Modal.show({
      title: errorTitle,
      friendlyMessage: friendlyError,
      technicalMessage: errorMessage
    });
  }
  handleSQLError(errorMessage) {
    this.handleError(errorMessage, true);
  }
  translateSqlError(sqlError) {
    const errorPatterns = [
      {
        pattern: /referenced column "([^"]+)" not found/i,
        message: (match) => `Column "${match[1]}" was not found in your data. Please check your column names.`
      }
    ];
    for (const { pattern, message } of errorPatterns) {
      const match = sqlError.match(pattern);
      if (match) return message(match);
    }
    return "An error occurred while processing your data query.";
  }
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
      initializeErrorHandling();
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
    plot.width = containerEl.clientWidth;
    plot.height = containerEl.clientHeight;
  } else if ("hconcat" in spec && spec.hconcat.length <= 2) {
    const hconcat = spec.hconcat;
    const plot = "plot" in hconcat[0] ? hconcat[0] : "plot" in hconcat[1] ? hconcat[1] : void 0;
    if (plot) {
      plot.width = containerEl.clientWidth - (spec.hconcat.length > 1 ? 80 : 0);
      plot.height = containerEl.clientHeight;
    }
  } else if ("vconcat" in spec && spec.vconcat.length <= 2) {
    const vconcat = spec.vconcat;
    const plot = "plot" in vconcat[0] ? vconcat[0] : "plot" in vconcat[1] ? vconcat[1] : void 0;
    if (plot) {
      plot.width = containerEl.clientWidth;
      plot.height = containerEl.clientHeight - (spec.vconcat.length > 1 ? 35 : 0);
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
