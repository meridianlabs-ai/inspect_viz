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
    this.params_ = /* @__PURE__ */ new Map();
    this.coordinator_ = new Coordinator();
    this.coordinator_.databaseConnector(wasmConnector({ connection: this.conn_ }));
  }
  addParam(name, value) {
    if (!this.params_.has(name)) {
      this.params_.set(name, Param.value(value));
    }
    return this.params_.get(name);
  }
  getParam(name) {
    return this.params_.get(name);
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
        params.set(p.name, this.addParam(p.name, p.value));
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
  async connectClient(client) {
    this.coordinator_.connect(client);
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

// js/clients/figure_view.ts
import {
  toDataColumns
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import Plotly from "https://esm.sh/plotly.js-dist-min@3.0.1";

// js/clients/viz_client.ts
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

// js/clients/figure_view.ts
var FigureView = class extends VizClient {
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

// js/widgets/figure_view.ts
async function render({ model, el }) {
  const df_id = model.get("df_id");
  const figure_json = model.get("figure");
  const figure = JSON.parse(figure_json);
  const axis_mappings_json = model.get("axis_mappings");
  const axis_mappings = JSON.parse(axis_mappings_json);
  const coordinator = await vizCoordinator();
  const df = await coordinator.getDataFrame(df_id);
  const view = new FigureView(
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
var figure_view_default = { render };
export {
  figure_view_default as default
};
