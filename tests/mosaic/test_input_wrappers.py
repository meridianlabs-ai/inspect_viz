from inspect_viz import Data, Param
from inspect_viz._core.selection import Selection
from inspect_viz.input import search, select, table
from inspect_viz.input._slider import slider

from ._schema import Menu, Search, Slider, Table
from .utils import check_component


def test_select_wrapper(penguins: Data) -> None:
    check_component(select(penguins, label="Species", column="species"), Menu)
    check_component(
        select(
            label="X",
            options=["body_mass", "flipper_length", "bill_depth", "bill_length"],
            param=Param("body_mass"),
        ),
        Menu,
    )


def test_search_wrapper(penguins: Data) -> None:
    check_component(
        search(penguins, label="Species", column="species", type="regexp"), Search
    )


def test_slider_wrapper(penguins: Data) -> None:
    check_component(
        slider(
            penguins,
            label="Species",
            column="species",
            value=1,
            min=1,
            max=22,
            field="species",
            step=1,
            width=200,
        ),
        Slider,
    )


def test_table_wrapper(penguins: Data) -> None:
    check_component(
        table(
            penguins,
            filter_by=Selection("intersect"),
            align={"bill_length": "left"},
            columns=["bill_length", "bill_depth"],
            width={"bill_length": 10},
            max_width=22,
            height=200,
            row_batch=10,
        ),
        Table,
    )
