from pydantic import JsonValue

from ._transform import Transform


def agg(agg: str, label: str | None = None) -> Transform:
    """Aggregation transform for a column.

    Args:
        agg: A SQL expression string to calculate an aggregate value. Embedded Param references, such as `f"SUM({param} + 1)"`, are supported. For expressions without aggregate functions, use `sql()` instead."
        label: A label for this expression, for example to label a plot axis.
    """
    config: dict[str, JsonValue] = dict(agg=agg)
    if label is not None:
        config["label"] = label
    return Transform(config)
