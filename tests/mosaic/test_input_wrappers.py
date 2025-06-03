from inspect_viz import Data, Param
from inspect_viz.input import select, table

from ._schema import Menu, Table
from .utils import check_component


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
    check_component(table(penguins), Table)