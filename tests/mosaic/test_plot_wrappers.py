from inspect_viz import Component, Data
from inspect_viz.plot import legend, plot
from pytest import mark

from ._schema import Legend, Plot
from .utils import check_component


def test_plot_wrapper(dot_mark: Component) -> None:
    check_component(
        Component(
            config=plot(dot_mark, grid=True, x_label="Foo", y_label="Bar").config[  # type: ignore[arg-type]
                "hconcat"  # type: ignore[index]
            ][0]  # type: ignore[index]
        ),
        Plot,
    )


@mark.xfail(reason="Legend schema no longer matches mosaic component")
def test_legend_wrapper(penguins: Data) -> None:
    check_component(
        legend(
            "color",
            label="foo",
            columns=1,
            target=penguins.selection,
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
