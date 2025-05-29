from typing import Any, Literal, Unpack

from pydantic import JsonValue
from shortuuid import uuid

from .._core import Component
from .._core.param import Param
from .._layout.concat import hconcat
from .mark import Mark
from .options import Interval, PlotOptions, plot_options_to_camel


def plot(
    marks: Mark | list[Mark],
    x_label: str | Param | None = None,
    y_label: str | Param | None = None,
    grid: bool | str | Param | None = None,
    x_grid: bool | str | Interval | list[str | float] | Param | None = None,
    y_grid: bool | str | Interval | list[str | float] | Param | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    legend: Literal["color", "opacity", "symbol"] | None = None,
    **options: Unpack[PlotOptions],
) -> Component:
    """Plot.

    Args:
        marks: Plot mark(s).
        x_label: A textual label to show on the axis or legend; if null, show no label.
          By default the scale label is inferred from channel definitions, possibly with
          an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value. For
          axes and legends only.
        y_label: A textual label to show on the axis or legend; if null, show no label.
          By default the scale label is inferred from channel definitions, possibly with
          an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value. For
          axes and legends only.
        grid: Whether to show a grid aligned with the scale's ticks. If true, show a grid
          with the currentColor stroke; if a string, show a grid with the specified
          stroke color.
        x_grid: Whether to show a grid aligned with the scale's ticks. If true, show a
          grid with the currentColor stroke; if a string, show a grid with the specified
          stroke color; if an approximate number of ticks, an interval, or an array
          of tick values, show corresponding grid lines.
        y_grid: Whether to show a grid aligned with the scale's ticks. If true, show a
          grid with the currentColor stroke; if a string, show a grid with the specified
          stroke color; if an approximate number of ticks, an interval, or an array
          of tick values, show corresponding grid lines.
        width: The outer width of the plot in pixels, including margins. Defaults to 640.
        height: The outer height of the plot in pixels, including margins. The default
          depends on the plot's scales, and the plot's width if an aspectRatio is
          specified. For example, if the *y* scale is linear and there is no *fy*
          scale, it might be 396.
        legend: Plot legend.
        options: Additional `PlotOptions`.
    """
    # resolve to list
    marks = marks if isinstance(marks, list) else [marks]

    # create plot
    components = [m.config for m in marks]
    plot: dict[str, Any] = dict(plot=components)

    if x_label is not None:
        plot["xLabel"] = x_label

    if y_label is not None:
        plot["yLabel"] = y_label

    if grid is not None:
        plot["grid"] = grid

    if x_grid is not None:
        plot["xGrid"] = x_grid

    if y_grid is not None:
        plot["yGrid"] = x_grid

    if width is not None:
        plot["width"] = width

    if height is not None:
        plot["height"] = height

    # merge other plot options
    plot = plot | plot_options_to_camel(options)

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
