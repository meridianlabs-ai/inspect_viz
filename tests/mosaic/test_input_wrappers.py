from inspect_viz import Data
from inspect_viz._core.selection import Selection
from inspect_viz.input import search, slider
from inspect_viz.table import column, table
from pytest import mark

from ._schema import Search, Slider, Table
from .utils import check_component


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


@mark.xfail(reason="Table schema no longer matches mosaic component")
def test_table_wrapper(penguins: Data) -> None:
    check_component(
        table(
            penguins,
            filter_by=Selection("intersect"),
            columns=[column("bill_length", align="left", width=10), "bill_depth"],
            max_width=22,
            height=200,
        ),
        Table,
    )
