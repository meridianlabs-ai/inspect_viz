from anywidget import AnyWidget

import inspect_viz as vz

from ..mosaic import LineY, Plot, PlotFrom, mosaic


def line_y(data: vz.Data, x: str, y: str) -> AnyWidget:
    """LineY graph.

    Args:
        data: Source data.
        x: Column name for x-coordinates.
        y: Column name for y-coordinates.
    """
    lineY = LineY(data=data_from(data), x=x, y=y)
    return mosaic(data=data, component=Plot(plot=[lineY]))


def data_from(df: vz.Data) -> PlotFrom:
    return PlotFrom.model_validate({"from": df.id, "filterBy": f"${df.selection.id}"})
