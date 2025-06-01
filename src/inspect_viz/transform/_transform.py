from pydantic import JsonValue

from inspect_viz._core.param import Param


class Transform(dict[str, JsonValue]):
    """Column transformation operation."""

    def __init__(self, config: dict[str, JsonValue]) -> None:
        super().__init__(config)


TransformArg = str | float | bool | Param | list[str | float | bool | Param]
