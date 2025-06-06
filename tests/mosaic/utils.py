from typing import Any, Type

from inspect_viz import Component, Selection
from inspect_viz.interactor import Brush
from inspect_viz.mark._text import TextStyles
from pydantic import BaseModel


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


def raster_args() -> dict[str, Any]:
    """Common raster visualization parameters."""
    return {
        "width": 50,
        "height": 40,
        "pixel_size": 2.0,
        "pad": 1.0,
        "interpolate": "linear",
        "bandwidth": 15.0,
    }


def image_args() -> dict[str, Any]:
    """Common image mark parameters."""
    return {
        "width": 50,
        "height": 40,
        "r": 25.0,
        "rotate": 45.0,
        "src": "image_url",
        "preserve_aspect_ratio": "xMidYMid meet",
        "cross_origin": "anonymous",
        "frame_anchor": "middle",
        "image_rendering": "auto",
    }


def density_args() -> dict[str, Any]:
    """Common density visualization parameters."""
    return {
        **raster_args(),
        "type": "circle",
        "symbol": "hexagon",
        "r": 4,
        "rotate": 30,
        "frame_anchor": "middle",
        "styles": text_styles(),
    }


def curve_args() -> dict[str, Any]:
    """Common curve and line styling parameters."""
    return {
        "curve": "linear",
        "tension": 0.5,
    }


def marker_args() -> dict[str, Any]:
    """Common marker parameters for lines and connections."""
    return {
        "marker": "circle",
        "marker_start": "arrow",
        "marker_mid": "dot",
        "marker_end": "arrow-reverse",
        **curve_args(),
    }


def axis_styling_args() -> dict[str, Any]:
    """Common axis styling parameters."""
    return {
        "text_stroke": "black",
        "text_stroke_opacity": 0.8,
        "text_stroke_width": 2,
        "styles": text_styles_dict(),
        "anchor": "bottom",
        "color": "blue",
        "ticks": 10,
        "tick_spacing": 50,
        "tick_size": 6,
        "tick_padding": 3,
        "tick_format": ".2f",
        "tick_rotate": 30,
        "label": "Test Label",
        "label_offset": 20,
        "label_anchor": "center",
        "label_arrow": True,
    }


def grid_styling_args() -> dict[str, Any]:
    """Common grid styling parameters."""
    return {
        "anchor": "bottom",
        "color": "lightgray",
        "ticks": 5,
        "tick_spacing": 30,
        "stroke": "gray",
        "stroke_width": 1,
        "stroke_opacity": 0.5,
        "stroke_dasharray": "2,2",
    }


def inset_args() -> dict[str, Any]:
    """Common inset parameters for rectangular marks."""
    return {
        "inset": 1,
        "inset_top": 0.5,
        "inset_right": 0.5,
        "inset_bottom": 0.5,
        "inset_left": 0.5,
        "rx": 2,
        "ry": 2,
    }


def error_bar_args() -> dict[str, Any]:
    """Common error bar parameters."""
    return {
        "ci": 0.95,
        **standard_marker_args(),
    }


def hexbin_args() -> dict[str, Any]:
    """Common hexbin parameters."""
    return {
        "bin_width": 25.0,
        "type": "hexagon",
        "r": 8.0,
        "rotate": 30.0,
        "frame_anchor": "middle",
        "styles": text_styles(),
    }


def day_interval_args() -> dict[str, Any]:
    """Common day interval parameters."""
    return {"interval": "day"}


def stacking_args() -> dict[str, Any]:
    """Common stacking parameters."""
    return {
        "offset": "center",
        "order": "appearance",
        "reverse": True,
    }


def rect_inset_args() -> dict[str, Any]:
    """Common rectangular inset parameters."""
    return {
        "inset": 2,
        "inset_top": 1,
        "inset_right": 1,
        "inset_bottom": 1,
        "inset_left": 1,
        "rx": 5,
        "ry": 3,
    }


def simple_inset_args() -> dict[str, Any]:
    """Simple inset parameters for basic marks."""
    return {
        "inset": 1,
        "rx": 2,
        "ry": 2,
    }


def waffle_args() -> dict[str, Any]:
    """Common waffle mark parameters."""
    return {
        "multiple": 10,
        "unit": 5,
        "gap": 2,
        "round": True,
        **day_interval_args(),
        **stacking_args(),
        **inset_args(),
    }


def tick_styling_args() -> dict[str, Any]:
    """Common tick mark styling."""
    return {
        **standard_marker_args(),
        **standard_inset_args(),
    }


def vector_args() -> dict[str, Any]:
    """Common vector mark parameters."""
    return {
        "r": 5,
        "length": 10,
        "rotate": 45,
        "shape": "arrow",
        "anchor": "middle",
        "frame_anchor": "middle",
    }


def arrow_args() -> dict[str, Any]:
    """Common arrow mark parameters."""
    return {
        "bend": 30.0,
        "head_angle": 45.0,
        "head_length": 10.0,
        "inset": 2.0,
        "inset_start": 1.0,
        "inset_end": 3.0,
        "sweep": 1.0,
    }


def axis_text_args() -> dict[str, Any]:
    """Common axis text styling."""
    return {
        "frame_anchor": "bottom",
        "line_anchor": "top",
        "rotate": 45,
        "text_stroke": "black",
        "text_stroke_opacity": 0.8,
        "text_stroke_width": 2,
        "styles": text_styles_dict(),
    }


def axis_tick_args() -> dict[str, Any]:
    """Common axis tick parameters."""
    return {
        "anchor": "bottom",
        "color": "blue",
        "ticks": 10,
        "tick_spacing": 50,
        "tick_size": 6,
        "tick_padding": 3,
        "tick_format": ".2f",
        "tick_rotate": 30,
    }


def axis_label_args() -> dict[str, Any]:
    """Common axis label parameters."""
    return {
        "label": "Test Label",
        "label_offset": 20,
        "label_anchor": "center",
        "label_arrow": True,
    }


def full_axis_args() -> dict[str, Any]:
    """Complete axis styling combining all components."""
    return {
        **axis_text_args(),
        **axis_tick_args(),
        **axis_label_args(),
    }


def grid_base_args() -> dict[str, Any]:
    """Base grid parameters."""
    return {
        "anchor": "bottom",
        "color": "lightgray",
        "ticks": 5,
        "tick_spacing": 30,
    }


def grid_stroke_args() -> dict[str, Any]:
    """Grid stroke styling."""
    return {
        "stroke": "gray",
        "stroke_width": 1,
        "stroke_opacity": 0.5,
        "stroke_dasharray": "2,2",
    }


def full_grid_args() -> dict[str, Any]:
    """Complete grid styling."""
    return {
        **grid_base_args(),
        **grid_stroke_args(),
    }


def area_args() -> dict[str, Any]:
    """Common area mark parameters."""
    return {
        **stacking_args(),
        "curve": "basis",
    }


def line_curve_args() -> dict[str, Any]:
    """Common line curve parameters."""
    return {
        "curve": "basis",
        "tension": 0.8,
    }


def regression_args() -> dict[str, Any]:
    """Common regression parameters."""
    return {
        "ci": 0.95,
        "precision": 4.0,
    }


def contour_args() -> dict[str, Any]:
    """Common contour parameters."""
    return {
        "thresholds": 10,
        **raster_args(),
    }


def delaunay_curve_args() -> dict[str, Any]:
    """Common delaunay curve parameters."""
    return {
        "curve": "linear",
        "tension": 0.5,
    }


def heatmap_args() -> dict[str, Any]:
    """Common heatmap parameters."""
    return {
        "width": 60,
        "height": 50,
        "pixel_size": 1.5,
        "pad": 0.0,
        "interpolate": "nearest",
        "bandwidth": 20.0,
        "image_rendering": "auto",
    }


def raster_tile_args() -> dict[str, Any]:
    """Common raster tile parameters."""
    return {
        "origin": [0.0, 0.0],
        "width": 40,
        "height": 30,
        "pixel_size": 3.0,
        "pad": 1.0,
        "interpolate": "barycentric",
        "bandwidth": 10.0,
        "image_rendering": "pixelated",
    }


def dense_line_args() -> dict[str, Any]:
    """Common dense line parameters."""
    return {
        "bandwidth": 15.0,
        "normalize": True,
        "interpolate": "linear",
        **raster_args(),
    }


def frame_args() -> dict[str, Any]:
    """Common frame parameters."""
    return {
        "anchor": "bottom",
        "inset": 5.0,
        "inset_top": 2.0,
        "inset_right": 3.0,
        "inset_bottom": 4.0,
        "inset_left": 1.0,
        "rx": 5,
        "ry": 3,
    }


def geo_args() -> dict[str, Any]:
    """Common geo mark parameters."""
    return {
        "geometry": "bill_length",
        "r": 5.0,
    }


def standard_inset_args() -> dict[str, Any]:
    """Standard inset parameters for marks."""
    return {
        "inset": 2,
        "inset_top": 1,
        "inset_bottom": 1,
    }


def full_inset_args() -> dict[str, Any]:
    """Full inset parameters with all sides and rounded corners."""
    return {
        "inset": 1,
        "inset_top": 0.5,
        "inset_right": 0.5,
        "inset_bottom": 0.5,
        "inset_left": 0.5,
        "rx": 2,
        "ry": 2,
    }


def standard_marker_args() -> dict[str, Any]:
    """Standard marker parameters for line-based marks."""
    return {
        "marker": "circle",
        "marker_start": "arrow",
        "marker_mid": "dot",
        "marker_end": "arrow-reverse",
    }
