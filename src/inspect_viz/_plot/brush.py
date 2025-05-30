from typing import Any, TypedDict

from inspect_viz._util.casing import snake_to_camel


class Brush(TypedDict, total=False):
    fill: str
    "The fill color of the brush rectangle."

    fill_opacity: float
    """The fill opacity of the brush rectangle."""

    opacity: float
    """The overall opacity of the brush rectangle."""

    stroke: str
    """The stroke color of the brush rectangle."""

    stroke_dasharray: str
    """The stroke dash array of the brush rectangle."""

    stroke_opacity: float
    """The stroke opacity of the brush rectangle."""


def brush_as_camel(brush: Brush) -> dict[str, Any]:
    return {snake_to_camel(key): value for key, value in brush.items()}
