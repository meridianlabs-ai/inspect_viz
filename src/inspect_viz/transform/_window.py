from typing import Any, Sequence, TypedDict, Unpack

from .._core.param import Param
from ._transform import Transform, TransformArg


class WindowOptions(TypedDict, total=False):
    """Window transform options."""

    orderby: str | Param | Sequence[str | Param]
    """One or more expressions by which to sort a windowed version of this aggregate function."""

    partitionby: str | Param | Sequence[str | Param]
    """One or more expressions by which to partition a windowed version of this aggregate function."""

    rows: Sequence[float | None] | Param
    """window rows frame specification as an array or array-valued expression."""

    range: Sequence[float | None] | Param
    """Window range frame specification as an array or array-valued expression."""


def row_number(**options: Unpack[WindowOptions]) -> Transform:
    """Compute the 1-based row number over an ordered window partition.

    Args:
        **options: Window transform options.
    """
    config: dict[str, Any] = dict(row_number=None) | options
    return Transform(config)


def rank(**options: Unpack[WindowOptions]) -> Transform:
    """Compute the row rank over an ordered window partition.

    Sorting ties result in gaps in the rank numbers ([1, 1, 3, ...]).

    Args:
        **options: Window transform options.
    """
    config: dict[str, Any] = dict(rank=None) | options
    return Transform(config)


def dense_rank(**options: Unpack[WindowOptions]) -> Transform:
    """Compute the dense row rank (no gaps) over an ordered window partition.

    Sorting ties do not result in gaps in the rank numbers ( [1, 1, 2, ...]).

    Args:
        **options: Window transform options.
    """
    config: dict[str, Any] = dict(dense_rank=None) | options
    return Transform(config)


def percent_rank(**options: Unpack[WindowOptions]) -> Transform:
    """Compute the percetange rank over an ordered window partition.

    Args:
        **options: Window transform options.
    """
    config: dict[str, Any] = dict(percent_rank=None) | options
    return Transform(config)


def cume_dist(**options: Unpack[WindowOptions]) -> Transform:
    """Compute the cumulative distribution value over an ordered window partition.

    Equals the number of partition rows preceding or peer with the current row, divided by the total number of partition rows.

    Args:
        **options: Window transform options.
    """
    config: dict[str, Any] = dict(cume_dist=None) | options
    return Transform(config)


def n_tile(num_buckets: int, **options: Unpack[WindowOptions]) -> Transform:
    """Compute an n-tile integer ranging from 1 to `num_buckets` dividing the partition as equally as possible.

    Args:
        num_buckets: Number of buckets.
        **options: Window transform options.
    """
    config: dict[str, Any] = dict(ntile=num_buckets) | options
    return Transform(config)


def lag(
    col: TransformArg,
    offset: int = 1,
    default: TransformArg | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Compute lagging values in a column.

    Returns the value at the row that is at `offset` rows (default `1`) before the current row within the window frame.

    Args:
        col: Column to take value from.
        offset: Rows to offset.
        default: Default value if thre is no such row.
        **options: Window transform options.
    """
    config: dict[str, Any] = dict(lag=[col, offset, default]) | options
    return Transform(config)


def lead(
    col: TransformArg,
    offset: int = 1,
    default: TransformArg | None = None,
    **options: Unpack[WindowOptions],
) -> Transform:
    """Compute leading values in a column.

    Returns the value at the row that is at `offset` rows (default `1`) after the current row within the window frame.

    Args:
        col: Column to take value from.
        offset: Rows to offset.
        default: Default value if thre is no such row.
        **options: Window transform options.
    """
    config: dict[str, Any] = dict(lag=[col, offset, default]) | options
    return Transform(config)


def first_value(col: TransformArg, **options: Unpack[WindowOptions]) -> Transform:
    """Get the first value of the given column in the current window frame.

    Args:
       col: Aggregate column to take first value from.
       **options: Window transform options.
    """
    config: dict[str, Any] = dict(first_value=col) | options
    return Transform(config)


def last_value(col: TransformArg, **options: Unpack[WindowOptions]) -> Transform:
    """Get the last value of the given column in the current window frame.

    Args:
       col: Aggregate column to take last value from.
       **options: Window transform options.
    """
    config: dict[str, Any] = dict(last_value=col) | options
    return Transform(config)


def nth_value(
    col: TransformArg, offset: int, **options: Unpack[WindowOptions]
) -> Transform:
    """Get the nth value of the given column in the current window frame, counting from one.

    Args:
       col: Aggregate column to take nth value from.
       offset: Offset for the nth row.
       **options: Window transform options.
    """
    config: dict[str, Any] = dict(nth_value=[col, offset]) | options
    return Transform(config)
