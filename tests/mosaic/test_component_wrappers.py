from pathlib import Path
from typing import Type

import inspect_viz as vz
import pytest
from inspect_viz._core.component import Component
from pydantic import BaseModel

from ._schema import Dot, HConcat, HSpace, Menu, Plot, Table, VConcat, VSpace


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


def test_plot_wrapper(dot_mark: vz.Component) -> None:
    check_component(vz.plot(dot_mark, grid=True, x_label="Foo", y_label="Bar"), Plot)


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


def check_component(component: Component, type: Type[BaseModel]) -> None:
    model = type.model_validate(component.config)
    assert model.model_dump(exclude_none=True, by_alias=True) == component.config
