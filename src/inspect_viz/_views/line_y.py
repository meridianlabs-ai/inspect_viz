from anywidget import AnyWidget

import inspect_viz as vz
import inspect_viz.plot as pl
from inspect_viz.plot.schema.plot import LineY, PlotFrom

from .plot import plot


def line_y(df: vz.DataFrame, x: str, y: str) -> AnyWidget:
    """LineY graph.

    Args:
        df: Source DataFrame.
        x: Column name for x-coordinates.
        y: Column name for y-coordinates.
    """
    lineY = LineY(data=data_from_df(df), x=x, y=y)
    return plot(df, pl.Plot(plot=[lineY]))


def data_from_df(df: vz.DataFrame) -> PlotFrom:
    return PlotFrom.model_validate({"from": df.source_id})
