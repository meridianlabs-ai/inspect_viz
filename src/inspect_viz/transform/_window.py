from typing import Any, Sequence, TypedDict, Unpack

from .._core.param import Param
from ._transform import Transform


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
