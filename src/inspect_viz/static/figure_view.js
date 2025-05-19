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

// js/coordinator/dataframe.ts
var DataFrame = class {
  constructor(table, queries, params, selection) {
    this.table = table;
    this.queries = queries;
    this.params = params;
    this.selection = selection;
  }
};

// js/util/wait.ts
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// js/coordinator/coodinator.ts
var DataFrameCoordinator = class {
  constructor(conn_) {
    this.conn_ = conn_;
    this.dfs_ = /* @__PURE__ */ new Map();
    this.coordinator_ = new Coordinator();
    this.coordinator_.databaseConnector(wasmConnector({ connection: this.conn_ }));
  }
  async addDataFrame(id, source_id, buffer, queries) {
    if (id === source_id) {
      await this.conn_?.insertArrowFromIPCStream(buffer, {
        name: id,
        create: true
      });
    }
    const params = /* @__PURE__ */ new Map();
    for (const query of queries) {
      for (const p of Object.values(query.parameters)) {
        params.set(p.name, Param.value(p.value));
      }
    }
    this.dfs_.set(id, new DataFrame(source_id, queries, params, Selection.intersect()));
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
import { Param as Param2 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
function toSelectQuery(query) {
  const selectExpressions = {};
  for (const [alias, expr] of Object.entries(query.select)) {
    selectExpressions[alias] = buildExpressionValue(expr);
  }
  let select = SelectQuery.select(selectExpressions);
  if (query.distinct === true) {
    select = select.distinct();
  }
  if (query.where) {
    select = applyWhereClause(select, query.where);
  }
  if (query.groupby && query.groupby.length > 0) {
    select = applyGroupByClause(select, query.groupby);
  }
  if (query.having) {
    select = applyHavingClause(select, query.having);
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
function interpretFunction(func) {
  const funcName = func.name.toLowerCase();
  const args = func.args.map(buildExpressionNode);
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
function applyWhereClause(query, whereExpr) {
  if (whereExpr.type === "and" || whereExpr.type === "or") {
    return applyLogicalExpression(query, whereExpr);
  } else if (whereExpr.type === "unknown") {
    return query.where(new VerbatimNode(whereExpr.expression));
  } else {
    const condition = buildBinaryExpression(whereExpr);
    return query.where(condition);
  }
}
function applyLogicalExpression(query, expr) {
  const { type, expressions } = expr;
  if (expressions.length === 0) {
    return query;
  } else if (expressions.length === 1) {
    return applyWhereClause(
      query,
      expressions[0]
    );
  } else {
    const conditions = expressions.map(buildExpressionValue);
    if (type === "and") {
      return query.where(and(...conditions));
    } else {
      return query.where(or(...conditions));
    }
  }
}
function applyGroupByClause(query, groupByFields) {
  const fields = groupByFields.map((field) => {
    if (typeof field === "string") {
      return field;
    } else {
      if (typeof field.field === "string") {
        return field.field;
      } else {
        return interpretFunction(field.field);
      }
    }
  });
  return query.groupby(...fields);
}
function applyHavingClause(query, havingExpr) {
  if ("type" in havingExpr) {
    if (havingExpr.type === "and" || havingExpr.type === "or") {
      const { type, expressions } = havingExpr;
      const conditions = expressions.map(buildExpressionValue);
      if (type === "and") {
        return query.having(and(...conditions));
      } else {
        return query.having(or(...conditions));
      }
    } else if (havingExpr.type === "unknown") {
      return query.having(new VerbatimNode(havingExpr.expression));
    } else {
      const condition = buildBinaryExpression(havingExpr);
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
function buildExpressionNode(expr) {
  if (typeof expr === "string" || typeof expr === "number" || typeof expr === "boolean") {
    return new LiteralNode(expr);
  } else if ("type" in expr) {
    if (expr.type === "parameter") {
      return new ParamNode(new Param2(expr.name));
    } else if (expr.type === "unknown") {
      return new VerbatimNode(expr.expression);
    } else if (expr.type === "function") {
      return interpretFunction(expr);
    } else if (expr.type === "and" || expr.type === "or") {
      return buildLogicalExpression(expr);
    } else {
      return buildBinaryExpression(expr);
    }
  } else {
    throw Error(`Unexpected type for expression: ${typeof expr}`);
  }
}
function buildExpressionValue(expr) {
  if (typeof expr === "string") {
    return expr;
  } else if (typeof expr !== "number" && typeof expr !== "boolean" && "type" in expr && expr.type === "unknown") {
    return expr.expression;
  } else {
    return buildExpressionNode(expr);
  }
}
function buildLogicalExpression(expr) {
  const { type, expressions } = expr;
  if (expressions.length === 0) {
    return new LiteralNode(true);
  } else if (expressions.length === 1) {
    return buildExpressionNode(expressions[0]);
  } else {
    const conditions = expressions.map(buildExpressionNode);
    if (type === "and") {
      return and(...conditions);
    } else {
      return or(...conditions);
    }
  }
}
function buildBinaryExpression(expr) {
  const { type, left, right } = expr;
  const leftOperand = buildExpressionValue(left);
  const rightOperand = buildExpressionNode(right);
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
      return new BinaryOpNode(type, buildExpressionNode(left), buildExpressionNode(right));
  }
}

// js/clients/figure_view.ts
import Plotly from "https://esm.sh/plotly.js-dist-min@3.0.1";

// js/clients/viz_client.ts
import {
  MosaicClient as MosaicClient2,
  toDataColumns
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import { SelectQuery as SelectQuery2 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm";
var VizClient = class extends MosaicClient2 {
  constructor(table_, filterBy, queries_) {
    super(filterBy);
    this.table_ = table_;
    this.queries_ = queries_;
  }
  query(filter = []) {
    let query = SelectQuery2.select("*").from(this.table_).where(filter);
    for (const q of this.queries_) {
      query = q.from(query);
    }
    return query;
  }
  queryResult(data) {
    const columns = toDataColumns(data).columns;
    this.onQueryResult(columns);
    return this;
  }
};

// js/clients/figure_view.ts
var FigureView = class extends VizClient {
  constructor(el_, figure_, table, filterBy, queries) {
    super(table, filterBy, queries);
    this.el_ = el_;
    this.figure_ = figure_;
  }
  onQueryResult(columns) {
    const table = bindTable(this.figure_.data, columns);
    Plotly.react(this.el_, table, this.figure_.layout, this.figure_.config);
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
  const queries = df.queries.map(toSelectQuery);
  const view = new FigureView(el, figure, df.table, df.selection, queries);
  await coordinator.connectClient(view);
}
var figure_view_default = { render };
export {
  figure_view_default as default
};
