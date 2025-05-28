from typing import Any, Literal

from shortuuid import uuid

from inspect_viz._core import Widget
from inspect_viz.mosaic import HConcat, Legend, Plot


def plot(
    mark: Widget | list[Widget],
    grid: bool | str = False,
    x_label: str | None = None,
    y_label: str | None = None,
    legend: Literal["color", "opacity", "symbol"] | None = None,
) -> Widget:
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
    components = [m.component for m in mark]
    plot = Plot(
        plot=components,  # type: ignore[arg-type]
        grid=grid,
        xLabel=x_label,
        yLabel=y_label,
    )

    # wrap with legend if specified
    if legend is not None:
        plot.name = uuid()
        legend_args: dict[str, Any] = dict(
            legend=legend, for_=plot.name, columns=1, width=80
        )
        return Widget(HConcat(hconcat=[plot, Legend(**legend_args)]))
    else:
        return Widget(plot)
