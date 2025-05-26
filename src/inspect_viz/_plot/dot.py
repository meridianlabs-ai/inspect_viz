from inspect_viz._core import Data, Widget
from inspect_viz.mosaic import Column, Dot


def dot(
    data: Data,
    x: str,
    y: str,
    stroke: str | None = None,
    symbol: str | None = None,
    fill: str | None = None,
) -> Widget:
    """A dot mark that draws circles, or other symbols, as in a scatterplot.

    Args:
        data: The data source for the mark.
        x: Column with x coordinates
        y: Column with y coordinates.
        stroke: Categorical column to bind stroke colors to or CSS color string.
        symbol: Categorical column to bind symbols to or CSS color string.
        fill: Categorical column to bind fill colors to or CSS color string.
    """
    return Widget(
        component=Dot(
            data=data.plot_from(),
            x=Column(column=x),
            y=Column(column=y),
            stroke=stroke,
            symbol=symbol,
            fill=fill,
        )
    )
