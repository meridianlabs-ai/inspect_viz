from typing import Any, Unpack

from inspect_viz.transform._window import WindowOptions

from .._util.marshall import dict_remove_none
from ._transform import Transform, TransformArg


def argmax(
    col1: TransformArg,
    col2: TransformArg,
    distinct: bool | None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Find a value of the first column that maximizes the second column.

    Args:
      col1: Column to yield the value from.
      col2: Column to check for maximum corresponding value of `col1`.
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(argmax=[col1, col2])
    return _to_transform(config, distinct, options)


def argmin(
    col1: TransformArg,
    col2: TransformArg,
    distinct: bool | None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Find a value of the first column that minimizes the second column.

    Args:
      col1: Column to yield the value from.
      col2: Column to check for minimum corresponding value of `col1`.
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(argmin=[col1, col2])
    return _to_transform(config, distinct, options)


def avg(
    col: TransformArg | None = None,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Compute the average (mean) value of the given column.

    col: Column to compute the mean for.
    distinct: Aggregate distinct.
    **options: Window transform options.
    """
    config: dict[str, Any] = dict(avg=col)
    return _to_transform(config, distinct, options)


def count(
    col: TransformArg | None = None,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """A count aggregate transform.

    col: Compute the count of records in an aggregation group. If specified, only non-null expression values are counted. If omitted, all rows within a group are counted.
    distinct: Aggregate distinct.
    **options: Window transform options.
    """
    config: dict[str, Any] = dict(count=col)
    return _to_transform(config, distinct, options)


def _to_transform(
    config: dict[str, Any], distinct: bool | None, options: WindowOptions
) -> Transform:
    config = config | dict_remove_none(dict(distinct=distinct) | options)
    return Transform(config)
