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

// js/clients/table.ts
import { Table as MosaicTable } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-inputs@0.16.2/+esm";

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

// js/clients/table.ts
var Table = class extends MosaicTable {
  constructor(el, table, filterBy, queries_, params_) {
    super({ element: el, filterBy, from: table });
    this.queries_ = queries_;
    this.params_ = params_;
    this.params_.forEach((value) => {
      value.addEventListener("value", () => this.requestUpdate());
    });
  }
  query(filter) {
    let query = super.query(filter);
    return VizClient.applyQueries(query, this.queries_);
  }
};

// js/widgets/table.ts
async function render({ model, el }) {
  const df_id = model.get("df_id");
  const coordinator = await vizCoordinator();
  const df = await coordinator.getDataFrame(df_id);
  const view = new Table(el, df.table, df.selection, df.queries, df.params);
  await coordinator.connectClient(view);
}
var table_default = { render };
export {
  table_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsiLi4vLi4vLi4vanMvY29vcmRpbmF0b3IvY29vZGluYXRvci50cyIsICIuLi8uLi8uLi9qcy9jb29yZGluYXRvci9kdWNrZGIudHMiLCAiLi4vLi4vLi4vanMvY29vcmRpbmF0b3IvZGF0YWZyYW1lLnRzIiwgIi4uLy4uLy4uL2pzL3V0aWwvd2FpdC50cyIsICIuLi8uLi8uLi9qcy9jb29yZGluYXRvci9zZWxlY3QudHMiLCAiLi4vLi4vLi4vanMvY2xpZW50cy90YWJsZS50cyIsICIuLi8uLi8uLi9qcy9jbGllbnRzL3Zpei50cyIsICIuLi8uLi8uLi9qcy93aWRnZXRzL3RhYmxlLnRzIl0sCiAgInNvdXJjZXNDb250ZW50IjogWyJpbXBvcnQgeyBBc3luY0R1Y2tEQkNvbm5lY3Rpb24gfSBmcm9tICdodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL0BkdWNrZGIvZHVja2RiLXdhc21AMS4yOS4wLytlc20nO1xuXG5pbXBvcnQge1xuICAgIE1vc2FpY0NsaWVudCxcbiAgICB3YXNtQ29ubmVjdG9yLFxuICAgIFNlbGVjdGlvbixcbiAgICBQYXJhbSxcbn0gZnJvbSAnaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L25wbS9AdXdkYXRhL21vc2FpYy1jb3JlQDAuMTYuMi8rZXNtJztcblxuaW1wb3J0IHsgSW5zdGFudGlhdGVDb250ZXh0IH0gZnJvbSAnaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L25wbS9AdXdkYXRhL21vc2FpYy1zcGVjQDAuMTYuMi8rZXNtJztcblxuaW1wb3J0IHsgaW5pdER1Y2tkYiB9IGZyb20gJy4vZHVja2RiJztcbmltcG9ydCB7IE1vc2FpY1F1ZXJ5IH0gZnJvbSAnLi9xdWVyeSc7XG5pbXBvcnQgeyBEYXRhRnJhbWUgfSBmcm9tICcuL2RhdGFmcmFtZSc7XG5pbXBvcnQgeyBzbGVlcCB9IGZyb20gJy4uL3V0aWwvd2FpdCc7XG5pbXBvcnQgeyB0b1NlbGVjdFF1ZXJ5IH0gZnJvbSAnLi9zZWxlY3QnO1xuXG5jbGFzcyBWaXpDb29yZGluYXRvciB7XG4gICAgcHJpdmF0ZSByZWFkb25seSBjdHhfOiBJbnN0YW50aWF0ZUNvbnRleHQ7XG4gICAgcHJpdmF0ZSByZWFkb25seSBkZnNfID0gbmV3IE1hcDxzdHJpbmcsIERhdGFGcmFtZT4oKTtcblxuICAgIGNvbnN0cnVjdG9yKHByaXZhdGUgcmVhZG9ubHkgY29ubl86IEFzeW5jRHVja0RCQ29ubmVjdGlvbikge1xuICAgICAgICB0aGlzLmN0eF8gPSBuZXcgSW5zdGFudGlhdGVDb250ZXh0KCk7XG4gICAgICAgIHRoaXMuY3R4Xy5jb29yZGluYXRvci5kYXRhYmFzZUNvbm5lY3Rvcih3YXNtQ29ubmVjdG9yKHsgY29ubmVjdGlvbjogdGhpcy5jb25uXyB9KSk7XG4gICAgfVxuXG4gICAgYWRkUGFyYW0obmFtZTogc3RyaW5nLCB2YWx1ZTogbnVtYmVyIHwgYm9vbGVhbiB8IHN0cmluZyk6IFBhcmFtIHtcbiAgICAgICAgaWYgKCF0aGlzLmN0eF8uYWN0aXZlUGFyYW1zLmhhcyhuYW1lKSkge1xuICAgICAgICAgICAgdGhpcy5jdHhfLmFjdGl2ZVBhcmFtcy5zZXQobmFtZSwgUGFyYW0udmFsdWUodmFsdWUpKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdGhpcy5jdHhfLmFjdGl2ZVBhcmFtcy5nZXQobmFtZSkhO1xuICAgIH1cblxuICAgIGdldFBhcmFtKG5hbWU6IHN0cmluZyk6IFBhcmFtIHwgdW5kZWZpbmVkIHtcbiAgICAgICAgcmV0dXJuIHRoaXMuY3R4Xy5hY3RpdmVQYXJhbXMuZ2V0KG5hbWUpO1xuICAgIH1cblxuICAgIGFzeW5jIGFkZERhdGFGcmFtZShpZDogc3RyaW5nLCBzb3VyY2VfaWQ6IHN0cmluZywgYnVmZmVyOiBVaW50OEFycmF5LCBxdWVyaWVzOiBNb3NhaWNRdWVyeVtdKSB7XG4gICAgICAgIC8vIGluc2VydCB0YWJsZSBpbnRvIGRhdGFiYXNlIGlmIHRoZXJlIGlzIGRhdGFcbiAgICAgICAgaWYgKGJ1ZmZlci5sZW5ndGggPiAwKSB7XG4gICAgICAgICAgICBhd2FpdCB0aGlzLmNvbm5fPy5pbnNlcnRBcnJvd0Zyb21JUENTdHJlYW0oYnVmZmVyLCB7XG4gICAgICAgICAgICAgICAgbmFtZTogaWQsXG4gICAgICAgICAgICAgICAgY3JlYXRlOiB0cnVlLFxuICAgICAgICAgICAgfSk7XG4gICAgICAgIH1cblxuICAgICAgICAvLyBleHRyYWN0IHBhcmFtZXRlcnMgZnJvbSBxdWVyaWVzIGFuZCByZWdpc3RlciB0aGVtXG4gICAgICAgIGNvbnN0IHBhcmFtcyA9IG5ldyBNYXA8c3RyaW5nLCBQYXJhbT4oKTtcbiAgICAgICAgZm9yIChjb25zdCBxdWVyeSBvZiBxdWVyaWVzKSB7XG4gICAgICAgICAgICBmb3IgKGNvbnN0IHAgb2YgT2JqZWN0LnZhbHVlcyhxdWVyeS5wYXJhbWV0ZXJzKSkge1xuICAgICAgICAgICAgICAgIHBhcmFtcy5zZXQocC5pZCwgdGhpcy5hZGRQYXJhbShwLmlkLCBwLmRlZmF1bHQpKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuXG4gICAgICAgIC8vIGNyZWF0ZSBhbmQgcmVnaXN0ZXIgZGZcbiAgICAgICAgY29uc3QgZGYgPSBuZXcgRGF0YUZyYW1lKFxuICAgICAgICAgICAgc291cmNlX2lkLFxuICAgICAgICAgICAgU2VsZWN0aW9uLmludGVyc2VjdCgpLFxuICAgICAgICAgICAgcXVlcmllcy5tYXAocSA9PiB0b1NlbGVjdFF1ZXJ5KHEsIHBhcmFtcykpLFxuICAgICAgICAgICAgcGFyYW1zXG4gICAgICAgICk7XG4gICAgICAgIHRoaXMuZGZzXy5zZXQoaWQsIGRmKTtcbiAgICB9XG5cbiAgICBhc3luYyBnZXREYXRhRnJhbWUoaWQ6IHN0cmluZykge1xuICAgICAgICAvLyBhdCBzdGFydHVwIHdlIGNhbid0IGNvbnRyb2wgdGhlIG9yZGVyIG9mIGRmIHByb2R1Y2luZyBhbmQgZGYgY29uc3VtaW5nXG4gICAgICAgIC8vIHdpZGdldHMsIHNvIHdlIG1heSBuZWVkIHRvIHdhaXQgYW5kIHJldHJ5IGZvciB0aGUgZGF0YSBmcmFtZVxuICAgICAgICB3aGlsZSAodHJ1ZSkge1xuICAgICAgICAgICAgY29uc3QgZGYgPSB0aGlzLmRmc18uZ2V0KGlkKTtcbiAgICAgICAgICAgIGlmIChkZikge1xuICAgICAgICAgICAgICAgIHJldHVybiBkZjtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgYXdhaXQgc2xlZXAoMTAwKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH1cblxuICAgIGdldEluc3RhbnRpYXRlQ29udGV4dCgpOiBJbnN0YW50aWF0ZUNvbnRleHQge1xuICAgICAgICByZXR1cm4gdGhpcy5jdHhfO1xuICAgIH1cblxuICAgIGFzeW5jIGNvbm5lY3RDbGllbnQoY2xpZW50OiBNb3NhaWNDbGllbnQpIHtcbiAgICAgICAgdGhpcy5jdHhfLmNvb3JkaW5hdG9yLmNvbm5lY3QoY2xpZW50KTtcbiAgICB9XG59XG5cbi8vIGdldCB0aGUgZ2xvYmFsIGNvb3JkaW5hdG9ycyBpbnN0YW5jZSwgZW5zdXJpbmcgd2UgZ2V0IHRoZSBzYW1lXG4vLyBpbnN0YW5jZSBldmFsIGFjcm9zcyBkaWZmZXJlbnQganMgYnVuZGxlcyBsb2FkZWQgaW50byB0aGUgcGFnZVxuY29uc3QgVklaX0NPT1JESU5BVE9SX0tFWSA9IFN5bWJvbC5mb3IoJ0BAaW5zcGVjdC12aXotY29vcmRpbmF0b3InKTtcbmFzeW5jIGZ1bmN0aW9uIHZpekNvb3JkaW5hdG9yKCk6IFByb21pc2U8Vml6Q29vcmRpbmF0b3I+IHtcbiAgICBjb25zdCBnbG9iYWxTY29wZTogYW55ID0gdHlwZW9mIHdpbmRvdyAhPT0gJ3VuZGVmaW5lZCcgPyB3aW5kb3cgOiBnbG9iYWxUaGlzO1xuICAgIGlmICghZ2xvYmFsU2NvcGVbVklaX0NPT1JESU5BVE9SX0tFWV0pIHtcbiAgICAgICAgZ2xvYmFsU2NvcGVbVklaX0NPT1JESU5BVE9SX0tFWV0gPSAoYXN5bmMgKCkgPT4ge1xuICAgICAgICAgICAgY29uc3QgZHVja2RiID0gYXdhaXQgaW5pdER1Y2tkYigpO1xuICAgICAgICAgICAgY29uc3QgY29ubiA9IGF3YWl0IGR1Y2tkYi5jb25uZWN0KCk7XG4gICAgICAgICAgICByZXR1cm4gbmV3IFZpekNvb3JkaW5hdG9yKGNvbm4pO1xuICAgICAgICB9KSgpO1xuICAgIH1cbiAgICByZXR1cm4gZ2xvYmFsU2NvcGVbVklaX0NPT1JESU5BVE9SX0tFWV0gYXMgUHJvbWlzZTxWaXpDb29yZGluYXRvcj47XG59XG5cbmV4cG9ydCB7IFZpekNvb3JkaW5hdG9yLCB2aXpDb29yZGluYXRvciB9O1xuIiwgImltcG9ydCB7XG4gICAgZ2V0SnNEZWxpdnJCdW5kbGVzLFxuICAgIHNlbGVjdEJ1bmRsZSxcbiAgICBBc3luY0R1Y2tEQixcbiAgICBDb25zb2xlTG9nZ2VyLFxuICAgIEFzeW5jRHVja0RCQ29ubmVjdGlvbixcbiAgICBMb2dMZXZlbCxcbn0gZnJvbSAnaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L25wbS9AZHVja2RiL2R1Y2tkYi13YXNtQDEuMjkuMC8rZXNtJztcblxuZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIGluaXREdWNrZGIoKSB7XG4gICAgY29uc3QgSlNERUxJVlJfQlVORExFUyA9IGdldEpzRGVsaXZyQnVuZGxlcygpO1xuXG4gICAgLy8gU2VsZWN0IGEgYnVuZGxlIGJhc2VkIG9uIGJyb3dzZXIgY2hlY2tzXG4gICAgY29uc3QgYnVuZGxlID0gYXdhaXQgc2VsZWN0QnVuZGxlKEpTREVMSVZSX0JVTkRMRVMpO1xuXG4gICAgY29uc3Qgd29ya2VyX3VybCA9IFVSTC5jcmVhdGVPYmplY3RVUkwoXG4gICAgICAgIG5ldyBCbG9iKFtgaW1wb3J0U2NyaXB0cyhcIiR7YnVuZGxlLm1haW5Xb3JrZXIhfVwiKTtgXSwge1xuICAgICAgICAgICAgdHlwZTogJ3RleHQvamF2YXNjcmlwdCcsXG4gICAgICAgIH0pXG4gICAgKTtcblxuICAgIC8vIEluc3RhbnRpYXRlIHRoZSBhc3luY2hyb25vdXMgdmVyc2lvbiBvZiBEdWNrREItd2FzbVxuICAgIGNvbnN0IHdvcmtlciA9IG5ldyBXb3JrZXIod29ya2VyX3VybCk7XG4gICAgY29uc3QgbG9nZ2VyID0gbmV3IENvbnNvbGVMb2dnZXIoTG9nTGV2ZWwuSU5GTyk7XG4gICAgY29uc3QgZGIgPSBuZXcgQXN5bmNEdWNrREIobG9nZ2VyLCB3b3JrZXIpO1xuICAgIGF3YWl0IGRiLmluc3RhbnRpYXRlKGJ1bmRsZS5tYWluTW9kdWxlLCBidW5kbGUucHRocmVhZFdvcmtlcik7XG4gICAgVVJMLnJldm9rZU9iamVjdFVSTCh3b3JrZXJfdXJsKTtcblxuICAgIHJldHVybiBkYjtcbn1cblxuZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIHdhaXRGb3JUYWJsZShcbiAgICBjb25uOiBBc3luY0R1Y2tEQkNvbm5lY3Rpb24sXG4gICAgdGFibGU6IHN0cmluZyxcbiAgICB7IHRpbWVvdXQgPSAxMF8wMDAsIGludGVydmFsID0gMjUwIH0gPSB7fVxuKSB7XG4gICAgY29uc3QgdDAgPSBwZXJmb3JtYW5jZS5ub3coKTtcblxuICAgIHdoaWxlICh0cnVlKSB7XG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgICBjb25zdCByZXMgPSBhd2FpdCBjb25uLnF1ZXJ5KFxuICAgICAgICAgICAgICAgIGBTRUxFQ1QgMVxuICAgICAgICAgICBGUk9NIGluZm9ybWF0aW9uX3NjaGVtYS50YWJsZXNcbiAgICAgICAgIFdIRVJFIHRhYmxlX3NjaGVtYSA9ICdtYWluJ1xuICAgICAgICAgICBBTkQgdGFibGVfbmFtZSAgID0gJyR7dGFibGV9J1xuICAgICAgICAgTElNSVQgMWBcbiAgICAgICAgICAgICk7XG5cbiAgICAgICAgICAgIGlmIChyZXMubnVtUm93cykgcmV0dXJuOyAvLyBzdWNjZXNzIFx1MjcyOFxuICAgICAgICB9IGNhdGNoIChlcnIpIHtcbiAgICAgICAgICAgIC8qIFRhYmxlIG9yIGV2ZW4gdGhlIGRhdGFiYXNlIGZpbGUgbWF5IG5vdCBiZSByZWFkeSB5ZXQuXG4gICAgICAgICBJZ25vcmUgdGhlIGVycm9yIGFuZCBrZWVwIHBvbGxpbmcuICovXG4gICAgICAgIH1cblxuICAgICAgICBpZiAocGVyZm9ybWFuY2Uubm93KCkgLSB0MCA+IHRpbWVvdXQpIHtcbiAgICAgICAgICAgIHRocm93IG5ldyBFcnJvcihgVGltZWQgb3V0IHdhaXRpbmcgZm9yIHRhYmxlIFwiJHt0YWJsZX1cImApO1xuICAgICAgICB9XG4gICAgICAgIGF3YWl0IG5ldyBQcm9taXNlKHIgPT4gc2V0VGltZW91dChyLCBpbnRlcnZhbCkpO1xuICAgIH1cbn1cbiIsICJpbXBvcnQgeyBQYXJhbSwgU2VsZWN0aW9uIH0gZnJvbSAnQHV3ZGF0YS9tb3NhaWMtY29yZSc7XG5pbXBvcnQgeyBTZWxlY3RRdWVyeSB9IGZyb20gJ2h0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9ucG0vQHV3ZGF0YS9tb3NhaWMtc3FsQDAuMTYuMi8rZXNtJztcblxuZXhwb3J0IGNsYXNzIERhdGFGcmFtZSB7XG4gICAgY29uc3RydWN0b3IoXG4gICAgICAgIHB1YmxpYyByZWFkb25seSB0YWJsZTogc3RyaW5nLFxuICAgICAgICBwdWJsaWMgcmVhZG9ubHkgc2VsZWN0aW9uOiBTZWxlY3Rpb24sXG4gICAgICAgIHB1YmxpYyByZWFkb25seSBxdWVyaWVzOiBTZWxlY3RRdWVyeVtdLFxuICAgICAgICBwdWJsaWMgcmVhZG9ubHkgcGFyYW1zOiBNYXA8c3RyaW5nLCBQYXJhbT5cbiAgICApIHt9XG59XG4iLCAiZXhwb3J0IGZ1bmN0aW9uIHNsZWVwKG1zOiBudW1iZXIpIHtcbiAgICByZXR1cm4gbmV3IFByb21pc2UocmVzb2x2ZSA9PiBzZXRUaW1lb3V0KHJlc29sdmUsIG1zKSk7XG59XG4iLCAiaW1wb3J0IHtcbiAgICBTZWxlY3RRdWVyeSxcbiAgICBlcSxcbiAgICBuZXEsXG4gICAgZ3QsXG4gICAgZ3RlLFxuICAgIGx0LFxuICAgIGx0ZSxcbiAgICBhbmQsXG4gICAgb3IsXG4gICAgc3VtLFxuICAgIGF2ZyxcbiAgICBtaW4sXG4gICAgbWF4LFxuICAgIG1vZGUsXG4gICAgbWVkaWFuLFxuICAgIGNvdW50LFxuICAgIGFkZCxcbiAgICBzdWIsXG4gICAgbXVsLFxuICAgIGRpdixcbiAgICBCaW5hcnlPcE5vZGUsXG4gICAgQWdncmVnYXRlTm9kZSxcbiAgICBFeHByVmFsdWUsXG4gICAgRnVuY3Rpb25Ob2RlLFxuICAgIEV4cHJOb2RlLFxuICAgIExpdGVyYWxOb2RlLFxuICAgIFBhcmFtTm9kZSxcbiAgICBWZXJiYXRpbU5vZGUsXG59IGZyb20gJ2h0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9ucG0vQHV3ZGF0YS9tb3NhaWMtc3FsQDAuMTYuMi8rZXNtJztcblxuaW1wb3J0IHtcbiAgICBNb3NhaWNRdWVyeSxcbiAgICBCaW5hcnlFeHByZXNzaW9uLFxuICAgIExvZ2ljYWxFeHByZXNzaW9uLFxuICAgIEZ1bmN0aW9uRXhwcmVzc2lvbixcbiAgICBVbmtub3duRXhwcmVzc2lvbixcbiAgICBQYXJhbWV0ZXJFeHByZXNzaW9uLFxuICAgIE9yZGVyQnlJdGVtLFxuICAgIEdyb3VwQnlGaWVsZCxcbiAgICBFeHByZXNzaW9uLFxufSBmcm9tICcuL3F1ZXJ5JztcbmltcG9ydCB7IFBhcmFtIH0gZnJvbSAnaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L25wbS9AdXdkYXRhL21vc2FpYy1jb3JlQDAuMTYuMi8rZXNtJztcblxuZXhwb3J0IGZ1bmN0aW9uIHRvU2VsZWN0UXVlcnkocXVlcnk6IE1vc2FpY1F1ZXJ5LCBwYXJhbXM6IE1hcDxzdHJpbmcsIFBhcmFtPik6IFNlbGVjdFF1ZXJ5IHtcbiAgICAvLyBjb252ZXJ0IHRvIGV4cHJlc3Npb25zXG4gICAgY29uc3Qgc2VsZWN0RXhwcmVzc2lvbnM6IFJlY29yZDxzdHJpbmcsIEV4cHJWYWx1ZT4gPSB7fTtcbiAgICBmb3IgKGNvbnN0IFthbGlhcywgZXhwcl0gb2YgT2JqZWN0LmVudHJpZXMocXVlcnkuc2VsZWN0KSkge1xuICAgICAgICBzZWxlY3RFeHByZXNzaW9uc1thbGlhc10gPSBidWlsZEV4cHJlc3Npb25WYWx1ZShleHByLCBwYXJhbXMpO1xuICAgIH1cbiAgICBsZXQgc2VsZWN0ID0gU2VsZWN0UXVlcnkuc2VsZWN0KHNlbGVjdEV4cHJlc3Npb25zKTtcblxuICAgIC8vIEFwcGx5IERJU1RJTkNUIGlmIG5lZWRlZFxuICAgIGlmIChxdWVyeS5kaXN0aW5jdCA9PT0gdHJ1ZSkge1xuICAgICAgICBzZWxlY3QgPSBzZWxlY3QuZGlzdGluY3QoKTtcbiAgICB9XG5cbiAgICAvLyBBcHBseSBXSEVSRSBjbGF1c2UgaWYgcHJlc2VudFxuICAgIGlmIChxdWVyeS53aGVyZSkge1xuICAgICAgICBzZWxlY3QgPSBhcHBseVdoZXJlQ2xhdXNlKHNlbGVjdCwgcGFyYW1zLCBxdWVyeS53aGVyZSk7XG4gICAgfVxuXG4gICAgLy8gQXBwbHkgR1JPVVAgQlkgY2xhdXNlIGlmIHByZXNlbnRcbiAgICBpZiAocXVlcnkuZ3JvdXBieSAmJiBxdWVyeS5ncm91cGJ5Lmxlbmd0aCA+IDApIHtcbiAgICAgICAgc2VsZWN0ID0gYXBwbHlHcm91cEJ5Q2xhdXNlKHNlbGVjdCwgcGFyYW1zLCBxdWVyeS5ncm91cGJ5KTtcbiAgICB9XG5cbiAgICAvLyBBcHBseSBIQVZJTkcgY2xhdXNlIGlmIHByZXNlbnRcbiAgICBpZiAocXVlcnkuaGF2aW5nKSB7XG4gICAgICAgIHNlbGVjdCA9IGFwcGx5SGF2aW5nQ2xhdXNlKHNlbGVjdCwgcGFyYW1zLCBxdWVyeS5oYXZpbmcpO1xuICAgIH1cblxuICAgIC8vIEFwcGx5IE9SREVSIEJZIGNsYXVzZSBpZiBwcmVzZW50XG4gICAgaWYgKHF1ZXJ5Lm9yZGVyYnkgJiYgcXVlcnkub3JkZXJieS5sZW5ndGggPiAwKSB7XG4gICAgICAgIHNlbGVjdCA9IGFwcGx5T3JkZXJCeUNsYXVzZShzZWxlY3QsIHF1ZXJ5Lm9yZGVyYnkpO1xuICAgIH1cblxuICAgIC8vIEFwcGx5IExJTUlUIGNsYXVzZSBpZiBwcmVzZW50XG4gICAgaWYgKHF1ZXJ5LmxpbWl0ICE9PSBudWxsICYmIHF1ZXJ5LmxpbWl0ICE9PSB1bmRlZmluZWQpIHtcbiAgICAgICAgc2VsZWN0ID0gc2VsZWN0LmxpbWl0KHF1ZXJ5LmxpbWl0KTtcbiAgICB9XG5cbiAgICAvLyBBcHBseSBTQU1QTEUgY2xhdXNlIGlmIHByZXNlbnRcbiAgICBpZiAocXVlcnkuc2FtcGxlICE9PSBudWxsICYmIHF1ZXJ5LnNhbXBsZSAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICAgIHNlbGVjdCA9IHNlbGVjdC5zYW1wbGUocXVlcnkuc2FtcGxlKTtcbiAgICB9XG5cbiAgICByZXR1cm4gc2VsZWN0O1xufVxuXG5mdW5jdGlvbiBpbnRlcnByZXRGdW5jdGlvbihcbiAgICBmdW5jOiBGdW5jdGlvbkV4cHJlc3Npb24sXG4gICAgcGFyYW1zOiBNYXA8c3RyaW5nLCBQYXJhbT5cbik6IEFnZ3JlZ2F0ZU5vZGUgfCBGdW5jdGlvbk5vZGUge1xuICAgIGNvbnN0IGZ1bmNOYW1lID0gZnVuYy5uYW1lLnRvTG93ZXJDYXNlKCk7XG4gICAgY29uc3QgYXJnczogRXhwck5vZGVbXSA9IGZ1bmMuYXJncy5tYXAoYSA9PiBidWlsZEV4cHJlc3Npb25Ob2RlKGEsIHBhcmFtcykpO1xuXG4gICAgLy8gSGFuZGxlIGNvbW1vbiBhZ2dyZWdhdGUgZnVuY3Rpb25zIGRpcmVjdGx5XG4gICAgc3dpdGNoIChmdW5jTmFtZSkge1xuICAgICAgICBjYXNlICdzdW0nOlxuICAgICAgICAgICAgcmV0dXJuIHN1bShhcmdzWzBdKTtcbiAgICAgICAgY2FzZSAnYXZnJzpcbiAgICAgICAgICAgIHJldHVybiBhdmcoYXJnc1swXSk7XG4gICAgICAgIGNhc2UgJ21pbic6XG4gICAgICAgICAgICByZXR1cm4gbWluKGFyZ3NbMF0pO1xuICAgICAgICBjYXNlICdtYXgnOlxuICAgICAgICAgICAgcmV0dXJuIG1heChhcmdzWzBdKTtcbiAgICAgICAgY2FzZSAnbW9kZSc6XG4gICAgICAgICAgICByZXR1cm4gbW9kZShhcmdzWzBdKTtcbiAgICAgICAgY2FzZSAnbWVkaWFuJzpcbiAgICAgICAgICAgIHJldHVybiBtZWRpYW4oYXJnc1swXSk7XG4gICAgICAgIGNhc2UgJ2NvdW50JzpcbiAgICAgICAgICAgIHJldHVybiBjb3VudChhcmdzWzBdKTtcbiAgICAgICAgZGVmYXVsdDpcbiAgICAgICAgICAgIC8vIEZvciBvdGhlciBmdW5jdGlvbnMsIHVzZSBhIGdlbmVyaWMgYXBwcm9hY2hcbiAgICAgICAgICAgIHJldHVybiBuZXcgRnVuY3Rpb25Ob2RlKGZ1bmNOYW1lLCBhcmdzKTtcbiAgICB9XG59XG5cbmZ1bmN0aW9uIGFwcGx5V2hlcmVDbGF1c2UoXG4gICAgcXVlcnk6IFNlbGVjdFF1ZXJ5LFxuICAgIHBhcmFtczogTWFwPHN0cmluZywgUGFyYW0+LFxuICAgIHdoZXJlRXhwcjogQmluYXJ5RXhwcmVzc2lvbiB8IExvZ2ljYWxFeHByZXNzaW9uIHwgVW5rbm93bkV4cHJlc3Npb25cbik6IFNlbGVjdFF1ZXJ5IHtcbiAgICAvLyBIYW5kbGUgZGlmZmVyZW50IGV4cHJlc3Npb24gdHlwZXNcbiAgICBpZiAod2hlcmVFeHByLnR5cGUgPT09ICdhbmQnIHx8IHdoZXJlRXhwci50eXBlID09PSAnb3InKSB7XG4gICAgICAgIC8vIExvZ2ljYWwgQU5EL09SIGV4cHJlc3Npb25cbiAgICAgICAgcmV0dXJuIGFwcGx5TG9naWNhbEV4cHJlc3Npb24ocXVlcnksIHBhcmFtcywgd2hlcmVFeHByIGFzIExvZ2ljYWxFeHByZXNzaW9uKTtcbiAgICB9IGVsc2UgaWYgKHdoZXJlRXhwci50eXBlID09PSAndW5rbm93bicpIHtcbiAgICAgICAgLy8gVW5rbm93biBleHByZXNzaW9uIC0gcGFzcyByYXcgU1FMXG4gICAgICAgIHJldHVybiBxdWVyeS53aGVyZShuZXcgVmVyYmF0aW1Ob2RlKCh3aGVyZUV4cHIgYXMgVW5rbm93bkV4cHJlc3Npb24pLmV4cHJlc3Npb24pKTtcbiAgICB9IGVsc2Uge1xuICAgICAgICBjb25zdCBjb25kaXRpb24gPSBidWlsZEJpbmFyeUV4cHJlc3Npb24od2hlcmVFeHByIGFzIEJpbmFyeUV4cHJlc3Npb24sIHBhcmFtcyk7XG4gICAgICAgIHJldHVybiBxdWVyeS53aGVyZShjb25kaXRpb24pO1xuICAgIH1cbn1cblxuZnVuY3Rpb24gYXBwbHlMb2dpY2FsRXhwcmVzc2lvbihcbiAgICBxdWVyeTogU2VsZWN0UXVlcnksXG4gICAgcGFyYW1zOiBNYXA8c3RyaW5nLCBQYXJhbT4sXG4gICAgZXhwcjogTG9naWNhbEV4cHJlc3Npb25cbik6IFNlbGVjdFF1ZXJ5IHtcbiAgICBjb25zdCB7IHR5cGUsIGV4cHJlc3Npb25zIH0gPSBleHByO1xuXG4gICAgaWYgKGV4cHJlc3Npb25zLmxlbmd0aCA9PT0gMCkge1xuICAgICAgICByZXR1cm4gcXVlcnk7XG4gICAgfSBlbHNlIGlmIChleHByZXNzaW9ucy5sZW5ndGggPT09IDEpIHtcbiAgICAgICAgcmV0dXJuIGFwcGx5V2hlcmVDbGF1c2UoXG4gICAgICAgICAgICBxdWVyeSxcbiAgICAgICAgICAgIHBhcmFtcyxcbiAgICAgICAgICAgIGV4cHJlc3Npb25zWzBdIGFzIEJpbmFyeUV4cHJlc3Npb24gfCBMb2dpY2FsRXhwcmVzc2lvbiB8IFVua25vd25FeHByZXNzaW9uXG4gICAgICAgICk7XG4gICAgfSBlbHNlIHtcbiAgICAgICAgY29uc3QgY29uZGl0aW9ucyA9IGV4cHJlc3Npb25zLm1hcChlID0+IGJ1aWxkRXhwcmVzc2lvblZhbHVlKGUsIHBhcmFtcykpO1xuICAgICAgICBpZiAodHlwZSA9PT0gJ2FuZCcpIHtcbiAgICAgICAgICAgIHJldHVybiBxdWVyeS53aGVyZShhbmQoLi4uY29uZGl0aW9ucykpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgcmV0dXJuIHF1ZXJ5LndoZXJlKG9yKC4uLmNvbmRpdGlvbnMpKTtcbiAgICAgICAgfVxuICAgIH1cbn1cblxuZnVuY3Rpb24gYXBwbHlHcm91cEJ5Q2xhdXNlKFxuICAgIHF1ZXJ5OiBTZWxlY3RRdWVyeSxcbiAgICBwYXJhbXM6IE1hcDxzdHJpbmcsIFBhcmFtPixcbiAgICBncm91cEJ5RmllbGRzOiAoc3RyaW5nIHwgR3JvdXBCeUZpZWxkKVtdXG4pOiBTZWxlY3RRdWVyeSB7XG4gICAgY29uc3QgZmllbGRzID0gZ3JvdXBCeUZpZWxkcy5tYXAoZmllbGQgPT4ge1xuICAgICAgICBpZiAodHlwZW9mIGZpZWxkID09PSAnc3RyaW5nJykge1xuICAgICAgICAgICAgcmV0dXJuIGZpZWxkO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgLy8gR3JvdXBCeUZpZWxkIG9iamVjdFxuICAgICAgICAgICAgaWYgKHR5cGVvZiBmaWVsZC5maWVsZCA9PT0gJ3N0cmluZycpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gZmllbGQuZmllbGQ7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIC8vIEZ1bmN0aW9uIGV4cHJlc3Npb24gaW4gR1JPVVAgQllcbiAgICAgICAgICAgICAgICByZXR1cm4gaW50ZXJwcmV0RnVuY3Rpb24oZmllbGQuZmllbGQsIHBhcmFtcyk7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICB9KTtcblxuICAgIHJldHVybiBxdWVyeS5ncm91cGJ5KC4uLmZpZWxkcyk7XG59XG5cbmZ1bmN0aW9uIGFwcGx5SGF2aW5nQ2xhdXNlKFxuICAgIHF1ZXJ5OiBTZWxlY3RRdWVyeSxcbiAgICBwYXJhbXM6IE1hcDxzdHJpbmcsIFBhcmFtPixcbiAgICBoYXZpbmdFeHByOiBCaW5hcnlFeHByZXNzaW9uIHwgTG9naWNhbEV4cHJlc3Npb24gfCBVbmtub3duRXhwcmVzc2lvblxuKTogU2VsZWN0UXVlcnkge1xuICAgIC8vIEhhdmluZyBjbGF1c2VzIGFyZSBzaW1pbGFyIHRvIFdIRVJFIGNsYXVzZXNcbiAgICBpZiAoJ3R5cGUnIGluIGhhdmluZ0V4cHIpIHtcbiAgICAgICAgLy8gSGFuZGxlIGRpZmZlcmVudCBleHByZXNzaW9uIHR5cGVzXG4gICAgICAgIGlmIChoYXZpbmdFeHByLnR5cGUgPT09ICdhbmQnIHx8IGhhdmluZ0V4cHIudHlwZSA9PT0gJ29yJykge1xuICAgICAgICAgICAgLy8gTG9naWNhbCBBTkQvT1IgZXhwcmVzc2lvblxuICAgICAgICAgICAgY29uc3QgeyB0eXBlLCBleHByZXNzaW9ucyB9ID0gaGF2aW5nRXhwciBhcyBMb2dpY2FsRXhwcmVzc2lvbjtcblxuICAgICAgICAgICAgLy8gQnVpbGQgdGhlIGNvbmRpdGlvbnMgYXJyYXlcbiAgICAgICAgICAgIGNvbnN0IGNvbmRpdGlvbnMgPSBleHByZXNzaW9ucy5tYXAoZSA9PiBidWlsZEV4cHJlc3Npb25WYWx1ZShlLCBwYXJhbXMpKTtcblxuICAgICAgICAgICAgLy8gQXBwbHkgdGhlIGNvbmRpdGlvbnMgdXNpbmcgdGhlIGFwcHJvcHJpYXRlIGxvZ2ljYWwgb3BlcmF0b3JcbiAgICAgICAgICAgIGlmICh0eXBlID09PSAnYW5kJykge1xuICAgICAgICAgICAgICAgIHJldHVybiBxdWVyeS5oYXZpbmcoYW5kKC4uLmNvbmRpdGlvbnMpKTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHF1ZXJ5LmhhdmluZyhvciguLi5jb25kaXRpb25zKSk7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0gZWxzZSBpZiAoaGF2aW5nRXhwci50eXBlID09PSAndW5rbm93bicpIHtcbiAgICAgICAgICAgIHJldHVybiBxdWVyeS5oYXZpbmcobmV3IFZlcmJhdGltTm9kZSgoaGF2aW5nRXhwciBhcyBVbmtub3duRXhwcmVzc2lvbikuZXhwcmVzc2lvbikpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgLy8gQmluYXJ5IGV4cHJlc3Npb24gKGNvbXBhcmlzb24pXG4gICAgICAgICAgICBjb25zdCBjb25kaXRpb24gPSBidWlsZEJpbmFyeUV4cHJlc3Npb24oaGF2aW5nRXhwciBhcyBCaW5hcnlFeHByZXNzaW9uLCBwYXJhbXMpO1xuICAgICAgICAgICAgcmV0dXJuIHF1ZXJ5LmhhdmluZyhjb25kaXRpb24pO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgLy8gRmFsbGJhY2sgLSBqdXN0IHBhc3MgdGhlIGV4cHJlc3Npb24gYXMgaXNcbiAgICByZXR1cm4gcXVlcnkuaGF2aW5nKGhhdmluZ0V4cHIpO1xufVxuXG5mdW5jdGlvbiBhcHBseU9yZGVyQnlDbGF1c2UocXVlcnk6IFNlbGVjdFF1ZXJ5LCBvcmRlckJ5SXRlbXM6IE9yZGVyQnlJdGVtW10pOiBTZWxlY3RRdWVyeSB7XG4gICAgLy8gVXNpbmcgc3RyaW5nIHByZWZpeGluZyBmb3IgZGVzY2VuZGluZyBvcmRlciBhcyB0aGF0J3Mgd2hhdCBNb3NhaWMgU1FMIHN1cHBvcnRzXG4gICAgY29uc3Qgb3JkZXJCeUZpZWxkcyA9IG9yZGVyQnlJdGVtcy5tYXAoaXRlbSA9PiB7XG4gICAgICAgIHJldHVybiBpdGVtLm9yZGVyID09PSAnZGVzYycgPyBgLSR7aXRlbS5maWVsZH1gIDogaXRlbS5maWVsZDtcbiAgICB9KTtcblxuICAgIHJldHVybiBxdWVyeS5vcmRlcmJ5KC4uLm9yZGVyQnlGaWVsZHMpO1xufVxuXG5mdW5jdGlvbiBidWlsZEV4cHJlc3Npb25Ob2RlKGV4cHI6IEV4cHJlc3Npb24sIHBhcmFtczogTWFwPHN0cmluZywgUGFyYW0+KTogRXhwck5vZGUge1xuICAgIGlmICh0eXBlb2YgZXhwciA9PT0gJ3N0cmluZycgfHwgdHlwZW9mIGV4cHIgPT09ICdudW1iZXInIHx8IHR5cGVvZiBleHByID09PSAnYm9vbGVhbicpIHtcbiAgICAgICAgcmV0dXJuIG5ldyBMaXRlcmFsTm9kZShleHByKTtcbiAgICB9IGVsc2UgaWYgKCd0eXBlJyBpbiBleHByKSB7XG4gICAgICAgIGlmIChleHByLnR5cGUgPT09ICdwYXJhbWV0ZXInKSB7XG4gICAgICAgICAgICBjb25zdCBuYW1lID0gKGV4cHIgYXMgUGFyYW1ldGVyRXhwcmVzc2lvbikubmFtZTtcbiAgICAgICAgICAgIGNvbnN0IHBhcmFtID0gcGFyYW1zLmdldChuYW1lKTtcbiAgICAgICAgICAgIGlmIChwYXJhbSA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKGBVbmtub3duIHBhcmFtZXRlciAke25hbWV9YCk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICByZXR1cm4gbmV3IFBhcmFtTm9kZShwYXJhbSk7XG4gICAgICAgIH0gZWxzZSBpZiAoZXhwci50eXBlID09PSAndW5rbm93bicpIHtcbiAgICAgICAgICAgIHJldHVybiBuZXcgVmVyYmF0aW1Ob2RlKChleHByIGFzIFVua25vd25FeHByZXNzaW9uKS5leHByZXNzaW9uKTtcbiAgICAgICAgfSBlbHNlIGlmIChleHByLnR5cGUgPT09ICdmdW5jdGlvbicpIHtcbiAgICAgICAgICAgIHJldHVybiBpbnRlcnByZXRGdW5jdGlvbihleHByIGFzIEZ1bmN0aW9uRXhwcmVzc2lvbiwgcGFyYW1zKTtcbiAgICAgICAgfSBlbHNlIGlmIChleHByLnR5cGUgPT09ICdhbmQnIHx8IGV4cHIudHlwZSA9PT0gJ29yJykge1xuICAgICAgICAgICAgcmV0dXJuIGJ1aWxkTG9naWNhbEV4cHJlc3Npb24oZXhwciBhcyBMb2dpY2FsRXhwcmVzc2lvbiwgcGFyYW1zKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHJldHVybiBidWlsZEJpbmFyeUV4cHJlc3Npb24oZXhwciBhcyBCaW5hcnlFeHByZXNzaW9uLCBwYXJhbXMpO1xuICAgICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgICAgdGhyb3cgRXJyb3IoYFVuZXhwZWN0ZWQgdHlwZSBmb3IgZXhwcmVzc2lvbjogJHt0eXBlb2YgZXhwcn1gKTtcbiAgICB9XG59XG5cbi8vIFRPRE86IFwiKlwiIGlzIGdldHRpbmcgcGFyc2VkIGFzIHVua25vd25cbmZ1bmN0aW9uIGJ1aWxkRXhwcmVzc2lvblZhbHVlKGV4cHI6IEV4cHJlc3Npb24sIHBhcmFtczogTWFwPHN0cmluZywgUGFyYW0+KTogRXhwclZhbHVlIHtcbiAgICBpZiAodHlwZW9mIGV4cHIgPT09ICdzdHJpbmcnKSB7XG4gICAgICAgIHJldHVybiBleHByO1xuICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybiBidWlsZEV4cHJlc3Npb25Ob2RlKGV4cHIsIHBhcmFtcyk7XG4gICAgfVxufVxuXG5mdW5jdGlvbiBidWlsZExvZ2ljYWxFeHByZXNzaW9uKGV4cHI6IExvZ2ljYWxFeHByZXNzaW9uLCBwYXJhbXM6IE1hcDxzdHJpbmcsIFBhcmFtPik6IEV4cHJOb2RlIHtcbiAgICBjb25zdCB7IHR5cGUsIGV4cHJlc3Npb25zIH0gPSBleHByO1xuXG4gICAgaWYgKGV4cHJlc3Npb25zLmxlbmd0aCA9PT0gMCkge1xuICAgICAgICByZXR1cm4gbmV3IExpdGVyYWxOb2RlKHRydWUpO1xuICAgIH0gZWxzZSBpZiAoZXhwcmVzc2lvbnMubGVuZ3RoID09PSAxKSB7XG4gICAgICAgIHJldHVybiBidWlsZEV4cHJlc3Npb25Ob2RlKGV4cHJlc3Npb25zWzBdLCBwYXJhbXMpO1xuICAgIH0gZWxzZSB7XG4gICAgICAgIGNvbnN0IGNvbmRpdGlvbnMgPSBleHByZXNzaW9ucy5tYXAoZSA9PiBidWlsZEV4cHJlc3Npb25Ob2RlKGUsIHBhcmFtcykpO1xuICAgICAgICBpZiAodHlwZSA9PT0gJ2FuZCcpIHtcbiAgICAgICAgICAgIHJldHVybiBhbmQoLi4uY29uZGl0aW9ucyk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICByZXR1cm4gb3IoLi4uY29uZGl0aW9ucyk7XG4gICAgICAgIH1cbiAgICB9XG59XG5cbmZ1bmN0aW9uIGJ1aWxkQmluYXJ5RXhwcmVzc2lvbihleHByOiBCaW5hcnlFeHByZXNzaW9uLCBwYXJhbXM6IE1hcDxzdHJpbmcsIFBhcmFtPik6IEJpbmFyeU9wTm9kZSB7XG4gICAgY29uc3QgeyB0eXBlLCBsZWZ0LCByaWdodCB9ID0gZXhwcjtcblxuICAgIGNvbnN0IGxlZnRPcGVyYW5kID0gYnVpbGRFeHByZXNzaW9uVmFsdWUobGVmdCwgcGFyYW1zKTtcbiAgICBjb25zdCByaWdodE9wZXJhbmQgPSBidWlsZEV4cHJlc3Npb25Ob2RlKHJpZ2h0LCBwYXJhbXMpO1xuXG4gICAgLy8gTWFwIGNvbW1vbiBjb21wYXJpc29uIG9wZXJhdG9ycyB0byBNb3NhaWMgU1FMIG1ldGhvZHNcbiAgICBzd2l0Y2ggKHR5cGUpIHtcbiAgICAgICAgY2FzZSAnZXEnOlxuICAgICAgICAgICAgcmV0dXJuIGVxKGxlZnRPcGVyYW5kLCByaWdodE9wZXJhbmQpO1xuICAgICAgICBjYXNlICduZXEnOlxuICAgICAgICAgICAgcmV0dXJuIG5lcShsZWZ0T3BlcmFuZCwgcmlnaHRPcGVyYW5kKTtcbiAgICAgICAgY2FzZSAnZ3QnOlxuICAgICAgICAgICAgcmV0dXJuIGd0KGxlZnRPcGVyYW5kLCByaWdodE9wZXJhbmQpO1xuICAgICAgICBjYXNlICdndGUnOlxuICAgICAgICAgICAgcmV0dXJuIGd0ZShsZWZ0T3BlcmFuZCwgcmlnaHRPcGVyYW5kKTtcbiAgICAgICAgY2FzZSAnbHQnOlxuICAgICAgICAgICAgcmV0dXJuIGx0KGxlZnRPcGVyYW5kLCByaWdodE9wZXJhbmQpO1xuICAgICAgICBjYXNlICdsdGUnOlxuICAgICAgICAgICAgcmV0dXJuIGx0ZShsZWZ0T3BlcmFuZCwgcmlnaHRPcGVyYW5kKTtcbiAgICAgICAgY2FzZSAnYWRkJzpcbiAgICAgICAgICAgIHJldHVybiBhZGQobGVmdE9wZXJhbmQsIHJpZ2h0T3BlcmFuZCk7XG4gICAgICAgIGNhc2UgJ3N1Yic6XG4gICAgICAgICAgICByZXR1cm4gc3ViKGxlZnRPcGVyYW5kLCByaWdodE9wZXJhbmQpO1xuICAgICAgICBjYXNlICdtdWwnOlxuICAgICAgICAgICAgcmV0dXJuIG11bChsZWZ0T3BlcmFuZCwgcmlnaHRPcGVyYW5kKTtcbiAgICAgICAgY2FzZSAnZGl2JzpcbiAgICAgICAgICAgIHJldHVybiBkaXYobGVmdE9wZXJhbmQsIHJpZ2h0T3BlcmFuZCk7XG4gICAgICAgIGRlZmF1bHQ6XG4gICAgICAgICAgICByZXR1cm4gbmV3IEJpbmFyeU9wTm9kZShcbiAgICAgICAgICAgICAgICB0eXBlLFxuICAgICAgICAgICAgICAgIGJ1aWxkRXhwcmVzc2lvbk5vZGUobGVmdCwgcGFyYW1zKSxcbiAgICAgICAgICAgICAgICBidWlsZEV4cHJlc3Npb25Ob2RlKHJpZ2h0LCBwYXJhbXMpXG4gICAgICAgICAgICApO1xuICAgIH1cbn1cbiIsICJpbXBvcnQgeyBQYXJhbSwgU2VsZWN0aW9uIH0gZnJvbSAnaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L25wbS9AdXdkYXRhL21vc2FpYy1jb3JlQDAuMTYuMi8rZXNtJztcbmltcG9ydCB7IFRhYmxlIGFzIE1vc2FpY1RhYmxlIH0gZnJvbSAnaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L25wbS9AdXdkYXRhL21vc2FpYy1pbnB1dHNAMC4xNi4yLytlc20nO1xuaW1wb3J0IHsgU2VsZWN0UXVlcnkgfSBmcm9tICdodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL0B1d2RhdGEvbW9zYWljLXNxbEAwLjE2LjIvK2VzbSc7XG5pbXBvcnQgeyBWaXpDbGllbnQgfSBmcm9tICcuL3Zpeic7XG5cbmV4cG9ydCBjbGFzcyBUYWJsZSBleHRlbmRzIE1vc2FpY1RhYmxlIHtcbiAgICBjb25zdHJ1Y3RvcihcbiAgICAgICAgZWw6IEhUTUxFbGVtZW50LFxuICAgICAgICB0YWJsZTogc3RyaW5nLFxuICAgICAgICBmaWx0ZXJCeTogU2VsZWN0aW9uLFxuICAgICAgICBwcml2YXRlIHJlYWRvbmx5IHF1ZXJpZXNfOiBTZWxlY3RRdWVyeVtdLFxuICAgICAgICBwcml2YXRlIHJlYWRvbmx5IHBhcmFtc186IE1hcDxzdHJpbmcsIFBhcmFtPlxuICAgICkge1xuICAgICAgICBzdXBlcih7IGVsZW1lbnQ6IGVsLCBmaWx0ZXJCeSwgZnJvbTogdGFibGUgfSk7XG4gICAgICAgIHRoaXMucGFyYW1zXy5mb3JFYWNoKHZhbHVlID0+IHtcbiAgICAgICAgICAgIHZhbHVlLmFkZEV2ZW50TGlzdGVuZXIoJ3ZhbHVlJywgKCkgPT4gdGhpcy5yZXF1ZXN0VXBkYXRlKCkpO1xuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBxdWVyeShmaWx0ZXI/OiBhbnlbXSk6IFNlbGVjdFF1ZXJ5IHtcbiAgICAgICAgbGV0IHF1ZXJ5ID0gc3VwZXIucXVlcnkoZmlsdGVyKTtcbiAgICAgICAgcmV0dXJuIFZpekNsaWVudC5hcHBseVF1ZXJpZXMocXVlcnksIHRoaXMucXVlcmllc18pO1xuICAgIH1cbn1cbiIsICJpbXBvcnQge1xuICAgIE1vc2FpY0NsaWVudCxcbiAgICBQYXJhbSxcbiAgICBTZWxlY3Rpb24sXG59IGZyb20gJ2h0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9ucG0vQHV3ZGF0YS9tb3NhaWMtY29yZUAwLjE2LjIvK2VzbSc7XG5pbXBvcnQgeyBTZWxlY3RRdWVyeSB9IGZyb20gJ2h0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9ucG0vQHV3ZGF0YS9tb3NhaWMtc3FsQDAuMTYuMi8rZXNtJztcblxuZXhwb3J0IGFic3RyYWN0IGNsYXNzIFZpekNsaWVudCBleHRlbmRzIE1vc2FpY0NsaWVudCB7XG4gICAgY29uc3RydWN0b3IoXG4gICAgICAgIHByaXZhdGUgcmVhZG9ubHkgdGFibGVfOiBzdHJpbmcsXG4gICAgICAgIGZpbHRlckJ5OiBTZWxlY3Rpb24sXG4gICAgICAgIHByaXZhdGUgcmVhZG9ubHkgcXVlcmllc186IFNlbGVjdFF1ZXJ5W10sXG4gICAgICAgIHByaXZhdGUgcmVhZG9ubHkgcGFyYW1zXzogTWFwPHN0cmluZywgUGFyYW0+XG4gICAgKSB7XG4gICAgICAgIHN1cGVyKGZpbHRlckJ5KTtcbiAgICAgICAgdGhpcy5wYXJhbXNfLmZvckVhY2godmFsdWUgPT4ge1xuICAgICAgICAgICAgdmFsdWUuYWRkRXZlbnRMaXN0ZW5lcigndmFsdWUnLCAoKSA9PiB0aGlzLnJlcXVlc3RVcGRhdGUoKSk7XG4gICAgICAgIH0pO1xuICAgIH1cblxuICAgIHF1ZXJ5KGZpbHRlcjogYW55W10gPSBbXSk6IFNlbGVjdFF1ZXJ5IHtcbiAgICAgICAgbGV0IHF1ZXJ5ID0gU2VsZWN0UXVlcnkuc2VsZWN0KCcqJykuZnJvbSh0aGlzLnRhYmxlXykud2hlcmUoZmlsdGVyKTtcbiAgICAgICAgcmV0dXJuIFZpekNsaWVudC5hcHBseVF1ZXJpZXMocXVlcnksIHRoaXMucXVlcmllc18pO1xuICAgIH1cblxuICAgIHN0YXRpYyBhcHBseVF1ZXJpZXMocXVlcnk6IFNlbGVjdFF1ZXJ5LCBxdWVyaWVzOiBTZWxlY3RRdWVyeVtdKTogU2VsZWN0UXVlcnkge1xuICAgICAgICBmb3IgKGxldCBxIG9mIHF1ZXJpZXMpIHtcbiAgICAgICAgICAgIHF1ZXJ5ID0gcS5jbG9uZSgpLmZyb20ocXVlcnkpO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBxdWVyeTtcbiAgICB9XG59XG4iLCAiaW1wb3J0IHR5cGUgeyBSZW5kZXJQcm9wcyB9IGZyb20gJ0Bhbnl3aWRnZXQvdHlwZXMnO1xuXG5pbXBvcnQgeyB2aXpDb29yZGluYXRvciB9IGZyb20gJy4uL2Nvb3JkaW5hdG9yJztcblxuaW1wb3J0IHsgVGFibGUgfSBmcm9tICcuLi9jbGllbnRzL3RhYmxlJztcblxuaW50ZXJmYWNlIFRhYmxlUHJvcHMge1xuICAgIGRmX2lkOiBzdHJpbmc7XG59XG5cbmFzeW5jIGZ1bmN0aW9uIHJlbmRlcih7IG1vZGVsLCBlbCB9OiBSZW5kZXJQcm9wczxUYWJsZVByb3BzPikge1xuICAgIC8vIHVud3JhcCB3aWRnZXQgcGFyYW1ldGVyc1xuICAgIGNvbnN0IGRmX2lkOiBzdHJpbmcgPSBtb2RlbC5nZXQoJ2RmX2lkJyk7XG5cbiAgICAvLyBnZXQgdGhlIGRhdGEgZnJhbWVcbiAgICBjb25zdCBjb29yZGluYXRvciA9IGF3YWl0IHZpekNvb3JkaW5hdG9yKCk7XG4gICAgY29uc3QgZGYgPSBhd2FpdCBjb29yZGluYXRvci5nZXREYXRhRnJhbWUoZGZfaWQpO1xuXG4gICAgLy8gY3JlYXRlIGFuZCBjb25uZWN0IHRoZSB0YWJsZSB2aWV3XG4gICAgY29uc3QgdmlldyA9IG5ldyBUYWJsZShlbCwgZGYudGFibGUsIGRmLnNlbGVjdGlvbiwgZGYucXVlcmllcywgZGYucGFyYW1zKTtcbiAgICBhd2FpdCBjb29yZGluYXRvci5jb25uZWN0Q2xpZW50KHZpZXcpO1xufVxuXG5leHBvcnQgZGVmYXVsdCB7IHJlbmRlciB9O1xuIl0sCiAgIm1hcHBpbmdzIjogIjtBQUVBO0FBQUEsRUFFSTtBQUFBLEVBQ0E7QUFBQSxFQUNBO0FBQUEsT0FDRztBQUVQLFNBQVMsMEJBQTBCOzs7QUNUbkM7QUFBQSxFQUNJO0FBQUEsRUFDQTtBQUFBLEVBQ0E7QUFBQSxFQUNBO0FBQUEsRUFFQTtBQUFBLE9BQ0c7QUFFUCxlQUFzQixhQUFhO0FBQy9CLFFBQU0sbUJBQW1CLG1CQUFtQjtBQUc1QyxRQUFNLFNBQVMsTUFBTSxhQUFhLGdCQUFnQjtBQUVsRCxRQUFNLGFBQWEsSUFBSTtBQUFBLElBQ25CLElBQUksS0FBSyxDQUFDLGtCQUFrQixPQUFPLFVBQVcsS0FBSyxHQUFHO0FBQUEsTUFDbEQsTUFBTTtBQUFBLElBQ1YsQ0FBQztBQUFBLEVBQ0w7QUFHQSxRQUFNLFNBQVMsSUFBSSxPQUFPLFVBQVU7QUFDcEMsUUFBTSxTQUFTLElBQUksY0FBYyxTQUFTLElBQUk7QUFDOUMsUUFBTSxLQUFLLElBQUksWUFBWSxRQUFRLE1BQU07QUFDekMsUUFBTSxHQUFHLFlBQVksT0FBTyxZQUFZLE9BQU8sYUFBYTtBQUM1RCxNQUFJLGdCQUFnQixVQUFVO0FBRTlCLFNBQU87QUFDWDs7O0FDMUJPLElBQU0sWUFBTixNQUFnQjtBQUFBLEVBQ25CLFlBQ29CLE9BQ0EsV0FDQSxTQUNBLFFBQ2xCO0FBSmtCO0FBQ0E7QUFDQTtBQUNBO0FBQUEsRUFDakI7QUFDUDs7O0FDVk8sU0FBUyxNQUFNLElBQVk7QUFDOUIsU0FBTyxJQUFJLFFBQVEsYUFBVyxXQUFXLFNBQVMsRUFBRSxDQUFDO0FBQ3pEOzs7QUNGQTtBQUFBLEVBQ0k7QUFBQSxFQUNBO0FBQUEsRUFDQTtBQUFBLEVBQ0E7QUFBQSxFQUNBO0FBQUEsRUFDQTtB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SUFBSTtBQUFBLElBQ2xDLEdBQUc7QUFBQSxFQUNQO0FBQ0EsU0FBTyxZQUFZLG1CQUFtQjtBQUMxQzs7O0FLbEdBLFNBQVMsU0FBUyxtQkFBbUI7OztBQ0RyQztBQUFBLEVBQ0ksZ0JBQUFBO0FBQUEsT0FHRztBQUNQLFNBQVMsZUFBQUMsb0JBQW1CO0FBRXJCLElBQWUsWUFBZixNQUFlLG1CQUFrQkQsY0FBYTtBQUFBLEVBQ2pELFlBQ3FCLFFBQ2pCLFVBQ2lCLFVBQ0EsU0FDbkI7QUFDRSxVQUFNLFFBQVE7QUFMRztBQUVBO0FBQ0E7QUFHakIsU0FBSyxRQUFRLFFBQVEsV0FBUztBQUMxQixZQUFNLGlCQUFpQixTQUFTLE1BQU0sS0FBSyxjQUFjLENBQUM7QUFBQSxJQUM5RCxDQUFDO0FBQUEsRUFDTDtBQUFBLEVBRUEsTUFBTSxTQUFnQixDQUFDLEdBQWdCO0FBQ25DLFFBQUksUUFBUUMsYUFBWSxPQUFPLEdBQUcsRUFBRSxLQUFLLEtBQUssTUFBTSxFQUFFLE1BQU0sTUFBTTtBQUNsRSxXQUFPLFdBQVUsYUFBYSxPQUFPLEtBQUssUUFBUTtBQUFBLEVBQ3REO0FBQUEsRUFFQSxPQUFPLGFBQWEsT0FBb0IsU0FBcUM7QUFDekUsYUFBUyxLQUFLLFNBQVM7QUFDbkIsY0FBUSxFQUFFLE1BQU0sRUFBRSxLQUFLLEtBQUs7QUFBQSxJQUNoQztBQUNBLFdBQU87QUFBQSxFQUNYO0FBQ0o7OztBRDFCTyxJQUFNLFFBQU4sY0FBb0IsWUFBWTtBQUFBLEVBQ25DLFlBQ0ksSUFDQSxPQUNBLFVBQ2lCLFVBQ0EsU0FDbkI7QUFDRSxVQUFNLEVBQUUsU0FBUyxJQUFJLFVBQVUsTUFBTSxNQUFNLENBQUM7QUFIM0I7QUFDQTtBQUdqQixTQUFLLFFBQVEsUUFBUSxXQUFTO0FBQzFCLFlBQU0saUJBQWlCLFNBQVMsTUFBTSxLQUFLLGNBQWMsQ0FBQztBQUFBLElBQzlELENBQUM7QUFBQSxFQUNMO0FBQUEsRUFFQSxNQUFNLFFBQTZCO0FBQy9CLFFBQUksUUFBUSxNQUFNLE1BQU0sTUFBTTtBQUM5QixXQUFPLFVBQVUsYUFBYSxPQUFPLEtBQUssUUFBUTtBQUFBLEVBQ3REO0FBQ0o7OztBRWJBLGVBQWUsT0FBTyxFQUFFLE9BQU8sR0FBRyxHQUE0QjtBQUUxRCxRQUFNLFFBQWdCLE1BQU0sSUFBSSxPQUFPO0FBR3ZDLFFBQU0sY0FBYyxNQUFNLGVBQWU7QUFDekMsUUFBTSxLQUFLLE1BQU0sWUFBWSxhQUFhLEtBQUs7QUFHL0MsUUFBTSxPQUFPLElBQUksTUFBTSxJQUFJLEdBQUcsT0FBTyxHQUFHLFdBQVcsR0FBRyxTQUFTLEdBQUcsTUFBTTtBQUN4RSxRQUFNLFlBQVksY0FBYyxJQUFJO0FBQ3hDO0FBRUEsSUFBTyxnQkFBUSxFQUFFLE9BQU87IiwKICAibmFtZXMiOiBbIk1vc2FpY0NsaWVudCIsICJTZWxlY3RRdWVyeSJdCn0K
