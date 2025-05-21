from anywidget import AnyWidget

import inspect_viz as vz
import inspect_viz.plot as pl

from .plot import plot


def scatterplot(df: vz.DataFrame, x: str, y: str) -> AnyWidget:
    """Adfs.

    Args:
        df: Source DataFrame.
        x: Column name for x-coordinates.
        y: Column name for y-coordinates.
    """
    return plot(df, pl.Plot(plot=[]))
