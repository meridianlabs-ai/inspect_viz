import { SelectQuery } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm';

import {
    MosaicQuery,
    BinaryExpression,
    LogicalExpression,
    FunctionExpression,
    UnknownExpression,
    ParameterExpression,
    Expression,
} from './query';

/**
 * Converts a MosaicQuery to a Mosaic SelectQuery
 * @param query The MosaicQuery to convert
 * @param tableName The name of the table to query from
 * @returns A Mosaic SelectQuery
 */
export function convertToSelectQuery(query: MosaicQuery): SelectQuery {
    // Process SELECT clause
    const selectExpressions: Record<string, any> = {};
    for (const [alias, expr] of Object.entries(query.select)) {
        if (typeof expr === 'string') {
            // Simple column selection
            selectExpressions[alias] = expr;
        } else {
            // Complex expression (function, binary expression, etc.)
            selectExpressions[alias] = convertExpression(expr);
        }
    }
    let selectQuery = SelectQuery.select(selectExpressions);

    // Process DISTINCT
    if (query.distinct === true) {
        selectQuery = selectQuery.distinct();
    }

    // Process WHERE clause
    if (query.where) {
        selectQuery = selectQuery.where(convertExpression(query.where));
    }

    // Process GROUP BY clause
    if (query.groupby && query.groupby.length > 0) {
        const groupByFields = query.groupby.map(field => {
            if (typeof field === 'string') {
                return field;
            } else {
                // Convert GroupByField objects
                if (typeof field.field === 'string') {
                    return field.field;
                } else {
                    return convertExpression(field.field);
                }
            }
        });

        selectQuery = selectQuery.groupby(...groupByFields);
    }

    // Process HAVING clause
    if (query.having) {
        selectQuery = selectQuery.having(convertExpression(query.having));
    }

    // Process ORDER BY clause
    if (query.orderby && query.orderby.length > 0) {
        // Using string prefixing for desc order - field names as is for asc, prefixed with '-' for desc
        const orderByFields = query.orderby.map(orderBy => {
            return orderBy.order === 'desc' ? `-${orderBy.field}` : orderBy.field;
        });

        selectQuery = selectQuery.orderby(...orderByFields);
    }

    // Process LIMIT clause
    if (query.limit !== null && query.limit !== undefined) {
        selectQuery = selectQuery.limit(query.limit);
    }

    // Process SAMPLE clause
    if (query.sample !== null && query.sample !== undefined) {
        selectQuery = selectQuery.sample(query.sample);
    }

    return selectQuery;
}

/**
 * Converts a MosaicQuery expression to a Mosaic SQL expression
 * @param expr The expression to convert
 * @returns A Mosaic SQL expression
 */
function convertExpression(expr: Expression): any {
    if (typeof expr === 'string' || typeof expr === 'number' || typeof expr === 'boolean') {
        // Primitive types can be used directly
        return expr;
    }

    // Handle different expression types
    if ('type' in expr) {
        switch (expr.type) {
            case 'function':
                return convertFunctionExpression(expr as FunctionExpression);

            case 'and':
            case 'or':
                return convertLogicalExpression(expr as LogicalExpression);

            case 'parameter':
                return convertParameterExpression(expr as ParameterExpression);

            case 'unknown':
                return convertUnknownExpression(expr as UnknownExpression);

            default:
                // Binary expressions (eq, neq, gt, gte, lt, lte, etc.)
                return convertBinaryExpression(expr as BinaryExpression);
        }
    }

    // Fallback for unknown expression types
    console.warn('Unknown expression type:', expr);
    return expr;
}

/**
 * Converts a FunctionExpression to a Mosaic SQL function call
 */
function convertFunctionExpression(expr: FunctionExpression): any {
    // Convert the function arguments
    const args = expr.args.map(arg => convertExpression(arg));

    // Create a function call using the appropriate Mosaic SQL API
    // This depends on the specific function being called
    const fnName = expr.name.toLowerCase();

    // For standard SQL functions, we create an object representation
    // that the Mosaic SQL parser can understand
    return {
        type: 'function',
        function: fnName,
        args: args,
    };
}

/**
 * Converts a LogicalExpression (AND/OR) to a Mosaic SQL condition
 */
function convertLogicalExpression(expr: LogicalExpression): any {
    // Convert each sub-expression
    const expressions = expr.expressions.map(e => convertExpression(e));

    // Create a logical operator using the appropriate Mosaic SQL API
    if (expr.type === 'and') {
        // Combine with AND
        return expressions.reduce((acc, curr) => ({ type: 'and', left: acc, right: curr }));
    } else {
        // Combine with OR
        return expressions.reduce((acc, curr) => ({ type: 'or', left: acc, right: curr }));
    }
}

/**
 * Converts a BinaryExpression (comparison, arithmetic) to a Mosaic SQL condition
 */
function convertBinaryExpression(expr: BinaryExpression): any {
    // Convert left and right operands
    const left = convertExpression(expr.left);
    const right = convertExpression(expr.right);

    // Create a binary operator using the appropriate Mosaic SQL API
    return {
        type: expr.type,
        left,
        right,
    };
}

/**
 * Converts a ParameterExpression to a Mosaic SQL parameter
 */
function convertParameterExpression(expr: ParameterExpression): any {
    // Parameters in Mosaic SQL can be represented as placeholders
    // The value should come from the parameters object in MosaicQuery
    return {
        type: 'parameter',
        name: expr.name,
    };
}

/**
 * Converts an UnknownExpression to a raw SQL expression string
 */
function convertUnknownExpression(expr: UnknownExpression): any {
    // For unknown expressions, pass through the raw expression string
    return {
        type: 'raw',
        expression: expr.expression,
    };
}
