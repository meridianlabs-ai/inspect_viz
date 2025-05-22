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
  constructor(table, selection, queries, params) {
    this.table = table;
    this.selection = selection;
    this.queries = queries;
    this.params = params;
  }
};

// js/util/wait.ts
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// js/coordinator/select.ts
import {
  SelectQuery,
  eq,
  neq,
  gt,
  gte,
  lt,
  lte,
  and,
  or,
  sum,
  avg,
  min,
  max,
  mode,
  median,
  count,
  add,
  sub,
  mul,
  div,
  BinaryOpNode,
  FunctionNode,
  LiteralNode,
  ParamNode,
  VerbatimNode
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm";
function toSelectQuery(query, params) {
  const selectExpressions = {};
  for (const [alias, expr] of Object.entries(query.select)) {
    selectExpressions[alias] = buildExpressionValue(expr, params);
  }
  let select = SelectQuery.select(selectExpressions);
  if (query.distinct === true) {
    select = select.distinct();
  }
  if (query.where) {
    select = applyWhereClause(select, params, query.where);
  }
  if (query.groupby && query.groupby.length > 0) {
    select = applyGroupByClause(select, params, query.groupby);
  }
  if (query.having) {
    select = applyHavingClause(select, params, query.having);
  }
  if (query.orderby && query.orderby.length > 0) {
    select = applyOrderByClause(select, query.orderby);
  }
  if (query.limit !== null && query.limit !== void 0) {
    select = select.limit(query.limit);
  }
  if (query.sample !== null && query.sample !== void 0) {
    select = select.sample(query.sample);
  }
  return select;
}
function interpretFunction(func, params) {
  const funcName = func.name.toLowerCase();
  const args = func.args.map((a) => buildExpressionNode(a, params));
  switch (funcName) {
    case "sum":
      return sum(args[0]);
    case "avg":
      return avg(args[0]);
    case "min":
      return min(args[0]);
    case "max":
      return max(args[0]);
    case "mode":
      return mode(args[0]);
    case "median":
      return median(args[0]);
    case "count":
      return count(args[0]);
    default:
      return new FunctionNode(funcName, args);
  }
}
function applyWhereClause(query, params, whereExpr) {
  if (whereExpr.type === "and" || whereExpr.type === "or") {
    return applyLogicalExpression(query, params, whereExpr);
  } else if (whereExpr.type === "unknown") {
    return query.where(new VerbatimNode(whereExpr.expression));
  } else {
    const condition = buildBinaryExpression(whereExpr, params);
    return query.where(condition);
  }
}
function applyLogicalExpression(query, params, expr) {
  const { type, expressions } = expr;
  if (expressions.length === 0) {
    return query;
  } else if (expressions.length === 1) {
    return applyWhereClause(
      query,
      params,
      expressions[0]
    );
  } else {
    const conditions = expressions.map((e) => buildExpressionValue(e, params));
    if (type === "and") {
      return query.where(and(...conditions));
    } else {
      return query.where(or(...conditions));
    }
  }
}
function applyGroupByClause(query, params, groupByFields) {
  const fields = groupByFields.map((field) => {
    if (typeof field === "string") {
      return field;
    } else {
      if (typeof field.field === "string") {
        return field.field;
      } else {
        return interpretFunction(field.field, params);
      }
    }
  });
  return query.groupby(...fields);
}
function applyHavingClause(query, params, havingExpr) {
  if ("type" in havingExpr) {
    if (havingExpr.type === "and" || havingExpr.type === "or") {
      const { type, expressions } = havingExpr;
      const conditions = expressions.map((e) => buildExpressionValue(e, params));
      if (type === "and") {
        return query.having(and(...conditions));
      } else {
        return query.having(or(...conditions));
      }
    } else if (havingExpr.type === "unknown") {
      return query.having(new VerbatimNode(havingExpr.expression));
    } else {
      const condition = buildBinaryExpression(havingExpr, params);
      return query.having(condition);
    }
  }
  return query.having(havingExpr);
}
function applyOrderByClause(query, orderByItems) {
  const orderByFields = orderByItems.map((item) => {
    return item.order === "desc" ? `-${item.field}` : item.field;
  });
  return query.orderby(...orderByFields);
}
function buildExpressionNode(expr, params) {
  if (typeof expr === "string" || typeof expr === "number" || typeof expr === "boolean") {
    return new LiteralNode(expr);
  } else if ("type" in expr) {
    if (expr.type === "parameter") {
      const name = expr.name;
      const param = params.get(name);
      if (param === void 0) {
        throw new Error(`Unknown parameter ${name}`);
      }
      return new ParamNode(param);
    } else if (expr.type === "unknown") {
      return new VerbatimNode(expr.expression);
    } else if (expr.type === "function") {
      return interpretFunction(expr, params);
    } else if (expr.type === "and" || expr.type === "or") {
      return buildLogicalExpression(expr, params);
    } else {
      return buildBinaryExpression(expr, params);
    }
  } else {
    throw Error(`Unexpected type for expression: ${typeof expr}`);
  }
}
function buildExpressionValue(expr, params) {
  if (typeof expr === "string") {
    return expr;
  } else {
    return buildExpressionNode(expr, params);
  }
}
function buildLogicalExpression(expr, params) {
  const { type, expressions } = expr;
  if (expressions.length === 0) {
    return new LiteralNode(true);
  } else if (expressions.length === 1) {
    return buildExpressionNode(expressions[0], params);
  } else {
    const conditions = expressions.map((e) => buildExpressionNode(e, params));
    if (type === "and") {
      return and(...conditions);
    } else {
      return or(...conditions);
    }
  }
}
function buildBinaryExpression(expr, params) {
  const { type, left, right } = expr;
  const leftOperand = buildExpressionValue(left, params);
  const rightOperand = buildExpressionNode(right, params);
  switch (type) {
    case "eq":
      return eq(leftOperand, rightOperand);
    case "neq":
      return neq(leftOperand, rightOperand);
    case "gt":
      return gt(leftOperand, rightOperand);
    case "gte":
      return gte(leftOperand, rightOperand);
    case "lt":
      return lt(leftOperand, rightOperand);
    case "lte":
      return lte(leftOperand, rightOperand);
    case "add":
      return add(leftOperand, rightOperand);
    case "sub":
      return sub(leftOperand, rightOperand);
    case "mul":
      return mul(leftOperand, rightOperand);
    case "div":
      return div(leftOperand, rightOperand);
    default:
      return new BinaryOpNode(
        type,
        buildExpressionNode(left, params),
        buildExpressionNode(right, params)
      );
  }
}

// js/coordinator/coodinator.ts
var VizCoordinator = class {
  constructor(conn_) {
    this.conn_ = conn_;
    this.dfs_ = /* @__PURE__ */ new Map();
    this.ctx_ = new InstantiateContext();
    this.ctx_.coordinator.databaseConnector(wasmConnector({ connection: this.conn_ }));
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
  async addDataFrame(id, source_id, buffer, queries) {
    if (buffer.length > 0) {
      await this.conn_?.insertArrowFromIPCStream(buffer, {
        name: id,
        create: true
      });
    }
    const params = /* @__PURE__ */ new Map();
    for (const query of queries) {
      for (const p of Object.values(query.parameters)) {
        params.set(p.id, this.addParam(p.id, p.default));
      }
    }
    const df = new DataFrame(
      source_id,
      Selection.intersect(),
      queries.map((q) => toSelectQuery(q, params)),
      params
    );
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

// js/clients/figure.ts
import {
  toDataColumns
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import Plotly from "https://esm.sh/plotly.js-dist-min@3.0.1";

// js/clients/viz.ts
import {
  MosaicClient as MosaicClient2
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import { SelectQuery as SelectQuery2 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm";
var VizClient = class _VizClient extends MosaicClient2 {
  constructor(table_, filterBy, queries_, params_) {
    super(filterBy);
    this.table_ = table_;
    this.queries_ = queries_;
    this.params_ = params_;
    this.params_.forEach((value) => {
      value.addEventListener("value", () => this.requestUpdate());
    });
  }
  query(filter = []) {
    let query = SelectQuery2.select("*").from(this.table_).where(filter);
    return _VizClient.applyQueries(query, this.queries_);
  }
  static applyQueries(query, queries) {
    for (let q of queries) {
      query = q.clone().from(query);
    }
    return query;
  }
};

// js/clients/figure.ts
var Figure = class extends VizClient {
  constructor(el_, figure_, axisMappings_, table, filterBy, queries, params) {
    super(table, filterBy, queries, params);
    this.el_ = el_;
    this.figure_ = figure_;
    this.axisMappings_ = axisMappings_;
  }
  queryResult(data) {
    const columns = toDataColumns(data).columns;
    const table = bindTable(this.figure_, this.axisMappings_, columns);
    console.log(this.figure_.data);
    console.log("---------");
    console.log(table);
    const layout = this.figure_.layout || {};
    layout.autosize = true;
    const config = this.figure_.config || {};
    config.responsive = true;
    Plotly.react(this.el_, table, layout, config);
    return this;
  }
};
function bindTable(figure, axisMappings, columns) {
  const traces = structuredClone(figure.data);
  const isMultiTrace = traces.length > 1;
  if (!isMultiTrace) {
    const trace = traces[0];
    const mapping = columnMapping(trace, Object.keys(columns), axisMappings);
    for (const [attr, col] of Object.entries(mapping)) {
      const arr = columns[col];
      if (arr) {
        setData(trace, attr.split("."), arr);
      } else {
        console.warn(`Column "${col}" not found in table`);
      }
    }
    return traces;
  }
  const isPlotlyExpressFigure = detectPlotlyExpressFigure(traces);
  const hasFacets = detectFacetSubplots(traces, figure.layout);
  if (hasFacets) {
    traces.forEach((trace) => {
      const mapping = columnMapping(trace, Object.keys(columns), axisMappings);
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
  const possibleCatColumns = findPossibleCategoricalColumns(traces, columns);
  const tracesByType = groupTracesByType(traces);
  traces.forEach((trace, _traceIndex) => {
    const mapping = columnMapping(trace, Object.keys(columns), axisMappings);
    let indexArray = void 0;
    if (isPlotlyExpressFigure) {
      indexArray = findIndicesForPlotlyExpressTrace(trace, possibleCatColumns, columns);
    }
    if (!indexArray) {
      const traceAny = trace;
      if (getProp(traceAny, "_index") !== void 0) {
        const indices = getProp(traceAny, "_index");
        if (Array.isArray(indices)) {
          indexArray = indices;
        }
      } else if (getProp(traceAny, "_filter") !== void 0) {
        const filterExpr = getProp(traceAny, "_filter");
        if (typeof filterExpr === "string") {
          indexArray = applyFilterExpression(filterExpr, columns);
        }
      } else {
        indexArray = inferIndicesFromTraceProperties(trace, columns, possibleCatColumns);
      }
    }
    const traceType = getProp(trace, "type") || "scatter";
    const tracesOfSameType = tracesByType[traceType] || [];
    if (!indexArray && tracesOfSameType.length > 1) {
      const tracePosition = tracesOfSameType.indexOf(trace);
      if (tracePosition !== -1 && tracePosition < tracesOfSameType.length) {
        const dataLength = Object.values(columns)[0]?.length || 0;
        const chunkSize = Math.ceil(dataLength / tracesOfSameType.length);
        const startIdx = tracePosition * chunkSize;
        const endIdx = Math.min(startIdx + chunkSize, dataLength);
        indexArray = Array.from({ length: endIdx - startIdx }, (_, i) => startIdx + i);
      }
    }
    for (const [attr, col] of Object.entries(mapping)) {
      const arr = columns[col];
      if (arr) {
        if (indexArray && indexArray.length > 0) {
          const filteredArr = Array.from(arr).filter((_, i) => indexArray.includes(i));
          setData(trace, attr.split("."), filteredArr);
        } else {
          setData(trace, attr.split("."), arr);
        }
      } else {
        console.warn(`Column "${col}" not found in table`);
      }
    }
  });
  return traces;
}
function columnMapping(trace, cols, axisMappings) {
  const map = {};
  const lc = cols.map((c) => c.toLowerCase());
  for (const p of arrayProps(trace)) {
    const simple = p.split(".").pop().toLowerCase();
    const i = lc.indexOf(simple);
    if (i === -1) continue;
    const exists = p.split(".").reduce((o, k) => o?.[k], trace) !== void 0;
    if (exists) map[p] = cols[i];
  }
  const needsX = !map.x && (!isOrientable(trace) || trace.orientation !== "h");
  if (needsX && axisMappings.x) {
    map.x = axisMappings.x;
  }
  const needsY = !map.y && (isOrientable(trace) && trace.orientation === "h" ? false : true);
  if (needsY && axisMappings.y) {
    map.y = axisMappings.y;
  }
  const is3d = ["scatter3d", "surface", "mesh3d"].includes(trace.type ?? "");
  if (is3d && !map.z && axisMappings.z) {
    map.z = axisMappings.z;
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
function groupTracesByType(traces) {
  const result = {};
  traces.forEach((trace) => {
    const type = trace.type || "scatter";
    if (!result[type]) {
      result[type] = [];
    }
    result[type].push(trace);
  });
  return result;
}
function getProp(obj, prop, defaultVal) {
  return obj && prop in obj ? obj[prop] : defaultVal;
}
function detectPlotlyExpressFigure(traces) {
  return traces.some((trace) => {
    const t = trace;
    if (t._px !== void 0 || t._plotlyExpressDefaults !== void 0) {
      return true;
    }
    const legendgroup = getProp(t, "legendgroup");
    if (legendgroup && typeof legendgroup === "string" && legendgroup.includes(":")) {
      return true;
    }
    const name = getProp(t, "name");
    if (name !== void 0 && typeof name === "string") {
      if (name.includes(" =") || name.match(/^[a-zA-Z_]+=[a-zA-Z0-9_]+$/)) {
        return true;
      }
    }
    return false;
  });
}
function detectFacetSubplots(traces, layout) {
  if (layout) {
    const hasGridStructure = layout.grid !== void 0 || Object.keys(layout).some((key) => key.startsWith("xaxis") && key !== "xaxis") || Object.keys(layout).some((key) => key.startsWith("yaxis") && key !== "yaxis");
    if (hasGridStructure) return true;
  }
  return traces.some((trace) => {
    const xaxis = getProp(trace, "xaxis");
    const yaxis = getProp(trace, "yaxis");
    const hasSubplot = getProp(trace, "_subplot") !== void 0;
    return xaxis !== void 0 && xaxis !== "x" || yaxis !== void 0 && yaxis !== "y" || // Some Plotly Express facet plots contain this meta information
    hasSubplot;
  });
}
function findIndicesForPlotlyExpressTrace(trace, categoricalColumns, columns) {
  const name = getProp(trace, "name");
  if (name === void 0) return void 0;
  for (const colName of categoricalColumns) {
    const colValues = columns[colName];
    if (!colValues) continue;
    const exactMatches = Array.from(colValues).map((val, idx) => val === name ? idx : -1).filter((idx) => idx !== -1);
    if (exactMatches.length > 0) {
      return exactMatches;
    }
    if (typeof name === "string" && name.includes("=")) {
      const parts = name.split("=").map((s) => s.trim());
      if (parts.length === 2 && parts[0] === colName) {
        const targetValue = parts[1];
        const matches = Array.from(colValues).map((val, idx) => String(val) === targetValue ? idx : -1).filter((idx) => idx !== -1);
        if (matches.length > 0) {
          return matches;
        }
      }
    }
  }
  const legendgroup = getProp(trace, "legendgroup");
  if (legendgroup) {
    for (const colName of categoricalColumns) {
      const colValues = columns[colName];
      if (!colValues) continue;
      if (typeof legendgroup === "string" && legendgroup.includes(colName) && legendgroup.includes(":")) {
        const valueMatch = legendgroup.match(new RegExp(`${colName}:([^:]+)`));
        if (valueMatch && valueMatch[1]) {
          const targetValue = valueMatch[1];
          const matches = Array.from(colValues).map((val, idx) => String(val) === targetValue ? idx : -1).filter((idx) => idx !== -1);
          if (matches.length > 0) {
            return matches;
          }
        }
      }
    }
  }
  return void 0;
}
function applyFilterExpression(filterExpr, columns) {
  const matches = filterExpr.match(/(\w+)\s*==\s*["']?([^"']+)["']?/);
  if (matches && matches.length === 3) {
    const [_, colName, value] = matches;
    if (columns[colName]) {
      const colValues = columns[colName];
      return Array.from(colValues).map((val, idx) => String(val) === value ? idx : -1).filter((idx) => idx !== -1);
    }
  }
  return void 0;
}
function inferIndicesFromTraceProperties(trace, columns, categoricalColumns) {
  const name = getProp(trace, "name");
  if (name !== void 0) {
    for (const colName of categoricalColumns) {
      const colValues = columns[colName];
      if (!colValues) continue;
      const matches = Array.from(colValues).map((val, idx) => String(val) === String(name) ? idx : -1).filter((idx) => idx !== -1);
      if (matches.length > 0) {
        return matches;
      }
    }
    if (typeof name === "string" && name.includes("=")) {
      const parts = name.split("=").map((p) => p.trim());
      if (parts.length === 2 && columns[parts[0]]) {
        const colValues = columns[parts[0]];
        const matches = Array.from(colValues).map((val, idx) => String(val) === parts[1] ? idx : -1).filter((idx) => idx !== -1);
        if (matches.length > 0) {
          return matches;
        }
      }
    }
  }
  const marker = getProp(trace, "marker");
  if (marker) {
    if (Array.isArray(marker.color)) {
      const nonNullIndices = marker.color.map((val, idx) => val != null ? idx : -1).filter((idx) => idx !== -1);
      if (nonNullIndices.length > 0 && nonNullIndices.length < (Object.values(columns)[0]?.length || 0)) {
        return nonNullIndices;
      }
    }
    if (Array.isArray(marker.symbol)) {
      const symbolName = marker.symbol[0];
      if (symbolName && typeof symbolName === "string") {
        const nonNullIndices = marker.symbol.map((val, idx) => val === symbolName ? idx : -1).filter((idx) => idx !== -1);
        if (nonNullIndices.length > 0) {
          return nonNullIndices;
        }
      }
    }
  }
  const line = getProp(trace, "line");
  if (line) {
    if (Array.isArray(line.color)) {
      const nonNullIndices = line.color.map((val, idx) => val != null ? idx : -1).filter((idx) => idx !== -1);
      if (nonNullIndices.length > 0 && nonNullIndices.length < (Object.values(columns)[0]?.length || 0)) {
        return nonNullIndices;
      }
    }
    if (Array.isArray(line.dash)) {
      const dashStyle = line.dash[0];
      if (dashStyle) {
        const matchingIndices = line.dash.map((val, idx) => val === dashStyle ? idx : -1).filter((idx) => idx !== -1);
        if (matchingIndices.length > 0) {
          return matchingIndices;
        }
      }
    }
  }
  const legendgroup = getProp(trace, "legendgroup");
  if (legendgroup && typeof legendgroup === "string") {
    const lgParts = legendgroup.split(":");
    if (lgParts.length >= 2 && columns[lgParts[0]]) {
      const colValues = columns[lgParts[0]];
      const matches = Array.from(colValues).map((val, idx) => String(val) === lgParts[1] ? idx : -1).filter((idx) => idx !== -1);
      if (matches.length > 0) {
        return matches;
      }
    }
  }
  return void 0;
}
function findPossibleCategoricalColumns(traces, columns) {
  const categoricalColumns = [];
  const traceNames = [];
  traces.forEach((trace) => {
    const name = getProp(trace, "name");
    if (name !== void 0) traceNames.push(name);
  });
  if (traceNames.length === 0) return [];
  for (const [colName, colValues] of Object.entries(columns)) {
    if (!colValues || colValues.length === 0) continue;
    const values = Array.from(colValues);
    const allNumbers = values.every((val) => typeof val === "number");
    if (allNumbers) {
      const matchesAnyTraceName = traceNames.some((name) => {
        if (typeof name === "string") {
          return values.some((val) => val === Number(name));
        } else {
          return values.some((val) => val === name);
        }
      });
      if (!matchesAnyTraceName) continue;
    }
    const uniqueValues = new Set(values);
    if (uniqueValues.size >= values.length * 0.5 && uniqueValues.size > 10) continue;
    const matchesTraceName = traceNames.some((name) => values.some((val) => val === name));
    const legendGroups = [];
    traces.forEach((trace) => {
      const legendgroup = getProp(trace, "legendgroup");
      if (legendgroup) legendGroups.push(legendgroup);
    });
    const matchesLegendGroup = legendGroups.some(
      (group) => values.some((val) => String(val) === group)
    );
    if (matchesTraceName || matchesLegendGroup) {
      categoricalColumns.push(colName);
    } else {
      if (uniqueValues.size <= 25 && uniqueValues.size > 0 && uniqueValues.size < values.length * 0.25) {
        categoricalColumns.push(colName);
      }
    }
  }
  return categoricalColumns;
}

// js/widgets/figure.ts
async function render({ model, el }) {
  const df_id = model.get("df_id");
  const figure_json = model.get("figure");
  const figure = JSON.parse(figure_json);
  const axis_mappings_json = model.get("axis_mappings");
  const axis_mappings = JSON.parse(axis_mappings_json);
  const coordinator = await vizCoordinator();
  const df = await coordinator.getDataFrame(df_id);
  const view = new Figure(
    el,
    figure,
    axis_mappings,
    df.table,
    df.selection,
    df.queries,
    df.params
  );
  await coordinator.connectClient(view);
}
var figure_default = { render };
export {
  figure_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsiLi4vLi4vLi4vanMvY29vcmRpbmF0b3IvY29vZGluYXRvci50cyIsICIuLi8uLi8uLi9qcy9jb29yZGluYXRvci9kdWNrZGIudHMiLCAiLi4vLi4vLi4vanMvY29vcmRpbmF0b3IvZGF0YWZyYW1lLnRzIiwgIi4uLy4uLy4uL2pzL3V0aWwvd2FpdC50cyIsICIuLi8uLi8uLi9qcy9jb29yZGluYXRvci9zZWxlY3QudHMiLCAiLi4vLi4vLi4vanMvY2xpZW50cy9maWd1cmUudHMiLCAiLi4vLi4vLi4vanMvY2xpZW50cy92aXoudHMiLCAiLi4vLi4vLi4vanMvd2lkZ2V0cy9maWd1cmUudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImltcG9ydCB7IEFzeW5jRHVja0RCQ29ubmVjdGlvbiB9IGZyb20gJ2h0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9ucG0vQGR1Y2tkYi9kdWNrZGItd2FzbUAxLjI5LjAvK2VzbSc7XG5cbmltcG9ydCB7XG4gICAgTW9zYWljQ2xpZW50LFxuICAgIHdhc21Db25uZWN0b3IsXG4gICAgU2VsZWN0aW9uLFxuICAgIFBhcmFtLFxufSBmcm9tICdodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL0B1d2RhdGEvbW9zYWljLWNvcmVAMC4xNi4yLytlc20nO1xuXG5pbXBvcnQgeyBJbnN0YW50aWF0ZUNvbnRleHQgfSBmcm9tICdodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL0B1d2RhdGEvbW9zYWljLXNwZWNAMC4xNi4yLytlc20nO1xuXG5pbXBvcnQgeyBpbml0RHVja2RiIH0gZnJvbSAnLi9kdWNrZGInO1xuaW1wb3J0IHsgTW9zYWljUXVlcnkgfSBmcm9tICcuL3F1ZXJ5JztcbmltcG9ydCB7IERhdGFGcmFtZSB9IGZyb20gJy4vZGF0YWZyYW1lJztcbmltcG9ydCB7IHNsZWVwIH0gZnJvbSAnLi4vdXRpbC93YWl0JztcbmltcG9ydCB7IHRvU2VsZWN0UXVlcnkgfSBmcm9tICcuL3NlbGVjdCc7XG5cbmNsYXNzIFZpekNvb3JkaW5hdG9yIHtcbiAgICBwcml2YXRlIHJlYWRvbmx5IGN0eF86IEluc3RhbnRpYXRlQ29udGV4dDtcbiAgICBwcml2YXRlIHJlYWRvbmx5IGRmc18gPSBuZXcgTWFwPHN0cmluZywgRGF0YUZyYW1lPigpO1xuXG4gICAgY29uc3RydWN0b3IocHJpdmF0ZSByZWFkb25seSBjb25uXzogQXN5bmNEdWNrREJDb25uZWN0aW9uKSB7XG4gICAgICAgIHRoaXMuY3R4XyA9IG5ldyBJbnN0YW50aWF0ZUNvbnRleHQoKTtcbiAgICAgICAgdGhpcy5jdHhfLmNvb3JkaW5hdG9yLmRhdGFiYXNlQ29ubmVjdG9yKHdhc21Db25uZWN0b3IoeyBjb25uZWN0aW9uOiB0aGlzLmNvbm5fIH0pKTtcbiAgICB9XG5cbiAgICBhZGRQYXJhbShuYW1lOiBzdHJpbmcsIHZhbHVlOiBudW1iZXIgfCBib29sZWFuIHwgc3RyaW5nKTogUGFyYW0ge1xuICAgICAgICBpZiAoIXRoaXMuY3R4Xy5hY3RpdmVQYXJhbXMuaGFzKG5hbWUpKSB7XG4gICAgICAgICAgICB0aGlzLmN0eF8uYWN0aXZlUGFyYW1zLnNldChuYW1lLCBQYXJhbS52YWx1ZSh2YWx1ZSkpO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiB0aGlzLmN0eF8uYWN0aXZlUGFyYW1zLmdldChuYW1lKSE7XG4gICAgfVxuXG4gICAgZ2V0UGFyYW0obmFtZTogc3RyaW5nKTogUGFyYW0gfCB1bmRlZmluZWQge1xuICAgICAgICByZXR1cm4gdGhpcy5jdHhfLmFjdGl2ZVBhcmFtcy5nZXQobmFtZSk7XG4gICAgfVxuXG4gICAgYXN5bmMgYWRkRGF0YUZyYW1lKGlkOiBzdHJpbmcsIHNvdXJjZV9pZDogc3RyaW5nLCBidWZmZXI6IFVpbnQ4QXJyYXksIHF1ZXJpZXM6IE1vc2FpY1F1ZXJ5W10pIHtcbiAgICAgICAgLy8gaW5zZXJ0IHRhYmxlIGludG8gZGF0YWJhc2UgaWYgdGhlcmUgaXMgZGF0YVxuICAgICAgICBpZiAoYnVmZmVyLmxlbmd0aCA+IDApIHtcbiAgICAgICAgICAgIGF3YWl0IHRoaXMuY29ubl8/Lmluc2VydEFycm93RnJvbUlQQ1N0cmVhbShidWZmZXIsIHtcbiAgICAgICAgICAgICAgICBuYW1lOiBpZCxcbiAgICAgICAgICAgICAgICBjcmVhdGU6IHRydWUsXG4gICAgICAgICAgICB9KTtcbiAgICAgICAgfVxuXG4gICAgICAgIC8vIGV4dHJhY3QgcGFyYW1ldGVycyBmcm9tIHF1ZXJpZXMgYW5kIHJlZ2lzdGVyIHRoZW1cbiAgICAgICAgY29uc3QgcGFyYW1zID0gbmV3IE1hcDxzdHJpbmcsIFBhcmFtPigpO1xuICAgICAgICBmb3IgKGNvbnN0IHF1ZXJ5IG9mIHF1ZXJpZXMpIHtcbiAgICAgICAgICAgIGZvciAoY29uc3QgcCBvZiBPYmplY3QudmFsdWVzKHF1ZXJ5LnBhcmFtZXRlcnMpKSB7XG4gICAgICAgICAgICAgICAgcGFyYW1zLnNldChwLmlkLCB0aGlzLmFkZFBhcmFtKHAuaWQsIHAuZGVmYXVsdCkpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG5cbiAgICAgICAgLy8gY3JlYXRlIGFuZCByZWdpc3RlciBkZlxuICAgICAgICBjb25zdCBkZiA9IG5ldyBEYXRhRnJhbWUoXG4gICAgICAgICAgICBzb3VyY2VfaWQsXG4gICAgICAgICAgICBTZWxlY3Rpb24uaW50ZXJzZWN0KCksXG4gICAgICAgICAgICBxdWVyaWVzLm1hcChxID0+IHRvU2VsZWN0UXVlcnkocSwgcGFyYW1zKSksXG4gICAgICAgICAgICBwYXJhbXNcbiAgICAgICAgKTtcbiAgICAgICAgdGhpcy5kZnNfLnNldChpZCwgZGYpO1xuICAgIH1cblxuICAgIGFzeW5jIGdldERhdGFGcmFtZShpZDogc3RyaW5nKSB7XG4gICAgICAgIC8vIGF0IHN0YXJ0dXAgd2UgY2FuJ3QgY29udHJvbCB0aGUgb3JkZXIgb2YgZGYgcHJvZHVjaW5nIGFuZCBkZiBjb25zdW1pbmdcbiAgICAgICAgLy8gd2lkZ2V0cywgc28gd2UgbWF5IG5lZWQgdG8gd2FpdCBhbmQgcmV0cnkgZm9yIHRoZSBkYXRhIGZyYW1lXG4gICAgICAgIHdoaWxlICh0cnVlKSB7XG4gICAgICAgICAgICBjb25zdCBkZiA9IHRoaXMuZGZzXy5nZXQoaWQpO1xuICAgICAgICAgICAgaWYgKGRmKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIGRmO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICBhd2FpdCBzbGVlcCgxMDApO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuXG4gICAgZ2V0SW5zdGFudGlhdGVDb250ZXh0KCk6IEluc3RhbnRpYXRlQ29udGV4dCB7XG4gICAgICAgIHJldHVybiB0aGlzLmN0eF87XG4gICAgfVxuXG4gICAgYXN5bmMgY29ubmVjdENsaWVudChjbGllbnQ6IE1vc2FpY0NsaWVudCkge1xuICAgICAgICB0aGlzLmN0eF8uY29vcmRpbmF0b3IuY29ubmVjdChjbGllbnQpO1xuICAgIH1cbn1cblxuLy8gZ2V0IHRoZSBnbG9iYWwgY29vcmRpbmF0b3JzIGluc3RhbmNlLCBlbnN1cmluZyB3ZSBnZXQgdGhlIHNhbWVcbi8vIGluc3RhbmNlIGV2YWwgYWNyb3NzIGRpZmZlcmVudCBqcyBidW5kbGVzIGxvYWRlZCBpbnRvIHRoZSBwYWdlXG5jb25zdCBWSVpfQ09PUkRJTkFUT1JfS0VZID0gU3ltYm9sLmZvcignQEBpbnNwZWN0LXZpei1jb29yZGluYXRvcicpO1xuYXN5bmMgZnVuY3Rpb24gdml6Q29vcmRpbmF0b3IoKTogUHJvbWlzZTxWaXpDb29yZGluYXRvcj4ge1xuICAgIGNvbnN0IGdsb2JhbFNjb3BlOiBhbnkgPSB0eXBlb2Ygd2luZG93ICE9PSAndW5kZWZpbmVkJyA/IHdpbmRvdyA6IGdsb2JhbFRoaXM7XG4gICAgaWYgKCFnbG9iYWxTY29wZVtWSVpfQ09PUkRJTkFUT1JfS0VZXSkge1xuICAgICAgICBnbG9iYWxTY29wZVtWSVpfQ09PUkRJTkFUT1JfS0VZXSA9IChhc3luYyAoKSA9PiB7XG4gICAgICAgICAgICBjb25zdCBkdWNrZGIgPSBhd2FpdCBpbml0RHVja2RiKCk7XG4gICAgICAgICAgICBjb25zdCBjb25uID0gYXdhaXQgZHVja2RiLmNvbm5lY3QoKTtcbiAgICAgICAgICAgIHJldHVybiBuZXcgVml6Q29vcmRpbmF0b3IoY29ubik7XG4gICAgICAgIH0pKCk7XG4gICAgfVxuICAgIHJldHVybiBnbG9iYWxTY29wZVtWSVpfQ09PUkRJTkFUT1JfS0VZXSBhcyBQcm9taXNlPFZpekNvb3JkaW5hdG9yPjtcbn1cblxuZXhwb3J0IHsgVml6Q29vcmRpbmF0b3IsIHZpekNvb3JkaW5hdG9yIH07XG4iLCAiaW1wb3J0IHtcbiAgICBnZXRKc0RlbGl2ckJ1bmRsZXMsXG4gICAgc2VsZWN0QnVuZGxlLFxuICAgIEFzeW5jRHVja0RCLFxuICAgIENvbnNvbGVMb2dnZXIsXG4gICAgQXN5bmNEdWNrREJDb25uZWN0aW9uLFxuICAgIExvZ0xldmVsLFxufSBmcm9tICdodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL0BkdWNrZGIvZHVja2RiLXdhc21AMS4yOS4wLytlc20nO1xuXG5leHBvcnQgYXN5bmMgZnVuY3Rpb24gaW5pdER1Y2tkYigpIHtcbiAgICBjb25zdCBKU0RFTElWUl9CVU5ETEVTID0gZ2V0SnNEZWxpdnJCdW5kbGVzKCk7XG5cbiAgICAvLyBTZWxlY3QgYSBidW5kbGUgYmFzZWQgb24gYnJvd3NlciBjaGVja3NcbiAgICBjb25zdCBidW5kbGUgPSBhd2FpdCBzZWxlY3RCdW5kbGUoSlNERUxJVlJfQlVORExFUyk7XG5cbiAgICBjb25zdCB3b3JrZXJfdXJsID0gVVJMLmNyZWF0ZU9iamVjdFVSTChcbiAgICAgICAgbmV3IEJsb2IoW2BpbXBvcnRTY3JpcHRzKFwiJHtidW5kbGUubWFpbldvcmtlciF9XCIpO2BdLCB7XG4gICAgICAgICAgICB0eXBlOiAndGV4dC9qYXZhc2NyaXB0JyxcbiAgICAgICAgfSlcbiAgICApO1xuXG4gICAgLy8gSW5zdGFudGlhdGUgdGhlIGFzeW5jaHJvbm91cyB2ZXJzaW9uIG9mIER1Y2tEQi13YXNtXG4gICAgY29uc3Qgd29ya2VyID0gbmV3IFdvcmtlcih3b3JrZXJfdXJsKTtcbiAgICBjb25zdCBsb2dnZXIgPSBuZXcgQ29uc29sZUxvZ2dlcihMb2dMZXZlbC5JTkZPKTtcbiAgICBjb25zdCBkYiA9IG5ldyBBc3luY0R1Y2tEQihsb2dnZXIsIHdvcmtlcik7XG4gICAgYXdhaXQgZGIuaW5zdGFudGlhdGUoYnVuZGxlLm1haW5Nb2R1bGUsIGJ1bmRsZS5wdGhyZWFkV29ya2VyKTtcbiAgICBVUkwucmV2b2tlT2JqZWN0VVJMKHdvcmtlcl91cmwpO1xuXG4gICAgcmV0dXJuIGRiO1xufVxuXG5leHBvcnQgYXN5bmMgZnVuY3Rpb24gd2FpdEZvclRhYmxlKFxuICAgIGNvbm46IEFzeW5jRHVja0RCQ29ubmVjdGlvbixcbiAgICB0YWJsZTogc3RyaW5nLFxuICAgIHsgdGltZW91dCA9IDEwXzAwMCwgaW50ZXJ2YWwgPSAyNTAgfSA9IHt9XG4pIHtcbiAgICBjb25zdCB0MCA9IHBlcmZvcm1hbmNlLm5vdygpO1xuXG4gICAgd2hpbGUgKHRydWUpIHtcbiAgICAgICAgdHJ5IHtcbiAgICAgICAgICAgIGNvbnN0IHJlcyA9IGF3YWl0IGNvbm4ucXVlcnkoXG4gICAgICAgICAgICAgICAgYFNFTEVDVCAxXG4gICAgICAgICAgIEZST00gaW5mb3JtYXRpb25fc2NoZW1hLnRhYmxlc1xuICAgICAgICAgV0hFUkUgdGFibGVfc2NoZW1hID0gJ21haW4nXG4gICAgICAgICAgIEFORCB0YWJsZV9uYW1lICAgPSAnJHt0YWJsZX0nXG4gICAgICAgICBMSU1JVCAxYFxuICAgICAgICAgICAgKTtcblxuICAgICAgICAgICAgaWYgKHJlcy5udW1Sb3dzKSByZXR1cm47IC8vIHN1Y2Nlc3MgXHUyNzI4XG4gICAgICAgIH0gY2F0Y2ggKGVycikge1xuICAgICAgICAgICAgLyogVGFibGUgb3IgZXZlbiB0aGUgZGF0YWJhc2UgZmlsZSBtYXkgbm90IGJlIHJlYWR5IHlldC5cbiAgICAgICAgIElnbm9yZSB0aGUgZXJyb3IgYW5kIGtlZXAgcG9sbGluZy4gKi9cbiAgICAgICAgfVxuXG4gICAgICAgIGlmIChwZXJmb3JtYW5jZS5ub3coKSAtIHQwID4gdGltZW91dCkge1xuICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKGBUaW1lZCBvdXQgd2FpdGluZyBmb3IgdGFibGUgXCIke3RhYmxlfVwiYCk7XG4gICAgICAgIH1cbiAgICAgICAgYXdhaXQgbmV3IFByb21pc2UociA9PiBzZXRUaW1lb3V0KHIsIGludGVydmFsKSk7XG4gICAgfVxufVxuIiwgImltcG9ydCB7IFBhcmFtLCBTZWxlY3Rpb24gfSBmcm9tICdAdXdkYXRhL21vc2FpYy1jb3JlJztcbmltcG9ydCB7IFNlbGVjdFF1ZXJ5IH0gZnJvbSAnaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L25wbS9AdXdkYXRhL21vc2FpYy1zcWxAMC4xNi4yLytlc20nO1xuXG5leHBvcnQgY2xhc3MgRGF0YUZyYW1lIHtcbiAgICBjb25zdHJ1Y3RvcihcbiAgICAgICAgcHVibGljIHJlYWRvbmx5IHRhYmxlOiBzdHJpbmcsXG4gICAgICAgIHB1YmxpYyByZWFkb25seSBzZWxlY3Rpb246IFNlbGVjdGlvbixcbiAgICAgICAgcHVibGljIHJlYWRvbmx5IHF1ZXJpZXM6IFNlbGVjdFF1ZXJ5W10sXG4gICAgICAgIHB1YmxpYyByZWFkb25seSBwYXJhbXM6IE1hcDxzdHJpbmcsIFBhcmFtPlxuICAgICkge31cbn1cbiIsICJleHBvcnQgZnVuY3Rpb24gc2xlZXAobXM6IG51bWJlcikge1xuICAgIHJldHVybiBuZXcgUHJvbWlzZShyZXNvbHZlID0+IHNldFRpbWVvdXQocmVzb2x2ZSwgbXMpKTtcbn1cbiIsICJpbXBvcnQge1xuICAgIFNlbGVjdFF1ZXJ5LFxuICAgIGVxLFxuICAgIG5lcSxcbiAgICBndCxcbiAgICBndGUsXG4gICAgbHQsXG4gICAgbHRlLFxuICAgIGFuZCxcbiAgICBvcixcbiAgICBzdW0sXG4gICAgYXZnLFxuICAgIG1pbixcbiAgICBtYXgsXG4gICAgbW9kZSxcbiAgICBtZWRpYW4sXG4gICAgY291bnQsXG4gICAgYWRkLFxuICAgIHN1YixcbiAgICBtdWwsXG4gICAgZGl2LFxuICAgIEJpbmFyeU9wTm9kZSxcbiAgICBBZ2dyZWdhdGVOb2RlLFxuICAgIEV4cHJWYWx1ZSxcbiAgICBGdW5jdGlvbk5vZGUsXG4gICAgRXhwck5vZGUsXG4gICAgTGl0ZXJhbE5vZGUsXG4gICAgUGFyYW1Ob2RlLFxuICAgIFZlcmJhdGltTm9kZSxcbn0gZnJvbSAnaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L25wbS9AdXdkYXRhL21vc2FpYy1zcWxAMC4xNi4yLytlc20nO1xuXG5pbXBvcnQge1xuICAgIE1vc2FpY1F1ZXJ5LFxuICAgIEJpbmFyeUV4cHJlc3Npb24sXG4gICAgTG9naWNhbEV4cHJlc3Npb24sXG4gICAgRnVuY3Rpb25FeHByZXNzaW9uLFxuICAgIFVua25vd25FeHByZXNzaW9uLFxuICAgIFBhcmFtZXRlckV4cHJlc3Npb24sXG4gICAgT3JkZXJCeUl0ZW0sXG4gICAgR3JvdXBCeUZpZWxkLFxuICAgIEV4cHJlc3Npb24sXG59IGZyb20gJy4vcXVlcnknO1xuaW1wb3J0IHsgUGFyYW0gfSBmcm9tICdodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL0B1d2RhdGEvbW9zYWljLWNvcmVAMC4xNi4yLytlc20nO1xuXG5leHBvcnQgZnVuY3Rpb24gdG9TZWxlY3RRdWVyeShxdWVyeTogTW9zYWljUXVlcnksIHBhcmFtczogTWFwPHN0cmluZywgUGFyYW0+KTogU2VsZWN0UXVlcnkge1xuICAgIC8vIGNvbnZlcnQgdG8gZXhwcmVzc2lvbnNcbiAgICBjb25zdCBzZWxlY3RFeHByZXNzaW9uczogUmVjb3JkPHN0cmluZywgRXhwclZhbHVlPiA9IHt9O1xuICAgIGZvciAoY29uc3QgW2FsaWFzLCBleHByXSBvZiBPYmplY3QuZW50cmllcyhxdWVyeS5zZWxlY3QpKSB7XG4gICAgICAgIHNlbGVjdEV4cHJlc3Npb25zW2FsaWFzXSA9IGJ1aWxkRXhwcmVzc2lvblZhbHVlKGV4cHIsIHBhcmFtcyk7XG4gICAgfVxuICAgIGxldCBzZWxlY3QgPSBTZWxlY3RRdWVyeS5zZWxlY3Qoc2VsZWN0RXhwcmVzc2lvbnMpO1xuXG4gICAgLy8gQXBwbHkgRElTVElOQ1QgaWYgbmVlZGVkXG4gICAgaWYgKHF1ZXJ5LmRpc3RpbmN0ID09PSB0cnVlKSB7XG4gICAgICAgIHNlbGVjdCA9IHNlbGVjdC5kaXN0aW5jdCgpO1xuICAgIH1cblxuICAgIC8vIEFwcGx5IFdIRVJFIGNsYXVzZSBpZiBwcmVzZW50XG4gICAgaWYgKHF1ZXJ5LndoZXJlKSB7XG4gICAgICAgIHNlbGVjdCA9IGFwcGx5V2hlcmVDbGF1c2Uoc2VsZWN0LCBwYXJhbXMsIHF1ZXJ5LndoZXJlKTtcbiAgICB9XG5cbiAgICAvLyBBcHBseSBHUk9VUCBCWSBjbGF1c2UgaWYgcHJlc2VudFxuICAgIGlmIChxdWVyeS5ncm91cGJ5ICYmIHF1ZXJ5Lmdyb3VwYnkubGVuZ3RoID4gMCkge1xuICAgICAgICBzZWxlY3QgPSBhcHBseUdyb3VwQnlDbGF1c2Uoc2VsZWN0LCBwYXJhbXMsIHF1ZXJ5Lmdyb3VwYnkpO1xuICAgIH1cblxuICAgIC8vIEFwcGx5IEhBVklORyBjbGF1c2UgaWYgcHJlc2VudFxuICAgIGlmIChxdWVyeS5oYXZpbmcpIHtcbiAgICAgICAgc2VsZWN0ID0gYXBwbHlIYXZpbmdDbGF1c2Uoc2VsZWN0LCBwYXJhbXMsIHF1ZXJ5LmhhdmluZyk7XG4gICAgfVxuXG4gICAgLy8gQXBwbHkgT1JERVIgQlkgY2xhdXNlIGlmIHByZXNlbnRcbiAgICBpZiAocXVlcnkub3JkZXJieSAmJiBxdWVyeS5vcmRlcmJ5Lmxlbmd0aCA+IDApIHtcbiAgICAgICAgc2VsZWN0ID0gYXBwbHlPcmRlckJ5Q2xhdXNlKHNlbGVjdCwgcXVlcnkub3JkZXJieSk7XG4gICAgfVxuXG4gICAgLy8gQXBwbHkgTElNSVQgY2xhdXNlIGlmIHByZXNlbnRcbiAgICBpZiAocXVlcnkubGltaXQgIT09IG51bGwgJiYgcXVlcnkubGltaXQgIT09IHVuZGVmaW5lZCkge1xuICAgICAgICBzZWxlY3QgPSBzZWxlY3QubGltaXQocXVlcnkubGltaXQpO1xuICAgIH1cblxuICAgIC8vIEFwcGx5IFNBTVBMRSBjbGF1c2UgaWYgcHJlc2VudFxuICAgIGlmIChxdWVyeS5zYW1wbGUgIT09IG51bGwgJiYgcXVlcnkuc2FtcGxlICE9PSB1bmRlZmluZWQpIHtcbiAgICAgICAgc2VsZWN0ID0gc2VsZWN0LnNhbXBsZShxdWVyeS5zYW1wbGUpO1xuICAgIH1cblxuICAgIHJldHVybiBzZWxlY3Q7XG59XG5cbmZ1bmN0aW9uIGludGVycHJldEZ1bmN0aW9uKFxuICAgIGZ1bmM6IEZ1bmN0aW9uRXhwcmVzc2lvbixcbiAgICBwYXJhbXM6IE1hcDxzdHJpbmcsIFBhcmFtPlxuKTogQWdncmVnYXRlTm9kZSB8IEZ1bmN0aW9uTm9kZSB7XG4gICAgY29uc3QgZnVuY05hbWUgPSBmdW5jLm5hbWUudG9Mb3dlckNhc2UoKTtcbiAgICBjb25zdCBhcmdzOiBFeHByTm9kZVtdID0gZnVuYy5hcmdzLm1hcChhID0+IGJ1aWxkRXhwcmVzc2lvbk5vZGUoYSwgcGFyYW1zKSk7XG5cbiAgICAvLyBIYW5kbGUgY29tbW9uIGFnZ3JlZ2F0ZSBmdW5jdGlvbnMgZGlyZWN0bHlcbiAgICBzd2l0Y2ggKGZ1bmNOYW1lKSB7XG4gICAgICAgIGNhc2UgJ3N1bSc6XG4gICAgICAgICAgICByZXR1cm4gc3VtKGFyZ3NbMF0pO1xuICAgICAgICBjYXNlICdhdmcnOlxuICAgICAgICAgICAgcmV0dXJuIGF2ZyhhcmdzWzBdKTtcbiAgICAgICAgY2FzZSAnbWluJzpcbiAgICAgICAgICAgIHJldHVybiBtaW4oYXJnc1swXSk7XG4gICAgICAgIGNhc2UgJ21heCc6XG4gICAgICAgICAgICByZXR1cm4gbWF4KGFyZ3NbMF0pO1xuICAgICAgICBjYXNlICdtb2RlJzpcbiAgICAgICAgICAgIHJldHVybiBtb2RlKGFyZ3NbMF0pO1xuICAgICAgICBjYXNlICdtZWRpYW4nOlxuICAgICAgICAgICAgcmV0dXJuIG1lZGlhbihhcmdzWzBdKTtcbiAgICAgICAgY2FzZSAnY291bnQnOlxuICAgICAgICAgICAgcmV0dXJuIGNvdW50KGFyZ3NbMF0pO1xuICAgICAgICBkZWZhdWx0OlxuICAgICAgICAgICAgLy8gRm9yIG90aGVyIGZ1bmN0aW9ucywgdXNlIGEgZ2VuZXJpYyBhcHByb2FjaFxuICAgICAgICAgICAgcmV0dXJuIG5ldyBGdW5jdGlvbk5vZGUoZnVuY05hbWUsIGFyZ3MpO1xuICAgIH1cbn1cblxuZnVuY3Rpb24gYXBwbHlXaGVyZUNsYXVzZShcbiAgICBxdWVyeTogU2VsZWN0UXVlcnksXG4gICAgcGFyYW1zOiBNYXA8c3RyaW5nLCBQYXJhbT4sXG4gICAgd2hlcmVFeHByOiBCaW5hcnlFeHByZXNzaW9uIHwgTG9naWNhbEV4cHJlc3Npb24gfCBVbmtub3duRXhwcmVzc2lvblxuKTogU2VsZWN0UXVlcnkge1xuICAgIC8vIEhhbmRsZSBkaWZmZXJlbnQgZXhwcmVzc2lvbiB0eXBlc1xuICAgIGlmICh3aGVyZUV4cHIudHlwZSA9PT0gJ2FuZCcgfHwgd2hlcmVFeHByLnR5cGUgPT09ICdvcicpIHtcbiAgICAgICAgLy8gTG9naWNhbCBBTkQvT1IgZXhwcmVzc2lvblxuICAgICAgICByZXR1cm4gYXBwbHlMb2dpY2FsRXhwcmVzc2lvbihxdWVyeSwgcGFyYW1zLCB3aGVyZUV4cHIgYXMgTG9naWNhbEV4cHJlc3Npb24pO1xuICAgIH0gZWxzZSBpZiAod2hlcmVFeHByLnR5cGUgPT09ICd1bmtub3duJykge1xuICAgICAgICAvLyBVbmtub3duIGV4cHJlc3Npb24gLSBwYXNzIHJhdyBTUUxcbiAgICAgICAgcmV0dXJuIHF1ZXJ5LndoZXJlKG5ldyBWZXJiYXRpbU5vZGUoKHdoZXJlRXhwciBhcyBVbmtub3duRXhwcmVzc2lvbikuZXhwcmVzc2lvbikpO1xuICAgIH0gZWxzZSB7XG4gICAgICAgIGNvbnN0IGNvbmRpdGlvbiA9IGJ1aWxkQmluYXJ5RXhwcmVzc2lvbih3aGVyZUV4cHIgYXMgQmluYXJ5RXhwcmVzc2lvbiwgcGFyYW1zKTtcbiAgICAgICAgcmV0dXJuIHF1ZXJ5LndoZXJlKGNvbmRpdGlvbik7XG4gICAgfVxufVxuXG5mdW5jdGlvbiBhcHBseUxvZ2ljYWxFeHByZXNzaW9uKFxuICAgIHF1ZXJ5OiBTZWxlY3RRdWVyeSxcbiAgICBwYXJhbXM6IE1hcDxzdHJpbmcsIFBhcmFtPixcbiAgICBleHByOiBMb2dpY2FsRXhwcmVzc2lvblxuKTogU2VsZWN0UXVlcnkge1xuICAgIGNvbnN0IHsgdHlwZSwgZXhwcmVzc2lvbnMgfSA9IGV4cHI7XG5cbiAgICBpZiAoZXhwcmVzc2lvbnMubGVuZ3RoID09PSAwKSB7XG4gICAgICAgIHJldHVybiBxdWVyeTtcbiAgICB9IGVsc2UgaWYgKGV4cHJlc3Npb25zLmxlbmd0aCA9PT0gMSkge1xuICAgICAgICByZXR1cm4gYXBwbHlXaGVyZUNsYXVzZShcbiAgICAgICAgICAgIHF1ZXJ5LFxuICAgICAgICAgICAgcGFyYW1zLFxuICAgICAgICAgICAgZXhwcmVzc2lvbnNbMF0gYXMgQmluYXJ5RXhwcmVzc2lvbiB8IExvZ2ljYWxFeHByZXNzaW9uIHwgVW5rbm93bkV4cHJlc3Npb25cbiAgICAgICAgKTtcbiAgICB9IGVsc2Uge1xuICAgICAgICBjb25zdCBjb25kaXRpb25zID0gZXhwcmVzc2lvbnMubWFwKGUgPT4gYnVpbGRFeHByZXNzaW9uVmFsdWUoZSwgcGFyYW1zKSk7XG4gICAgICAgIGlmICh0eXBlID09PSAnYW5kJykge1xuICAgICAgICAgICAgcmV0dXJuIHF1ZXJ5LndoZXJlKGFuZCguLi5jb25kaXRpb25zKSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICByZXR1cm4gcXVlcnkud2hlcmUob3IoLi4uY29uZGl0aW9ucykpO1xuICAgICAgICB9XG4gICAgfVxufVxuXG5mdW5jdGlvbiBhcHBseUdyb3VwQnlDbGF1c2UoXG4gICAgcXVlcnk6IFNlbGVjdFF1ZXJ5LFxuICAgIHBhcmFtczogTWFwPHN0cmluZywgUGFyYW0+LFxuICAgIGdyb3VwQnlGaWVsZHM6IChzdHJpbmcgfCBHcm91cEJ5RmllbGQpW11cbik6IFNlbGVjdFF1ZXJ5IHtcbiAgICBjb25zdCBmaWVsZHMgPSBncm91cEJ5RmllbGRzLm1hcChmaWVsZCA9PiB7XG4gICAgICAgIGlmICh0eXBlb2YgZmllbGQgPT09ICdzdHJpbmcnKSB7XG4gICAgICAgICAgICByZXR1cm4gZmllbGQ7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAvLyBHcm91cEJ5RmllbGQgb2JqZWN0XG4gICAgICAgICAgICBpZiAodHlwZW9mIGZpZWxkLmZpZWxkID09PSAnc3RyaW5nJykge1xuICAgICAgICAgICAgICAgIHJldHVybiBmaWVsZC5maWVsZDtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgLy8gRnVuY3Rpb24gZXhwcmVzc2lvbiBpbiBHUk9VUCBCWVxuICAgICAgICAgICAgICAgIHJldHVybiBpbnRlcnByZXRGdW5jdGlvbihmaWVsZC5maWVsZCwgcGFyYW1zKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH0pO1xuXG4gICAgcmV0dXJuIHF1ZXJ5Lmdyb3VwYnkoLi4uZmllbGRzKTtcbn1cblxuZnVuY3Rpb24gYXBwbHlIYXZpbmdDbGF1c2UoXG4gICAgcXVlcnk6IFNlbGVjdFF1ZXJ5LFxuICAgIHBhcmFtczogTWFwPHN0cmluZywgUGFyYW0+LFxuICAgIGhhdmluZ0V4cHI6IEJpbmFyeUV4cHJlc3Npb24gfCBMb2dpY2FsRXhwcmVzc2lvbiB8IFVua25vd25FeHByZXNzaW9uXG4pOiBTZWxlY3RRdWVyeSB7XG4gICAgLy8gSGF2aW5nIGNsYXVzZXMgYXJlIHNpbWlsYXIgdG8gV0hFUkUgY2xhdXNlc1xuICAgIGlmICgndHlwZScgaW4gaGF2aW5nRXhwcikge1xuICAgICAgICAvLyBIYW5kbGUgZGlmZmVyZW50IGV4cHJlc3Npb24gdHlwZXNcbiAgICAgICAgaWYgKGhhdmluZ0V4cHIudHlwZSA9PT0gJ2FuZCcgfHwgaGF2aW5nRXhwci50eXBlID09PSAnb3InKSB7XG4gICAgICAgICAgICAvLyBMb2dpY2FsIEFORC9PUiBleHByZXNzaW9uXG4gICAgICAgICAgICBjb25zdCB7IHR5cGUsIGV4cHJlc3Npb25zIH0gPSBoYXZpbmdFeHByIGFzIExvZ2ljYWxFeHByZXNzaW9uO1xuXG4gICAgICAgICAgICAvLyBCdWlsZCB0aGUgY29uZGl0aW9ucyBhcnJheVxuICAgICAgICAgICAgY29uc3QgY29uZGl0aW9ucyA9IGV4cHJlc3Npb25zLm1hcChlID0+IGJ1aWxkRXhwcmVzc2lvblZhbHVlKGUsIHBhcmFtcykpO1xuXG4gICAgICAgICAgICAvLyBBcHBseSB0aGUgY29uZGl0aW9ucyB1c2luZyB0aGUgYXBwcm9wcmlhdGUgbG9naWNhbCBvcGVyYXRvclxuICAgICAgICAgICAgaWYgKHR5cGUgPT09ICdhbmQnKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHF1ZXJ5LmhhdmluZyhhbmQoLi4uY29uZGl0aW9ucykpO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gcXVlcnkuaGF2aW5nKG9yKC4uLmNvbmRpdGlvbnMpKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSBlbHNlIGlmIChoYXZpbmdFeHByLnR5cGUgPT09ICd1bmtub3duJykge1xuICAgICAgICAgICAgcmV0dXJuIHF1ZXJ5LmhhdmluZyhuZXcgVmVyYmF0aW1Ob2RlKChoYXZpbmdFeHByIGFzIFVua25vd25FeHByZXNzaW9uKS5leHByZXNzaW9uKSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAvLyBCaW5hcnkgZXhwcmVzc2lvbiAoY29tcGFyaXNvbilcbiAgICAgICAgICAgIGNvbnN0IGNvbmRpdGlvbiA9IGJ1aWxkQmluYXJ5RXhwcmVzc2lvbihoYXZpbmdFeHByIGFzIEJpbmFyeUV4cHJlc3Npb24sIHBhcmFtcyk7XG4gICAgICAgICAgICByZXR1cm4gcXVlcnkuaGF2aW5nKGNvbmRpdGlvbik7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICAvLyBGYWxsYmFjayAtIGp1c3QgcGFzcyB0aGUgZXhwcmVzc2lvbiBhcyBpc1xuICAgIHJldHVybiBxdWVyeS5oYXZpbmcoaGF2aW5nRXhwcik7XG59XG5cbmZ1bmN0aW9uIGFwcGx5T3JkZXJCeUNsYXVzZShxdWVyeTogU2VsZWN0UXVlcnksIG9yZGVyQnlJdGVtczogT3JkZXJCeUl0ZW1bXSk6IFNlbGVjdFF1ZXJ5IHtcbiAgICAvLyBVc2luZyBzdHJpbmcgcHJlZml4aW5nIGZvciBkZXNjZW5kaW5nIG9yZGVyIGFzIHRoYXQncyB3aGF0IE1vc2FpYyBTUUwgc3VwcG9ydHNcbiAgICBjb25zdCBvcmRlckJ5RmllbGRzID0gb3JkZXJCeUl0ZW1zLm1hcChpdGVtID0+IHtcbiAgICAgICAgcmV0dXJuIGl0ZW0ub3JkZXIgPT09ICdkZXNjJyA/IGAtJHtpdGVtLmZpZWxkfWAgOiBpdGVtLmZpZWxkO1xuICAgIH0pO1xuXG4gICAgcmV0dXJuIHF1ZXJ5Lm9yZGVyYnkoLi4ub3JkZXJCeUZpZWxkcyk7XG59XG5cbmZ1bmN0aW9uIGJ1aWxkRXhwcmVzc2lvbk5vZGUoZXhwcjogRXhwcmVzc2lvbiwgcGFyYW1zOiBNYXA8c3RyaW5nLCBQYXJhbT4pOiBFeHByTm9kZSB7XG4gICAgaWYgKHR5cGVvZiBleHByID09PSAnc3RyaW5nJyB8fCB0eXBlb2YgZXhwciA9PT0gJ251bWJlcicgfHwgdHlwZW9mIGV4cHIgPT09ICdib29sZWFuJykge1xuICAgICAgICByZXR1cm4gbmV3IExpdGVyYWxOb2RlKGV4cHIpO1xuICAgIH0gZWxzZSBpZiAoJ3R5cGUnIGluIGV4cHIpIHtcbiAgICAgICAgaWYgKGV4cHIudHlwZSA9PT0gJ3BhcmFtZXRlcicpIHtcbiAgICAgICAgICAgIGNvbnN0IG5hbWUgPSAoZXhwciBhcyBQYXJhbWV0ZXJFeHByZXNzaW9uKS5uYW1lO1xuICAgICAgICAgICAgY29uc3QgcGFyYW0gPSBwYXJhbXMuZ2V0KG5hbWUpO1xuICAgICAgICAgICAgaWYgKHBhcmFtID09PSB1bmRlZmluZWQpIHtcbiAgICAgICAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoYFVua25vd24gcGFyYW1ldGVyICR7bmFtZX1gKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHJldHVybiBuZXcgUGFyYW1Ob2RlKHBhcmFtKTtcbiAgICAgICAgfSBlbHNlIGlmIChleHByLnR5cGUgPT09ICd1bmtub3duJykge1xuICAgICAgICAgICAgcmV0dXJuIG5ldyBWZXJiYXRpbU5vZGUoKGV4cHIgYXMgVW5rbm93bkV4cHJlc3Npb24pLmV4cHJlc3Npb24pO1xuICAgICAgICB9IGVsc2UgaWYgKGV4cHIudHlwZSA9PT0gJ2Z1bmN0aW9uJykge1xuICAgICAgICAgICAgcmV0dXJuIGludGVycHJldEZ1bmN0aW9uKGV4cHIgYXMgRnVuY3Rpb25FeHByZXNzaW9uLCBwYXJhbXMpO1xuICAgICAgICB9IGVsc2UgaWYgKGV4cHIudHlwZSA9PT0gJ2FuZCcgfHwgZXhwci50eXBlID09PSAnb3InKSB7XG4gICAgICAgICAgICByZXR1cm4gYnVpbGRMb2dpY2FsRXhwcmVzc2lvbihleHByIGFzIExvZ2ljYWxFeHByZXNzaW9uLCBwYXJhbXMpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgcmV0dXJuIGJ1aWxkQmluYXJ5RXhwcmVzc2lvbihleHByIGFzIEJpbmFyeUV4cHJlc3Npb24sIHBhcmFtcyk7XG4gICAgICAgIH1cbiAgICB9IGVsc2Uge1xuICAgICAgICB0aHJvdyBFcnJvcihgVW5leHBlY3RlZCB0eXBlIGZvciBleHByZXNzaW9uOiAke3R5cGVvZiBleHByfWApO1xuICAgIH1cbn1cblxuLy8gVE9ETzogXCIqXCIgaXMgZ2V0dGluZyBwYXJzZWQgYXMgdW5rbm93blxuZnVuY3Rpb24gYnVpbGRFeHByZXNzaW9uVmFsdWUoZXhwcjogRXhwcmVzc2lvbiwgcGFyYW1zOiBNYXA8c3RyaW5nLCBQYXJhbT4pOiBFeHByVmFsdWUge1xuICAgIGlmICh0eXBlb2YgZXhwciA9PT0gJ3N0cmluZycpIHtcbiAgICAgICAgcmV0dXJuIGV4cHI7XG4gICAgfSBlbHNlIHtcbiAgICAgICAgcmV0dXJuIGJ1aWxkRXhwcmVzc2lvbk5vZGUoZXhwciwgcGFyYW1zKTtcbiAgICB9XG59XG5cbmZ1bmN0aW9uIGJ1aWxkTG9naWNhbEV4cHJlc3Npb24oZXhwcjogTG9naWNhbEV4cHJlc3Npb24sIHBhcmFtczogTWFwPHN0cmluZywgUGFyYW0+KTogRXhwck5vZGUge1xuICAgIGNvbnN0IHsgdHlwZSwgZXhwcmVzc2lvbnMgfSA9IGV4cHI7XG5cbiAgICBpZiAoZXhwcmVzc2lvbnMubGVuZ3RoID09PSAwKSB7XG4gICAgICAgIHJldHVybiBuZXcgTGl0ZXJhbE5vZGUodHJ1ZSk7XG4gICAgfSBlbHNlIGlmIChleHByZXNzaW9ucy5sZW5ndGggPT09IDEpIHtcbiAgICAgICAgcmV0dXJuIGJ1aWxkRXhwcmVzc2lvbk5vZGUoZXhwcmVzc2lvbnNbMF0sIHBhcmFtcyk7XG4gICAgfSBlbHNlIHtcbiAgICAgICAgY29uc3QgY29uZGl0aW9ucyA9IGV4cHJlc3Npb25zLm1hcChlID0+IGJ1aWxkRXhwcmVzc2lvbk5vZGUoZSwgcGFyYW1zKSk7XG4gICAgICAgIGlmICh0eXBlID09PSAnYW5kJykge1xuICAgICAgICAgICAgcmV0dXJuIGFuZCguLi5jb25kaXRpb25zKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHJldHVybiBvciguLi5jb25kaXRpb25zKTtcbiAgICAgICAgfVxuICAgIH1cbn1cblxuZnVuY3Rpb24gYnVpbGRCaW5hcnlFeHByZXNzaW9uKGV4cHI6IEJpbmFyeUV4cHJlc3Npb24sIHBhcmFtczogTWFwPHN0cmluZywgUGFyYW0+KTogQmluYXJ5T3BOb2RlIHtcbiAgICBjb25zdCB7IHR5cGUsIGxlZnQsIHJpZ2h0IH0gPSBleHByO1xuXG4gICAgY29uc3QgbGVmdE9wZXJhbmQgPSBidWlsZEV4cHJlc3Npb25WYWx1ZShsZWZ0LCBwYXJhbXMpO1xuICAgIGNvbnN0IHJpZ2h0T3BlcmFuZCA9IGJ1aWxkRXhwcmVzc2lvbk5vZGUocmlnaHQsIHBhcmFtcyk7XG5cbiAgICAvLyBNYXAgY29tbW9uIGNvbXBhcmlzb24gb3BlcmF0b3JzIHRvIE1vc2FpYyBTUUwgbWV0aG9kc1xuICAgIHN3aXRjaCAodHlwZSkge1xuICAgICAgICBjYXNlICdlcSc6XG4gICAgICAgICAgICByZXR1cm4gZXEobGVmdE9wZXJhbmQsIHJpZ2h0T3BlcmFuZCk7XG4gICAgICAgIGNhc2UgJ25lcSc6XG4gICAgICAgICAgICByZXR1cm4gbmVxKGxlZnRPcGVyYW5kLCByaWdodE9wZXJhbmQpO1xuICAgICAgICBjYXNlICdndCc6XG4gICAgICAgICAgICByZXR1cm4gZ3QobGVmdE9wZXJhbmQsIHJpZ2h0T3BlcmFuZCk7XG4gICAgICAgIGNhc2UgJ2d0ZSc6XG4gICAgICAgICAgICByZXR1cm4gZ3RlKGxlZnRPcGVyYW5kLCByaWdodE9wZXJhbmQpO1xuICAgICAgICBjYXNlICdsdCc6XG4gICAgICAgICAgICByZXR1cm4gbHQobGVmdE9wZXJhbmQsIHJpZ2h0T3BlcmFuZCk7XG4gICAgICAgIGNhc2UgJ2x0ZSc6XG4gICAgICAgICAgICByZXR1cm4gbHRlKGxlZnRPcGVyYW5kLCByaWdodE9wZXJhbmQpO1xuICAgICAgICBjYXNlICdhZGQnOlxuICAgICAgICAgICAgcmV0dXJuIGFkZChsZWZ0T3BlcmFuZCwgcmlnaHRPcGVyYW5kKTtcbiAgICAgICAgY2FzZSAnc3ViJzpcbiAgICAgICAgICAgIHJldHVybiBzdWIobGVmdE9wZXJhbmQsIHJpZ2h0T3BlcmFuZCk7XG4gICAgICAgIGNhc2UgJ211bCc6XG4gICAgICAgICAgICByZXR1cm4gbXVsKGxlZnRPcGVyYW5kLCByaWdodE9wZXJhbmQpO1xuICAgICAgICBjYXNlICdkaXYnOlxuICAgICAgICAgICAgcmV0dXJuIGRpdihsZWZ0T3BlcmFuZCwgcmlnaHRPcGVyYW5kKTtcbiAgICAgICAgZGVmYXVsdDpcbiAgICAgICAgICAgIHJldHVybiBuZXcgQmluYXJ5T3BOb2RlKFxuICAgICAgICAgICAgICAgIHR5cGUsXG4gICAgICAgICAgICAgICAgYnVpbGRFeHByZXNzaW9uTm9kZShsZWZ0LCBwYXJhbXMpLFxuICAgICAgICAgICAgICAgIGJ1aWxkRXhwcmVzc2lvbk5vZGUocmlnaHQsIHBhcmFtcylcbiAgICAgICAgICAgICk7XG4gICAgfVxufVxuIiwgImltcG9ydCB7XG4gICAgUGFyYW0sXG4gICAgU2VsZWN0aW9uLFxuICAgIHRvRGF0YUNvbHVtbnMsXG59IGZyb20gJ2h0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9ucG0vQHV3ZGF0YS9tb3NhaWMtY29yZUAwLjE2LjIvK2VzbSc7XG5pbXBvcnQgeyBTZWxlY3RRdWVyeSB9IGZyb20gJ2h0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9ucG0vQHV3ZGF0YS9tb3NhaWMtc3FsQDAuMTYuMi8rZXNtJztcblxuaW1wb3J0IFBsb3RseSBmcm9tICdodHRwczovL2VzbS5zaC9wbG90bHkuanMtZGlzdC1taW5AMy4wLjEnO1xuaW1wb3J0IHsgVml6Q2xpZW50IH0gZnJvbSAnLi92aXonO1xuXG5leHBvcnQgaW50ZXJmYWNlIFBsb3RseUF4aXNNYXBwaW5ncyB7XG4gICAgeDogc3RyaW5nIHwgbnVsbDtcbiAgICB5OiBzdHJpbmcgfCBudWxsO1xuICAgIHo6IHN0cmluZyB8IG51bGw7XG59XG5cbmV4cG9ydCBpbnRlcmZhY2UgUGxvdGx5RmlndXJlIHtcbiAgICBkYXRhOiBQbG90bHkuRGF0YVtdO1xuICAgIGxheW91dD86IFBhcnRpYWw8UGxvdGx5LkxheW91dD47XG4gICAgY29uZmlnPzogUGFydGlhbDxQbG90bHkuQ29uZmlnPjtcbn1cblxuZXhwb3J0IGNsYXNzIEZpZ3VyZSBleHRlbmRzIFZpekNsaWVudCB7XG4gICAgY29uc3RydWN0b3IoXG4gICAgICAgIHByaXZhdGUgcmVhZG9ubHkgZWxfOiBIVE1MRWxlbWVudCxcbiAgICAgICAgcHJpdmF0ZSByZWFkb25seSBmaWd1cmVfOiBQbG90bHlGaWd1cmUsXG4gICAgICAgIHByaXZhdGUgcmVhZG9ubHkgYXhpc01hcHBpbmdzXzogUGxvdGx5QXhpc01hcHBpbmdzLFxuICAgICAgICB0YWJsZTogc3RyaW5nLFxuICAgICAgICBmaWx0ZXJCeTogU2VsZWN0aW9uLFxuICAgICAgICBxdWVyaWVzOiBTZWxlY3RRdWVyeVtdLFxuICAgICAgICBwYXJhbXM6IE1hcDxzdHJpbmcsIFBhcmFtPlxuICAgICkge1xuICAgICAgICBzdXBlcih0YWJsZSwgZmlsdGVyQnksIHF1ZXJpZXMsIHBhcmFtcyk7XG4gICAgfVxuXG4gICAgcXVlcnlSZXN1bHQoZGF0YTogYW55KSB7XG4gICAgICAgIC8vIHJlc29sdmUgZGF0YVxuICAgICAgICBjb25zdCBjb2x1bW5zID0gdG9EYXRhQ29sdW1ucyhkYXRhKS5jb2x1bW5zIGFzIFJlY29yZDxzdHJpbmcsIEFycmF5TGlrZTx1bmtub3duPj47XG4gICAgICAgIGNvbnN0IHRhYmxlID0gYmluZFRhYmxlKHRoaXMuZmlndXJlXywgdGhpcy5heGlzTWFwcGluZ3NfLCBjb2x1bW5zKTtcblxuICAgICAgICBjb25zb2xlLmxvZyh0aGlzLmZpZ3VyZV8uZGF0YSk7XG4gICAgICAgIGNvbnNvbGUubG9nKCctLS0tLS0tLS0nKTtcbiAgICAgICAgY29uc29sZS5sb2codGFibGUpO1xuXG4gICAgICAgIC8vIHJlc29sdmUgbGF5b3V0XG4gICAgICAgIGNvbnN0IGxheW91dCA9IHRoaXMuZmlndXJlXy5sYXlvdXQgfHwge307XG4gICAgICAgIGxheW91dC5hdXRvc2l6ZSA9IHRydWU7XG5cbiAgICAgICAgLy8gcmVzb2x2ZSBjb25maWdcbiAgICAgICAgY29uc3QgY29uZmlnID0gdGhpcy5maWd1cmVfLmNvbmZpZyB8fCB7fTtcbiAgICAgICAgY29uZmlnLnJlc3BvbnNpdmUgPSB0cnVlO1xuXG4gICAgICAgIC8vIHJlbmRlclxuICAgICAgICBQbG90bHkucmVhY3QodGhpcy5lbF8sIHRhYmxlLCBsYXlvdXQsIGNvbmZpZyk7XG4gICAgICAgIHJldHVybiB0aGlzO1xuICAgIH1cbn1cblxuZnVuY3Rpb24gYmluZFRhYmxlKFxuICAgIGZpZ3VyZTogUGxvdGx5RmlndXJlLFxuICAgIGF4aXNNYXBwaW5nczogUGxvdGx5QXhpc01hcHBpbmdzLFxuICAgIGNvbHVtbnM6IFJlY29yZDxzdHJpbmcsIEFycmF5TGlrZTx1bmtub3duPj5cbik6IFBsb3RseS5EYXRhW10ge1xuICAgIC8vIGRvbid0IG11dGF0ZSB0aGUgcGFzc2VkIHRyYWNlc1xuICAgIGNvbnN0IHRyYWNlcyA9IHN0cnVjdHVyZWRDbG9uZShmaWd1cmUuZGF0YSk7XG5cbiAgICAvLyBDaGVjayBpZiB0aGlzIGlzIGEgbXVsdGktdHJhY2UgZmlndXJlXG4gICAgY29uc3QgaXNNdWx0aVRyYWNlID0gdHJhY2VzLmxlbmd0aCA+IDE7XG5cbiAgICAvLyBFYXJseSByZXR1cm4gZm9yIHNpbmdsZS10cmFjZSBmaWd1cmVzXG4gICAgaWYgKCFpc011bHRpVHJhY2UpIHtcbiAgICAgICAgY29uc3QgdHJhY2UgPSB0cmFjZXNbMF07XG4gICAgICAgIGNvbnN0IG1hcHBpbmcgPSBjb2x1bW5NYXBwaW5nKHRyYWNlLCBPYmplY3Qua2V5cyhjb2x1bW5zKSwgYXhpc01hcHBpbmdzKTtcblxuICAgICAgICBmb3IgKGNvbnN0IFthdHRyLCBjb2xdIG9mIE9iamVjdC5lbnRyaWVzKG1hcHBpbmcpKSB7XG4gICAgICAgICAgICBjb25zdCBhcnIgPSBjb2x1bW5zW2NvbF07XG4gICAgICAgICAgICBpZiAoYXJyKSB7XG4gICAgICAgICAgICAgICAgc2V0RGF0YSh0cmFjZSwgYXR0ci5zcGxpdCgnLicpLCBhcnIpO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICBjb25zb2xlLndhcm4oYENvbHVtbiBcIiR7Y29sfVwiIG5vdCBmb3VuZCBpbiB0YWJsZWApO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIHJldHVybiB0cmFjZXM7XG4gICAgfVxuXG4gICAgLy8gRm9yIG11bHRpLXRyYWNlIGZpZ3VyZXMsIHdlIG5lZWQgdG8gZXhhbWluZSBob3cgdHJhY2VzIGFyZSByZWxhdGVkIHRvIGRhdGFcblxuICAgIC8vIEZpcnN0LCBkZXRlY3QgaWYgdGhpcyBpcyBhIFBsb3RseSBFeHByZXNzIGZpZ3VyZSB3aXRoIHNwZWNpZmljIHByb3BlcnRpZXNcbiAgICBjb25zdCBpc1Bsb3RseUV4cHJlc3NGaWd1cmUgPSBkZXRlY3RQbG90bHlFeHByZXNzRmlndXJlKHRyYWNlcyk7XG5cbiAgICAvLyBDaGVjayBmb3Igc3BlY2lhbCBjYXNlcyBsaWtlIGZhY2V0cyB3aGljaCBoYXZlIHNwZWNpZmljIGhhbmRsaW5nIG5lZWRzXG4gICAgY29uc3QgaGFzRmFjZXRzID0gZGV0ZWN0RmFjZXRTdWJwbG90cyh0cmFjZXMsIGZpZ3VyZS5sYXlvdXQpO1xuXG4gICAgLy8gSGFuZGxlIGZhY2V0ZWQgZmlndXJlcyBzcGVjaWFsbHkgc2luY2UgdGhleSBrZWVwIGFsbCBkYXRhIGluIGVhY2ggdHJhY2UgYnV0IHVzZSBkaWZmZXJlbnQgZG9tYWluc1xuICAgIGlmIChoYXNGYWNldHMpIHtcbiAgICAgICAgLy8gRm9yIGZhY2V0ZWQgcGxvdHMsIGVhY2ggdHJhY2UgcmVwcmVzZW50cyBhIGRpZmZlcmVudCBzdWJwbG90IGJ1dCBoYXMgYWxsIHRoZSBkYXRhXG4gICAgICAgIC8vIFdlIG5lZWQgdG8gYXBwbHkgYWxsIGRhdGEgdG8gZWFjaCB0cmFjZVxuICAgICAgICB0cmFjZXMuZm9yRWFjaCgodHJhY2U6IFBsb3RseS5EYXRhKSA9PiB7XG4gICAgICAgICAgICBjb25zdCBtYXBwaW5nID0gY29sdW1uTWFwcGluZyh0cmFjZSwgT2JqZWN0LmtleXMoY29sdW1ucyksIGF4aXNNYXBwaW5ncyk7XG4gICAgICAgICAgICBmb3IgKGNvbnN0IFthdHRyLCBjb2xdIG9mIE9iamVjdC5lbnRyaWVzKG1hcHBpbmcpKSB7XG4gICAgICAgICAgICAgICAgY29uc3QgYXJyID0gY29sdW1uc1tjb2xdO1xuICAgICAgICAgICAgICAgIGlmIChhcnIpIHtcbiAgICAgICAgICAgICAgICAgICAgc2V0RGF0YSh0cmFjZSwgYXR0ci5zcGxpdCgnLicpLCBhcnIpO1xuICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIGNvbnNvbGUud2FybihgQ29sdW1uIFwiJHtjb2x9XCIgbm90IGZvdW5kIGluIHRhYmxlYCk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICAgICAgcmV0dXJuIHRyYWNlcztcbiAgICB9XG5cbiAgICAvLyBUcnkgdG8gaWRlbnRpZnkgY2F0ZWdvcmljYWwgY29sdW1ucyB0aGF0IG1pZ2h0IGJlIHVzZWQgZm9yIHRyYWNlIHNlcGFyYXRpb25cbiAgICBjb25zdCBwb3NzaWJsZUNhdENvbHVtbnMgPSBmaW5kUG9zc2libGVDYXRlZ29yaWNhbENvbHVtbnModHJhY2VzLCBjb2x1bW5zKTtcblxuICAgIC8vIEdyb3VwIHRyYWNlcyBieSB0eXBlIHRvIGhhbmRsZSBkaWZmZXJlbnQgdHJhY2UgdHlwZXMgd2l0aCBkaWZmZXJlbnQgc3RyYXRlZ2llc1xuICAgIGNvbnN0IHRyYWNlc0J5VHlwZSA9IGdyb3VwVHJhY2VzQnlUeXBlKHRyYWNlcyk7XG5cbiAgICAvLyBGb3IgZWFjaCB0cmFjZSwgZGV0ZXJtaW5lIGhvdyB0byBtYXAgdGhlIGRhdGFcbiAgICB0cmFjZXMuZm9yRWFjaCgodHJhY2U6IFBsb3RseS5EYXRhLCBfdHJhY2VJbmRleDogbnVtYmVyKSA9PiB7XG4gICAgICAgIC8vIE1hcCB0aGUgY29sdW1ucyBmb3IgdGhpcyB0cmFjZVxuICAgICAgICBjb25zdCBtYXBwaW5nID0gY29sdW1uTWFwcGluZyh0cmFjZSwgT2JqZWN0LmtleXMoY29sdW1ucyksIGF4aXNNYXBwaW5ncyk7XG5cbiAgICAgICAgLy8gVHJ5IHRvIGRldGVybWluZSB3aGljaCByb3dzIGJlbG9uZyB0byB0aGlzIHRyYWNlXG4gICAgICAgIGxldCBpbmRleEFycmF5OiBudW1iZXJbXSB8IHVuZGVmaW5lZCA9IHVuZGVmaW5lZDtcblxuICAgICAgICAvLyBEaWZmZXJlbnQgYXBwcm9hY2hlcyBmb3IgdHJhY2UgZmlsdGVyaW5nXG4gICAgICAgIGlmIChpc1Bsb3RseUV4cHJlc3NGaWd1cmUpIHtcbiAgICAgICAgICAgIC8vIEZvciBQbG90bHkgRXhwcmVzcyBmaWd1cmVzLCB1c2UgdHJhY2UgbmFtZSBhbmQgY2F0ZWdvcmljYWwgY29sdW1uc1xuICAgICAgICAgICAgaW5kZXhBcnJheSA9IGZpbmRJbmRpY2VzRm9yUGxvdGx5RXhwcmVzc1RyYWNlKHRyYWNlLCBwb3NzaWJsZUNhdENvbHVtbnMsIGNvbHVtbnMpO1xuICAgICAgICB9XG5cbiAgICAgICAgLy8gSWYgd2UgY291bGRuJ3QgZ2V0IGluZGljZXMgZm9yIGEgUEUgdHJhY2Ugb3IgdGhpcyBpcyBhIGN1c3RvbSBmaWd1cmUsIHRyeSBvdGhlciBhcHByb2FjaGVzXG4gICAgICAgIGlmICghaW5kZXhBcnJheSkge1xuICAgICAgICAgICAgY29uc3QgdHJhY2VBbnkgPSB0cmFjZSBhcyBhbnk7XG5cbiAgICAgICAgICAgIC8vIEZpcnN0LCB0cnkgdG8gdXNlIHRyYWNlIG1ldGFkYXRhIGRpcmVjdGx5IGlmIGF2YWlsYWJsZVxuICAgICAgICAgICAgaWYgKGdldFByb3A8YW55W10+KHRyYWNlQW55LCAnX2luZGV4JykgIT09IHVuZGVmaW5lZCkge1xuICAgICAgICAgICAgICAgIGNvbnN0IGluZGljZXMgPSBnZXRQcm9wPGFueVtdPih0cmFjZUFueSwgJ19pbmRleCcpO1xuICAgICAgICAgICAgICAgIGlmIChBcnJheS5pc0FycmF5KGluZGljZXMpKSB7XG4gICAgICAgICAgICAgICAgICAgIGluZGV4QXJyYXkgPSBpbmRpY2VzIGFzIG51bWJlcltdO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIC8vIE5leHQsIGxvb2sgZm9yIGZpbHRlciBleHByZXNzaW9uIGluIHRoZSB0cmFjZVxuICAgICAgICAgICAgZWxzZSBpZiAoZ2V0UHJvcDxzdHJpbmc+KHRyYWNlQW55LCAnX2ZpbHRlcicpICE9PSB1bmRlZmluZWQpIHtcbiAgICAgICAgICAgICAgICBjb25zdCBmaWx0ZXJFeHByID0gZ2V0UHJvcDxzdHJpbmc+KHRyYWNlQW55LCAnX2ZpbHRlcicpO1xuICAgICAgICAgICAgICAgIGlmICh0eXBlb2YgZmlsdGVyRXhwciA9PT0gJ3N0cmluZycpIHtcbiAgICAgICAgICAgICAgICAgICAgaW5kZXhBcnJheSA9IGFwcGx5RmlsdGVyRXhwcmVzc2lvbihmaWx0ZXJFeHByLCBjb2x1bW5zKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICAvLyBUcnkgdmFyaW91cyBvdGhlciB0cmFjZSBwcm9wZXJ0aWVzIHRoYXQgbWlnaHQgaW5kaWNhdGUgZGF0YSBtYXBwaW5nXG4gICAgICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgICAgICBpbmRleEFycmF5ID0gaW5mZXJJbmRpY2VzRnJvbVRyYWNlUHJvcGVydGllcyh0cmFjZSwgY29sdW1ucywgcG9zc2libGVDYXRDb2x1bW5zKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuXG4gICAgICAgIC8vIElmIHdlJ3JlIGRlYWxpbmcgd2l0aCB0aGUgc2FtZSB0cmFjZSB0eXBlIHJlcGVhdGVkIG11bHRpcGxlIHRpbWVzLFxuICAgICAgICAvLyB0aGUgdHJhY2VzIG1heSBiZSBzcGxpdCBieSBjYXRlZ29yaWNhbCB2YXJpYWJsZVxuICAgICAgICBjb25zdCB0cmFjZVR5cGUgPSBnZXRQcm9wPHN0cmluZz4odHJhY2UsICd0eXBlJykgfHwgJ3NjYXR0ZXInO1xuICAgICAgICBjb25zdCB0cmFjZXNPZlNhbWVUeXBlID0gdHJhY2VzQnlUeXBlW3RyYWNlVHlwZV0gfHwgW107XG5cbiAgICAgICAgaWYgKCFpbmRleEFycmF5ICYmIHRyYWNlc09mU2FtZVR5cGUubGVuZ3RoID4gMSkge1xuICAgICAgICAgICAgLy8gV2UgbWF5IG5lZWQgdG8gc3BsaXQgYnkgaW5kZXggYmFzZWQgb24gdHJhY2UgcG9zaXRpb25cbiAgICAgICAgICAgIGNvbnN0IHRyYWNlUG9zaXRpb24gPSB0cmFjZXNPZlNhbWVUeXBlLmluZGV4T2YodHJhY2UpO1xuICAgICAgICAgICAgaWYgKHRyYWNlUG9zaXRpb24gIT09IC0xICYmIHRyYWNlUG9zaXRpb24gPCB0cmFjZXNPZlNhbWVUeXBlLmxlbmd0aCkge1xuICAgICAgICAgICAgICAgIC8vIFRyeSBzcGxpdHRpbmcgdGhlIGRhdGEgZXZlbmx5IGFtb25nIHRyYWNlcyBvZiB0aGUgc2FtZSB0eXBlXG4gICAgICAgICAgICAgICAgY29uc3QgZGF0YUxlbmd0aCA9IE9iamVjdC52YWx1ZXMoY29sdW1ucylbMF0/Lmxlbmd0aCB8fCAwO1xuICAgICAgICAgICAgICAgIGNvbnN0IGNodW5rU2l6ZSA9IE1hdGguY2VpbChkYXRhTGVuZ3RoIC8gdHJhY2VzT2ZTYW1lVHlwZS5sZW5ndGgpO1xuICAgICAgICAgICAgICAgIGNvbnN0IHN0YXJ0SWR4ID0gdHJhY2VQb3NpdGlvbiAqIGNodW5rU2l6ZTtcbiAgICAgICAgICAgICAgICBjb25zdCBlbmRJZHggPSBNYXRoLm1pbihzdGFydElkeCArIGNodW5rU2l6ZSwgZGF0YUxlbmd0aCk7XG4gICAgICAgICAgICAgICAgaW5kZXhBcnJheSA9IEFycmF5LmZyb20oeyBsZW5ndGg6IGVuZElkeCAtIHN0YXJ0SWR4IH0sIChfLCBpKSA9PiBzdGFydElkeCArIGkpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG5cbiAgICAgICAgLy8gQXBwbHkgdGhlIGRhdGEgZnJvbSBjb2x1bW5zIHRvIHRoZSB0cmFjZVxuICAgICAgICBmb3IgKGNvbnN0IFthdHRyLCBjb2xdIG9mIE9iamVjdC5lbnRyaWVzKG1hcHBpbmcpKSB7XG4gICAgICAgICAgICBjb25zdCBhcnIgPSBjb2x1bW5zW2NvbF07XG4gICAgICAgICAgICBpZiAoYXJyKSB7XG4gICAgICAgICAgICAgICAgaWYgKGluZGV4QXJyYXkgJiYgaW5kZXhBcnJheS5sZW5ndGggPiAwKSB7XG4gICAgICAgICAgICAgICAgICAgIC8vIEZpbHRlciB0aGUgYXJyYXkgdG8gb25seSBpbmNsdWRlIHZhbHVlcyBhdCBzcGVjaWZpZWQgaW5kaWNlc1xuICAgICAgICAgICAgICAgICAgICBjb25zdCBmaWx0ZXJlZEFyciA9IEFycmF5LmZyb20oYXJyKS5maWx0ZXIoKF8sIGkpID0+IGluZGV4QXJyYXkhLmluY2x1ZGVzKGkpKTtcbiAgICAgICAgICAgICAgICAgICAgc2V0RGF0YSh0cmFjZSwgYXR0ci5zcGxpdCgnLicpLCBmaWx0ZXJlZEFycik7XG4gICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gTm8gZmlsdGVyaW5nIHJlcXVpcmVkIG9yIHVuYWJsZSB0byBkZXRlcm1pbmUgZmlsdGVyaW5nIGxvZ2ljLFxuICAgICAgICAgICAgICAgICAgICAvLyBzbyB1c2UgYWxsIGRhdGEgKGZhbGxpbmcgYmFjayB0byBvcmlnaW5hbCBiZWhhdmlvcilcbiAgICAgICAgICAgICAgICAgICAgc2V0RGF0YSh0cmFjZSwgYXR0ci5zcGxpdCgnLicpLCBhcnIpO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgY29uc29sZS53YXJuKGBDb2x1bW4gXCIke2NvbH1cIiBub3QgZm91bmQgaW4gdGFibGVgKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH0pO1xuXG4gICAgcmV0dXJuIHRyYWNlcztcbn1cblxuZnVuY3Rpb24gY29sdW1uTWFwcGluZyhcbiAgICB0cmFjZTogUGxvdGx5LkRhdGEsXG4gICAgY29sczogc3RyaW5nW10sXG4gICAgYXhpc01hcHBpbmdzOiBQbG90bHlBeGlzTWFwcGluZ3Ncbik6IFJlY29yZDxzdHJpbmcsIHN0cmluZz4ge1xuICAgIGNvbnN0IG1hcDogUmVjb3JkPHN0cmluZywgc3RyaW5nPiA9IHt9O1xuICAgIGNvbnN0IGxjID0gY29scy5tYXAoYyA9PiBjLnRvTG93ZXJDYXNlKCkpO1xuXG4gICAgZm9yIChjb25zdCBwIG9mIGFycmF5UHJvcHModHJhY2UpKSB7XG4gICAgICAgIGNvbnN0IHNpbXBsZSA9IHAuc3BsaXQoJy4nKS5wb3AoKSEudG9Mb3dlckNhc2UoKTtcbiAgICAgICAgY29uc3QgaSA9IGxjLmluZGV4T2Yoc2ltcGxlKTtcbiAgICAgICAgaWYgKGkgPT09IC0xKSBjb250aW51ZTtcblxuICAgICAgICBjb25zdCBleGlzdHMgPSBwLnNwbGl0KCcuJykucmVkdWNlPHVua25vd24+KChvLCBrKSA9PiAobyBhcyBhbnkpPy5ba10sIHRyYWNlKSAhPT0gdW5kZWZpbmVkO1xuICAgICAgICBpZiAoZXhpc3RzKSBtYXBbcF0gPSBjb2xzW2ldO1xuICAgIH1cblxuICAgIC8vIGZpbGwgeFxuICAgIGNvbnN0IG5lZWRzWCA9ICFtYXAueCAmJiAoIWlzT3JpZW50YWJsZSh0cmFjZSkgfHwgdHJhY2Uub3JpZW50YXRpb24gIT09ICdoJyk7XG4gICAgaWYgKG5lZWRzWCAmJiBheGlzTWFwcGluZ3MueCkge1xuICAgICAgICBtYXAueCA9IGF4aXNNYXBwaW5ncy54O1xuICAgIH1cblxuICAgIC8vIGZpbGwgeVxuICAgIGNvbnN0IG5lZWRzWSA9ICFtYXAueSAmJiAoaXNPcmllbnRhYmxlKHRyYWNlKSAmJiB0cmFjZS5vcmllbnRhdGlvbiA9PT0gJ2gnID8gZmFsc2UgOiB0cnVlKTtcbiAgICBpZiAobmVlZHNZICYmIGF4aXNNYXBwaW5ncy55KSB7XG4gICAgICAgIG1hcC55ID0gYXhpc01hcHBpbmdzLnk7XG4gICAgfVxuXG4gICAgLy8gb3B0aW9uYWwgeiBmb3IgMy1EIHRyYWNlc1xuICAgIGNvbnN0IGlzM2QgPSBbJ3NjYXR0ZXIzZCcsICdzdXJmYWNlJywgJ21lc2gzZCddLmluY2x1ZGVzKHRyYWNlLnR5cGUgPz8gJycpO1xuICAgIGlmIChpczNkICYmICFtYXAueiAmJiBheGlzTWFwcGluZ3Mueikge1xuICAgICAgICBtYXAueiA9IGF4aXNNYXBwaW5ncy56O1xuICAgIH1cblxuICAgIHJldHVybiBtYXA7XG59XG5cbmZ1bmN0aW9uIHNldERhdGEodHJhY2U6IFBsb3RseS5EYXRhLCBwYXRoOiBzdHJpbmdbXSwgdmFsOiB1bmtub3duKSB7XG4gICAgY29uc3QgbGFzdCA9IHBhdGgucG9wKCkhO1xuICAgIGxldCBjdXIgPSB0cmFjZSBhcyBSZWNvcmQ8c3RyaW5nLCB1bmtub3duPjtcbiAgICBmb3IgKGNvbnN0IGsgb2YgcGF0aCkge1xuICAgICAgICBpZiAoY3VyW2tdID09IG51bGwgfHwgdHlwZW9mIGN1cltrXSAhPT0gJ29iamVjdCcpIGN1cltrXSA9IHt9O1xuICAgICAgICBjdXIgPSBjdXJba10gYXMgUmVjb3JkPHN0cmluZywgdW5rbm93bj47XG4gICAgfVxuICAgIGN1cltsYXN0XSA9IHZhbDtcbn1cblxuZnVuY3Rpb24gYXJyYXlQcm9wcyhvYmo6IGFueSwgcHJlZml4ID0gJycpOiBzdHJpbmdbXSB7XG4gICAgcmV0dXJuIE9iamVjdC5lbnRyaWVzKG9iaikuZmxhdE1hcCgoW2ssIHZdKSA9PlxuICAgICAgICBBcnJheS5pc0FycmF5KHYpIHx8IEFycmF5QnVmZmVyLmlzVmlldyh2KVxuICAgICAgICAgICAgPyBbYCR7cHJlZml4fSR7a31gXVxuICAgICAgICAgICAgOiB0eXBlb2YgdiA9PT0gJ29iamVjdCcgJiYgdiAhPT0gbnVsbFxuICAgICAgICAgICAgICA/IGFycmF5UHJvcHModiwgYCR7cHJlZml4fSR7a30uYClcbiAgICAgICAgICAgICAgOiBbXVxuICAgICk7XG59XG5cbmludGVyZmFjZSBPcmllbnRhYmxlVHJhY2Uge1xuICAgIG9yaWVudGF0aW9uPzogJ2gnIHwgJ3YnO1xufVxuXG5mdW5jdGlvbiBpc09yaWVudGFibGUodDogUGxvdGx5LkRhdGEpOiB0IGlzIFBsb3RseS5EYXRhICYgT3JpZW50YWJsZVRyYWNlIHtcbiAgICByZXR1cm4gJ29yaWVudGF0aW9uJyBpbiB0O1xufVxuXG4vKipcbiAqIEdyb3VwcyB0cmFjZXMgYnkgdGhlaXIgdHlwZSBmb3IgZWFzaWVyIHByb2Nlc3NpbmdcbiAqL1xuZnVuY3Rpb24gZ3JvdXBUcmFjZXNCeVR5cGUodHJhY2VzOiBQbG90bHkuRGF0YVtdKTogUmVjb3JkPHN0cmluZywgUGxvdGx5LkRhdGFbXT4ge1xuICAgIGNvbnN0IHJlc3VsdDogUmVjb3JkPHN0cmluZywgUGxvdGx5LkRhdGFbXT4gPSB7fTtcblxuICAgIHRyYWNlcy5mb3JFYWNoKHRyYWNlID0+IHtcbiAgICAgICAgY29uc3QgdHlwZSA9IHRyYWNlLnR5cGUgfHwgJ3NjYXR0ZXInOyAvLyBEZWZhdWx0IHRvIHNjYXR0ZXIgaWYgbm8gdHlwZSBzcGVjaWZpZWRcbiAgICAgICAgaWYgKCFyZXN1bHRbdHlwZV0pIHtcbiAgICAgICAgICAgIHJlc3VsdFt0eXBlXSA9IFtdO1xuICAgICAgICB9XG4gICAgICAgIHJlc3VsdFt0eXBlXS5wdXNoKHRyYWNlKTtcbiAgICB9KTtcblxuICAgIHJldHVybiByZXN1bHQ7XG59XG5cbi8qKlxuICogVHlwZS1zYWZlIHByb3BlcnR5IGFjY2Vzc29yIGZvciBQbG90bHkgdHJhY2Ugb2JqZWN0c1xuICogQWxsb3dzIGFjY2Vzc2luZyBwcm9wZXJ0aWVzIHRoYXQgbWlnaHQgbm90IGJlIGRlZmluZWQgaW4gYWxsIHRyYWNlIHR5cGVzXG4gKi9cbmZ1bmN0aW9uIGdldFByb3A8VD4ob2JqOiBhbnksIHByb3A6IHN0cmluZywgZGVmYXVsdFZhbD86IFQpOiBUIHwgdW5kZWZpbmVkIHtcbiAgICByZXR1cm4gb2JqICYmIHByb3AgaW4gb2JqID8gb2JqW3Byb3BdIDogZGVmYXVsdFZhbDtcbn1cblxuLyoqXG4gKiBEZXRlY3RzIGlmIGEgZmlndXJlIGlzIGxpa2VseSBjcmVhdGVkIHdpdGggUGxvdGx5IEV4cHJlc3NcbiAqL1xuZnVuY3Rpb24gZGV0ZWN0UGxvdGx5RXhwcmVzc0ZpZ3VyZSh0cmFjZXM6IFBsb3RseS5EYXRhW10pOiBib29sZWFuIHtcbiAgICAvLyBDb21tb24gY2hhcmFjdGVyaXN0aWNzIG9mIFBsb3RseSBFeHByZXNzIGZpZ3VyZXNcbiAgICByZXR1cm4gdHJhY2VzLnNvbWUodHJhY2UgPT4ge1xuICAgICAgICAvLyBDYXN0IHRyYWNlIHRvIGFueSB0byBzYWZlbHkgYWNjZXNzIGFsbCBwcm9wZXJ0aWVzXG4gICAgICAgIGNvbnN0IHQgPSB0cmFjZSBhcyBhbnk7XG5cbiAgICAgICAgLy8gUGxvdGx5IEV4cHJlc3MgdXN1YWxseSBhZGRzIG1ldGFkYXRhIHRvIHRyYWNlc1xuICAgICAgICBpZiAodC5fcHggIT09IHVuZGVmaW5lZCB8fCB0Ll9wbG90bHlFeHByZXNzRGVmYXVsdHMgIT09IHVuZGVmaW5lZCkge1xuICAgICAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICAgIH1cblxuICAgICAgICAvLyBPZnRlbiBoYXZlIHN0YW5kYXJkIGxlZ2VuZCBncm91cHMgb3IgcGF0dGVybiBtYXRjaGluZyBmb3IgaG92ZXJcbiAgICAgICAgY29uc3QgbGVnZW5kZ3JvdXAgPSBnZXRQcm9wPHN0cmluZz4odCwgJ2xlZ2VuZGdyb3VwJyk7XG4gICAgICAgIGlmIChsZWdlbmRncm91cCAmJiB0eXBlb2YgbGVnZW5kZ3JvdXAgPT09ICdzdHJpbmcnICYmIGxlZ2VuZGdyb3VwLmluY2x1ZGVzKCc6JykpIHtcbiAgICAgICAgICAgIHJldHVybiB0cnVlO1xuICAgICAgICB9XG5cbiAgICAgICAgLy8gU3BlY2lmaWMgdHJhY2UgbmFtaW5nIHBhdHRlcm5zIGluIG5ld2VyIHZlcnNpb25zXG4gICAgICAgIGNvbnN0IG5hbWUgPSBnZXRQcm9wPHN0cmluZyB8IG51bWJlcj4odCwgJ25hbWUnKTtcbiAgICAgICAgaWYgKG5hbWUgIT09IHVuZGVmaW5lZCAmJiB0eXBlb2YgbmFtZSA9PT0gJ3N0cmluZycpIHtcbiAgICAgICAgICAgIGlmIChuYW1lLmluY2x1ZGVzKCcgPScpIHx8IG5hbWUubWF0Y2goL15bYS16QS1aX10rPVthLXpBLVowLTlfXSskLykpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuXG4gICAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9KTtcbn1cblxuLyoqXG4gKiBEZXRlY3RzIGlmIGEgZmlndXJlIGhhcyBmYWNldCBzdWJwbG90c1xuICovXG5mdW5jdGlvbiBkZXRlY3RGYWNldFN1YnBsb3RzKHRyYWNlczogUGxvdGx5LkRhdGFbXSwgbGF5b3V0PzogUGFydGlhbDxQbG90bHkuTGF5b3V0Pik6IGJvb2xlYW4ge1xuICAgIC8vIEZpcnN0IGNoZWNrIGxheW91dCBmb3IgZmFjZXQgZ3JpZCBwcm9wZXJ0aWVzXG4gICAgaWYgKGxheW91dCkge1xuICAgICAgICAvLyBDaGVjayBmb3IgZ3JpZCBzdHJ1Y3R1cmUgaW4gbGF5b3V0XG4gICAgICAgIGNvbnN0IGhhc0dyaWRTdHJ1Y3R1cmUgPVxuICAgICAgICAgICAgbGF5b3V0LmdyaWQgIT09IHVuZGVmaW5lZCB8fFxuICAgICAgICAgICAgT2JqZWN0LmtleXMobGF5b3V0KS5zb21lKGtleSA9PiBrZXkuc3RhcnRzV2l0aCgneGF4aXMnKSAmJiBrZXkgIT09ICd4YXhpcycpIHx8XG4gICAgICAgICAgICBPYmplY3Qua2V5cyhsYXlvdXQpLnNvbWUoa2V5ID0+IGtleS5zdGFydHNXaXRoKCd5YXhpcycpICYmIGtleSAhPT0gJ3lheGlzJyk7XG5cbiAgICAgICAgaWYgKGhhc0dyaWRTdHJ1Y3R1cmUpIHJldHVybiB0cnVlO1xuICAgIH1cblxuICAgIC8vIFRoZW4gY2hlY2sgdHJhY2VzIGZvciBmYWNldC1zcGVjaWZpYyBwcm9wZXJ0aWVzXG4gICAgcmV0dXJuIHRyYWNlcy5zb21lKHRyYWNlID0+IHtcbiAgICAgICAgLy8gU2FmZWx5IGNoZWNrIGZvciBzdWJwbG90IHByb3BlcnRpZXMgdXNpbmcgb3VyIGhlbHBlclxuICAgICAgICBjb25zdCB4YXhpcyA9IGdldFByb3A8c3RyaW5nPih0cmFjZSwgJ3hheGlzJyk7XG4gICAgICAgIGNvbnN0IHlheGlzID0gZ2V0UHJvcDxzdHJpbmc+KHRyYWNlLCAneWF4aXMnKTtcbiAgICAgICAgY29uc3QgaGFzU3VicGxvdCA9IGdldFByb3A8YW55Pih0cmFjZSBhcyBhbnksICdfc3VicGxvdCcpICE9PSB1bmRlZmluZWQ7XG5cbiAgICAgICAgLy8gVHJhY2VzIGluIGZhY2V0IHBsb3RzIG9mdGVuIGhhdmUgc3BlY2lmaWMgc3VicGxvdCBhc3NpZ25tZW50c1xuICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgKHhheGlzICE9PSB1bmRlZmluZWQgJiYgeGF4aXMgIT09ICd4JykgfHxcbiAgICAgICAgICAgICh5YXhpcyAhPT0gdW5kZWZpbmVkICYmIHlheGlzICE9PSAneScpIHx8XG4gICAgICAgICAgICAvLyBTb21lIFBsb3RseSBFeHByZXNzIGZhY2V0IHBsb3RzIGNvbnRhaW4gdGhpcyBtZXRhIGluZm9ybWF0aW9uXG4gICAgICAgICAgICBoYXNTdWJwbG90XG4gICAgICAgICk7XG4gICAgfSk7XG59XG5cbi8qKlxuICogRmluZCBhcHByb3ByaWF0ZSBpbmRpY2VzIGZvciBhIFBsb3RseSBFeHByZXNzIHRyYWNlXG4gKi9cbmZ1bmN0aW9uIGZpbmRJbmRpY2VzRm9yUGxvdGx5RXhwcmVzc1RyYWNlKFxuICAgIHRyYWNlOiBQbG90bHkuRGF0YSxcbiAgICBjYXRlZ29yaWNhbENvbHVtbnM6IHN0cmluZ1tdLFxuICAgIGNvbHVtbnM6IFJlY29yZDxzdHJpbmcsIEFycmF5TGlrZTx1bmtub3duPj5cbik6IG51bWJlcltdIHwgdW5kZWZpbmVkIHtcbiAgICBjb25zdCBuYW1lID0gZ2V0UHJvcDxzdHJpbmcgfCBudW1iZXI+KHRyYWNlLCAnbmFtZScpO1xuICAgIGlmIChuYW1lID09PSB1bmRlZmluZWQpIHJldHVybiB1bmRlZmluZWQ7XG5cbiAgICAvLyBUcnkgdG8gbWF0Y2ggdHJhY2UgbmFtZSBhZ2FpbnN0IGNhdGVnb3JpY2FsIGNvbHVtbiB2YWx1ZXNcbiAgICBmb3IgKGNvbnN0IGNvbE5hbWUgb2YgY2F0ZWdvcmljYWxDb2x1bW5zKSB7XG4gICAgICAgIGNvbnN0IGNvbFZhbHVlcyA9IGNvbHVtbnNbY29sTmFtZV07XG4gICAgICAgIGlmICghY29sVmFsdWVzKSBjb250aW51ZTtcblxuICAgICAgICAvLyBUcnkgZXhhY3QgbWF0Y2ggKG1vc3QgY29tbW9uIHdpdGggY2F0ZWdvcmljYWwgdmFyaWFibGVzKVxuICAgICAgICBjb25zdCBleGFjdE1hdGNoZXMgPSBBcnJheS5mcm9tKGNvbFZhbHVlcylcbiAgICAgICAgICAgIC5tYXAoKHZhbCwgaWR4KSA9PiAodmFsID09PSBuYW1lID8gaWR4IDogLTEpKVxuICAgICAgICAgICAgLmZpbHRlcihpZHggPT4gaWR4ICE9PSAtMSk7XG5cbiAgICAgICAgaWYgKGV4YWN0TWF0Y2hlcy5sZW5ndGggPiAwKSB7XG4gICAgICAgICAgICByZXR1cm4gZXhhY3RNYXRjaGVzO1xuICAgICAgICB9XG5cbiAgICAgICAgLy8gVHJ5IG1vcmUgZmxleGlibGUgbWF0Y2hlcyBiYXNlZCBvbiBjb21tb24gUGxvdGx5IEV4cHJlc3MgdHJhY2UgbmFtaW5nIHBhdHRlcm5zXG4gICAgICAgIC8vIEV4OiBcInNwZWNpZXMgPSBzZXRvc2FcIiBvciBcInNwZWNpZXM9c2V0b3NhXCJcbiAgICAgICAgaWYgKHR5cGVvZiBuYW1lID09PSAnc3RyaW5nJyAmJiBuYW1lLmluY2x1ZGVzKCc9JykpIHtcbiAgICAgICAgICAgIGNvbnN0IHBhcnRzID0gbmFtZS5zcGxpdCgnPScpLm1hcChzID0+IHMudHJpbSgpKTtcbiAgICAgICAgICAgIGlmIChwYXJ0cy5sZW5ndGggPT09IDIgJiYgcGFydHNbMF0gPT09IGNvbE5hbWUpIHtcbiAgICAgICAgICAgICAgICBjb25zdCB0YXJnZXRWYWx1ZSA9IHBhcnRzWzFdO1xuICAgICAgICAgICAgICAgIGNvbnN0IG1hdGNoZXMgPSBBcnJheS5mcm9tKGNvbFZhbHVlcylcbiAgICAgICAgICAgICAgICAgICAgLm1hcCgodmFsLCBpZHgpID0+IChTdHJpbmcodmFsKSA9PT0gdGFyZ2V0VmFsdWUgPyBpZHggOiAtMSkpXG4gICAgICAgICAgICAgICAgICAgIC5maWx0ZXIoaWR4ID0+IGlkeCAhPT0gLTEpO1xuXG4gICAgICAgICAgICAgICAgaWYgKG1hdGNoZXMubGVuZ3RoID4gMCkge1xuICAgICAgICAgICAgICAgICAgICByZXR1cm4gbWF0Y2hlcztcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICAvLyBJZiB3ZSBjb3VsZG4ndCBmaW5kIGEgZGlyZWN0IGNhdGVnb3J5IG1hdGNoLCB0cnkgdXNpbmcgdGhlIGxlZ2VuZGdyb3VwXG4gICAgY29uc3QgbGVnZW5kZ3JvdXAgPSBnZXRQcm9wPHN0cmluZz4odHJhY2UsICdsZWdlbmRncm91cCcpO1xuICAgIGlmIChsZWdlbmRncm91cCkge1xuICAgICAgICBmb3IgKGNvbnN0IGNvbE5hbWUgb2YgY2F0ZWdvcmljYWxDb2x1bW5zKSB7XG4gICAgICAgICAgICBjb25zdCBjb2xWYWx1ZXMgPSBjb2x1bW5zW2NvbE5hbWVdO1xuICAgICAgICAgICAgaWYgKCFjb2xWYWx1ZXMpIGNvbnRpbnVlO1xuXG4gICAgICAgICAgICAvLyBDaGVjayBpZiBsZWdlbmRncm91cCBjb250YWlucyBjb2x1bW4gbmFtZVxuICAgICAgICAgICAgaWYgKFxuICAgICAgICAgICAgICAgIHR5cGVvZiBsZWdlbmRncm91cCA9PT0gJ3N0cmluZycgJiZcbiAgICAgICAgICAgICAgICBsZWdlbmRncm91cC5pbmNsdWRlcyhjb2xOYW1lKSAmJlxuICAgICAgICAgICAgICAgIGxlZ2VuZGdyb3VwLmluY2x1ZGVzKCc6JylcbiAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgIC8vIEV4dHJhY3QgdGhlIHZhbHVlIHBhcnQgZnJvbSBmb3JtYXRzIGxpa2UgXCJzcGVjaWVzOnNldG9zYVwiXG4gICAgICAgICAgICAgICAgY29uc3QgdmFsdWVNYXRjaCA9IGxlZ2VuZGdyb3VwLm1hdGNoKG5ldyBSZWdFeHAoYCR7Y29sTmFtZX06KFteOl0rKWApKTtcbiAgICAgICAgICAgICAgICBpZiAodmFsdWVNYXRjaCAmJiB2YWx1ZU1hdGNoWzFdKSB7XG4gICAgICAgICAgICAgICAgICAgIGNvbnN0IHRhcmdldFZhbHVlID0gdmFsdWVNYXRjaFsxXTtcblxuICAgICAgICAgICAgICAgICAgICBjb25zdCBtYXRjaGVzID0gQXJyYXkuZnJvbShjb2xWYWx1ZXMpXG4gICAgICAgICAgICAgICAgICAgICAgICAubWFwKCh2YWwsIGlkeCkgPT4gKFN0cmluZyh2YWwpID09PSB0YXJnZXRWYWx1ZSA/IGlkeCA6IC0xKSlcbiAgICAgICAgICAgICAgICAgICAgICAgIC5maWx0ZXIoaWR4ID0+IGlkeCAhPT0gLTEpO1xuXG4gICAgICAgICAgICAgICAgICAgIGlmIChtYXRjaGVzLmxlbmd0aCA+IDApIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiBtYXRjaGVzO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuXG4gICAgcmV0dXJuIHVuZGVmaW5lZDtcbn1cblxuLyoqXG4gKiBBcHBseSBhIGZpbHRlciBleHByZXNzaW9uIHRvIGdldCBpbmRpY2VzXG4gKiAocGxhY2Vob2xkZXIgZm9yIHBvdGVudGlhbCBmdXR1cmUgZW5oYW5jZW1lbnQpXG4gKi9cbmZ1bmN0aW9uIGFwcGx5RmlsdGVyRXhwcmVzc2lvbihcbiAgICBmaWx0ZXJFeHByOiBzdHJpbmcsXG4gICAgY29sdW1uczogUmVjb3JkPHN0cmluZywgQXJyYXlMaWtlPHVua25vd24+PlxuKTogbnVtYmVyW10gfCB1bmRlZmluZWQge1xuICAgIC8vIFRoaXMgaXMgYSBwbGFjZWhvbGRlciBmb3IgcG90ZW50aWFsIGZ1dHVyZSBlbmhhbmNlbWVudFxuICAgIC8vIEltcGxlbWVudGluZyBhIGZ1bGwgZmlsdGVyIGV4cHJlc3Npb24gcGFyc2VyIGlzIGNvbXBsZXhcblxuICAgIC8vIEZvciBub3csIHdlJ2xsIGp1c3QgaGFuZGxlIHNpbXBsZSBjYXNlcyB3aXRoIGV4YWN0IG1hdGNoZXNcbiAgICBjb25zdCBtYXRjaGVzID0gZmlsdGVyRXhwci5tYXRjaCgvKFxcdyspXFxzKj09XFxzKltcIiddPyhbXlwiJ10rKVtcIiddPy8pO1xuICAgIGlmIChtYXRjaGVzICYmIG1hdGNoZXMubGVuZ3RoID09PSAzKSB7XG4gICAgICAgIGNvbnN0IFtfLCBjb2xOYW1lLCB2YWx1ZV0gPSBtYXRjaGVzO1xuXG4gICAgICAgIGlmIChjb2x1bW5zW2NvbE5hbWVdKSB7XG4gICAgICAgICAgICBjb25zdCBjb2xWYWx1ZXMgPSBjb2x1bW5zW2NvbE5hbWVdO1xuICAgICAgICAgICAgcmV0dXJuIEFycmF5LmZyb20oY29sVmFsdWVzKVxuICAgICAgICAgICAgICAgIC5tYXAoKHZhbCwgaWR4KSA9PiAoU3RyaW5nKHZhbCkgPT09IHZhbHVlID8gaWR4IDogLTEpKVxuICAgICAgICAgICAgICAgIC5maWx0ZXIoaWR4ID0+IGlkeCAhPT0gLTEpO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgcmV0dXJuIHVuZGVmaW5lZDtcbn1cblxuLyoqXG4gKiBUcnkgdG8gaW5mZXIgaW5kaWNlcyBieSBleGFtaW5pbmcgdmFyaW91cyB0cmFjZSBwcm9wZXJ0aWVzXG4gKi9cbmZ1bmN0aW9uIGluZmVySW5kaWNlc0Zyb21UcmFjZVByb3BlcnRpZXMoXG4gICAgdHJhY2U6IFBsb3RseS5EYXRhLFxuICAgIGNvbHVtbnM6IFJlY29yZDxzdHJpbmcsIEFycmF5TGlrZTx1bmtub3duPj4sXG4gICAgY2F0ZWdvcmljYWxDb2x1bW5zOiBzdHJpbmdbXVxuKTogbnVtYmVyW10gfCB1bmRlZmluZWQge1xuICAgIC8vIFRyeSB0byBtYXRjaCB0cmFjZSBuYW1lIHdpdGggY2F0ZWdvcmljYWwgY29sdW1uc1xuICAgIGNvbnN0IG5hbWUgPSBnZXRQcm9wPHN0cmluZyB8IG51bWJlcj4odHJhY2UsICduYW1lJyk7XG4gICAgaWYgKG5hbWUgIT09IHVuZGVmaW5lZCkge1xuICAgICAgICAvLyBGaXJzdCBjaGVjayBjYXRlZ29yaWNhbCBjb2x1bW5zIGRpcmVjdGx5XG4gICAgICAgIGZvciAoY29uc3QgY29sTmFtZSBvZiBjYXRlZ29yaWNhbENvbHVtbnMpIHtcbiAgICAgICAgICAgIGNvbnN0IGNvbFZhbHVlcyA9IGNvbHVtbnNbY29sTmFtZV07XG4gICAgICAgICAgICBpZiAoIWNvbFZhbHVlcykgY29udGludWU7XG5cbiAgICAgICAgICAgIGNvbnN0IG1hdGNoZXMgPSBBcnJheS5mcm9tKGNvbFZhbHVlcylcbiAgICAgICAgICAgICAgICAubWFwKCh2YWwsIGlkeCkgPT4gKFN0cmluZyh2YWwpID09PSBTdHJpbmcobmFtZSkgPyBpZHggOiAtMSkpXG4gICAgICAgICAgICAgICAgLmZpbHRlcihpZHggPT4gaWR4ICE9PSAtMSk7XG5cbiAgICAgICAgICAgIGlmIChtYXRjaGVzLmxlbmd0aCA+IDApIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gbWF0Y2hlcztcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuXG4gICAgICAgIC8vIFRoZW4gY2hlY2sgaWYgdGhlIHRyYWNlIG5hbWUgY29udGFpbnMgYSB2YWx1ZSBpbiBhIGtleS12YWx1ZSBmb3JtYXRcbiAgICAgICAgaWYgKHR5cGVvZiBuYW1lID09PSAnc3RyaW5nJyAmJiBuYW1lLmluY2x1ZGVzKCc9JykpIHtcbiAgICAgICAgICAgIGNvbnN0IHBhcnRzID0gbmFtZS5zcGxpdCgnPScpLm1hcChwID0+IHAudHJpbSgpKTtcbiAgICAgICAgICAgIGlmIChwYXJ0cy5sZW5ndGggPT09IDIgJiYgY29sdW1uc1twYXJ0c1swXV0pIHtcbiAgICAgICAgICAgICAgICBjb25zdCBjb2xWYWx1ZXMgPSBjb2x1bW5zW3BhcnRzWzBdXTtcbiAgICAgICAgICAgICAgICBjb25zdCBtYXRjaGVzID0gQXJyYXkuZnJvbShjb2xWYWx1ZXMpXG4gICAgICAgICAgICAgICAgICAgIC5tYXAoKHZhbCwgaWR4KSA9PiAoU3RyaW5nKHZhbCkgPT09IHBhcnRzWzFdID8gaWR4IDogLTEpKVxuICAgICAgICAgICAgICAgICAgICAuZmlsdGVyKGlkeCA9PiBpZHggIT09IC0xKTtcblxuICAgICAgICAgICAgICAgIGlmIChtYXRjaGVzLmxlbmd0aCA+IDApIHtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIG1hdGNoZXM7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuXG4gICAgLy8gVHJ5IHdvcmtpbmcgd2l0aCBtYXJrZXIgY29sb3JzIG9yIHN5bWJvbHMgaWYgdGhleSdyZSBhcnJheXNcbiAgICBjb25zdCBtYXJrZXIgPSBnZXRQcm9wPGFueT4odHJhY2UsICdtYXJrZXInKTtcbiAgICBpZiAobWFya2VyKSB7XG4gICAgICAgIGlmIChBcnJheS5pc0FycmF5KG1hcmtlci5jb2xvcikpIHtcbiAgICAgICAgICAgIC8vIFVzZSBub24tbnVsbCBhcyBhIGZpbHRlciAoZm9yIHRyYWNlcyB3aGVyZSBtaXNzaW5nIHZhbHVlcyBhcmUgbnVsbHMpXG4gICAgICAgICAgICBjb25zdCBub25OdWxsSW5kaWNlcyA9IG1hcmtlci5jb2xvclxuICAgICAgICAgICAgICAgIC5tYXAoKHZhbDogYW55LCBpZHg6IG51bWJlcikgPT4gKHZhbCAhPSBudWxsID8gaWR4IDogLTEpKVxuICAgICAgICAgICAgICAgIC5maWx0ZXIoKGlkeDogbnVtYmVyKSA9PiBpZHggIT09IC0xKTtcblxuICAgICAgICAgICAgLy8gT25seSB1c2UgdGhpcyBtZXRob2QgaWYgaXQgcmVzdWx0cyBpbiBhIG1lYW5pbmdmdWwgc3Vic2V0XG4gICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgbm9uTnVsbEluZGljZXMubGVuZ3RoID4gMCAmJlxuICAgICAgICAgICAgICAgIG5vbk51bGxJbmRpY2VzLmxlbmd0aCA8IChPYmplY3QudmFsdWVzKGNvbHVtbnMpWzBdPy5sZW5ndGggfHwgMClcbiAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgIHJldHVybiBub25OdWxsSW5kaWNlcztcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuXG4gICAgICAgIGlmIChBcnJheS5pc0FycmF5KG1hcmtlci5zeW1ib2wpKSB7XG4gICAgICAgICAgICAvLyBJZiBzeW1ib2xzIGFyZSBjYXRlZ29yaWNhbCwgdXNlIHRoZSBzcGVjaWZpYyBzeW1ib2wgZm9yIHRoaXMgdHJhY2VcbiAgICAgICAgICAgIGNvbnN0IHN5bWJvbE5hbWUgPSBtYXJrZXIuc3ltYm9sWzBdOyAvLyBVc2UgZmlyc3Qgc3ltYm9sIGFzIHJlcHJlc2VudGF0aXZlXG4gICAgICAgICAgICBpZiAoc3ltYm9sTmFtZSAmJiB0eXBlb2Ygc3ltYm9sTmFtZSA9PT0gJ3N0cmluZycpIHtcbiAgICAgICAgICAgICAgICBjb25zdCBub25OdWxsSW5kaWNlcyA9IG1hcmtlci5zeW1ib2xcbiAgICAgICAgICAgICAgICAgICAgLm1hcCgodmFsOiBhbnksIGlkeDogbnVtYmVyKSA9PiAodmFsID09PSBzeW1ib2xOYW1lID8gaWR4IDogLTEpKVxuICAgICAgICAgICAgICAgICAgICAuZmlsdGVyKChpZHg6IG51bWJlcikgPT4gaWR4ICE9PSAtMSk7XG5cbiAgICAgICAgICAgICAgICBpZiAobm9uTnVsbEluZGljZXMubGVuZ3RoID4gMCkge1xuICAgICAgICAgICAgICAgICAgICByZXR1cm4gbm9uTnVsbEluZGljZXM7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuXG4gICAgLy8gVHJ5IHdvcmtpbmcgd2l0aCBsaW5lIHByb3BlcnRpZXMgZm9yIGxpbmUgY2hhcnRzXG4gICAgY29uc3QgbGluZSA9IGdldFByb3A8YW55Pih0cmFjZSwgJ2xpbmUnKTtcbiAgICBpZiAobGluZSkge1xuICAgICAgICBpZiAoQXJyYXkuaXNBcnJheShsaW5lLmNvbG9yKSkge1xuICAgICAgICAgICAgY29uc3Qgbm9uTnVsbEluZGljZXMgPSBsaW5lLmNvbG9yXG4gICAgICAgICAgICAgICAgLm1hcCgodmFsOiBhbnksIGlkeDogbnVtYmVyKSA9PiAodmFsICE9IG51bGwgPyBpZHggOiAtMSkpXG4gICAgICAgICAgICAgICAgLmZpbHRlcigoaWR4OiBudW1iZXIpID0+IGlkeCAhPT0gLTEpO1xuXG4gICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgbm9uTnVsbEluZGljZXMubGVuZ3RoID4gMCAmJlxuICAgICAgICAgICAgICAgIG5vbk51bGxJbmRpY2VzLmxlbmd0aCA8IChPYmplY3QudmFsdWVzKGNvbHVtbnMpWzBdPy5sZW5ndGggfHwgMClcbiAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgIHJldHVybiBub25OdWxsSW5kaWNlcztcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuXG4gICAgICAgIGlmIChBcnJheS5pc0FycmF5KGxpbmUuZGFzaCkpIHtcbiAgICAgICAgICAgIGNvbnN0IGRhc2hTdHlsZSA9IGxpbmUuZGFzaFswXTtcbiAgICAgICAgICAgIGlmIChkYXNoU3R5bGUpIHtcbiAgICAgICAgICAgICAgICBjb25zdCBtYXRjaGluZ0luZGljZXMgPSBsaW5lLmRhc2hcbiAgICAgICAgICAgICAgICAgICAgLm1hcCgodmFsOiBhbnksIGlkeDogbnVtYmVyKSA9PiAodmFsID09PSBkYXNoU3R5bGUgPyBpZHggOiAtMSkpXG4gICAgICAgICAgICAgICAgICAgIC5maWx0ZXIoKGlkeDogbnVtYmVyKSA9PiBpZHggIT09IC0xKTtcblxuICAgICAgICAgICAgICAgIGlmIChtYXRjaGluZ0luZGljZXMubGVuZ3RoID4gMCkge1xuICAgICAgICAgICAgICAgICAgICByZXR1cm4gbWF0Y2hpbmdJbmRpY2VzO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH1cblxuICAgIC8vIElmIHdlIGhhdmUgYSBsZWdlbmRncm91cCwgaXQgbWlnaHQgY29udGFpbiBmaWx0ZXJpbmcgaW5mb3JtYXRpb25cbiAgICBjb25zdCBsZWdlbmRncm91cCA9IGdldFByb3A8c3RyaW5nPih0cmFjZSwgJ2xlZ2VuZGdyb3VwJyk7XG4gICAgaWYgKGxlZ2VuZGdyb3VwICYmIHR5cGVvZiBsZWdlbmRncm91cCA9PT0gJ3N0cmluZycpIHtcbiAgICAgICAgLy8gQ2hlY2sgZm9yIHBhdHRlcm5zIGxpa2UgXCJjb2x1bW5OYW1lOnZhbHVlXCJcbiAgICAgICAgY29uc3QgbGdQYXJ0cyA9IGxlZ2VuZGdyb3VwLnNwbGl0KCc6Jyk7XG4gICAgICAgIGlmIChsZ1BhcnRzLmxlbmd0aCA+PSAyICYmIGNvbHVtbnNbbGdQYXJ0c1swXV0pIHtcbiAgICAgICAgICAgIGNvbnN0IGNvbFZhbHVlcyA9IGNvbHVtbnNbbGdQYXJ0c1swXV07XG4gICAgICAgICAgICBjb25zdCBtYXRjaGVzID0gQXJyYXkuZnJvbShjb2xWYWx1ZXMpXG4gICAgICAgICAgICAgICAgLm1hcCgodmFsLCBpZHgpID0+IChTdHJpbmcodmFsKSA9PT0gbGdQYXJ0c1sxXSA/IGlkeCA6IC0xKSlcbiAgICAgICAgICAgICAgICAuZmlsdGVyKGlkeCA9PiBpZHggIT09IC0xKTtcblxuICAgICAgICAgICAgaWYgKG1hdGNoZXMubGVuZ3RoID4gMCkge1xuICAgICAgICAgICAgICAgIHJldHVybiBtYXRjaGVzO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuXG4gICAgcmV0dXJuIHVuZGVmaW5lZDtcbn1cblxuLyoqXG4gKiBJZGVudGlmaWVzIHBvdGVudGlhbCBjYXRlZ29yaWNhbCBjb2x1bW5zIHRoYXQgbWlnaHQgaGF2ZSBiZWVuIHVzZWQgZm9yIHRyYWNlIHNlcGFyYXRpb25cbiAqIGJ5IGV4YW1pbmluZyB0cmFjZSBuYW1lcyBhbmQgZGF0YSBjb2x1bW5zXG4gKi9cbmZ1bmN0aW9uIGZpbmRQb3NzaWJsZUNhdGVnb3JpY2FsQ29sdW1ucyhcbiAgICB0cmFjZXM6IFBsb3RseS5EYXRhW10sXG4gICAgY29sdW1uczogUmVjb3JkPHN0cmluZywgQXJyYXlMaWtlPHVua25vd24+PlxuKTogc3RyaW5nW10ge1xuICAgIGNvbnN0IGNhdGVnb3JpY2FsQ29sdW1uczogc3RyaW5nW10gPSBbXTtcblxuICAgIC8vIFNhZmVseSBleHRyYWN0IHRyYWNlIG5hbWVzIHVzaW5nIG91ciBoZWxwZXIgZnVuY3Rpb25cbiAgICBjb25zdCB0cmFjZU5hbWVzOiAoc3RyaW5nIHwgbnVtYmVyKVtdID0gW107XG4gICAgdHJhY2VzLmZvckVhY2godHJhY2UgPT4ge1xuICAgICAgICBjb25zdCBuYW1lID0gZ2V0UHJvcDxzdHJpbmcgfCBudW1iZXI+KHRyYWNlLCAnbmFtZScpO1xuICAgICAgICBpZiAobmFtZSAhPT0gdW5kZWZpbmVkKSB0cmFjZU5hbWVzLnB1c2gobmFtZSk7XG4gICAgfSk7XG5cbiAgICAvLyBJZiB3ZSBkb24ndCBoYXZlIHRyYWNlIG5hbWVzLCB3ZSBjYW4ndCBpZGVudGlmeSBjYXRlZ29yaWNhbCBjb2x1bW5zXG4gICAgaWYgKHRyYWNlTmFtZXMubGVuZ3RoID09PSAwKSByZXR1cm4gW107XG5cbiAgICAvLyBDaGVjayBlYWNoIGNvbHVtbiB0byBzZWUgaWYgaXQgbWlnaHQgYmUgY2F0ZWdvcmljYWxcbiAgICBmb3IgKGNvbnN0IFtjb2xOYW1lLCBjb2xWYWx1ZXNdIG9mIE9iamVjdC5lbnRyaWVzKGNvbHVtbnMpKSB7XG4gICAgICAgIGlmICghY29sVmFsdWVzIHx8IGNvbFZhbHVlcy5sZW5ndGggPT09IDApIGNvbnRpbnVlO1xuXG4gICAgICAgIC8vIENvbnZlcnQgY29sdW1uIHZhbHVlcyB0byBhbiBhcnJheVxuICAgICAgICBjb25zdCB2YWx1ZXMgPSBBcnJheS5mcm9tKGNvbFZhbHVlcyk7XG5cbiAgICAgICAgLy8gU2tpcCBpZiBhbGwgdmFsdWVzIGFyZSBudW1iZXJzIChleGNlcHQgZm9yIG51bWVyaWNhbCBjYXRlZ29yaWVzKVxuICAgICAgICBjb25zdCBhbGxOdW1iZXJzID0gdmFsdWVzLmV2ZXJ5KHZhbCA9PiB0eXBlb2YgdmFsID09PSAnbnVtYmVyJyk7XG4gICAgICAgIGlmIChhbGxOdW1iZXJzKSB7XG4gICAgICAgICAgICAvLyBDaGVjayBpZiB0aGVzZSBjb3VsZCBiZSBudW1lcmljYWwgY2F0ZWdvcmllcyBieSBzZWVpbmcgaWYgdHJhY2UgbmFtZXMgbWF0Y2ggYW55IHZhbHVlc1xuICAgICAgICAgICAgY29uc3QgbWF0Y2hlc0FueVRyYWNlTmFtZSA9IHRyYWNlTmFtZXMuc29tZShuYW1lID0+IHtcbiAgICAgICAgICAgICAgICAvLyBGb3IgdHlwZSBzYWZldHksIGNoZWNrIHVzaW5nIHNvbWUoKSBpbnN0ZWFkIG9mIGluY2x1ZGVzKClcbiAgICAgICAgICAgICAgICBpZiAodHlwZW9mIG5hbWUgPT09ICdzdHJpbmcnKSB7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiB2YWx1ZXMuc29tZSh2YWwgPT4gdmFsID09PSBOdW1iZXIobmFtZSkpO1xuICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiB2YWx1ZXMuc29tZSh2YWwgPT4gdmFsID09PSBuYW1lKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9KTtcblxuICAgICAgICAgICAgaWYgKCFtYXRjaGVzQW55VHJhY2VOYW1lKSBjb250aW51ZTtcbiAgICAgICAgfVxuXG4gICAgICAgIC8vIFNraXAgY29sdW1ucyB3aXRoIHRvbyBtYW55IHVuaXF1ZSB2YWx1ZXMgKD49IDUwJSBvZiB0b3RhbCByb3dzKVxuICAgICAgICAvLyBhcyB0aGV5J3JlIHVubGlrZWx5IHRvIGJlIGNhdGVnb3JpY2FsXG4gICAgICAgIGNvbnN0IHVuaXF1ZVZhbHVlcyA9IG5ldyBTZXQodmFsdWVzKTtcbiAgICAgICAgaWYgKHVuaXF1ZVZhbHVlcy5zaXplID49IHZhbHVlcy5sZW5ndGggKiAwLjUgJiYgdW5pcXVlVmFsdWVzLnNpemUgPiAxMCkgY29udGludWU7XG5cbiAgICAgICAgLy8gQ2hlY2sgaWYgYW55IHRyYWNlIG5hbWUgaXMgaW4gdGhpcyBjb2x1bW5cbiAgICAgICAgY29uc3QgbWF0Y2hlc1RyYWNlTmFtZSA9IHRyYWNlTmFtZXMuc29tZShuYW1lID0+IHZhbHVlcy5zb21lKHZhbCA9PiB2YWwgPT09IG5hbWUpKTtcblxuICAgICAgICAvLyBBbHNvIGNoZWNrIGlmIHRyYWNlIGxlZ2VuZGdyb3VwcyBtYXRjaCBhbnkgY29sdW1uIHZhbHVlc1xuICAgICAgICBjb25zdCBsZWdlbmRHcm91cHM6IHN0cmluZ1tdID0gW107XG4gICAgICAgIHRyYWNlcy5mb3JFYWNoKHRyYWNlID0+IHtcbiAgICAgICAgICAgIGNvbnN0IGxlZ2VuZGdyb3VwID0gZ2V0UHJvcDxzdHJpbmc+KHRyYWNlLCAnbGVnZW5kZ3JvdXAnKTtcbiAgICAgICAgICAgIGlmIChsZWdlbmRncm91cCkgbGVnZW5kR3JvdXBzLnB1c2gobGVnZW5kZ3JvdXApO1xuICAgICAgICB9KTtcblxuICAgICAgICBjb25zdCBtYXRjaGVzTGVnZW5kR3JvdXAgPSBsZWdlbmRHcm91cHMuc29tZShncm91cCA9PlxuICAgICAgICAgICAgdmFsdWVzLnNvbWUodmFsID0+IFN0cmluZyh2YWwpID09PSBncm91cClcbiAgICAgICAgKTtcblxuICAgICAgICBpZiAobWF0Y2hlc1RyYWNlTmFtZSB8fCBtYXRjaGVzTGVnZW5kR3JvdXApIHtcbiAgICAgICAgICAgIGNhdGVnb3JpY2FsQ29sdW1ucy5wdXNoKGNvbE5hbWUpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgLy8gSWYgd2UgZG9uJ3QgaGF2ZSBkaXJlY3QgbWF0Y2hlcywgY2hlY2sgaWYgdGhpcyBjb2x1bW4gaGFzIGZldyB1bmlxdWUgdmFsdWVzXG4gICAgICAgICAgICAvLyB3aGljaCBtaWdodCBpbmRpY2F0ZSBpdCdzIGEgY2F0ZWdvcmljYWwgdmFyaWFibGVcbiAgICAgICAgICAgIGlmIChcbiAgICAgICAgICAgICAgICB1bmlxdWVWYWx1ZXMuc2l6ZSA8PSAyNSAmJlxuICAgICAgICAgICAgICAgIHVuaXF1ZVZhbHVlcy5zaXplID4gMCAmJlxuICAgICAgICAgICAgICAgIHVuaXF1ZVZhbHVlcy5zaXplIDwgdmFsdWVzLmxlbmd0aCAqIDAuMjVcbiAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgIGNhdGVnb3JpY2FsQ29sdW1ucy5wdXNoKGNvbE5hbWUpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuXG4gICAgcmV0dXJuIGNhdGVnb3JpY2FsQ29sdW1ucztcbn1cbiIsICJpbXBvcnQge1xuICAgIE1vc2FpY0NsaWVudCxcbiAgICBQYXJhbSxcbiAgICBTZWxlY3Rpb24sXG59IGZyb20gJ2h0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9ucG0vQHV3ZGF0YS9tb3NhaWMtY29yZUAwLjE2LjIvK2VzbSc7XG5pbXBvcnQgeyBTZWxlY3RRdWVyeSB9IGZyb20gJ2h0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9ucG0vQHV3ZGF0YS9tb3NhaWMtc3FsQDAuMTYuMi8rZXNtJztcblxuZXhwb3J0IGFic3RyYWN0IGNsYXNzIFZpekNsaWVudCBleHRlbmRzIE1vc2FpY0NsaWVudCB7XG4gICAgY29uc3RydWN0b3IoXG4gICAgICAgIHByaXZhdGUgcmVhZG9ubHkgdGFibGVfOiBzdHJpbmcsXG4gICAgICAgIGZpbHRlckJ5OiBTZWxlY3Rpb24sXG4gICAgICAgIHByaXZhdGUgcmVhZG9ubHkgcXVlcmllc186IFNlbGVjdFF1ZXJ5W10sXG4gICAgICAgIHByaXZhdGUgcmVhZG9ubHkgcGFyYW1zXzogTWFwPHN0cmluZywgUGFyYW0+XG4gICAgKSB7XG4gICAgICAgIHN1cGVyKGZpbHRlckJ5KTtcbiAgICAgICAgdGhpcy5wYXJhbXNfLmZvckVhY2godmFsdWUgPT4ge1xuICAgICAgICAgICAgdmFsdWUuYWRkRXZlbnRMaXN0ZW5lcigndmFsdWUnLCAoKSA9PiB0aGlzLnJlcXVlc3RVcGRhdGUoKSk7XG4gICAgICAgIH0pO1xuICAgIH1cblxuICAgIHF1ZXJ5KGZpbHRlcjogYW55W10gPSBbXSk6IFNlbGVjdFF1ZXJ5IHtcbiAgICAgICAgbGV0IHF1ZXJ5ID0gU2VsZWN0UXVlcnkuc2VsZWN0KCcqJykuZnJvbSh0aGlzLnRhYmxlXykud2hlcmUoZmlsdGVyKTtcbiAgICAgICAgcmV0dXJuIFZpekNsaWVudC5hcHBseVF1ZXJpZXMocXVlcnksIHRoaXMucXVlcmllc18pO1xuICAgIH1cblxuICAgIHN0YXRpYyBhcHBseVF1ZXJpZXMocXVlcnk6IFNlbGVjdFF1ZXJ5LCBxdWVyaWVzOiBTZWxlY3RRdWVyeVtdKTogU2VsZWN0UXVlcnkge1xuICAgICAgICBmb3IgKGxldCBxIG9mIHF1ZXJpZXMpIHtcbiAgICAgICAgICAgIHF1ZXJ5ID0gcS5jbG9uZSgpLmZyb20ocXVlcnkpO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBxdWVyeTtcbiAgICB9XG59XG4iLCAiaW1wb3J0IHR5cGUgeyBSZW5kZXJQcm9wcyB9IGZyb20gJ0Bhbnl3aWRnZXQvdHlwZXMnO1xuXG5pbXBvcnQgeyB2aXpDb29yZGluYXRvciB9IGZyb20gJy4uL2Nvb3JkaW5hdG9yJztcblxuaW1wb3J0IHsgRmlndXJlLCBQbG90bHlBeGlzTWFwcGluZ3MsIFBsb3RseUZpZ3VyZSB9IGZyb20gJy4uL2NsaWVudHMvZmlndXJlJztcblxuaW50ZXJmYWNlIEZpZ3VyZVByb3BzIHtcbiAgICBkZl9pZDogc3RyaW5nO1xuICAgIGZpZ3VyZTogc3RyaW5nO1xuICAgIGF4aXNfbWFwcGluZ3M6IHN0cmluZztcbn1cblxuYXN5bmMgZnVuY3Rpb24gcmVuZGVyKHsgbW9kZWwsIGVsIH06IFJlbmRlclByb3BzPEZpZ3VyZVByb3BzPikge1xuICAgIC8vIHVud3JhcCB0aGUgd2lkZ2V0IHBheWxvYWRcbiAgICBjb25zdCBkZl9pZDogc3RyaW5nID0gbW9kZWwuZ2V0KCdkZl9pZCcpO1xuICAgIGNvbnN0IGZpZ3VyZV9qc29uOiBzdHJpbmcgPSBtb2RlbC5nZXQoJ2ZpZ3VyZScpO1xuICAgIGNvbnN0IGZpZ3VyZTogUGxvdGx5RmlndXJlID0gSlNPTi5wYXJzZShmaWd1cmVfanNvbik7XG4gICAgY29uc3QgYXhpc19tYXBwaW5nc19qc29uOiBzdHJpbmcgPSBtb2RlbC5nZXQoJ2F4aXNfbWFwcGluZ3MnKTtcbiAgICBjb25zdCBheGlzX21hcHBpbmdzOiBQbG90bHlBeGlzTWFwcGluZ3MgPSBKU09OLnBhcnNlKGF4aXNfbWFwcGluZ3NfanNvbik7XG5cbiAgICAvLyBnZXQgdGhlIGRhdGEgZnJhbWVcbiAgICBjb25zdCBjb29yZGluYXRvciA9IGF3YWl0IHZpekNvb3JkaW5hdG9yKCk7XG4gICAgY29uc3QgZGYgPSBhd2FpdCBjb29yZGluYXRvci5nZXREYXRhRnJhbWUoZGZfaWQpO1xuXG4gICAgLy8gY3JlYXRlIHRoZSB2aWV3IGFuZCBjb25uZWN0IGl0XG4gICAgY29uc3QgdmlldyA9IG5ldyBGaWd1cmUoXG4gICAgICAgIGVsLFxuICAgICAgICBmaWd1cmUsXG4gICAgICAgIGF4aXNfbWFwcGluZ3MsXG4gICAgICAgIGRmLnRhYmxlLFxuICAgICAgICBkZi5zZWxlY3Rpb24sXG4gICAgICAgIGRmLnF1ZXJpZXMsXG4gICAgICAgIGRmLnBhcmFtc1xuICAgICk7XG4gICAgYXdhaXQgY29vcmRpbmF0b3IuY29ubmVjdENsaWVudCh2aWV3KTtcbn1cblxuZXhwb3J0IGRlZmF1bHQgeyByZW5kZXIgfTtcbiJdLAogICJtYXBwaW5ncyI6ICI7QUFFQTtBQUFBLEVBRUk7QUFBQSxFQUNBO0FBQUEsRUFDQTtBQUFBLE9BQ0c7QUFFUCxTQUFTLDBCQUEwQjs7O0FDVG5DO0FBQUEsRUFDSTtBQUFBLEVBQ0E7QUFBQSxFQUNBO0FBQUEsRUFDQTtBQUFBLEVBRUE7QUFBQSxPQUNHO0FBRVAsZUFBc0IsYUFBYTtBQUMvQixRQUFNLG1CQUFtQixtQkFBbUI7QUFHNUMsUUFBTSxTQUFTLE1BQU0sYUFBYSxnQkFBZ0I7QUFFbEQsUUFBTSxhQUFhLElBQUk7QUFBQSxJ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
