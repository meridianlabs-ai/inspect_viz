from inspect_viz import Component, Data
from inspect_viz.mark import (
    area,
    area_x,
    area_y,
    bar_x,
    bar_y,
    circle,
    dot,
    dot_x,
    dot_y,
    hexagon,
    line,
    line_x,
    line_y,
    text,
    text_x,
    text_y,
)

from ._schema import (
    Area,
    AreaX,
    AreaY,
    BarX,
    BarY,
    Circle,
    Dot,
    DotX,
    DotY,
    Hexagon,
    Line,
    LineX,
    LineY,
    Text,
    TextX,
    TextY,
)
from .utils import (
    basic_selection_args,
    bar_styling_args,
    check_component,
    line_marker_args,
    mark_position_args,
    text_font_args,
    text_positioning_args,
)


def test_dot_wrapper(dot_mark: Component) -> None:
    check_component(dot_mark, Dot)


def test_dot_x_wrapper(penguins: Data) -> None:
    check_component(
        dot_x(
            penguins,
            x="bill_depth",
            z="species",
            r=5,
            interval="day",
            symbol="circle",
            **basic_selection_args(),
            **{"rotate": 45, "frame_anchor": "middle"},
        ),
        DotX,
    )


def test_dot_y_wrapper(penguins: Data) -> None:
    check_component(
        dot_y(
            penguins,
            y="flipper_length",
            z="species",
            r=3,
            interval="month",
            symbol="square",
            **basic_selection_args(),
            **{"rotate": 90, "frame_anchor": "top"},
        ),
        DotY,
    )


def test_circle_wrapper(penguins: Data) -> None:
    check_component(
        circle(
            penguins,
            r=4,
            **mark_position_args(),
            **basic_selection_args(),
            **{"rotate": 30, "frame_anchor": "bottom"},
        ),
        Circle,
    )


def test_hexagon_wrapper(penguins: Data) -> None:
    check_component(
        hexagon(
            penguins,
            x="bill_length",
            y="body_mass",
            z="species",
            r=6,
            **basic_selection_args(),
            **{"rotate": 60, "frame_anchor": "left"},
        ),
        Hexagon,
    )


def test_line_wrapper(penguins: Data) -> None:
    check_component(
        line(
            penguins,
            **mark_position_args(),
            **basic_selection_args(),
            **line_marker_args(),
        ),
        Line,
    )


def test_line_x_wrapper(penguins: Data) -> None:
    check_component(
        line_x(
            penguins,
            **mark_position_args(),
            **basic_selection_args(),
            marker="circle-fill",
            marker_start="tick",
            marker_mid="circle",
            marker_end="tick-x",
            curve="basis",
            tension=0.8,
        ),
        LineX,
    )


def test_line_y_wrapper(penguins: Data) -> None:
    check_component(
        line_y(
            penguins,
            y="body_mass",
            x="bill_length",
            z="species",
            **basic_selection_args(),
            marker="circle-stroke",
            marker_start="dot",
            marker_mid="tick-y",
            marker_end="circle-fill",
            curve="cardinal",
            tension=0.3,
        ),
        LineY,
    )


def test_bar_x_wrapper(penguins: Data) -> None:
    check_component(
        bar_x(
            penguins,
            x="bill_depth",
            x1="bill_depth",
            x2="bill_depth",
            y="bill_depth",
            z="bill_depth",
            **basic_selection_args(),
            **bar_styling_args(),
        ),
        BarX,
    )


def test_bar_y_wrapper(penguins: Data) -> None:
    check_component(
        bar_y(
            penguins,
            y="bill_depth",
            y1="bill_depth",
            y2="bill_depth",
            x="bill_depth",
            z="bill_depth",
            **basic_selection_args(),
            **bar_styling_args(),
        ),
        BarY,
    )


def test_area_wrapper(penguins: Data) -> None:
    check_component(
        area(
            penguins,
            x1="bill_depth",
            y1="flipper_length",
            x2="bill_length",
            y2="body_mass",
            z="species",
            **basic_selection_args(),
            offset="center",
            order="appearance",
            curve="basis",
            reverse=True,
        ),
        Area,
    )


def test_area_x_wrapper(penguins: Data) -> None:
    check_component(
        area_x(
            penguins,
            x="bill_depth",
            x1="bill_depth",
            x2="bill_length",
            y="flipper_length",
            z="species",
            **basic_selection_args(),
            offset="center",
            order="appearance",
            curve="linear",
            reverse=True,
        ),
        AreaX,
    )


def test_area_y_wrapper(penguins: Data) -> None:
    check_component(
        area_y(
            penguins,
            y="bill_depth",
            y1="bill_depth",
            y2="bill_length",
            x="flipper_length",
            z="species",
            **basic_selection_args(),
            offset="center",
            order="appearance",
            curve="monotone-y",
            reverse=True,
        ),
        AreaY,
    )


def test_text_wrapper(penguins: Data) -> None:
    check_component(
        text(
            penguins,
            text="species",
            **mark_position_args(),
            **basic_selection_args(),
            **text_positioning_args(),
            **text_font_args(),
        ),
        Text,
    )


def test_text_x_wrapper(penguins: Data) -> None:
    check_component(
        text_x(
            penguins,
            text="species",
            interval="day",
            **mark_position_args(),
            **basic_selection_args(),
            frame_anchor="top",
            line_anchor="top",
            rotate=90,
            text_anchor="start",
            line_height=1.5,
            line_width=15,
            text_overflow="clip",
            monospace=False,
            font_family="Helvetica",
            font_size=14,
            font_variant="normal",
            font_weight=400,
        ),
        TextX,
    )


def test_text_y_wrapper(penguins: Data) -> None:
    check_component(
        text_y(
            penguins,
            y="body_mass",
            x="bill_length",
            z="species",
            text="island",
            interval="month",
            **basic_selection_args(),
            frame_anchor="left",
            line_anchor="bottom",
            rotate=180,
            text_anchor="end",
            line_height=1.0,
            line_width=25,
            text_overflow="clip",
            monospace=True,
            font_family="monospace",
            font_size=10,
            font_variant="tabular-nums",
            font_weight=400,
        ),
        TextY,
    )