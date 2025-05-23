from anywidget import AnyWidget

import inspect_viz as vz
from inspect_viz.mosaic import LineY, Plot, PlotFrom

from .spec import spec


def line_y(data: vz.Data, x: str, y: str) -> AnyWidget:
    """LineY graph.

    Args:
        data: Source data.
        x: Column name for x-coordinates.
        y: Column name for y-coordinates.
    """
    lineY = LineY(data=data_from(data), x=x, y=y)
    return spec(data, Plot(plot=[lineY]))


def data_from(df: vz.Data) -> PlotFrom:
    return PlotFrom.model_validate({"from": df.id})
