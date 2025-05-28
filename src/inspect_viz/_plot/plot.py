from typing import Literal

from pydantic import JsonValue
from shortuuid import uuid

from inspect_viz._core import Component
from inspect_viz._layout.concat import hconcat


def plot(
    mark: Component | list[Component],
    grid: bool | str = False,
    x_label: str | None = None,
    y_label: str | None = None,
    legend: Literal["color", "opacity", "symbol"] | None = None,
) -> Component:
    """Plot.

    Args:
        mark: Plot mark(s).
        grid: Whether to show a grid aligned with the scale’s ticks. If true, show a grid with the current color stroke; if a string, show a grid with the specified stroke color;
        x_label: A textual label to show on the axis or legend; if `None`, show no label.
        y_label: A textual label to show on the axis or legend; if `None`, show no label.
        legend: foo
    """
    # resolve to list
    mark = mark if isinstance(mark, list) else [mark]

    # create plot
    components = [m.config for m in mark]
    plot: dict[str, JsonValue] = dict(
        plot=components,
        grid=grid,
        xLabel=x_label,
        yLabel=y_label,
    )

    # wrap with legend if specified
    if legend is not None:
        plot["name"] = uuid()
        legend_config: dict[str, JsonValue] = {
            "legend": legend,
            "for": plot["name"],
            "columns": 1,
            "width": 80,
        }
        return hconcat(Component(config=plot), Component(config=legend_config))
    else:
        return Component(config=plot)
