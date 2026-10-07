import json
import re
from typing import Callable

import pandas as pd
import pytest
from inspect_viz import Component, Data
from inspect_viz.input import select
from inspect_viz.layout import vconcat
from inspect_viz.mark import dot, rule_x
from inspect_viz.plot import plot, to_html
from inspect_viz.table import table
from inspect_viz.transform import sql


def embedded_tables(html: str) -> set[str]:
    match = re.search(r"const state = (.+);$", html, re.MULTILINE)
    assert match is not None, "widget bootstrap state not found"
    return set(json.loads(match[1])["tables"])


@pytest.mark.parametrize(
    "build",
    [
        lambda data: plot(dot(data, x="x", y="y")),
        lambda data: vconcat(select(data, column="x"), plot(dot(data, x="x", y="y"))),
        lambda data: table(data),
    ],
)
def test_to_html_embeds_only_the_tables_the_component_reads(
    build: Callable[[Data], Component],
) -> None:
    used = Data.from_dataframe(pd.DataFrame({"x": [1], "y": [2]}))
    Data.from_dataframe(pd.DataFrame({"x": [3], "y": [4]}))  # not read by the component

    assert embedded_tables(to_html(build(used))) == {used.table}


def test_to_html_embeds_no_tables_for_a_component_without_data() -> None:
    Data.from_dataframe(pd.DataFrame({"x": [1]}))

    assert embedded_tables(to_html(plot(rule_x(None, x=[1, 2])))) == set()


def test_to_html_embeds_every_table_a_component_reads() -> None:
    first = Data.from_dataframe(pd.DataFrame({"x": [1], "y": [2]}))
    second = Data.from_dataframe(pd.DataFrame({"x": [3], "y": [4]}))
    component = vconcat(plot(dot(first, x="x", y="y")), plot(dot(second, x="x", y="y")))

    assert embedded_tables(to_html(component)) == {first.table, second.table}


def test_to_html_embeds_a_table_named_in_a_sql_expression() -> None:
    plotted = Data.from_dataframe(pd.DataFrame({"x": [1], "y": [2]}))
    queried = Data.from_dataframe(pd.DataFrame({"x": [3]}))
    component = plot(
        dot(plotted, x=sql(f"(SELECT max(x) FROM {queried.table})"), y="y")
    )

    assert embedded_tables(to_html(component)) == {plotted.table, queried.table}
