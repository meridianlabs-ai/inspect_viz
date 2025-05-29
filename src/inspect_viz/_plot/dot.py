from pydantic import JsonValue

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
    config: dict[str, JsonValue] = dict(
        mark="dot",
        data=data.plot_from(),
        x=dict(column=x),
        y=dict(column=y),
    )
    if stroke is not None:
        config["stroke"] = stroke
    if symbol is not None:
        config["symbol"] = symbol
    if fill is not None:
        config["fill"] = fill

    return Component(config=config)
