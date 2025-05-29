from pydantic import JsonValue

from ._transform import Transform


def sql(sql: str, label: str | None = None) -> Transform:
    """SQL transform for a column.

    Args:
        sql: A SQL expression string to derive a new column value. Embedded Param references, such as `f"{param} + 1"`, are supported. For expressions with aggregate functions, use `agg()` instead.
        label: A label for this expression, for example to label a plot axis.
    """
    config: dict[str, JsonValue] = dict(sql=sql)
    if label is not None:
        config["label"] = label
    return Transform(config)
