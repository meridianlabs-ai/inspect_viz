from inspect_viz import Component
from inspect_viz.layout import hconcat, hspace, vconcat, vspace

from ._schema import HConcat, HSpace, VConcat, VSpace
from .utils import check_component


def test_vconcat_wrapper(dot_mark: Component) -> None:
    check_component(vconcat(dot_mark), VConcat)


def test_hconcat_wrapper(dot_mark: Component) -> None:
    check_component(hconcat(dot_mark), HConcat)


def test_vspace_wrapper() -> None:
    check_component(vspace(10), VSpace)


def test_hspace_wrapper() -> None:
    check_component(hspace(10), HSpace)
