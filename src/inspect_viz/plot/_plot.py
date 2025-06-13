from typing import Any, Literal, Sequence, Unpack

from shortuuid import uuid

from inspect_viz._util.notgiven import NOT_GIVEN, NotGiven

from .._core import Component
from .._core.param import Param
from .._core.types import Interval
from ..interactor._interactors import Interactor
from ..layout._concat import hconcat, vconcat
from ..mark._mark import Mark
from ._legend import Legend
from ._legend import legend as create_legend
from ._options import PlotOptions, plot_options_mosaic


def plot(
    plot: Mark | Sequence[Mark | Interactor],
    x_label: str | Param | None | NotGiven = NOT_GIVEN,
    y_label: str | Param | None | NotGiven = NOT_GIVEN,
    grid: bool | str | Param | None = None,
    x_grid: bool | str | Interval | list[str | float] | Param | None = None,
    y_grid: bool | str | Interval | list[str | float] | Param | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    name: str | None = None,
    legend: Literal["color", "opacity", "symbol"] | Legend | None = None,
    **options: Unpack[PlotOptions],
) -> Component:
    """Plot.

    Args:
        plot: Plot mark(s).
        x_label: A textual label to show on the axis or legend; if null, show no label.
          By default the scale label is inferred from channel definitions, possibly with
          an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value. Pass
          `None` for no x_label.
        y_label: A textual label to show on the axis or legend; if null, show no label.
          By default the scale label is inferred from channel definitions, possibly with
          an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value. Pass
          `None` for no y_label.
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
        name: A unique name for the plot. The name is used by standalone legend
          components to to lookup the plot and access scale mappings.
        legend: Plot legend.
        options: Additional `PlotOptions`.
    """
    # resolve to list
    plot = plot if isinstance(plot, Sequence) else [plot]

    # create plot
    components = [m.config for m in plot]
    config: dict[str, Any] = dict(plot=components)

    if not isinstance(x_label, NotGiven):
        config["xLabel"] = x_label
    if not isinstance(y_label, NotGiven):
        config["yLabel"] = y_label

    if grid is not None:
        config["grid"] = grid

    if x_grid is not None:
        config["xGrid"] = x_grid

    if y_grid is not None:
        config["yGrid"] = x_grid

    if width is not None:
        config["width"] = width

    if height is not None:
        config["height"] = height

    if name is not None:
        config["name"] = name

    # merge other plot options
    config = config | plot_options_mosaic(options)

    # wrap with legend if specified
    if legend is not None:
        # create name for plot and resolve/bind legend to it
        config["name"] = f"plot_{uuid()}"
        if isinstance(legend, str):
            legend = create_legend(legend, location="right")
        legend.config["for"] = config["name"]

        # handle legend location
        plot_component = Component(config=config)
        if legend.location in ["left", "right"]:
            if "width" not in legend.config:
                legend.config["width"] = 80
            if legend.location == "left":
                return hconcat(legend, plot_component)
            else:
                return hconcat(plot_component, legend)
        elif legend.location == "bottom":
            return vconcat(plot_component, legend)
        else:
            return vconcat(legend, plot_component)
    else:
        return Component(config=config)
