from inspect_viz import Selection
from inspect_viz.interactor import (
    highlight,
    interval_x,
    interval_xy,
    interval_y,
    nearest_x,
    nearest_y,
    pan,
    pan_x,
    pan_y,
    pan_zoom,
    pan_zoom_x,
    pan_zoom_y,
    region,
    toggle,
    toggle_color,
    toggle_x,
    toggle_y,
)

from ._schema import (
    Highlight,
    IntervalX,
    IntervalXY,
    IntervalY,
    NearestX,
    NearestY,
    Pan,
    PanX,
    PanY,
    PanZoom,
    PanZoomX,
    PanZoomY,
    Region,
    Toggle,
    ToggleColor,
    ToggleX,
    ToggleY,
)
from .utils import (
    brush_args,
    check_component,
    intersect_selection_args,
    interval_args,
    pan_selection_args,
)


def test_highlight_wrapper() -> None:
    check_component(
        highlight(
            by=Selection("intersect"),
            opacity=0.5,
            fill_opacity=0.5,
            stroke_opacity=0.5,
            fill="red",
            stroke="blue",
        ),
        Highlight,
    )


def test_interval_x_wrapper() -> None:
    check_component(
        interval_x(
            field="foo",
            **interval_args(),
        ),
        IntervalX,
    )


def test_interval_xy_wrapper() -> None:
    check_component(
        interval_xy(
            xfield="foo",
            yfield="bar",
            **interval_args(),
        ),
        IntervalXY,
    )


def test_interval_y_wrapper() -> None:
    check_component(
        interval_y(
            field="foo",
            **interval_args(),
        ),
        IntervalY,
    )


def test_toggle_wrapper() -> None:
    check_component(
        toggle(
            channels=["x", "y"],
            **intersect_selection_args(),
            peers=True,
        ),
        Toggle,
    )


def test_toggle_x_wrapper() -> None:
    check_component(
        toggle_x(
            **intersect_selection_args(),
            peers=True,
        ),
        ToggleX,
    )


def test_toggle_color_wrapper() -> None:
    check_component(
        toggle_color(
            **intersect_selection_args(),
            peers=True,
        ),
        ToggleColor,
    )


def test_nearest_x_wrapper() -> None:
    check_component(
        nearest_x(
            channels=["x", "color"],
            fields=["field1", "field2"],
            max_radius=50,
            **intersect_selection_args(),
        ),
        NearestX,
    )


def test_nearest_y_wrapper() -> None:
    check_component(
        nearest_y(
            channels=["y", "color"],
            fields=["field1", "field2"],
            max_radius=50,
            **intersect_selection_args(),
        ),
        NearestY,
    )


def test_region_wrapper() -> None:
    check_component(
        region(
            channels=["x", "y"],
            **intersect_selection_args(),
            peers=True,
            **brush_args(),
        ),
        Region,
    )


def test_toggle_y_wrapper() -> None:
    check_component(
        toggle_y(
            **intersect_selection_args(),
            peers=True,
        ),
        ToggleY,
    )


def test_pan_wrapper() -> None:
    check_component(
        pan(**pan_selection_args()),
        Pan,
    )


def test_pan_x_wrapper() -> None:
    check_component(
        pan_x(**pan_selection_args()),
        PanX,
    )


def test_pan_y_wrapper() -> None:
    check_component(
        pan_y(**pan_selection_args()),
        PanY,
    )


def test_pan_zoom_wrapper() -> None:
    check_component(
        pan_zoom(**pan_selection_args()),
        PanZoom,
    )


def test_pan_zoom_x_wrapper() -> None:
    check_component(
        pan_zoom_x(**pan_selection_args()),
        PanZoomX,
    )


def test_pan_zoom_y_wrapper() -> None:
    check_component(
        pan_zoom_y(**pan_selection_args()),
        PanZoomY,
    )