from typing import Literal, Optional, Sequence, TypeAlias, TypedDict

from inspect_viz._core.types import Interval

from ..transform._transform import Transform

ChannelName: TypeAlias = Literal[
    "ariaLabel",
    "fill",
    "fillOpacity",
    "fontSize",
    "fx",
    "fy",
    "geometry",
    "height",
    "href",
    "length",
    "opacity",
    "path",
    "r",
    "rotate",
    "src",
    "stroke",
    "strokeOpacity",
    "strokeWidth",
    "symbol",
    "text",
    "title",
    "weight",
    "width",
    "x",
    "x1",
    "x2",
    "y",
    "y1",
    "y2",
    "z",
]
"""Known channel names."""


ChannelValue: TypeAlias = (
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


class ChannelValueWithScale(TypedDict):
    """Channel with label and scale to override the scale that would normally be associated with the channel."""

    value: ChannelValue
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


ChannelValueSpec: TypeAlias = ChannelValue | ChannelValueWithScale
"""Data channel spec for visualization.

Data channel specs can be either:
  - a field name, to extract the corresponding value from the source data
  - a channel transform  (aggregation or SQL expression)
  - a sequence of values, typically of the same length as the source data
  - a constant number or boolean
  - None to represent no value.
  - a data channel with an associated scale to override the scale that would normally be associated with the channel.
"""


class ChannelValueWithInterval(TypedDict):
    """Channel with associated interval."""

    value: ChannelValue
    interval: Interval


ChannelValueIntervalSpec: TypeAlias = ChannelValueSpec | ChannelValueWithInterval
"""In some contexts, when specifying a mark channel’s value, you can provide a
{value, interval} object to specify an associated interval."""


class ChannelWithOrder(TypedDict, total=False):
    value: ChannelValue
    order: Literal["ascending", "descending"]


SortOrder: TypeAlias = ChannelValue | ChannelWithOrder
"""Sort order for a plot mark's index.

  - a channel value definition for sorting given values (ascending)
  - a {value, order} object for sorting given values
"""
