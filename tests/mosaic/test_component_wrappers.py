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
    Legend,
    Menu,
    Plot,
    Table,
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


def check_component(component: Component, type: Type[BaseModel]) -> None:
    model = type.model_validate(component.config)
    assert model.model_dump(exclude_none=True, by_alias=True) == component.config
