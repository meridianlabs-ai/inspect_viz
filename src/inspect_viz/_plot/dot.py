from inspect_viz._core import Component, Data


def dot(
    data: Data,
    x: str,
    y: str,
    stroke: str | None = None,
    symbol: str | None = None,
    fill: str | None = None,
) -> Component:
    """A dot mark that draws circles, or other symbols, as in a scatterplot.

    Args:
        data: The data source for the mark.
        x: Column with x coordinates
        y: Column with y coordinates.
        stroke: Categorical column to bind stroke colors to or CSS color string.
        symbol: Categorical column to bind symbols to or CSS color string.
        fill: Categorical column to bind fill colors to or CSS color string.
    """
    return Component(
        config=dict(
            mark="dot",
            data=data.plot_from(),
            x=dict(column=x),
            y=dict(column=y),
            stroke=stroke,
            symbol=symbol,
            fill=fill,
        )
    )
