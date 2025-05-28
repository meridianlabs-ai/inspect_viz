from pydantic import JsonValue

from inspect_viz._core import Component


def radio(label: str | None = None) -> Component:
    radio: dict[str, JsonValue] = {"input": "radio", "label": label}
    return Component(config=radio)
