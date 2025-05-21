from anywidget import AnyWidget

import inspect_viz as vz
import inspect_viz.plot as pl

from ..plot._widget import plot_widget


def scatterplot(df: vz.DataFrame, x: str, y: str) -> AnyWidget:
    """Adfs.

    Args:
        df: Source DataFrame.
        x: Column name for x-coordinates.
        y: Column name for y-coordinates.
    """
    return plot_widget(df, pl.Plot(plot=[]))
