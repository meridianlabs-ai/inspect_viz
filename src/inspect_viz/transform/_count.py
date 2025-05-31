from pydantic import JsonValue

from inspect_viz._core.param import Param
from inspect_viz.transform._transform import Transform


def count(expr: str | Param | None = None) -> Transform:
    """Compute a count aggregate.

    expr: An optional expression to count. If specified, only non-null expression values are counted. If omitted, all rows within a group are counted.
    """
    config: dict[str, JsonValue] = {"count": expr}
    return Transform(config)
