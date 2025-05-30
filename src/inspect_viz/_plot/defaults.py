from typing import Any

from typing_extensions import Unpack

from inspect_viz._util.casing import snake_to_camel

from .._core.param import Param
from .options import Interval, PlotOptions


class PlotDefaults(PlotOptions, total=False):
    x_label: str | Param
    """A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.
    """

    y_label: str | Param
    """A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.
    """

    grid: bool | str | Param
    """Whether to show a grid aligned with the scale's ticks. If true, show a grid with the currentColor stroke; if a string, show a grid with the specified stroke color.
    """

    x_grid: bool | str | Interval | list[str | float] | Param
    """Whether to show a grid aligned with the scale's ticks. If true, show a grid with the currentColor stroke; if a string, show a grid with the specified stroke color; if an approximate number of ticks, an interval, or an array of tick values, show corresponding grid lines.
    """

    y_grid: bool | str | Interval | list[str | float] | Param
    """Whether to show a grid aligned with the scale's ticks. If true, show a grid with the currentColor stroke; if a string, show a grid with the specified stroke color; if an approximate number of ticks, an interval, or an array of tick values, show corresponding grid lines."""

    width: float | Param
    """The outer width of the plot in pixels, including margins. Defaults to 640.
    """

    height: float | Param
    """The outer height of the plot in pixels, including margins. The default depends on the plot's scales, and the plot's width if an aspectRatio is specified. For example, if the *y* scale is linear and there is no *fy* scale, it might be 396.
    """


def plot_defaults(**defaults: Unpack[PlotDefaults]) -> None:
    """Set global plot defaults.

    Note that this function should be called once at the outset (subsequent calls to it do not reset the defaults).

    Args:
       defaults: Keyword args from `PlotDefaults`
    """
    global _plot_defaults
    _plot_defaults = defaults


def plot_defaults_as_camel() -> dict[str, Any]:
    global _plot_defaults
    return {snake_to_camel(key): value for key, value in _plot_defaults.items()}


_plot_defaults = PlotDefaults()
