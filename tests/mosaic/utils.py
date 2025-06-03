from typing import Any, Type

from inspect_viz import Component, Selection
from inspect_viz.interactor import Brush
from pydantic import BaseModel

from inspect_viz.mark._text import TextStyles


def check_component(component: Component, type: Type[BaseModel]) -> None:
    model = type.model_validate(component.config)
    assert model.model_dump(exclude_none=True, by_alias=True) == component.config


def basic_selection_args() -> dict[str, Any]:
    return {"filter_by": Selection("intersect")}


def intersect_selection_args() -> dict[str, Any]:
    return {"selection": Selection("intersect")}


def mark_position_args() -> dict[str, Any]:
    return {"x": "bill_depth", "y": "flipper_length", "z": "species"}


def dot_mark_args() -> dict[str, Any]:
    return {
        **mark_position_args(),
        **basic_selection_args(),
        "r": 3,
        "rotate": 45,
        "frame_anchor": "middle",
    }


def line_marker_args() -> dict[str, Any]:
    return {
        "marker": "circle",
        "marker_start": "arrow",
        "marker_mid": "dot",
        "marker_end": "arrow-reverse",
        "curve": "linear",
        "tension": 0.5,
    }


def bar_styling_args() -> dict[str, Any]:
    return {
        "interval": "minute",
        "offset": "center",
        "order": "appearance",
        "inset": 1,
        "inset_left": 1,
        "inset_right": 1,
        "inset_bottom": 1,
        "inset_top": 1,
        "rx": 1,
        "ry": 1,
        "reverse": True,
    }


def pan_selection_args() -> dict[str, Any]:
    return {
        "x": Selection("intersect"),
        "y": Selection("intersect"),
        "xfield": "x_field",
        "yfield": "y_field",
    }


def brush_args() -> dict[str, Any]:
    return {"brush": Brush(fill="red", fill_opacity=0.6)}


def interval_args() -> dict[str, Any]:
    return {
        **intersect_selection_args(),
        "pixel_size": 2,
        "peers": True,
        **brush_args(),
    }


def text_styles() -> TextStyles:
    return TextStyles(
        text_anchor="middle",
        line_height=1.2,
        line_width=20,
        text_overflow="ellipsis",
        monospace=True,
        font_family="Arial",
        font_size=12,
        font_variant="small-caps",
        font_weight=700,
    )


def text_styles_dict() -> dict[str, Any]:
    return dict(text_styles())


def text_positioning_args() -> dict[str, Any]:
    return {
        "frame_anchor": "middle",
        "line_anchor": "middle",
        "rotate": 45,
    }


def rotate_and_frame_args() -> dict[str, Any]:
    return {"rotate": 30, "frame_anchor": "bottom"}
