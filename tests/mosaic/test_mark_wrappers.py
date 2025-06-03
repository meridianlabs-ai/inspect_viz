from inspect_viz import Component, Data
from inspect_viz.mark import (
    area,
    area_x,
    area_y,
    bar_x,
    bar_y,
    cell,
    cell_x,
    cell_y,
    circle,
    density,
    density_x,
    density_y,
    dot_x,
    dot_y,
    hexagon,
    line,
    line_x,
    line_y,
    rect,
    rect_x,
    rect_y,
    rule_x,
    rule_y,
    spike,
    text,
    text_x,
    text_y,
    tick_x,
    tick_y,
    vector,
    vector_x,
    vector_y,
    waffle_x,
    waffle_y,
)

from ._schema import (
    Area,
    AreaX,
    AreaY,
    BarX,
    BarY,
    Cell,
    CellX,
    CellY,
    Circle,
    Density,
    DensityX1,
    DensityY1,
    Dot,
    DotX,
    DotY,
    Hexagon,
    Line,
    LineX,
    LineY,
    Rect,
    RectX,
    RectY,
    RuleX,
    RuleY,
    Spike,
    Text,
    TextX,
    TextY,
    TickX,
    TickY,
    Vector,
    VectorX,
    VectorY,
    WaffleX,
    WaffleY,
)
from .utils import (
    bar_styling_args,
    basic_selection_args,
    check_component,
    line_marker_args,
    mark_position_args,
    rotate_and_frame_args,
    text_positioning_args,
    text_styles,
    text_styles_dict,
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
            **rotate_and_frame_args(),
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
            **rotate_and_frame_args(),
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
            **rotate_and_frame_args(),
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
            **rotate_and_frame_args(),
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
            **dict(text_styles_dict()),
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
            **dict(text_styles_dict()),
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
            **dict(text_styles_dict()),
        ),
        TextY,
    )


def test_density_wrapper(penguins: Data) -> None:
    check_component(
        density(
            penguins,
            x="bill_length",
            y="body_mass",
            z="species",
            **basic_selection_args(),
            type="circle",
            width=50,
            height=40,
            pixel_size=2.5,
            pad=1,
            bandwidth=15,
            interpolate="linear",
            symbol="hexagon",
            r=4,
            rotate=30,
            frame_anchor="middle",
            styles=text_styles(),
        ),
        Density,
    )


def test_density_x_wrapper(penguins: Data) -> None:
    check_component(
        density_x(
            penguins,
            y="bill_length",
            z="species",
            **basic_selection_args(),
            type="areaX",
            bandwidth=15,
        ),
        DensityX1,
    )


def test_density_y_wrapper(penguins: Data) -> None:
    check_component(
        density_y(
            penguins,
            x="bill_length",
            z="species",
            **basic_selection_args(),
            type="areaY",
            bandwidth=15,
        ),
        DensityY1,
    )


def test_rect_wrapper(penguins: Data) -> None:
    check_component(
        rect(
            penguins,
            x="bill_length",
            x1="bill_depth",
            x2="flipper_length",
            y="body_mass",
            y1="bill_length",
            y2="flipper_length",
            **basic_selection_args(),
            interval="day",
            inset=2,
            inset_top=1,
            inset_right=1,
            inset_bottom=1,
            inset_left=1,
            rx=5,
            ry=3,
            offset="center",
            order="sum",
            reverse=True,
            z="species",
        ),
        Rect,
    )


def test_rect_x_wrapper(penguins: Data) -> None:
    check_component(
        rect_x(
            penguins,
            x="bill_length",
            x1="bill_depth",
            x2="flipper_length",
            y="island",
            **basic_selection_args(),
            interval="month",
            inset=1,
            rx=2,
            ry=2,
            offset="normalize",
            order="appearance",
            z="species",
        ),
        RectX,
    )


def test_rect_y_wrapper(penguins: Data) -> None:
    check_component(
        rect_y(
            penguins,
            x="species",
            y="body_mass",
            y1="bill_length",
            y2="flipper_length",
            **basic_selection_args(),
            interval="week",
            inset=0.5,
            rx=1,
            ry=1,
            offset="wiggle",
            order="inside-out",
            reverse=False,
            z="island",
        ),
        RectY,
    )


def test_cell_wrapper(penguins: Data) -> None:
    check_component(
        cell(
            penguins,
            x="species",
            y="island",
            **basic_selection_args(),
            inset=1,
            inset_top=0.5,
            inset_right=0.5,
            inset_bottom=0.5,
            inset_left=0.5,
            rx=2,
            ry=2,
            reverse=True,
        ),
        Cell,
    )


def test_cell_x_wrapper(penguins: Data) -> None:
    check_component(
        cell_x(
            penguins,
            x="species",
            y="island",
            **basic_selection_args(),
            inset=2,
            rx=3,
            ry=1,
            reverse=False,
        ),
        CellX,
    )


def test_cell_y_wrapper(penguins: Data) -> None:
    check_component(
        cell_y(
            penguins,
            x="island",
            y="species",
            **basic_selection_args(),
            inset=1.5,
            inset_top=1,
            inset_bottom=1,
            rx=1,
            ry=1,
        ),
        CellY,
    )


def test_vector_wrapper(penguins: Data) -> None:
    check_component(
        vector(
            penguins,
            x="bill_length",
            y="body_mass",
            r=5,
            length="flipper_length",
            rotate=45,
            shape="arrow",
            anchor="middle",
            frame_anchor="middle",
            **basic_selection_args(),
        ),
        Vector,
    )


def test_vector_x_wrapper(penguins: Data) -> None:
    check_component(
        vector_x(
            penguins,
            x="bill_length",
            y="species",
            r="bill_depth",
            length=10,
            rotate=90,
            shape="spike",
            anchor="start",
            frame_anchor="left",
            **basic_selection_args(),
        ),
        VectorX,
    )


def test_vector_y_wrapper(penguins: Data) -> None:
    check_component(
        vector_y(
            penguins,
            x="island",
            y="body_mass",
            r=3,
            length="bill_depth",
            rotate=180,
            shape="arrow",
            anchor="end",
            frame_anchor="top",
            **basic_selection_args(),
        ),
        VectorY,
    )


def test_spike_wrapper(penguins: Data) -> None:
    check_component(
        spike(
            penguins,
            x="flipper_length",
            y="bill_length",
            r="body_mass",
            length=8,
            rotate=270,
            shape="spike",
            anchor="middle",
            frame_anchor="bottom",
            **basic_selection_args(),
        ),
        Spike,
    )


def test_tick_x_wrapper(penguins: Data) -> None:
    check_component(
        tick_x(
            penguins,
            x="bill_length",
            y="species",
            **basic_selection_args(),
            marker="tick",
            marker_start="arrow",
            marker_mid="dot",
            marker_end="arrow-reverse",
            inset=2,
            inset_top=1,
            inset_bottom=1,
        ),
        TickX,
    )


def test_tick_y_wrapper(penguins: Data) -> None:
    check_component(
        tick_y(
            penguins,
            y="body_mass",
            x="island",
            **basic_selection_args(),
            marker="circle",
            marker_start="tick-x",
            marker_mid="circle-fill",
            marker_end="tick-y",
            inset=1.5,
            inset_left=0.5,
            inset_right=0.5,
        ),
        TickY,
    )


def test_waffle_x_wrapper(penguins: Data) -> None:
    check_component(
        waffle_x(
            penguins,
            x="bill_length",
            x1="bill_depth",
            x2="flipper_length",
            y="species",
            z="island",
            **basic_selection_args(),
            multiple=10,
            unit=5,
            gap=2,
            round=True,
            interval="day",
            offset="center",
            order="sum",
            inset=1,
            inset_top=0.5,
            inset_right=0.5,
            inset_bottom=0.5,
            inset_left=0.5,
            rx=2,
            ry=1,
        ),
        WaffleX,
    )


def test_waffle_y_wrapper(penguins: Data) -> None:
    check_component(
        waffle_y(
            penguins,
            y="body_mass",
            y1="bill_length",
            y2="flipper_length",
            x="island",
            z="species",
            **basic_selection_args(),
            multiple=5,
            unit=2,
            gap=1,
            round=False,
            interval="month",
            offset="normalize",
            order="appearance",
            inset=2,
            rx=1,
            ry=2,
        ),
        WaffleY,
    )


def test_rule_x_wrapper(penguins: Data) -> None:
    check_component(
        rule_x(
            penguins,
            x="bill_length",
            y="species",
            **basic_selection_args(),
            interval="day",
            marker="tick",
            marker_start="arrow",
            marker_mid="dot",
            marker_end="arrow-reverse",
            inset=1,
        ),
        RuleX,
    )


def test_rule_y_wrapper(penguins: Data) -> None:
    check_component(
        rule_y(
            penguins,
            y="body_mass",
            x="island",
            **basic_selection_args(),
            interval="month",
            marker="circle",
            marker_start="tick-x",
            marker_mid="circle-fill",
            marker_end="tick-y",
            inset=2,
        ),
        RuleY,
    )
