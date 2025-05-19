from typing import Any, Callable, Sequence, TypeVar, cast

import sqlglot
import sqlglot.expressions as exp

from .constants import DEFAULT_TABLE
from .mosaic import (
    BinaryExpression,
    Expression,
    FunctionExpression,
    GroupByField,
    LogicalExpression,
    MosaicQuery,
    OrderByItem,
    ParameterExpression,
    UnknownExpression,
    extract_parameters_with_types,
)

T = TypeVar("T")


def parse_sql(sql: str | exp.Select, **parameters: Any) -> MosaicQuery:
    # resolve to exp.Select
    if isinstance(sql, str):
        expr = sqlglot.parse_one(sql, dialect="duckdb")
        if not isinstance(expr, exp.Select):
            raise ValueError(f"Unsupported SQL expression type: {type(sql)}")
        sql = expr

    # ensure we have a select clause
    if len(sql.selects) == 0:
        sql = sql.select("*")

    # map from to the target table
    sql = sql.from_(DEFAULT_TABLE)

    # create query
    query = MosaicQuery.model_validate(_convert_select(sql))

    # extract parameters
    query.parameters = extract_parameters_with_types(query, parameters)

    # return
    return query


def _convert_select(select: exp.Select) -> dict[str, Any]:
    """Convert a SELECT statement to mosaic-sql structure."""
    result: dict[str, object] = {"sql": select.sql(dialect="duckdb"), "parameters": {}}

    # Process each clause in the SELECT statement
    _process_clause(
        select, "expressions", result, "select", _convert_select_expressions
    )
    _process_clause(select, "distinct", result, "distinct", lambda x: True)
    _process_clause(select, "where", result, "where", _convert_where)
    _process_clause(select, "group", result, "groupby", _convert_group_by)
    _process_clause(select, "having", result, "having", _convert_having)
    _process_clause(select, "order", result, "orderby", _convert_order_by)
    _process_clause(select, "limit", result, "limit", _convert_limit)

    return result


def _process_clause(
    sql_obj: exp.Expression,
    arg_name: str,
    result: dict[str, Any],
    result_key: str,
    converter: Callable[[Any], T],
) -> None:
    """Process a SQL clause and add it to the result if present."""
    if arg := sql_obj.args.get(arg_name):
        result[result_key] = converter(arg)


def _get_expression_from_args(expr: exp.Expression, arg_name: str) -> exp.Expression:
    """Extract an expression from args."""
    if arg_name in expr.args and expr.args[arg_name] is not None:
        return cast(exp.Expression, expr.args[arg_name])
    return expr


def _convert_having(
    having_clause: exp.Expression,
) -> BinaryExpression | LogicalExpression | UnknownExpression:
    """Convert HAVING clause to mosaic-sql structure."""
    if isinstance(having_clause, exp.Having):
        # Extract the actual condition from the Having object
        return _convert_logical_expression(having_clause.args["this"])

    # If it's already the condition expression, convert it directly
    return _convert_logical_expression(having_clause)


def _convert_select_expressions(
    expressions: Sequence[exp.Expression],
) -> dict[str, str | FunctionExpression | BinaryExpression | UnknownExpression]:
    """Convert SELECT expressions to mosaic-sql structure."""
    result: dict[
        str, str | FunctionExpression | BinaryExpression | UnknownExpression
    ] = {}

    for expr in expressions:
        if isinstance(expr, exp.Column):
            # Simple column selection
            column_name = expr.args["this"].args["this"]
            result[column_name] = column_name

        elif isinstance(expr, exp.Alias):
            # Aliased expression
            alias_name = expr.args["alias"].args["this"]
            expression = expr.args["this"]

            if isinstance(expression, exp.Column):
                # Simple aliased column
                result[alias_name] = expression.args["this"].args["this"]
            else:
                # More complex aliased expression
                result[alias_name] = _convert_expression(expression)

        elif _is_aggregate_function(expr):
            # Aggregate functions without aliases
            result[expr.key] = _convert_expression(expr)

        else:
            # Other expressions
            expr_result = _convert_expression(expr)
            # If it's a string identifier, use it as is
            if isinstance(expr_result, str):
                result[expr_result] = expr_result
            else:
                # For complex expressions, use a generated key
                result[f"expr_{len(result)}"] = expr_result

    return result


def _convert_where(
    where_clause: exp.Expression,
) -> BinaryExpression | LogicalExpression | UnknownExpression:
    """Convert WHERE clause to mosaic-sql structure."""
    where_expr = (
        _get_expression_from_args(where_clause, "this")
        if isinstance(where_clause, exp.Where)
        else where_clause
    )
    return _convert_logical_expression(where_expr)


def _is_same_logical_type(expr: exp.Expression, logical_type: str) -> bool:
    """Check if an expression is of the same logical type (AND/OR)."""
    return (
        (isinstance(expr, exp.And) or (hasattr(expr, "key") and expr.key == "and"))
        and logical_type == "and"
    ) or (
        (isinstance(expr, exp.Or) or (hasattr(expr, "key") and expr.key == "or"))
        and logical_type == "or"
    )


def _convert_logical_expression(
    expr: exp.Expression,
) -> BinaryExpression | LogicalExpression | UnknownExpression:
    """Convert logical expressions, handling nested AND/OR structures."""
    # Unwrap parenthesized expressions
    if isinstance(expr, exp.Paren) and "this" in expr.args:
        return _convert_logical_expression(expr.args["this"])

    # Handle logical operations (AND, OR)
    if (
        isinstance(expr, (exp.And, exp.Or))
        or isinstance(expr, exp.Binary)
        and (expr.key == "and" or expr.key == "or")
    ):
        # Determine the logical type
        logical_type = (
            "and"
            if isinstance(expr, exp.And) or (hasattr(expr, "key") and expr.key == "and")
            else "or"
        )

        # Start with expressions from the current logical operation
        expressions = []

        # Process left and right side expressions
        for arg_name in ["this", "expression"]:
            if arg_name in expr.args and expr.args[arg_name] is not None:
                side_expr = expr.args[arg_name]

                # If the side is the same logical operation, flatten it
                if _is_same_logical_type(side_expr, logical_type):
                    # Recursively convert and merge the expressions
                    side_result = _convert_logical_expression(side_expr)
                    if (
                        isinstance(side_result, LogicalExpression)
                        and side_result.type == logical_type
                    ):
                        expressions.extend(side_result.expressions)
                    else:
                        expressions.append(side_result)
                else:
                    # Different logical operation or basic expression
                    expressions.append(_convert_logical_expression(side_expr))

        # Create the logical expression with all collected expressions
        return LogicalExpression(
            type="and" if logical_type == "and" else "or", expressions=expressions
        )

    # For basic conditions or other expressions
    return cast(
        BinaryExpression | LogicalExpression | UnknownExpression,
        _convert_expression(expr),
    )


def _convert_group_by(group_clause: exp.Expression) -> list[str | GroupByField]:
    """Convert GROUP BY clause to mosaic-sql structure."""
    result: list[str | GroupByField] = []

    if isinstance(group_clause, exp.Group):
        expressions = group_clause.args.get("expressions", [])

        for expr in expressions:
            if isinstance(expr, exp.Column):
                # Simple column reference
                result.append(expr.args["this"].args["this"])
            elif isinstance(expr, exp.Alias) and isinstance(
                expr.args["this"], exp.Column
            ):
                # Column with alias
                field = expr.args["this"].args["this"].args["this"]
                result.append(GroupByField(field=field))
            elif _is_aggregate_function(expr):
                # Function expression
                func_expr = _convert_expression(expr)
                if isinstance(func_expr, FunctionExpression):
                    result.append(GroupByField(field=func_expr))
                else:
                    result.append(GroupByField(field=str(expr)))
            else:
                # Other expressions
                converted = _convert_expression(expr)
                if isinstance(converted, str):
                    result.append(converted)
                else:
                    result.append(GroupByField(field=converted))
    else:
        # If it's not a Group object, try to convert it directly
        converted = _convert_expression(group_clause)
        if isinstance(converted, str):
            result.append(converted)
        else:
            result.append(GroupByField(field=converted))

    return result


def _extract_field_from_expression(expression: exp.Expression) -> Any:
    """Extract field from an expression."""
    if isinstance(expression, exp.Column):
        return expression.args["this"].args["this"]
    else:
        return _convert_expression(expression)


def _extract_direction(expr: exp.Expression) -> str:
    """Extract sort direction from an expression."""
    return "desc" if expr.args.get("desc") else "asc"


def _convert_order_by(order_clause: exp.Expression) -> list[OrderByItem]:
    """Convert ORDER BY clause to mosaic-sql structure."""
    result: list[OrderByItem] = []

    # Handle Order object with expressions list
    if isinstance(order_clause, exp.Order):
        if "expressions" in order_clause.args:
            expressions = order_clause.args["expressions"]
            for expr in expressions:
                if isinstance(expr, exp.Ordered):
                    direction = _extract_direction(expr)

                    if "this" in expr.args and expr.args["this"] is not None:
                        field = _extract_field_from_expression(expr.args["this"])
                        result.append(
                            OrderByItem(
                                field=field,
                                order="asc" if direction == "asc" else "desc",
                            )
                        )
        return result

    # Handle list of expressions
    if isinstance(order_clause, list):
        for expr in order_clause:
            if hasattr(expr, "args"):
                direction = _extract_direction(expr)
                field = None

                # Try to extract field from different arg positions
                for arg_name in ["expression", "this"]:
                    if arg_name in expr.args and expr.args[arg_name] is not None:
                        field = _extract_field_from_expression(expr.args[arg_name])
                        break

                if field is not None:
                    result.append(
                        OrderByItem(
                            field=field, order="asc" if direction == "asc" else "desc"
                        )
                    )

    return result


def _convert_limit(limit_clause: exp.Expression) -> int:
    """Convert LIMIT clause to mosaic-sql structure."""
    if isinstance(limit_clause, exp.Literal):
        return int(limit_clause.args["this"])
    elif isinstance(limit_clause, exp.Limit):
        if "expression" in limit_clause.args and isinstance(
            limit_clause.args["expression"], exp.Literal
        ):
            return int(limit_clause.args["expression"].args["this"])
    elif (
        hasattr(limit_clause, "args")
        and "expression" in limit_clause.args
        and isinstance(limit_clause.args["expression"], exp.Literal)
    ):
        return int(limit_clause.args["expression"].args["this"])
    return cast(int, _convert_expression(limit_clause))


def _is_aggregate_function(expr: exp.Expression) -> bool:
    """Check if an expression is an aggregate function."""
    return any(
        isinstance(expr, agg_type)
        for agg_type in [exp.Avg, exp.Count, exp.Sum, exp.Min, exp.Max]
    )


def _convert_expression(expr: exp.Expression) -> Any:
    """
    Convert a sqlglot expression to a mosaic-sql compatible structure.

    This is a generic handler for different expression types.
    """
    if expr is None:
        return None

    # star as string
    if isinstance(expr, exp.Star):
        return "*"

    # Unwrap parenthesized expressions
    if isinstance(expr, exp.Paren) and "this" in expr.args:
        return _convert_expression(expr.args["this"])

    # Handle different expression types
    if isinstance(expr, exp.Column):
        return expr.args["this"].args["this"]

    elif isinstance(expr, exp.Parameter | exp.Placeholder):
        return _convert_parameter_expression(expr)

    elif isinstance(expr, exp.Literal):
        return _convert_literal(expr)

    # Handle logical operations (AND, OR)
    elif isinstance(expr, (exp.And, exp.Or)):
        return _convert_logical_op(expr)

    elif (
        isinstance(expr, exp.Binary)
        or hasattr(expr, "args")
        and "this" in expr.args
        and "expression" in expr.args
    ):
        return _convert_binary_expression(expr)

    # Handle aggregate functions
    elif _is_aggregate_function(expr):
        return _convert_function_expression(expr)

    # Return a generic representation for unsupported expressions
    return UnknownExpression(expression=str(expr.sql(dialect="duckdb")))


def _convert_parameter_expression(
    expr: exp.Expression,
) -> ParameterExpression | UnknownExpression:
    """Convert parameter expressions."""
    # Handle parameter expressions (e.g., :param_name or $param_name)
    param_name = expr.args.get("this", "")
    # For unnamed parameters (like ?), we can't create a meaningful parameter expression
    if not param_name:
        # Return a placeholder that will be recognized as a parameter but without a specific name
        return UnknownExpression(expression="?")

    # Remove any prefix like : or $ if present
    if (
        param_name.startswith(":")
        or param_name.startswith("$")
        or param_name.startswith("@")
    ):
        param_name = param_name[1:]

    return ParameterExpression(name=param_name)


def _convert_literal(expr: exp.Literal) -> Any:
    """Convert literal expressions to appropriate Python types."""
    value = expr.args["this"]
    is_string = expr.args.get("is_string", False)

    if is_string:
        return value

    try:
        if "." in value:
            return float(value)
        else:
            return int(value)
    except (ValueError, TypeError):
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        return value


def _convert_logical_op(expr: exp.Expression) -> LogicalExpression:
    """Convert logical operations (AND, OR)."""
    # Determine logical operation type
    logical_type = "and" if isinstance(expr, exp.And) else "or"

    # Get the expressions to combine
    left = _convert_expression(cast(exp.Expression, expr.args.get("this")))
    right = _convert_expression(cast(exp.Expression, expr.args.get("expression")))

    # Create a list of expressions
    expressions = []

    # If either side is the same type of logical expression, flatten it
    if isinstance(left, LogicalExpression) and left.type == logical_type:
        expressions.extend(left.expressions)
    else:
        expressions.append(left)

    if isinstance(right, LogicalExpression) and right.type == logical_type:
        expressions.extend(right.expressions)
    else:
        expressions.append(right)

    return LogicalExpression(
        type="and" if logical_type == "and" else "or", expressions=expressions
    )


def _convert_binary_expression(
    expr: exp.Expression,
) -> BinaryExpression | LogicalExpression:
    """Convert binary expressions."""
    left = _convert_expression(expr.args["this"])
    right = _convert_expression(expr.args["expression"])
    op = expr.key

    # Map sqlglot operators to mosaic-sql operators
    op_map = {
        "eq": "eq",  # equals
        "neq": "neq",  # not equals
        "gt": "gt",  # greater than
        "gte": "gte",  # greater than or equal
        "lt": "lt",  # less than
        "lte": "lte",  # less than or equal
        "and": "and",  # logical AND
        "or": "or",  # logical OR
        "add": "add",  # addition
        "sub": "sub",  # subtraction
        "mul": "mul",  # multiplication
        "div": "div",  # division
    }

    if op in op_map:
        return BinaryExpression(type=op_map[op], left=left, right=right)

    # Special case for AND/OR since they could be binary or logical depending on the SQL dialect/version
    elif op == "and" or op == "or":
        return LogicalExpression(
            type="and" if op == "and" else "or", expressions=[left, right]
        )
    else:
        # Default structure for unsupported operators
        return BinaryExpression(type="binary", left=left, right=right)


def _convert_function_expression(expr: exp.Expression) -> FunctionExpression:
    """Convert function expressions."""
    func_name = expr.key.upper()

    # Handle different argument patterns for aggregates
    args: list[Expression] = []

    # Handle COUNT(*) special case
    if isinstance(expr, exp.Count) and isinstance(expr.args["this"], exp.Star):
        args = ["*"]
    elif "this" in expr.args and expr.args["this"] is not None:
        args = [_convert_expression(expr.args["this"])]

    return FunctionExpression(name=func_name, args=args)
