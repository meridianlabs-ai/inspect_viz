from inspect_viz import Component, Data
from inspect_viz.mark import (
    area,
    area_x,
    area_y,
    arrow,
    axis_fx,
    axis_fy,
    axis_x,
    axis_y,
    bar_x,
    bar_y,
    cell,
    cell_x,
    cell_y,
    circle,
    contour,
    delaunay_link,
    delaunay_mesh,
    dense_line,
    density,
    density_x,
    density_y,
    dot_x,
    dot_y,
    error_bar_x,
    error_bar_y,
    frame,
    geo,
    graticule,
    grid_fx,
    grid_fy,
    grid_x,
    grid_y,
    heatmap,
    hexagon,
    hexbin,
    hexgrid,
    hull,
    image,
    line,
    line_x,
    line_y,
    link,
    raster,
    raster_tile,
    rect,
    rect_x,
    rect_y,
    regression_y,
    rule_x,
    rule_y,
    sphere,
    spike,
    text,
    text_x,
    text_y,
    tick_x,
    tick_y,
    vector,
    vector_x,
    vector_y,
    voronoi,
    voronoi_mesh,
    waffle_x,
    waffle_y,
)

from ._schema import (
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
    DensityY1,
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
    Heatmap,
    Hexagon,
    Hexbin,
    Hexgrid,
    Hull,
    Image,
    Line,
    LineX,
    LineY,
    Link,
    Raster,
    RasterTile,
    Rect,
    RectX,
    RectY,
    RegressionY,
    RuleX,
    RuleY,
    Sphere,
    Spike,
    Text,
    TextX,
    TextY,
    TickX,
    TickY,
    Vector,
    VectorX,
    VectorY,
    Voronoi,
    VoronoiMesh,
    WaffleX,
    WaffleY,
)
from .utils import (
    area_args,
    arrow_args,
    bar_styling_args,
    basic_selection_args,
    check_component,
    contour_args,
    dense_line_args,
    density_args,
    error_bar_args,
    frame_args,
    full_inset_args,
    geo_args,
    heatmap_args,
    hexbin_args,
    image_args,
    line_marker_args,
    mark_position_args,
    marker_args,
    raster_args,
    raster_tile_args,
    regression_args,
    rotate_and_frame_args,
    stacking_args,
    standard_marker_args,
    text_positioning_args,
    text_styles_dict,
    tick_styling_args,
)


def test_dot_wrapper(dot_mark: Component) -> None:
    check_component(dot_mark, Dot)


def test_dot_x_wrapper(penguins: Data) -> None:
    check_component(
        dot_x(
            penguins,
            x="bill_depth",
            z="species",
            r=5,
            interval="day",
            symbol="circle",
            **basic_selection_args(),
            **rotate_and_frame_args(),
        ),
        DotX,
    )


def test_dot_y_wrapper(penguins: Data) -> None:
    check_component(
        dot_y(
            penguins,
            y="flipper_length",
            z="species",
            r=3,
            interval="month",
            symbol="square",
            **basic_selection_args(),
            **rotate_and_frame_args(),
        ),
        DotY,
    )


def test_circle_wrapper(penguins: Data) -> None:
    check_component(
        circle(
            penguins,
            r=4,
            **mark_position_args(),
            **basic_selection_args(),
            **rotate_and_frame_args(),
        ),
        Circle,
    )


def test_hexagon_wrapper(penguins: Data) -> None:
    check_component(
        hexagon(
            penguins,
            x="bill_length",
            y="body_mass",
            z="species",
            r=6,
            **basic_selection_args(),
            **rotate_and_frame_args(),
        ),
        Hexagon,
    )


def test_line_wrapper(penguins: Data) -> None:
    check_component(
        line(
            penguins,
            **mark_position_args(),
            **basic_selection_args(),
            **line_marker_args(),
        ),
        Line,
    )


def test_line_x_wrapper(penguins: Data) -> None:
    check_component(
        line_x(
            penguins,
            **mark_position_args(),
            **basic_selection_args(),
            **standard_marker_args(),
            curve="basis",
            tension=0.8,
        ),
        LineX,
    )


def test_line_y_wrapper(penguins: Data) -> None:
    check_component(
        line_y(
            penguins,
            y="body_mass",
            x="bill_length",
            z="species",
            **basic_selection_args(),
            **standard_marker_args(),
            curve="cardinal",
            tension=0.3,
        ),
        LineY,
    )


def test_bar_x_wrapper(penguins: Data) -> None:
    check_component(
        bar_x(
            penguins,
            x="bill_depth",
            x1="bill_depth",
            x2="bill_depth",
            y="bill_depth",
            z="bill_depth",
            **basic_selection_args(),
            **bar_styling_args(),
        ),
        BarX,
    )


def test_bar_y_wrapper(penguins: Data) -> None:
    check_component(
        bar_y(
            penguins,
            y="bill_depth",
            y1="bill_depth",
            y2="bill_depth",
            x="bill_depth",
            z="bill_depth",
            **basic_selection_args(),
            **bar_styling_args(),
        ),
        BarY,
    )


def test_area_wrapper(penguins: Data) -> None:
    check_component(
        area(
            penguins,
            x1="bill_depth",
            y1="flipper_length",
            x2="bill_length",
            y2="body_mass",
            z="species",
            **basic_selection_args(),
            **area_args(),
        ),
        Area,
    )


def test_area_x_wrapper(penguins: Data) -> None:
    check_component(
        area_x(
            penguins,
            x="bill_depth",
            x1="bill_depth",
            x2="bill_length",
            y="flipper_length",
            z="species",
            **basic_selection_args(),
            **stacking_args(),
            curve="linear",
        ),
        AreaX,
    )


def test_area_y_wrapper(penguins: Data) -> None:
    check_component(
        area_y(
            penguins,
            y="bill_depth",
            y1="bill_depth",
            y2="bill_length",
            x="flipper_length",
            z="species",
            **basic_selection_args(),
            offset="center",
            order="appearance",
            curve="monotone-y",
            reverse=True,
        ),
        AreaY,
    )


def test_text_wrapper(penguins: Data) -> None:
    check_component(
        text(
            penguins,
            text="species",
            **mark_position_args(),
            **basic_selection_args(),
            **text_positioning_args(),
            **dict(text_styles_dict()),
        ),
        Text,
    )


def test_text_x_wrapper(penguins: Data) -> None:
    check_component(
        text_x(
            penguins,
            text="species",
            interval="day",
            **mark_position_args(),
            **basic_selection_args(),
            frame_anchor="top",
            line_anchor="top",
            rotate=90,
            **dict(text_styles_dict()),
        ),
        TextX,
    )


def test_text_y_wrapper(penguins: Data) -> None:
    check_component(
        text_y(
            penguins,
            y="body_mass",
            x="bill_length",
            z="species",
            text="island",
            interval="month",
            **basic_selection_args(),
            frame_anchor="left",
            line_anchor="bottom",
            rotate=180,
            **dict(text_styles_dict()),
        ),
        TextY,
    )


def test_density_wrapper(penguins: Data) -> None:
    check_component(
        density(
            penguins,
            x="bill_length",
            y="body_mass",
            z="species",
            **basic_selection_args(),
            **density_args(),
        ),
        Density,
    )


def test_density_x_wrapper(penguins: Data) -> None:
    check_component(
        density_x(
            penguins,
            y="bill_length",
            z="species",
            **basic_selection_args(),
            type="areaX",
            bandwidth=15,
        ),
        DensityX1,
    )


def test_density_y_wrapper(penguins: Data) -> None:
    check_component(
        density_y(
            penguins,
            x="bill_length",
            z="species",
            **basic_selection_args(),
            type="areaY",
            bandwidth=15,
        ),
        DensityY1,
    )


def test_rect_wrapper(penguins: Data) -> None:
    check_component(
        rect(
            penguins,
            x="bill_length",
            x1="bill_depth",
            x2="flipper_length",
            y="body_mass",
            y1="bill_length",
            y2="flipper_length",
            **basic_selection_args(),
            interval="day",
            inset=2,
            inset_top=1,
            inset_right=1,
            inset_bottom=1,
            inset_left=1,
            rx=5,
            ry=3,
            offset="center",
            order="sum",
            reverse=True,
            z="species",
        ),
        Rect,
    )


def test_rect_x_wrapper(penguins: Data) -> None:
    check_component(
        rect_x(
            penguins,
            x="bill_length",
            x1="bill_depth",
            x2="flipper_length",
            y="island",
            **basic_selection_args(),
            interval="month",
            inset=1,
            rx=2,
            ry=2,
            offset="normalize",
            order="appearance",
            z="species",
        ),
        RectX,
    )


def test_rect_y_wrapper(penguins: Data) -> None:
    check_component(
        rect_y(
            penguins,
            x="species",
            y="body_mass",
            y1="bill_length",
            y2="flipper_length",
            **basic_selection_args(),
            interval="week",
            inset=0.5,
            rx=1,
            ry=1,
            offset="wiggle",
            order="inside-out",
            reverse=False,
            z="island",
        ),
        RectY,
    )


def test_cell_wrapper(penguins: Data) -> None:
    check_component(
        cell(
            penguins,
            x="species",
            y="island",
            **basic_selection_args(),
            inset=1,
            inset_top=0.5,
            inset_right=0.5,
            inset_bottom=0.5,
            inset_left=0.5,
            rx=2,
            ry=2,
            reverse=True,
        ),
        Cell,
    )


def test_cell_x_wrapper(penguins: Data) -> None:
    check_component(
        cell_x(
            penguins,
            x="species",
            y="island",
            **basic_selection_args(),
            inset=2,
            rx=3,
            ry=1,
            reverse=False,
        ),
        CellX,
    )


def test_cell_y_wrapper(penguins: Data) -> None:
    check_component(
        cell_y(
            penguins,
            x="island",
            y="species",
            **basic_selection_args(),
            inset=1.5,
            inset_top=1,
            inset_bottom=1,
            rx=1,
            ry=1,
        ),
        CellY,
    )


def test_vector_wrapper(penguins: Data) -> None:
    check_component(
        vector(
            penguins,
            x="bill_length",
            y="body_mass",
            r=5,
            length="flipper_length",
            rotate=45,
            shape="arrow",
            anchor="middle",
            frame_anchor="middle",
            **basic_selection_args(),
        ),
        Vector,
    )


def test_vector_x_wrapper(penguins: Data) -> None:
    check_component(
        vector_x(
            penguins,
            x="bill_length",
            y="species",
            r="bill_depth",
            length=10,
            rotate=90,
            shape="spike",
            anchor="start",
            frame_anchor="left",
            **basic_selection_args(),
        ),
        VectorX,
    )


def test_vector_y_wrapper(penguins: Data) -> None:
    check_component(
        vector_y(
            penguins,
            x="island",
            y="body_mass",
            r=3,
            length="bill_depth",
            rotate=180,
            shape="arrow",
            anchor="end",
            frame_anchor="top",
            **basic_selection_args(),
        ),
        VectorY,
    )


def test_spike_wrapper(penguins: Data) -> None:
    check_component(
        spike(
            penguins,
            x="flipper_length",
            y="bill_length",
            r="body_mass",
            length=8,
            rotate=270,
            shape="spike",
            anchor="middle",
            frame_anchor="bottom",
            **basic_selection_args(),
        ),
        Spike,
    )


def test_tick_x_wrapper(penguins: Data) -> None:
    check_component(
        tick_x(
            penguins,
            x="bill_length",
            y="species",
            **basic_selection_args(),
            **tick_styling_args(),
        ),
        TickX,
    )


def test_tick_y_wrapper(penguins: Data) -> None:
    check_component(
        tick_y(
            penguins,
            y="body_mass",
            x="island",
            **basic_selection_args(),
            **standard_marker_args(),
            inset=1.5,
            inset_left=0.5,
            inset_right=0.5,
        ),
        TickY,
    )


def test_waffle_x_wrapper(penguins: Data) -> None:
    check_component(
        waffle_x(
            penguins,
            x="bill_length",
            x1="bill_depth",
            x2="flipper_length",
            y="species",
            z="island",
            **basic_selection_args(),
            multiple=10,
            unit=5,
            gap=2,
            round=True,
            interval="day",
            offset="center",
            order="sum",
            **full_inset_args(),
        ),
        WaffleX,
    )


def test_waffle_y_wrapper(penguins: Data) -> None:
    check_component(
        waffle_y(
            penguins,
            y="body_mass",
            y1="bill_length",
            y2="flipper_length",
            x="island",
            z="species",
            **basic_selection_args(),
            multiple=5,
            unit=2,
            gap=1,
            round=False,
            interval="month",
            offset="normalize",
            order="appearance",
            inset=2,
            rx=1,
            ry=2,
        ),
        WaffleY,
    )


def test_rule_x_wrapper(penguins: Data) -> None:
    check_component(
        rule_x(
            penguins,
            x="bill_length",
            y="species",
            **basic_selection_args(),
            interval="day",
            marker="tick",
            marker_start="arrow",
            marker_mid="dot",
            marker_end="arrow-reverse",
            inset=1,
        ),
        RuleX,
    )


def test_rule_y_wrapper(penguins: Data) -> None:
    check_component(
        rule_y(
            penguins,
            y="body_mass",
            x="island",
            **basic_selection_args(),
            interval="month",
            marker="circle",
            marker_start="tick-x",
            marker_mid="circle-fill",
            marker_end="tick-y",
            inset=2,
        ),
        RuleY,
    )


def test_axis_x_wrapper(penguins: Data) -> None:
    check_component(
        axis_x(
            x="bill_length",
            interval="day",
            text="species",
            frame_anchor="bottom",
            line_anchor="top",
            rotate=45,
            text_stroke="black",
            text_stroke_opacity=0.8,
            text_stroke_width=2,
            styles=text_styles_dict(),
            anchor="bottom",
            color="blue",
            ticks=10,
            tick_spacing=50,
            tick_size=6,
            tick_padding=3,
            tick_format=".2f",
            tick_rotate=30,
            label="Bill Length (mm)",
            label_offset=20,
            label_anchor="center",
            label_arrow=True,
        ),
        AxisX,
    )


def test_axis_y_wrapper(penguins: Data) -> None:
    check_component(
        axis_y(
            y="body_mass",
            interval="week",
            text="island",
            frame_anchor="left",
            line_anchor="middle",
            rotate=90,
            text_stroke="red",
            text_stroke_opacity=0.9,
            text_stroke_width=1,
            styles=text_styles_dict(),
            anchor="left",
            color="green",
            ticks=[1000, 2000, 3000, 4000, 5000],
            tick_spacing=40,
            tick_size=8,
            tick_padding=5,
            tick_format=".0f",
            tick_rotate=0,
            label="Body Mass (g)",
            label_offset=30,
            label_anchor="middle",
            label_arrow="auto",
        ),
        AxisY,
    )


def test_axis_fx_wrapper(penguins: Data) -> None:
    check_component(
        axis_fx(
            x="bill_depth",
            interval="month",
            text="species",
            frame_anchor="top",
            line_anchor="bottom",
            rotate=60,
            text_stroke="purple",
            text_stroke_opacity=0.7,
            text_stroke_width=1.5,
            styles=text_styles_dict(),
            anchor="top",
            color="orange",
            ticks=8,
            tick_spacing=60,
            tick_size=4,
            tick_padding=2,
            tick_format=".1f",
            tick_rotate=45,
            label="Bill Depth (mm)",
            label_offset=25,
            label_anchor="start",
            label_arrow=False,
        ),
        AxisFx,
    )


def test_axis_fy_wrapper(penguins: Data) -> None:
    check_component(
        axis_fy(
            y="flipper_length",
            interval="year",
            text="species",
            frame_anchor="right",
            line_anchor="left",
            rotate=270,
            text_stroke="teal",
            text_stroke_opacity=0.6,
            text_stroke_width=0.8,
            styles=text_styles_dict(),
            anchor="right",
            color="navy",
            ticks=[180, 200, 220, 240],
            tick_spacing=35,
            tick_size=10,
            tick_padding=4,
            tick_format=".0f",
            tick_rotate=15,
            label="Flipper Length (mm)",
            label_offset=40,
            label_anchor="end",
            label_arrow="yes",
        ),
        AxisFy,
    )


def test_grid_x_wrapper(penguins: Data) -> None:
    check_component(
        grid_x(
            x="bill_length",
            y1="island",
            y2="species",
            interval="day",
            anchor="bottom",
            color="lightgray",
            ticks=5,
            tick_spacing=30,
            stroke="gray",
            stroke_width=1,
            stroke_opacity=0.5,
            stroke_dasharray="2,2",
        ),
        GridX,
    )


def test_grid_y_wrapper(penguins: Data) -> None:
    check_component(
        grid_y(
            y="body_mass",
            x1="bill_depth",
            x2="flipper_length",
            interval="week",
            anchor="left",
            color="lightblue",
            ticks=[2000, 3000, 4000, 5000],
            tick_spacing=40,
            inset_left=5,
            inset_right=10,
            stroke="blue",
            stroke_width=0.8,
            stroke_opacity=0.7,
            stroke_dasharray="3,1",
        ),
        GridY,
    )


def test_grid_fx_wrapper(penguins: Data) -> None:
    check_component(
        grid_fx(
            x="bill_depth",
            y1="body_mass",
            y2="flipper_length",
            interval="month",
            anchor="top",
            color="lightgreen",
            ticks=8,
            tick_spacing=25,
            stroke="green",
            stroke_width=1.2,
            stroke_opacity=0.6,
            stroke_dasharray="4,2",
        ),
        GridFx,
    )


def test_grid_fy_wrapper(penguins: Data) -> None:
    check_component(
        grid_fy(
            y="flipper_length",
            x1="bill_length",
            x2="body_mass",
            interval="year",
            anchor="right",
            color="lightyellow",
            ticks=[190, 210, 230],
            tick_spacing=50,
            inset_left=2,
            inset_right=8,
            stroke="orange",
            stroke_width=1.5,
            stroke_opacity=0.8,
            stroke_dasharray="5,3",
        ),
        GridFy,
    )


def test_arrow_wrapper(penguins: Data) -> None:
    check_component(
        arrow(
            penguins,
            x="bill_length",
            y="body_mass",
            x1="bill_depth",
            y1="flipper_length",
            x2="bill_length",
            y2="body_mass",
            **arrow_args(),
            **basic_selection_args(),
        ),
        Arrow,
    )


def test_error_bar_x_wrapper(penguins: Data) -> None:
    check_component(
        error_bar_x(
            penguins,
            x="bill_length",
            y="species",
            z="island",
            **basic_selection_args(),
            **error_bar_args(),
        ),
        ErrorBarX,
    )


def test_error_bar_y_wrapper(penguins: Data) -> None:
    check_component(
        error_bar_y(
            penguins,
            y="body_mass",
            x="island",
            ci=0.90,
            z="species",
            **basic_selection_args(),
            marker="circle",
            marker_start="tick",
            marker_mid="circle-fill",
            marker_end="tick-x",
        ),
        ErrorBarY,
    )


def test_regression_y_wrapper(penguins: Data) -> None:
    check_component(
        regression_y(
            penguins,
            x="bill_length",
            y="body_mass",
            z="species",
            **basic_selection_args(),
            **regression_args(),
        ),
        RegressionY,
    )


def test_contour_wrapper(penguins: Data) -> None:
    check_component(
        contour(
            penguins,
            x="bill_length",
            y="body_mass",
            **basic_selection_args(),
            **contour_args(),
        ),
        Contour,
    )


def test_delaunay_link_wrapper(penguins: Data) -> None:
    check_component(
        delaunay_link(
            penguins,
            x="bill_length",
            y="body_mass",
            z="species",
            **basic_selection_args(),
            **marker_args(),
        ),
        DelaunayLink,
    )


def test_delaunay_mesh_wrapper(penguins: Data) -> None:
    check_component(
        delaunay_mesh(
            penguins,
            x="bill_length",
            y="body_mass",
            z="species",
            **basic_selection_args(),
            **standard_marker_args(),
            curve="basis",
            tension=0.8,
        ),
        DelaunayMesh,
    )


def test_hull_wrapper(penguins: Data) -> None:
    check_component(
        hull(
            penguins,
            x="bill_length",
            y="body_mass",
            z="species",
            **basic_selection_args(),
            **standard_marker_args(),
            curve="cardinal",
            tension=0.3,
        ),
        Hull,
    )


def test_voronoi_wrapper(penguins: Data) -> None:
    check_component(
        voronoi(
            penguins,
            x="bill_length",
            y="body_mass",
            z="species",
            **basic_selection_args(),
            marker="circle-stroke",
            marker_start="arrow-reverse",
            marker_mid="tick-x",
            marker_end="circle-fill",
            curve="monotone-x",
            tension=0.7,
        ),
        Voronoi,
    )


def test_voronoi_mesh_wrapper(penguins: Data) -> None:
    check_component(
        voronoi_mesh(
            penguins,
            x="bill_length",
            y="body_mass",
            z="species",
            **basic_selection_args(),
            marker="tick-y",
            marker_start="dot",
            marker_mid="arrow",
            marker_end="circle",
            curve="catmull-rom",
            tension=0.4,
        ),
        VoronoiMesh,
    )


def test_raster_wrapper(penguins: Data) -> None:
    check_component(
        raster(
            penguins,
            x="bill_length",
            y="body_mass",
            **basic_selection_args(),
            **raster_args(),
            image_rendering="pixelated",
        ),
        Raster,
    )


def test_heatmap_wrapper(penguins: Data) -> None:
    check_component(
        heatmap(
            penguins,
            x="bill_length",
            y="body_mass",
            **basic_selection_args(),
            **heatmap_args(),
        ),
        Heatmap,
    )


def test_raster_tile_wrapper(penguins: Data) -> None:
    check_component(
        raster_tile(
            penguins,
            x="bill_length",
            y="body_mass",
            **basic_selection_args(),
            **raster_tile_args(),
        ),
        RasterTile,
    )


def test_link_wrapper(penguins: Data) -> None:
    check_component(
        link(
            penguins,
            x="bill_length",
            y="body_mass",
            x1="bill_depth",
            y1="flipper_length",
            x2="bill_length",
            y2="body_mass",
            **basic_selection_args(),
            marker="circle",
            marker_start="arrow",
            marker_mid="dot",
            marker_end="arrow-reverse",
            curve="linear",
            tension=0.5,
        ),
        Link,
    )


def test_dense_line_wrapper(penguins: Data) -> None:
    check_component(
        dense_line(
            penguins,
            x="bill_length",
            y="body_mass",
            z="species",
            **basic_selection_args(),
            **dense_line_args(),
        ),
        DenseLine,
    )


def test_frame_wrapper() -> None:
    check_component(
        frame(
            **frame_args(),
        ),
        Frame,
    )


def test_geo_wrapper(penguins: Data) -> None:
    check_component(
        geo(
            penguins,
            **geo_args(),
            **basic_selection_args(),
        ),
        Geo,
    )


def test_sphere_wrapper() -> None:
    check_component(
        sphere(),
        Sphere,
    )


def test_graticule_wrapper() -> None:
    check_component(
        graticule(),
        Graticule,
    )


def test_hexbin_wrapper(penguins: Data) -> None:
    check_component(
        hexbin(
            penguins,
            x="bill_length",
            y="body_mass",
            z="species",
            **basic_selection_args(),
            **hexbin_args(),
        ),
        Hexbin,
    )


def test_hexgrid_wrapper() -> None:
    check_component(
        hexgrid(
            bin_width=25.0,
            stroke="lightgray",
            stroke_width=1,
            stroke_opacity=0.5,
        ),
        Hexgrid,
    )


def test_image_wrapper(penguins: Data) -> None:
    check_component(
        image(
            penguins,
            x="bill_length",
            y="body_mass",
            **image_args(),
            **basic_selection_args(),
        ),
        Image,
    )
