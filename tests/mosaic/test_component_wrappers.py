from pathlib import Path
from typing import Type

import pytest
from inspect_viz import Component, Data, Param, Selection
from inspect_viz.input import select, table
from inspect_viz.interactor import (
    Brush,
    highlight,
    interval_x,
    interval_xy,
    interval_y,
    nearest_x,
    nearest_y,
    pan,
    pan_x,
    pan_y,
    pan_zoom,
    pan_zoom_x,
    pan_zoom_y,
    region,
    toggle,
    toggle_color,
    toggle_x,
    toggle_y,
)
from inspect_viz.layout import hconcat, hspace, vconcat, vspace
from inspect_viz.mark import (
    area,
    area_x,
    area_y,
    bar_x,
    bar_y,
    circle,
    dot,
    dot_x,
    dot_y,
    hexagon,
    line,
    line_x,
    line_y,
)
from inspect_viz.plot import legend, plot
from pydantic import BaseModel

from ._schema import (
    Area,
    AreaX,
    AreaY,
    BarX,
    BarY,
    Circle,
    Dot,
    DotX,
    DotY,
    HConcat,
    Hexagon,
    Highlight,
    HSpace,
    IntervalX,
    IntervalXY,
    IntervalY,
    Legend,
    Line,
    LineX,
    LineY,
    Menu,
    NearestX,
    NearestY,
    Pan,
    PanX,
    PanY,
    PanZoom,
    PanZoomX,
    PanZoomY,
    Plot,
    Region,
    Table,
    Toggle,
    ToggleColor,
    ToggleX,
    ToggleY,
    VConcat,
    VSpace,
)


@pytest.fixture
def penguins() -> Data:
    return Data(Path(__file__).parent.parent / "_data" / "penguins.parquet")


@pytest.fixture
def dot_mark(penguins: Data) -> Component:
    return dot(
        penguins,
        x="bill_depth",
        y="flipper_length",
        fill="species",
        symbol="species",
        margin_bottom=0,
        margin_right=0,
    )


def test_vconcat_wrapper(dot_mark: Component) -> None:
    check_component(vconcat(dot_mark), VConcat)


def test_hconcat_wrapper(dot_mark: Component) -> None:
    check_component(hconcat(dot_mark), HConcat)


def test_vspace_wrapper() -> None:
    check_component(vspace(10), VSpace)


def test_hspace_wrapper() -> None:
    check_component(hspace(10), HSpace)


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
            filter_by=Selection("intersect"),
            rotate=45,
            symbol="circle",
            frame_anchor="middle",
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
            filter_by=Selection("intersect"),
            rotate=90,
            symbol="square",
            frame_anchor="top",
        ),
        DotY,
    )


def test_circle_wrapper(penguins: Data) -> None:
    check_component(
        circle(
            penguins,
            x="bill_depth",
            y="flipper_length",
            z="species",
            r=4,
            filter_by=Selection("intersect"),
            rotate=30,
            frame_anchor="bottom",
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
            filter_by=Selection("intersect"),
            rotate=60,
            frame_anchor="left",
        ),
        Hexagon,
    )


def test_line_wrapper(penguins: Data) -> None:
    check_component(
        line(
            penguins,
            x="bill_depth",
            y="flipper_length",
            z="species",
            filter_by=Selection("intersect"),
            marker="circle",
            marker_start="arrow",
            marker_mid="dot",
            marker_end="arrow-reverse",
            curve="linear",
            tension=0.5,
        ),
        Line,
    )


def test_line_x_wrapper(penguins: Data) -> None:
    check_component(
        line_x(
            penguins,
            x="bill_depth",
            y="flipper_length",
            z="species",
            filter_by=Selection("intersect"),
            marker="circle-fill",
            marker_start="tick",
            marker_mid="circle",
            marker_end="tick-x",
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
            filter_by=Selection("intersect"),
            marker="circle-stroke",
            marker_start="dot",
            marker_mid="tick-y",
            marker_end="circle-fill",
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
            interval="minute",
            filter_by=Selection("intersect"),
            offset="center",
            order="appearance",
            z="bill_depth",
            inset=1,
            inset_left=1,
            inset_right=1,
            inset_bottom=1,
            inset_top=1,
            rx=1,
            ry=1,
            reverse=True,
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
            interval="minute",
            filter_by=Selection("intersect"),
            offset="center",
            order="appearance",
            z="bill_depth",
            inset=1,
            inset_left=1,
            inset_right=1,
            inset_bottom=1,
            inset_top=1,
            rx=1,
            ry=1,
            reverse=True,
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
            filter_by=Selection("intersect"),
            offset="center",
            order="appearance",
            curve="basis",
            reverse=True,
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
            filter_by=Selection("intersect"),
            offset="center",
            order="appearance",
            curve="linear",
            reverse=True,
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
            filter_by=Selection("intersect"),
            offset="center",
            order="appearance",
            curve="monotone-y",
            reverse=True,
        ),
        AreaY,
    )


def test_plot_wrapper(dot_mark: Component) -> None:
    check_component(plot(dot_mark, grid=True, x_label="Foo", y_label="Bar"), Plot)


def test_highlight_wrapper() -> None:
    check_component(
        highlight(
            by=Selection("intersect"),
            opacity=0.5,
            fill_opacity=0.5,
            stroke_opacity=0.5,
            fill="red",
            stroke="blue",
        ),
        Highlight,
    )


def test_interval_x_wrapper() -> None:
    check_component(
        interval_x(
            selection=Selection("intersect"),
            field="foo",
            pixel_size=2,
            peers=True,
            brush=Brush(fill="red", fill_opacity=0.6),  # noqa: F821
        ),
        IntervalX,
    )


def test_interval_xy_wrapper() -> None:
    check_component(
        interval_xy(
            selection=Selection("intersect"),
            xfield="foo",
            yfield="bar",
            pixel_size=2,
            peers=True,
            brush=Brush(fill="red", fill_opacity=0.6),
        ),
        IntervalXY,
    )


def test_interval_y_wrapper() -> None:
    check_component(
        interval_y(
            selection=Selection("intersect"),
            field="foo",
            pixel_size=2,
            peers=True,
            brush=Brush(fill="red", fill_opacity=0.6),
        ),
        IntervalY,
    )


def test_toggle_wrapper() -> None:
    check_component(
        toggle(
            selection=Selection("intersect"),
            channels=["x", "y"],
            peers=True,
        ),
        Toggle,
    )


def test_toggle_x_wrapper() -> None:
    check_component(
        toggle_x(
            selection=Selection("intersect"),
            peers=True,
        ),
        ToggleX,
    )


def test_toggle_color_wrapper() -> None:
    check_component(
        toggle_color(
            selection=Selection("intersect"),
            peers=True,
        ),
        ToggleColor,
    )


def test_nearest_x_wrapper() -> None:
    check_component(
        nearest_x(
            selection=Selection("intersect"),
            channels=["x", "color"],
            fields=["field1", "field2"],
            max_radius=50,
        ),
        NearestX,
    )


def test_nearest_y_wrapper() -> None:
    check_component(
        nearest_y(
            selection=Selection("intersect"),
            channels=["y", "color"],
            fields=["field1", "field2"],
            max_radius=50,
        ),
        NearestY,
    )


def test_region_wrapper() -> None:
    check_component(
        region(
            selection=Selection("intersect"),
            channels=["x", "y"],
            peers=True,
            brush=Brush(fill="red", fill_opacity=0.6),
        ),
        Region,
    )


def test_toggle_y_wrapper() -> None:
    check_component(
        toggle_y(
            selection=Selection("intersect"),
            peers=True,
        ),
        ToggleY,
    )


def test_select_wrapper(penguins: Data) -> None:
    check_component(select("Species", penguins, column="species"), Menu)
    check_component(
        select(
            "X",
            options=["body_mass", "flipper_length", "bill_depth", "bill_length"],
            param=Param("body_mass"),
        ),
        Menu,
    )


def test_table_wrapper(penguins: Data) -> None:
    check_component(table(penguins), Table)  # noqa: F821


def test_legend_wrapper(penguins: Data) -> None:
    check_component(
        legend(
            "color",
            label="foo",
            columns=1,
            selection=penguins.selection,
            field="species",
            width=100,
            height=100,
            tick_size=5,
            margin_bottom=5,
            margin_left=5,
            margin_right=5,
            margin_top=5,
            for_plot="foo",
        ),
        Legend,
    )


def test_pan_wrapper() -> None:
    check_component(
        pan(
            x=Selection("intersect"),
            y=Selection("intersect"),
            xfield="x_field",
            yfield="y_field",
        ),
        Pan,
    )


def test_pan_x_wrapper() -> None:
    check_component(
        pan_x(
            x=Selection("intersect"),
            y=Selection("intersect"),
            xfield="x_field",
            yfield="y_field",
        ),
        PanX,
    )


def test_pan_y_wrapper() -> None:
    check_component(
        pan_y(
            x=Selection("intersect"),
            y=Selection("intersect"),
            xfield="x_field",
            yfield="y_field",
        ),
        PanY,
    )


def test_pan_zoom_wrapper() -> None:
    check_component(
        pan_zoom(
            x=Selection("intersect"),
            y=Selection("intersect"),
            xfield="x_field",
            yfield="y_field",
        ),
        PanZoom,
    )


def test_pan_zoom_x_wrapper() -> None:
    check_component(
        pan_zoom_x(
            x=Selection("intersect"),
            y=Selection("intersect"),
            xfield="x_field",
            yfield="y_field",
        ),
        PanZoomX,
    )


def test_pan_zoom_y_wrapper() -> None:
    check_component(
        pan_zoom_y(
            x=Selection("intersect"),
            y=Selection("intersect"),
            xfield="x_field",
            yfield="y_field",
        ),
        PanZoomY,
    )


def check_component(component: Component, type: Type[BaseModel]) -> None:
    model = type.model_validate(component.config)
    assert model.model_dump(exclude_none=True, by_alias=True) == component.config
