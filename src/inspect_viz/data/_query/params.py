from typing import Any

from .mosaic import (
    BinaryExpression,
    FunctionExpression,
    LogicalExpression,
    MosaicQuery,
    Parameter,
    ParameterExpression,
)


def extract_parameter_names(query: MosaicQuery) -> list[str]:
    parameter_names: list[str] = []

    # Helper function to search for parameters in expressions
    def search_expression(expr: Any) -> None:
        if expr is None:
            return

        if isinstance(expr, ParameterExpression):
            parameter_names.append(expr.name)
        elif isinstance(expr, BinaryExpression):
            search_expression(expr.left)
            search_expression(expr.right)
        elif isinstance(expr, LogicalExpression):
            for sub_expr in expr.expressions:
                search_expression(sub_expr)
        elif isinstance(expr, FunctionExpression):
            for arg in expr.args:
                search_expression(arg)

    # Search in WHERE clause
    if query.where:
        search_expression(query.where)

    # Search in SELECT expressions
    if query.select:
        for expr in query.select.values():
            if not isinstance(expr, str):
                search_expression(expr)

    # Search in HAVING clause
    if query.having:
        search_expression(query.having)

    # Search in ORDER BY expressions if they contain complex expressions
    if query.orderby:
        for item in query.orderby:
            if hasattr(item, "field") and not isinstance(item.field, str):
                search_expression(item.field)

    # Return unique parameter names
    return list(set(parameter_names))


def extract_parameters_with_types(
    query: MosaicQuery, values: dict[str, int | float | bool | str]
) -> dict[str, Parameter]:
    """
    Extract parameters from a MosaicQuery and create Parameter objects with types.

    This function finds all parameter names in the query and creates Parameter
    objects for them, inferring types from the provided values.

    Args:
        query: The MosaicQuery object to search
        values: A dictionary of parameter values

    Returns:
        A dictionary of parameter name to Parameter object mappings
    """
    # Get all parameter names from the query
    parameter_names = extract_parameter_names(query)

    # Create Parameter objects for each parameter name
    parameters = {}
    for name in parameter_names:
        if name in values:
            # Infer the SQL type of the parameter value
            param_type = _infer_type(values[name])

            # Create Parameter object
            parameters[name] = Parameter(name=name, value=values[name], type=param_type)
        else:
            raise ValueError(f"Default value not provided for parameter '{name}'")

    return parameters


def _infer_type(value: Any) -> str:
    """Infer the SQL type of a Python value."""
    if isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, bool):
        return "boolean"
    elif isinstance(value, str):
        return "text"
    elif value is None:
        return "null"
    else:
        return "text"  # Default fallback
