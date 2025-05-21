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

// js/widgets/dataframe.ts
async function render({ model, el }) {
  const id = model.get("id");
  const source_id = model.get("source_id");
  const buffer = model.get("buffer");
  const queries = model.get("queries");
  const dfQueries = queries ? JSON.parse(queries) : [];
  setTimeout(() => {
    const elCellOutput = el.closest(".cell-output");
    if (elCellOutput) {
      elCellOutput.style.display = "none";
    }
  }, 100);
  const coordinator = await vizCoordinator();
  const arrowBuffer = new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength);
  await coordinator.addDataFrame(id, source_id, arrowBuffer, dfQueries);
}
var dataframe_default = { render };
export {
  dataframe_default as default
};
