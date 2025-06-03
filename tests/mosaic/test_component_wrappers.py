from pathlib import Path
from typing import Any, Type

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
    text,
    text_x,
    text_y,
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
    Text,
    TextX,
    TextY,
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
            symbol="circle",
            **basic_selection_args(),
            **{"rotate": 45, "frame_anchor": "middle"},
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
            **{"rotate": 90, "frame_anchor": "top"},
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
            **{"rotate": 30, "frame_anchor": "bottom"},
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
            **{"rotate": 60, "frame_anchor": "left"},
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
            **basic_selection_args(),
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
            **basic_selection_args(),
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
            **basic_selection_args(),
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
            field="foo",
            **interval_args(),
        ),
        IntervalX,
    )


def test_interval_xy_wrapper() -> None:
    check_component(
        interval_xy(
            xfield="foo",
            yfield="bar",
            **interval_args(),
        ),
        IntervalXY,
    )


def test_interval_y_wrapper() -> None:
    check_component(
        interval_y(
            field="foo",
            **interval_args(),
        ),
        IntervalY,
    )


def test_toggle_wrapper() -> None:
    check_component(
        toggle(
            channels=["x", "y"],
            **intersect_selection_args(),
            peers=True,
        ),
        Toggle,
    )


def test_toggle_x_wrapper() -> None:
    check_component(
        toggle_x(
            **intersect_selection_args(),
            peers=True,
        ),
        ToggleX,
    )


def test_toggle_color_wrapper() -> None:
    check_component(
        toggle_color(
            **intersect_selection_args(),
            peers=True,
        ),
        ToggleColor,
    )


def test_nearest_x_wrapper() -> None:
    check_component(
        nearest_x(
            channels=["x", "color"],
            fields=["field1", "field2"],
            max_radius=50,
            **intersect_selection_args(),
        ),
        NearestX,
    )


def test_nearest_y_wrapper() -> None:
    check_component(
        nearest_y(
            channels=["y", "color"],
            fields=["field1", "field2"],
            max_radius=50,
            **intersect_selection_args(),
        ),
        NearestY,
    )


def test_region_wrapper() -> None:
    check_component(
        region(
            channels=["x", "y"],
            **intersect_selection_args(),
            peers=True,
            **brush_args(),
        ),
        Region,
    )


def test_toggle_y_wrapper() -> None:
    check_component(
        toggle_y(
            **intersect_selection_args(),
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
        pan(**pan_selection_args()),
        Pan,
    )


def test_pan_x_wrapper() -> None:
    check_component(
        pan_x(**pan_selection_args()),
        PanX,
    )


def test_pan_y_wrapper() -> None:
    check_component(
        pan_y(**pan_selection_args()),
        PanY,
    )


def test_pan_zoom_wrapper() -> None:
    check_component(
        pan_zoom(**pan_selection_args()),
        PanZoom,
    )


def test_pan_zoom_x_wrapper() -> None:
    check_component(
        pan_zoom_x(**pan_selection_args()),
        PanZoomX,
    )


def test_pan_zoom_y_wrapper() -> None:
    check_component(
        pan_zoom_y(**pan_selection_args()),
        PanZoomY,
    )


def test_text_wrapper(penguins: Data) -> None:
    check_component(
        text(
            penguins,
            text="species",
            **mark_position_args(),
            **basic_selection_args(),
            **text_positioning_args(),
            **text_font_args(),
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
            text_anchor="start",
            line_height=1.5,
            line_width=15,
            text_overflow="clip",
            monospace=False,
            font_family="Helvetica",
            font_size=14,
            font_variant="normal",
            font_weight=400,
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
            text_anchor="end",
            line_height=1.0,
            line_width=25,
            text_overflow="clip",
            monospace=True,
            font_family="monospace",
            font_size=10,
            font_variant="tabular-nums",
            font_weight=400,
        ),
        TextY,
    )


def check_component(component: Component, type: Type[BaseModel]) -> None:
    model = type.model_validate(component.config)
    assert model.model_dump(exclude_none=True, by_alias=True) == component.config


def basic_selection_args() -> dict[str, Selection]:
    return {"filter_by": Selection("intersect")}


def intersect_selection_args() -> dict[str, Selection]:
    return {"selection": Selection("intersect")}


def mark_position_args() -> dict[str, str]:
    return {"x": "bill_depth", "y": "flipper_length", "z": "species"}


def dot_mark_args() -> dict[str, Any]:
    return {
        **mark_position_args(),
        **basic_selection_args(),
        "r": 3,
        "rotate": 45,
        "frame_anchor": "middle",
    }


def line_marker_args() -> dict[str, str]:
    return {
        "marker": "circle",
        "marker_start": "arrow",
        "marker_mid": "dot",
        "marker_end": "arrow-reverse",
        "curve": "linear",
        "tension": 0.5,
    }


def bar_styling_args() -> dict[str, Any]:
    return {
        "interval": "minute",
        "offset": "center",
        "order": "appearance",
        "inset": 1,
        "inset_left": 1,
        "inset_right": 1,
        "inset_bottom": 1,
        "inset_top": 1,
        "rx": 1,
        "ry": 1,
        "reverse": True,
    }


def pan_selection_args() -> dict[str, Selection]:
    return {
        "x": Selection("intersect"),
        "y": Selection("intersect"),
        "xfield": "x_field",
        "yfield": "y_field",
    }


def brush_args() -> dict[str, Brush]:
    return {"brush": Brush(fill="red", fill_opacity=0.6)}


def interval_args() -> dict[str, Any]:
    return {
        **intersect_selection_args(),
        "pixel_size": 2,
        "peers": True,
        **brush_args(),
    }


def text_font_args() -> dict[str, Any]:
    return {
        "line_height": 1.2,
        "line_width": 20,
        "text_overflow": "ellipsis",
        "monospace": True,
        "font_family": "Arial",
        "font_size": 12,
        "font_variant": "small-caps",
        "font_weight": 700,
    }


def text_positioning_args() -> dict[str, Any]:
    return {
        "frame_anchor": "middle",
        "line_anchor": "middle",
        "rotate": 45,
        "text_anchor": "middle",
    }
