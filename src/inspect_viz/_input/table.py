from pydantic import JsonValue

from inspect_viz._core import Component, Data


def table(data: Data) -> Component:
    table: dict[str, JsonValue] = {
        "input": "table",
        "from": data.table,
        "filterBy": data.selection,
    }
    return Component(config=table)
