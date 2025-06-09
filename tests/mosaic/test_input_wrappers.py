from inspect_viz import Data, Param
from inspect_viz.input import search, select, table

from ._schema import Menu, Search, Table
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


def test_table_wrapper(penguins: Data) -> None:
    check_component(table(penguins), Table)
