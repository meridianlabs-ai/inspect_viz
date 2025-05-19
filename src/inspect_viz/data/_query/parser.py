from typing import Any, Sequence, cast

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
)
from .params import extract_parameters_with_types


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

    # Handle SELECT expressions
    if select.args.get("expressions"):
        result["select"] = _convert_select_expressions(select.args["expressions"])

    # Handle DISTINCT clause
    if select.args.get("distinct"):
        # DISTINCT can be a boolean or an expression in sqlglot
        # For mosaic-sql, we just need a boolean flag
        result["distinct"] = True

    # Handle SAMPLE clause (if sqlglot supports it)
    if hasattr(select, "sample") and select.sample is not None:
        # Sample might be expressed as a percentage or count
        sample_expr = select.sample
        if isinstance(sample_expr, exp.Literal):
            sample_value = _convert_expression(sample_expr)
            # If it's a percentage (0-1), keep as is, otherwise convert to count
            if isinstance(sample_value, (int, float)):
                if sample_value <= 1:  # Percentage
                    result["sample"] = sample_value
                else:  # Count
                    result["sample"] = int(sample_value)

    # Handle WHERE clause
    if select.args.get("where"):
        result["where"] = _convert_where(select.args["where"])

    # Handle GROUP BY clause
    if select.args.get("group"):
        result["groupby"] = _convert_group_by(select.args["group"])

    # Handle HAVING clause
    if select.args.get("having"):
        result["having"] = _convert_having(select.args["having"])

    # Handle ORDER BY clause
    if select.args.get("order"):
        result["orderby"] = _convert_order_by(select.args["order"])

    # Handle LIMIT clause
    if select.args.get("limit"):
        result["limit"] = _convert_limit(select.args["limit"])

    return result


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

        elif any(
            isinstance(expr, agg_type)
            for agg_type in [exp.Avg, exp.Count, exp.Sum, exp.Min, exp.Max]
        ):
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
    if isinstance(where_clause, exp.Where):
        where_expr = where_clause.args["this"]
    else:
        where_expr = where_clause

    return _convert_logical_expression(where_expr)


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

        # Handle left side (this)
        if "this" in expr.args and expr.args["this"] is not None:
            left_expr = expr.args["this"]
            # If the left side is the same logical operation, flatten it
            if (
                (
                    isinstance(left_expr, exp.And)
                    or (hasattr(left_expr, "key") and left_expr.key == "and")
                )
                and logical_type == "and"
                or (
                    isinstance(left_expr, exp.Or)
                    or (hasattr(left_expr, "key") and left_expr.key == "or")
                )
                and logical_type == "or"
            ):
                # Recursively convert and merge the expressions
                left_result = _convert_logical_expression(left_expr)
                if (
                    isinstance(left_result, LogicalExpression)
                    and left_result.type == logical_type
                ):
                    expressions.extend(left_result.expressions)
                else:
                    expressions.append(left_result)
            else:
                # Different logical operation or basic expression
                expressions.append(_convert_logical_expression(left_expr))

        # Handle right side (expression)
        if "expression" in expr.args and expr.args["expression"] is not None:
            right_expr = expr.args["expression"]
            if (
                (
                    isinstance(right_expr, exp.And)
                    or (hasattr(right_expr, "key") and right_expr.key == "and")
                )
                and logical_type == "and"
                or (
                    isinstance(right_expr, exp.Or)
                    or (hasattr(right_expr, "key") and right_expr.key == "or")
                )
                and logical_type == "or"
            ):
                # Recursively convert and merge the expressions
                right_result = _convert_logical_expression(right_expr)
                if (
                    isinstance(right_result, LogicalExpression)
                    and right_result.type == logical_type
                ):
                    expressions.extend(right_result.expressions)
                else:
                    expressions.append(right_result)
            else:
                # Different logical operation or basic expression
                expressions.append(_convert_logical_expression(right_expr))

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
            elif any(
                isinstance(expr, func_type)
                for func_type in [exp.Avg, exp.Count, exp.Sum, exp.Min, exp.Max]
            ):
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


def _convert_order_by(order_clause: exp.Expression) -> list[OrderByItem]:
    """Convert ORDER BY clause to mosaic-sql structure."""
    result: list[OrderByItem] = []

    # Handle Order object with expressions list
    if isinstance(order_clause, exp.Order):
        if "expressions" in order_clause.args:
            expressions = order_clause.args["expressions"]
            for expr in expressions:
                if isinstance(expr, exp.Ordered):
                    direction = "desc" if expr.args.get("desc") else "asc"

                    if "this" in expr.args and expr.args["this"] is not None:
                        expression = expr.args["this"]

                        if isinstance(expression, exp.Column):
                            field = expression.args["this"].args["this"]
                        else:
                            field = _convert_expression(expression)

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
                direction = "desc" if expr.args.get("desc") else "asc"

                field = None
                if "expression" in expr.args:
                    expression = expr.args["expression"]

                    if isinstance(expression, exp.Column):
                        field = expression.args["this"].args["this"]
                    else:
                        field = _convert_expression(expression)
                elif "this" in expr.args:
                    # Sometimes the expression is in 'this' instead
                    expression = expr.args["this"]
                    if isinstance(expression, exp.Column):
                        field = expression.args["this"].args["this"]
                    else:
                        field = _convert_expression(expression)

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

    elif isinstance(expr, exp.Literal):
        # Convert literals to appropriate Python types
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

    # Handle logical operations (AND, OR)
    elif isinstance(expr, (exp.And, exp.Or)):
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

    elif (
        isinstance(expr, exp.Binary)
        or hasattr(expr, "args")
        and "this" in expr.args
        and "expression" in expr.args
    ):
        # Handle binary operations (comparisons, arithmetic, etc.)
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

    # Handle aggregate functions
    elif any(
        isinstance(expr, agg_type)
        for agg_type in [exp.Avg, exp.Count, exp.Sum, exp.Min, exp.Max]
    ):
        func_name = expr.key.upper()

        # Handle different argument patterns for aggregates
        args: list[Expression] = []

        # Handle COUNT(*) special case
        if isinstance(expr, exp.Count) and isinstance(expr.args["this"], exp.Star):
            args = ["*"]
        elif "this" in expr.args and expr.args["this"] is not None:
            args = [_convert_expression(expr.args["this"])]

        return FunctionExpression(name=func_name, args=args)

    # Return a generic representation for unsupported expressions
    return UnknownExpression(expression=str(expr.sql(dialect="duckdb")))
