from typing import Literal, Optional, Sequence, TypeAlias, TypedDict

from inspect_viz._core.types import Interval

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


class ChannelWithScale(TypedDict):
    """Channel with label and scale to override the scale that would normally be associated with the channel."""

    value: Channel
    label: Optional[str]
    scale: Optional[
        (
            Literal[
                "x",
                "y",
                "fx",
                "fy",
                "r",
                "color",
                "opacity",
                "symbol",
                "length",
                "auto",
            ]
            | bool
        )
    ]


ChannelSpec: TypeAlias = Channel | ChannelWithScale
"""Data channel spec for visualization.

Data channel specs can be either:
  - a field name, to extract the corresponding value from the source data
  - a channel transform  (aggregation or SQL expression)
  - a sequence of values, typically of the same length as the source data
  - a constant number or boolean
  - None to represent no value.
  - a data channel with an associated scale to override the scale that would normally be associated with the channel.
"""


class ChannelWithInterval(TypedDict):
    """Channel with associated interval."""

    value: Channel
    interval: Interval


ChannelIntervalSpec: TypeAlias = ChannelSpec | ChannelWithInterval
"""In some contexts, when specifying a mark channel’s value, you can provide a
{value, interval} object to specify an associated interval."""


class ChannelWithOrder(TypedDict, total=False):
    value: Channel
    order: Literal["ascending", "descending"]


SortOrder: TypeAlias = Channel | ChannelWithOrder
"""Sort order for a plot mark's index.

  - a channel value definition for sorting given values (ascending)
  - a {value, order} object for sorting given values
"""
