from typing import Any, Literal, Sequence, cast

from shortuuid import uuid
from typing_extensions import Unpack

from inspect_viz._util.notgiven import NOT_GIVEN, NotGiven
from inspect_viz._util.platform import quarto_fig_size

from .._core import Component
from .._core.param import Param
from ..interactor._interactors import Interactor
from ..layout._concat import hconcat
from ..mark._mark import Mark
from ..mark._title import Title
from ..mark._title import title as title_mark
from ._attributes import PlotAttributes, plot_attributes_mosaic
from ._legend import Legend
from ._legend import legend as create_legend


def plot(
    *plot: Mark | Interactor | Legend | Sequence[Mark | Interactor | Legend],
    x_label: str | Param | None | NotGiven = NOT_GIVEN,
    fx_label: str | Param | None | NotGiven = NOT_GIVEN,
    y_label: str | Param | None | NotGiven = NOT_GIVEN,
    fy_label: str | Param | None | NotGiven = NOT_GIVEN,
    title: str | Title | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    name: str | None = None,
    legend: Literal["color", "opacity", "symbol"]
    | Sequence[Literal["color", "opacity", "symbol"]]
    | Legend
    | Sequence[Legend]
    | None = None,
    **attributes: Unpack[PlotAttributes],
) -> Component:
    """Create a plot.

    Args:
        *plot: Plot elements (marks, interactors, legends)
        x_label: A textual label to show on the axis or legend; if null, show no label.
            By default the scale label is inferred from channel definitions, possibly with
            an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value. Pass
            `None` for no x_label.
        fx_label:  A textual label to show on the axis or legend; if `None`, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.
        y_label: A textual label to show on the axis or legend; if null, show no label.
            By default the scale label is inferred from channel definitions, possibly with
            an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value. Pass
            `None` for no y_label.
        fy_label:  A textual label to show on the axis or legend; if `None`, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.
        title: Title for plot (`str` or mark created with the `title()` function).
        width: The outer width of the plot in pixels, including margins. Defaults to 700.
        height: The outer height of the plot in pixels, including margins. The default is width / 1.618 (the [golden ratio](https://en.wikipedia.org/wiki/Golden_ratio))
        name: A unique name for the plot. The name is used by standalone legend
            components to to lookup the plot and access scale mappings.
        legend: Plot legend.
        **attributes: Additional `PlotAttributes`.
    """
    # resolve items
    items: list[Mark | Interactor | Legend] = []
    for item in plot:
        if isinstance(item, Title):
            title = title or item
        if isinstance(item, (Mark, Interactor, Legend)):
            items.append(item)
        else:  # it's a sequence
            items.extend(item)

    # prepend title if provided
    title = title_mark(title) if isinstance(title, str) else title
    if title is not None:
        items.insert(0, title)
        if "margin" not in attributes and "margin_top" not in attributes:
            attributes["margin_top"] = title.margin_top

    # create plot
    components = [m.config for m in items]
    config: dict[str, Any] = dict(plot=components)

    if not isinstance(x_label, NotGiven):
        config["xLabel"] = x_label
    if not isinstance(y_label, NotGiven):
        config["yLabel"] = y_label
    if not isinstance(fx_label, NotGiven):
        config["fxLabel"] = fx_label
    if not isinstance(fy_label, NotGiven):
        config["fyLabel"] = fy_label

    # plot width and height (use quarto default if not specified)
    quarto_size = quarto_fig_size()
    if width is not None:
        config["width"] = width
    elif quarto_size:
        config["width"] = quarto_size[0]
    else:
        config["width"] = 700
    if height is not None:
        config["height"] = height
    elif quarto_size:
        config["height"] = quarto_size[1]
    else:
        config["height"] = config["width"] / 1.618

    if name is not None:
        config["name"] = name

    # merge other plot options
    config = config | plot_attributes_mosaic(attributes)

    # wrap with legend if specified
    if legend is not None:
        # create name for plot and resolve/bind legend to it
        config["name"] = f"plot_{uuid()}"

        # resolve the legend into components
        legend_components: list[Legend]
        if isinstance(legend, str):
            legend_components = [create_legend(legend)]
        elif isinstance(legend, Legend):
            legend_components = [legend]
        elif isinstance(legend, Sequence):
            legend_components = []
            for legend_item in legend:
                if isinstance(legend_item, str):
                    legend_components.append(
                        create_legend(
                            cast(Literal["color", "opacity", "symbol"], legend_item)
                        )
                    )
                elif isinstance(legend_item, Legend):
                    legend_components.append(legend_item)

        for leg in legend_components:
            leg.config["for"] = config["name"]

        # handle legend location
        plot_component = Component(config=config)
        if leg.frame_anchor in [
            "left",
            "right",
            "top-left",
            "top-right",
            "bottom-left",
            "bottom-right",
        ]:
            return hconcat(plot_component, *legend_components)
        else:
            return hconcat(plot_component, *legend_components)

    else:
        return hconcat(Component(config=config))
