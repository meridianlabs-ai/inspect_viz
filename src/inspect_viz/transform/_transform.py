from typing import TypeAlias

from pydantic import JsonValue

from inspect_viz._core.param import Param

Transform: TypeAlias = dict[str, JsonValue]
"""Column transformation operation."""


TransformArg = str | float | bool | Param | list[str | float | bool | Param]
