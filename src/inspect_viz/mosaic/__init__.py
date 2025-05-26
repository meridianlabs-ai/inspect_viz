# ruff: noqa: F401 F403 F405

from typing import TypeAlias

from ._generate.schema import *
from ._inputs import *

PlotMark: TypeAlias = (
    Area
    | AreaX
    | AreaY
    | Arrow
    | AxisX
    | AxisY
    | AxisFx
    | AxisFy
    | GridX
    | GridY
    | GridFx
    | GridFy
    | BarX
    | BarY
    | Cell
    | CellX
    | CellY
    | Contour
    | DelaunayLink
    | DelaunayMesh
    | Hull
    | Voronoi
    | VoronoiMesh
    | DenseLine
    | Density
    | DensityX1
    | DensityX2
    | DensityX3
    | DensityX4
    | DensityY1
    | DensityY2
    | DensityY3
    | DensityY4
    | Dot
    | DotX
    | DotY
    | Circle
    | Hexagon
    | ErrorBarX
    | ErrorBarY
    | Frame
    | Geo
    | Graticule
    | Sphere
    | Hexbin
    | Hexgrid
    | Image
    | Line
    | LineX
    | LineY
    | Link
    | Raster
    | Heatmap
    | RasterTile
    | Rect
    | RectX
    | RectY
    | RegressionY
    | RuleX
    | RuleY
    | Text
    | TextX
    | TextY
    | TickX
    | TickY
    | Vector
    | VectorX
    | VectorY
    | Spike
    | WaffleX
    | WaffleY
    | PlotLegend
)

Input: TypeAlias = Menu | Search | Slider | Table | Radio

Component: TypeAlias = (
    HConcat | VConcat | HSpace | VSpace | Input | Plot | PlotMark | Legend
)

ParamLiteral: TypeAlias = None | str | int | float | bool
ParamValue: TypeAlias = ParamLiteral | list[ParamLiteral | ParamRef]

ParamDefinition: TypeAlias = ParamValue | Param | ParamDate | Selection

Params: TypeAlias = dict[str, ParamDefinition]
