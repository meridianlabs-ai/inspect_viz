from typing import Literal, TypeAlias

Curve: TypeAlias = Literal[
    "basis",
    "basis-closed",
    "basis-open",
    "bundle",
    "bump-x",
    "bump-y",
    "cardinal",
    "cardinal-closed",
    "cardinal-open",
    "catmull-rom",
    "catmull-rom-closed",
    "catmull-rom-open",
    "linear",
    "linear-closed",
    "monotone-x",
    "monotone-y",
    "natural",
    "step",
    "step-after",
    "step-before",
]
"""The curve (interpolation) method for connecting adjacent points."""


Interpolate: TypeAlias = Literal[
    "none", "linear", "nearest", "barycentric", "random-walk"
]
"""The spatial interpolation method.

- *none* - do not perform interpolation (the default)
- *linear* - apply proportional linear interpolation across adjacent bins
- *nearest* - assign each pixel to the closest sample's value (Voronoi diagram)
- *barycentric* - apply barycentric interpolation over the Delaunay triangulation
- *random-walk* - apply a random walk from each pixel
"""


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
"""Symbol type for dot or density plot."""

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
"""Defaults for **x** and **y** based on the plot's frame."""

Marker: TypeAlias = Literal[
    "arrow",
    "arrow-reverse",
    "dot",
    "circle",
    "circle-fill",
    "circle-stroke",
    "tick",
    "tick-x",
    "tick-y",
]
"""Symbols used as plot markers."""
