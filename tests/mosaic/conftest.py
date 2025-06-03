from pathlib import Path

import pytest
from inspect_viz import Component, Data


@pytest.fixture
def penguins() -> Data:
    return Data(Path(__file__).parent.parent / "_data" / "penguins.parquet")


@pytest.fixture
def dot_mark(penguins: Data) -> Component:
    from inspect_viz.mark import dot

    return dot(
        penguins,
        x="bill_depth",
        y="flipper_length",
        fill="species",
        symbol="species",
        margin_bottom=0,
        margin_right=0,
    )
