from typing import Any, Sequence

from .._core.param import Param
from .._util.marshall import dict_remove_none
from ._transform import Transform, TransformArg


def count(
    count: TransformArg | None = None,
    distinct: bool | None = None,
    orderby: str | Param | Sequence[str | Param] | None = None,
    partitionby: str | Param | Sequence[str | Param] | None = None,
    rows: Sequence[float | None] | Param | None = None,
    range: Sequence[float | None] | Param | None = None,
) -> Transform:
    """A count aggregate transform.

    count: Compute the count of records in an aggregation group. If specified, only non-null expression values are counted. If omitted, all rows within a group are counted.
    distinct: Aggregate distinct.
    orderby: Window transform orderby.
    partitionby: Window transform partitionby.
    rows: Window transform rows.
    range: Window transform range.
    """
    config: dict[str, Any] = dict(count=count)
    config = config | dict_remove_none(
        dict(
            distinct=distinct,
            orderby=orderby,
            partitionby=partitionby,
            rows=rows,
            range=range,
        )
    )
    return Transform(config)
