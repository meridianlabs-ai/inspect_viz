from typing import Any

from inspect_viz.transform._window import WindowOptions

from .._util.marshall import dict_remove_none
from ._transform import Transform, TransformArg


def count(
    count: TransformArg | None = None,
    distinct: bool | None = None,
    **options: WindowOptions,
) -> Transform:
    """A count aggregate transform.

    count: Compute the count of records in an aggregation group. If specified, only non-null expression values are counted. If omitted, all rows within a group are counted.
    distinct: Aggregate distinct.
    **options: Window transform options.
    """
    config: dict[str, Any] = dict(count=count)
    config = config | dict_remove_none(dict(distinct=distinct) | options)
    return Transform(config)
