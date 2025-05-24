from typing import TypeAlias

from ._schema.schema import (
    Area,
    AreaX,
    AreaY,
    Arrow,
    AxisFx,
    AxisFy,
    AxisX,
    AxisY,
    BarX,
    BarY,
    Cell,
    CellX,
    CellY,
    Circle,
    Contour,
    DelaunayLink,
    DelaunayMesh,
    DenseLine,
    Density,
    DensityX1,
    DensityX2,
    DensityX3,
    DensityX4,
    DensityY1,
    DensityY2,
    DensityY3,
    DensityY4,
    Dot,
    DotX,
    DotY,
    ErrorBarX,
    ErrorBarY,
    Frame,
    Geo,
    Graticule,
    GridFx,
    GridFy,
    GridX,
    GridY,
    HConcat,
    Heatmap,
    Hexagon,
    Hexbin,
    Hexgrid,
    HSpace,
    Hull,
    Image,
    Legend,
    Line,
    LineX,
    LineY,
    Link,
    Menu,
    Param,
    ParamDate,
    ParamRef,
    Plot,
    Raster,
    RasterTile,
    Rect,
    RectX,
    RectY,
    RegressionY,
    RuleX,
    RuleY,
    Search,
    Selection,
    Slider,
    Sphere,
    Spike,
    Table,
    Text,
    TextX,
    TextY,
    TickX,
    TickY,
    VConcat,
    Vector,
    VectorX,
    VectorY,
    Voronoi,
    VoronoiMesh,
    VSpace,
    WaffleX,
    WaffleY,
)

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
)


Component: TypeAlias = (
    HConcat
    | VConcat
    | HSpace
    | VSpace
    | Menu
    | Search
    | Slider
    | Table
    | Plot
    | PlotMark
    | Legend
)

ParamLiteral: TypeAlias = None | str | int | float | bool
ParamValue: TypeAlias = ParamLiteral | list[ParamLiteral | ParamRef]

ParamDefinition: TypeAlias = ParamValue | Param | ParamDate | Selection

Params: TypeAlias = dict[str, ParamDefinition]
