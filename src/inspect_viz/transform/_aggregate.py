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


def first(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Return the first column value found in an aggregation group.

    Args:
      col: Column to get the first value from.
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(first=col)
    return _to_transform(config, distinct, options)


def last(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Return the last column value found in an aggregation group.

    Args:
      col: Column to get the last value from.
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(last=col)
    return _to_transform(config, distinct, options)


def max(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Compute the maximum value of the given column.

    Args:
      col: Column to compute the maximum for.
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(max=col)
    return _to_transform(config, distinct, options)


def min(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Compute the minimum value of the given column.

    Args:
      col: Column to compute the minimum for.
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(min=col)
    return _to_transform(config, distinct, options)


def median(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Compute the median value of the given column.

    Args:
      col: Column to compute the median for.
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(median=col)
    return _to_transform(config, distinct, options)


def mode(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Compute the mode value of the given column.

    Args:
      col: Column to compute the mode for.
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(mode=col)
    return _to_transform(config, distinct, options)


def product(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Compute the product of the given column.

    Args:
      col: Column to compute the product for.
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(product=col)
    return _to_transform(config, distinct, options)


def stddev(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Compute the standard deviation of the given column.

    Args:
      col: Column to compute the standard deviation for.
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(stddev=col)
    return _to_transform(config, distinct, options)


def sum(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Compute the sum of the given column.

    Args:
      col: Column to compute the sum for.
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(sum=col)
    return _to_transform(config, distinct, options)


def variance(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Compute the sample variance of the given column.

    Args:
      col: Column to compute the variance for.
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(variance=col)
    return _to_transform(config, distinct, options)


def stddev_pop(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Compute the population standard deviation of the given column.

    Args:
      col: Column to compute the population standard deviation for.
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(stddevPop=col)
    return _to_transform(config, distinct, options)


def var_pop(
    col: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Compute the population variance of the given column.

    Args:
      col: Column to compute the population variance for.
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(varPop=col)
    return _to_transform(config, distinct, options)


def quantile(
    col: TransformArg,
    threshold: TransformArg,
    distinct: bool | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Compute the quantile value of the given column at the provided probability threshold.

    Args:
      col: Column to compute the quantile for.
      threshold: Probability threshold (e.g., 0.5 for median).
      distinct: Aggregate distinct.
      **options: Window transform options.
    """
    config: dict[str, Any] = dict(quantile=[col, threshold])
    return _to_transform(config, distinct, options)


def _to_transform(
    config: dict[str, Any], distinct: bool | None, options: WindowOptions
) -> Transform:
    config = config | dict_remove_none(dict(distinct=distinct) | options)
    return Transform(config)
