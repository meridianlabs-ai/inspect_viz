from typing import Literal, Sequence, TypeAlias, TypedDict

from ..transform._transform import Transform

Channel: TypeAlias = (
    str | Transform | Sequence[int | float | bool] | int | float | bool | None
)
"""Data channel for visualization.

Data channels can be either:
  - a field name, to extract the corresponding value from the source data
  - a channel transform  (aggregation or SQL expression)
  - a sequence of values, typically of the same length as the source data
  - a constant number or boolean
  - None to represent no value.
"""


class SortedChannel(TypedDict, total=False):
    value: Channel
    order: Literal["ascending", "descending"]


SortOrder: TypeAlias = Channel | SortedChannel
"""Sort order for a plot mark's index.

  - a channel value definition for sorting given values (ascending)
  - a {value, order} object for sorting given values
"""
