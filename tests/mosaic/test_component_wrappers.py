from pathlib import Path
from typing import Type

import inspect_viz as vz
import pytest
from inspect_viz._core.component import Component
from pydantic import BaseModel

from ._schema import (
    BarX,
    Dot,
    HConcat,
    Highlight,
    HSpace,
    IntervalX,
    IntervalXY,
    IntervalY,
    Legend,
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
def penguins() -> vz.Data:
    return vz.Data(Path(__file__).parent.parent / "_data" / "penguins.parquet")


@pytest.fixture
def dot_mark(penguins: vz.Data) -> vz.Component:
    return vz.dot(
        penguins,
        x="bill_depth",
        y="flipper_length",
        fill="species",
        symbol="species",
        margin_bottom=0,
        margin_right=0,
    )


def test_vconcat_wrapper(dot_mark: vz.Component) -> None:
    check_component(vz.vconcat(dot_mark), VConcat)


def test_hconcat_wrapper(dot_mark: vz.Component) -> None:
    check_component(vz.hconcat(dot_mark), HConcat)


def test_vspace_wrapper() -> None:
    check_component(vz.vspace(10), VSpace)


def test_hspace_wrapper() -> None:
    check_component(vz.hspace(10), HSpace)


def test_dot_wrapper(dot_mark: vz.Component) -> None:
    check_component(dot_mark, Dot)


def test_bar_x_wrapper(penguins: vz.Data) -> None:
    check_component(
        vz.bar_x(
            penguins,
            x="bill_depth",
            x1="bill_depth",
            x2="bill_depth",
            y="bill_depth",
            interval="minute",
            filter_by=vz.Selection("intersect"),
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


def test_plot_wrapper(dot_mark: vz.Component) -> None:
    check_component(vz.plot(dot_mark, grid=True, x_label="Foo", y_label="Bar"), Plot)


def test_highlight_wrapper() -> None:
    check_component(
        vz.highlight(
            by=vz.Selection("intersect"),
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
        vz.interval_x(
            selection=vz.Selection("intersect"),
            field="foo",
            pixel_size=2,
            peers=True,
            brush=vz.Brush(fill="red", fill_opacity=0.6),
        ),
        IntervalX,
    )


def test_interval_xy_wrapper() -> None:
    check_component(
        vz.interval_xy(
            selection=vz.Selection("intersect"),
            xfield="foo",
            yfield="bar",
            pixel_size=2,
            peers=True,
            brush=vz.Brush(fill="red", fill_opacity=0.6),
        ),
        IntervalXY,
    )


def test_interval_y_wrapper() -> None:
    check_component(
        vz.interval_y(
            selection=vz.Selection("intersect"),
            field="foo",
            pixel_size=2,
            peers=True,
            brush=vz.Brush(fill="red", fill_opacity=0.6),
        ),
        IntervalY,
    )


def test_toggle_wrapper() -> None:
    check_component(
        vz.toggle(
            selection=vz.Selection("intersect"),
            channels=["x", "y"],
            peers=True,
        ),
        Toggle,
    )


def test_toggle_x_wrapper() -> None:
    check_component(
        vz.toggle_x(
            selection=vz.Selection("intersect"),
            peers=True,
        ),
        ToggleX,
    )


def test_toggle_color_wrapper() -> None:
    check_component(
        vz.toggle_color(
            selection=vz.Selection("intersect"),
            peers=True,
        ),
        ToggleColor,
    )


def test_nearest_x_wrapper() -> None:
    check_component(
        vz.nearest_x(
            selection=vz.Selection("intersect"),
            channels=["x", "color"],
            fields=["field1", "field2"],
            max_radius=50,
        ),
        NearestX,
    )


def test_nearest_y_wrapper() -> None:
    check_component(
        vz.nearest_y(
            selection=vz.Selection("intersect"),
            channels=["y", "color"],
            fields=["field1", "field2"],
            max_radius=50,
        ),
        NearestY,
    )


def test_region_wrapper() -> None:
    check_component(
        vz.region(
            selection=vz.Selection("intersect"),
            channels=["x", "y"],
            peers=True,
            brush=vz.Brush(fill="red", fill_opacity=0.6),
        ),
        Region,
    )


def test_toggle_y_wrapper() -> None:
    check_component(
        vz.toggle_y(
            selection=vz.Selection("intersect"),
            peers=True,
        ),
        ToggleY,
    )


def test_select_wrapper(penguins: vz.Data) -> None:
    check_component(vz.select("Species", penguins, column="species"), Menu)
    check_component(
        vz.select(
            "X",
            options=["body_mass", "flipper_length", "bill_depth", "bill_length"],
            param=vz.Param("body_mass"),
        ),
        Menu,
    )


def test_table_wrapper(penguins: vz.Data) -> None:
    check_component(vz.table(penguins), Table)


def test_legend_wrapper(penguins: vz.Data) -> None:
    check_component(
        vz.legend(
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
        vz.pan(
            x=vz.Selection("intersect"),
            y=vz.Selection("intersect"),
            xfield="x_field",
            yfield="y_field",
        ),
        Pan,
    )


def test_pan_x_wrapper() -> None:
    check_component(
        vz.pan_x(
            x=vz.Selection("intersect"),
            y=vz.Selection("intersect"),
            xfield="x_field",
            yfield="y_field",
        ),
        PanX,
    )


def test_pan_y_wrapper() -> None:
    check_component(
        vz.pan_y(
            x=vz.Selection("intersect"),
            y=vz.Selection("intersect"),
            xfield="x_field",
            yfield="y_field",
        ),
        PanY,
    )


def test_pan_zoom_wrapper() -> None:
    check_component(
        vz.pan_zoom(
            x=vz.Selection("intersect"),
            y=vz.Selection("intersect"),
            xfield="x_field",
            yfield="y_field",
        ),
        PanZoom,
    )


def test_pan_zoom_x_wrapper() -> None:
    check_component(
        vz.pan_zoom_x(
            x=vz.Selection("intersect"),
            y=vz.Selection("intersect"),
            xfield="x_field",
            yfield="y_field",
        ),
        PanZoomX,
    )


def test_pan_zoom_y_wrapper() -> None:
    check_component(
        vz.pan_zoom_y(
            x=vz.Selection("intersect"),
            y=vz.Selection("intersect"),
            xfield="x_field",
            yfield="y_field",
        ),
        PanZoomY,
    )


def check_component(component: Component, type: Type[BaseModel]) -> None:
    model = type.model_validate(component.config)
    assert model.model_dump(exclude_none=True, by_alias=True) == component.config
