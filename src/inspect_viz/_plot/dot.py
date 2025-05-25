from inspect_viz._core import Data, Widget
from inspect_viz.mosaic import Dot


def dot(
    data: Data, x: str, y: str, stroke: str | None = None, symbol: str | None = None
) -> Widget:
    """A dot mark that draws circles, or other symbols, as in a scatterplot.

    Args:
        data: The data source for the mark.
        x: Column with x coordinates
        y: Column with y coordinates.
        stroke: Categorical column to bind colors to or CSS color string.
        symbol: Categorical column to bind symbols to or CSS color string.
    """
    return Widget(
        component=Dot(
            data=data.plot_from(),
            x=data.validate_column(x),
            y=data.validate_column(y),
            stroke=stroke,
            symbol=symbol,
        )
    )
