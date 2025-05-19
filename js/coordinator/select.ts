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
    AggregateNode,
    ExprValue,
    FunctionNode,
    ExprNode,
    LiteralNode,
    ParamNode,
    VerbatimNode,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm';

import {
    MosaicQuery,
    BinaryExpression,
    LogicalExpression,
    FunctionExpression,
    UnknownExpression,
    ParameterExpression,
    OrderByItem,
    GroupByField,
    Expression,
} from './query';
import { Param } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

export function toSelectQuery(query: MosaicQuery, params: Map<string, Param>): SelectQuery {
    // convert to expressions
    const selectExpressions: Record<string, ExprValue> = {};
    for (const [alias, expr] of Object.entries(query.select)) {
        selectExpressions[alias] = buildExpressionValue(expr, params);
    }
    let select = SelectQuery.select(selectExpressions);

    // Apply DISTINCT if needed
    if (query.distinct === true) {
        select = select.distinct();
    }

    // Apply WHERE clause if present
    if (query.where) {
        select = applyWhereClause(select, params, query.where);
    }

    // Apply GROUP BY clause if present
    if (query.groupby && query.groupby.length > 0) {
        select = applyGroupByClause(select, params, query.groupby);
    }

    // Apply HAVING clause if present
    if (query.having) {
        select = applyHavingClause(select, params, query.having);
    }

    // Apply ORDER BY clause if present
    if (query.orderby && query.orderby.length > 0) {
        select = applyOrderByClause(select, query.orderby);
    }

    // Apply LIMIT clause if present
    if (query.limit !== null && query.limit !== undefined) {
        select = select.limit(query.limit);
    }

    // Apply SAMPLE clause if present
    if (query.sample !== null && query.sample !== undefined) {
        select = select.sample(query.sample);
    }

    return select;
}

function interpretFunction(
    func: FunctionExpression,
    params: Map<string, Param>
): AggregateNode | FunctionNode {
    const funcName = func.name.toLowerCase();
    const args: ExprNode[] = func.args.map(a => buildExpressionNode(a, params));

    // Handle common aggregate functions directly
    switch (funcName) {
        case 'sum':
            return sum(args[0]);
        case 'avg':
            return avg(args[0]);
        case 'min':
            return min(args[0]);
        case 'max':
            return max(args[0]);
        case 'mode':
            return mode(args[0]);
        case 'median':
            return median(args[0]);
        case 'count':
            return count(args[0]);
        default:
            // For other functions, use a generic approach
            return new FunctionNode(funcName, args);
    }
}

function applyWhereClause(
    query: SelectQuery,
    params: Map<string, Param>,
    whereExpr: BinaryExpression | LogicalExpression | UnknownExpression
): SelectQuery {
    // Handle different expression types
    if (whereExpr.type === 'and' || whereExpr.type === 'or') {
        // Logical AND/OR expression
        return applyLogicalExpression(query, params, whereExpr as LogicalExpression);
    } else if (whereExpr.type === 'unknown') {
        // Unknown expression - pass raw SQL
        return query.where(new VerbatimNode((whereExpr as UnknownExpression).expression));
    } else {
        const condition = buildBinaryExpression(whereExpr as BinaryExpression, params);
        return query.where(condition);
    }
}

function applyLogicalExpression(
    query: SelectQuery,
    params: Map<string, Param>,
    expr: LogicalExpression
): SelectQuery {
    const { type, expressions } = expr;

    if (expressions.length === 0) {
        return query;
    } else if (expressions.length === 1) {
        return applyWhereClause(
            query,
            params,
            expressions[0] as BinaryExpression | LogicalExpression | UnknownExpression
        );
    } else {
        const conditions = expressions.map(e => buildExpressionValue(e, params));
        if (type === 'and') {
            return query.where(and(...conditions));
        } else {
            return query.where(or(...conditions));
        }
    }
}

function applyGroupByClause(
    query: SelectQuery,
    params: Map<string, Param>,
    groupByFields: (string | GroupByField)[]
): SelectQuery {
    const fields = groupByFields.map(field => {
        if (typeof field === 'string') {
            return field;
        } else {
            // GroupByField object
            if (typeof field.field === 'string') {
                return field.field;
            } else {
                // Function expression in GROUP BY
                return interpretFunction(field.field, params);
            }
        }
    });

    return query.groupby(...fields);
}

function applyHavingClause(
    query: SelectQuery,
    params: Map<string, Param>,
    havingExpr: BinaryExpression | LogicalExpression | UnknownExpression
): SelectQuery {
    // Having clauses are similar to WHERE clauses
    if ('type' in havingExpr) {
        // Handle different expression types
        if (havingExpr.type === 'and' || havingExpr.type === 'or') {
            // Logical AND/OR expression
            const { type, expressions } = havingExpr as LogicalExpression;

            // Build the conditions array
            const conditions = expressions.map(e => buildExpressionValue(e, params));

            // Apply the conditions using the appropriate logical operator
            if (type === 'and') {
                return query.having(and(...conditions));
            } else {
                return query.having(or(...conditions));
            }
        } else if (havingExpr.type === 'unknown') {
            return query.having(new VerbatimNode((havingExpr as UnknownExpression).expression));
        } else {
            // Binary expression (comparison)
            const condition = buildBinaryExpression(havingExpr as BinaryExpression, params);
            return query.having(condition);
        }
    }

    // Fallback - just pass the expression as is
    return query.having(havingExpr);
}

function applyOrderByClause(query: SelectQuery, orderByItems: OrderByItem[]): SelectQuery {
    // Using string prefixing for descending order as that's what Mosaic SQL supports
    const orderByFields = orderByItems.map(item => {
        return item.order === 'desc' ? `-${item.field}` : item.field;
    });

    return query.orderby(...orderByFields);
}

function buildExpressionNode(expr: Expression, params: Map<string, Param>): ExprNode {
    if (typeof expr === 'string' || typeof expr === 'number' || typeof expr === 'boolean') {
        return new LiteralNode(expr);
    } else if ('type' in expr) {
        if (expr.type === 'parameter') {
            const name = (expr as ParameterExpression).name;
            const param = params.get(name);
            if (param === undefined) {
                throw new Error(`Unknown parameter ${name}`);
            }
            return new ParamNode(param);
        } else if (expr.type === 'unknown') {
            return new VerbatimNode((expr as UnknownExpression).expression);
        } else if (expr.type === 'function') {
            return interpretFunction(expr as FunctionExpression, params);
        } else if (expr.type === 'and' || expr.type === 'or') {
            return buildLogicalExpression(expr as LogicalExpression, params);
        } else {
            return buildBinaryExpression(expr as BinaryExpression, params);
        }
    } else {
        throw Error(`Unexpected type for expression: ${typeof expr}`);
    }
}

// TODO: "*" is getting parsed as unknown
function buildExpressionValue(expr: Expression, params: Map<string, Param>): ExprValue {
    if (typeof expr === 'string') {
        return expr;
    } else {
        return buildExpressionNode(expr, params);
    }
}

function buildLogicalExpression(expr: LogicalExpression, params: Map<string, Param>): ExprNode {
    const { type, expressions } = expr;

    if (expressions.length === 0) {
        return new LiteralNode(true);
    } else if (expressions.length === 1) {
        return buildExpressionNode(expressions[0], params);
    } else {
        const conditions = expressions.map(e => buildExpressionNode(e, params));
        if (type === 'and') {
            return and(...conditions);
        } else {
            return or(...conditions);
        }
    }
}

function buildBinaryExpression(expr: BinaryExpression, params: Map<string, Param>): BinaryOpNode {
    const { type, left, right } = expr;

    const leftOperand = buildExpressionValue(left, params);
    const rightOperand = buildExpressionNode(right, params);

    // Map common comparison operators to Mosaic SQL methods
    switch (type) {
        case 'eq':
            return eq(leftOperand, rightOperand);
        case 'neq':
            return neq(leftOperand, rightOperand);
        case 'gt':
            return gt(leftOperand, rightOperand);
        case 'gte':
            return gte(leftOperand, rightOperand);
        case 'lt':
            return lt(leftOperand, rightOperand);
        case 'lte':
            return lte(leftOperand, rightOperand);
        case 'add':
            return add(leftOperand, rightOperand);
        case 'sub':
            return sub(leftOperand, rightOperand);
        case 'mul':
            return mul(leftOperand, rightOperand);
        case 'div':
            return div(leftOperand, rightOperand);
        default:
            return new BinaryOpNode(
                type,
                buildExpressionNode(left, params),
                buildExpressionNode(right, params)
            );
    }
}
