from inspect_viz import Component, Data
from inspect_viz.plot import legend, plot

from ._schema import Legend, Plot
from .utils import check_component


def test_plot_wrapper(dot_mark: Component) -> None:
    check_component(plot(dot_mark, grid=True, x_label="Foo", y_label="Bar"), Plot)


def test_legend_wrapper(penguins: Data) -> None:
    check_component(
        legend(
            "color",
            label="foo",
            columns=1,
            selection=penguins.selection,
            field="species",
            width=100,
            height=100,
            tick_size=5,
            margin_bottom=5,
            margin_left=5,
            margin_right=5,
            margin_top=5,
            for_plot="foo",
        ),
        Legend,
    )
