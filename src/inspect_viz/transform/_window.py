from typing import Sequence, TypedDict

from .._core.param import Param


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
