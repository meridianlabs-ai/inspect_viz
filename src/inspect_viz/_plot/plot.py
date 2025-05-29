from typing import Literal, Unpack

from pydantic import JsonValue
from shortuuid import uuid

from .._core import Component
from .._layout.concat import hconcat
from .options import PlotOptions, plot_options_to_camel


def plot(
    mark: Component | list[Component],
    legend: Literal["color", "opacity", "symbol"] | None = None,
    **options: Unpack[PlotOptions],
) -> Component:
    """Plot.

    Args:
        mark: Plot mark(s).
        legend: Plot legend.
        options: Additional `PlotOptions`.
    """
    # resolve to list
    mark = mark if isinstance(mark, list) else [mark]

    # create plot
    components = [m.config for m in mark]
    plot: dict[str, JsonValue] = dict(plot=components) | plot_options_to_camel(options)

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
