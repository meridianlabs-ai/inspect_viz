from anywidget import AnyWidget

import inspect_viz as vz

from .._core._widget import mosaic_widget
from ..mosaic import LineY, Plot


def line_y(data: vz.Data, x: str, y: str) -> AnyWidget:
    """LineY graph.

    Args:
        data: Source data.
        x: Column name for x-coordinates.
        y: Column name for y-coordinates.
    """
    lineY = LineY(data=data.plot_from(), x=x, y=y)
    return mosaic_widget(data=data, component=Plot(plot=[lineY]))
