import { Param } from './param';

export type Expression =
    | string
    | number
    | boolean
    | BinaryExpression
    | LogicalExpression
    | FunctionExpression
    | ParameterExpression
    | UnknownExpression;

export interface FunctionExpression {
    type: 'function';
    name: string;
    args: Expression[];
}

export interface BinaryExpression {
    type: string; // eq, neq, gt, gte, lt, lte, and, or, add, sub, mul, div
    left: Expression;
    right: Expression;
}

export interface LogicalExpression {
    type: 'and' | 'or';
    expressions: Expression[];
}

export interface ParameterExpression {
    type: 'parameter';
    name: string;
}

export interface UnknownExpression {
    type: 'unknown';
    expression: string;
}

export interface GroupByField {
    field: string | FunctionExpression;
}

export interface OrderByItem {
    field: string;
    order: 'asc' | 'desc';
}

export interface MosaicQuery {
    sql: string;
    parameters: Record<string, Param>;
    select: Record<string, string | FunctionExpression | BinaryExpression | UnknownExpression>;
    distinct?: boolean | null;
    sample?: number | null;
    where?: BinaryExpression | LogicalExpression | UnknownExpression | null;
    groupby?: (string | GroupByField)[] | null;
    having?: BinaryExpression | LogicalExpression | UnknownExpression | null;
    orderby?: OrderByItem[] | null;
    limit?: number | null;
}
