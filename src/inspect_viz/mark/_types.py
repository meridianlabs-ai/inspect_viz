from typing import Literal, TypeAlias

Symbol: TypeAlias = Literal[
    "asterisk",
    "circle",
    "cross",
    "diamond",
    "diamond2",
    "hexagon",
    "plus",
    "square",
    "square2",
    "star",
    "times",
    "triangle",
    "triangle2",
    "wye",
]

FrameAnchor: TypeAlias = Literal[
    "middle",
    "top-left",
    "top",
    "top-right",
    "right",
    "bottom-right",
    "bottom",
    "bottom-left",
    "left",
]
