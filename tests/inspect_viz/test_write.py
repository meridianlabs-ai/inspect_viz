import json
import re
from typing import Any, Callable

import pandas as pd
import pytest
from inspect_viz import Component, Data, Param
from inspect_viz.input import select
from inspect_viz.layout import vconcat
from inspect_viz.mark import dot, rule_x
from inspect_viz.plot import HtmlPage, plot, to_html
from inspect_viz.table import table
from inspect_viz.transform import sql

EMPTY_TABLE = {"__iv_bytes__": True, "data": ""}


def widget_tables(html: str) -> list[dict[str, Any]]:
    """The `tables` payload of each widget bootstrap in the html, in order."""
    states = re.findall(r"const state = (.+);$", html, re.MULTILINE)
    assert states, "widget bootstrap state not found"
    return [json.loads(state)["tables"] for state in states]


def embedded_tables(html: str) -> set[str]:
    """The tables a single-widget html carries the bytes of.

    A standalone document has no other fragment to wait for, so every table
    it names must carry bytes.
    """
    (tables,) = widget_tables(html)
    assert EMPTY_TABLE not in tables.values(), "standalone html awaits a table"
    return set(tables)


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


def test_to_html_embeds_a_table_named_in_a_different_case() -> None:
    plotted = Data.from_dataframe(pd.DataFrame({"x": [1], "y": [2]}))
    queried = Data.from_dataframe(pd.DataFrame({"x": [3]}))
    component = plot(
        dot(plotted, x=sql(f"(SELECT max(x) FROM {queried.table.lower()})"), y="y")
    )

    assert embedded_tables(to_html(component)) == {plotted.table, queried.table}


def test_to_html_skips_a_table_whose_selection_filters_the_component() -> None:
    plotted = Data.from_dataframe(pd.DataFrame({"x": [1], "y": [2]}))
    other = Data.from_dataframe(pd.DataFrame({"x": [3], "y": [4]}))
    component = plot(dot(plotted, x="x", y="y", filter_by=other.selection))

    assert embedded_tables(to_html(component)) == {plotted.table}


def test_to_html_embeds_a_table_named_by_a_referenced_param() -> None:
    plotted = Data.from_dataframe(pd.DataFrame({"x": [1], "y": [2]}))
    queried = Data.from_dataframe(pd.DataFrame({"x": [3]}))
    name = Param(queried.table)
    component = plot(
        dot(plotted, x=sql(f"(SELECT max(x) FROM query_table({name}))"), y="y")
    )

    assert embedded_tables(to_html(component)) == {plotted.table, queried.table}


def test_to_html_skips_a_table_named_by_an_unreferenced_param() -> None:
    plotted = Data.from_dataframe(pd.DataFrame({"x": [1], "y": [2]}))
    other = Data.from_dataframe(pd.DataFrame({"x": [3]}))
    Param(other.table)  # not read by the component

    assert embedded_tables(to_html(plot(dot(plotted, x="x", y="y")))) == {plotted.table}


def test_to_html_embeds_a_table_in_each_document() -> None:
    data = Data.from_dataframe(pd.DataFrame({"x": [1], "y": [2]}))
    component = plot(dot(data, x="x", y="y"))

    assert embedded_tables(to_html(component)) == {data.table}
    assert embedded_tables(to_html(component)) == {data.table}


def test_to_html_carries_the_bundle_once_in_the_head() -> None:
    data = Data.from_dataframe(pd.DataFrame({"x": [1], "y": [2]}))

    html = to_html(plot(dot(data, x="x", y="y")), extra_head="<style>b{}</style>")

    head = html[: html.index("</head>")]
    assert head.count('id="iv-esm"') == 1 and html.count('id="iv-esm"') == 1
    assert head.index("<style>b{}</style>") < head.index('id="iv-css"')


def test_page_embeds_a_table_once_and_later_fragments_wait_for_it() -> None:
    shared = Data.from_dataframe(pd.DataFrame({"x": [1], "y": [2]}))
    own = Data.from_dataframe(pd.DataFrame({"x": [3], "y": [4]}))
    page = HtmlPage()

    html = page.fragment(plot(dot(shared, x="x", y="y"))) + page.fragment(
        vconcat(plot(dot(shared, x="x", y="y")), plot(dot(own, x="x", y="y")))
    )

    first, second = widget_tables(html)
    assert set(first) == {shared.table} and first[shared.table] != EMPTY_TABLE
    assert second[shared.table] == EMPTY_TABLE and second[own.table] != EMPTY_TABLE


def test_page_embeds_a_table_first_read_by_a_middle_fragment() -> None:
    first_data = Data.from_dataframe(pd.DataFrame({"x": [1], "y": [2]}))
    later = Data.from_dataframe(pd.DataFrame({"x": [3], "y": [4]}))
    page = HtmlPage()

    html = "".join(
        page.fragment(plot(dot(data, x="x", y="y")))
        for data in (first_data, later, later)
    )

    first, middle, last = widget_tables(html)
    assert set(first) == {first_data.table}
    assert middle[later.table] != EMPTY_TABLE and last[later.table] == EMPTY_TABLE


def test_page_embeds_a_component_rendered_twice_once() -> None:
    data = Data.from_dataframe(pd.DataFrame({"x": [1], "y": [2]}))
    component = plot(dot(data, x="x", y="y"))
    page = HtmlPage()

    first, second = widget_tables(page.fragment(component) + page.fragment(component))

    assert first[data.table] != EMPTY_TABLE and second == {data.table: EMPTY_TABLE}


def test_page_fragment_without_data_carries_no_tables() -> None:
    Data.from_dataframe(pd.DataFrame({"x": [1]}))

    (tables,) = widget_tables(HtmlPage().fragment(plot(rule_x(None, x=[1, 2]))))

    assert tables == {}


def test_page_skips_a_table_without_bytes(monkeypatch: pytest.MonkeyPatch) -> None:
    plotted = Data.from_dataframe(pd.DataFrame({"x": [1], "y": [2]}))
    empty = Data.from_dataframe(pd.DataFrame({"x": [3]}))
    monkeypatch.setattr(empty, "_data", b"")
    component = plot(dot(plotted, x=sql(f"(SELECT max(x) FROM {empty.table})"), y="y"))

    (tables,) = widget_tables(HtmlPage().fragment(component))

    assert set(tables) == {plotted.table}


def test_page_head_carries_the_bundle_and_fragments_do_not() -> None:
    data = Data.from_dataframe(pd.DataFrame({"x": [1], "y": [2]}))
    page = HtmlPage()

    head = page.head()
    fragment = page.fragment(plot(dot(data, x="x", y="y")))

    assert 'id="iv-esm"' in head and 'id="iv-css"' in head
    assert head == page.head()
    assert 'id="iv-esm"' not in fragment and 'id="iv-css"' not in fragment


def test_page_head_loads_the_stylesheet_before_any_component_exists(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(Component, "_css_initialized", False)
    monkeypatch.setattr(Component, "_css", "")
    monkeypatch.setattr(Component, "_quarto_assets_embedded_for_doc", None)

    head = HtmlPage().head()

    assert '<style id="iv-css">' in head and ".mosaic-widget" in head
    assert Component._quarto_assets_embedded_for_doc is None
