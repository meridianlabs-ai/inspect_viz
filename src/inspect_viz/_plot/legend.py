from pydantic import JsonValue
from typing_extensions import Literal

from .._core.component import Component


class Legend(Component):
    pass


def legend(
    legend: Literal["color", "opacity", "symbol"],
    columns: int = 1,
    width: float | None = None,
    height: float | None = None,
    for_plot: str | None = None,
) -> Legend:
    config: dict[str, JsonValue] = {"legend": legend, "columns": columns}
    if width is not None:
        config["width"] = width
    if height is not None:
        config["height"] = height
    if for_plot is not None:
        config["for"] = for_plot

    return Legend(config=config)
