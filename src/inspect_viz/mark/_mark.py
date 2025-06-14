from typing import Any

from pydantic import JsonValue

from inspect_viz.mark._options import MarkOptions

from .._core.component import Component
from .._util.marshall import snake_to_camel


class Mark(Component):
    """Plot mark (create marks using mark functions, e.g. `dot()`, `bar()`, etc.)."""

    def __init__(
        self, type: str, config: dict[str, JsonValue], options: MarkOptions
    ) -> None:
        super().__init__({"mark": type} | config | mark_options_to_camel(options))


def mark_options_to_camel(options: MarkOptions) -> dict[str, Any]:
    mark_options = {snake_to_camel(key): value for key, value in options.items()}
    if "tip" in mark_options and isinstance(mark_options["tip"], dict):
        mark_options["tip"] = {
            snake_to_camel(key): value for key, value in mark_options["tip"].items()
        }
    return mark_options
