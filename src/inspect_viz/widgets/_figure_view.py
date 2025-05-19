import json
from typing import TypedDict, cast

import anywidget
import plotly.graph_objects as go
import plotly.io as pio
import traitlets

from .._util.constants import STATIC_DIR
from ..data.reactive_df import ReactiveDF


class FigureView(anywidget.AnyWidget):
    _esm = STATIC_DIR / "figure_view.js"
    df_id = traitlets.CUnicode("").tag(sync=True)
    figure = traitlets.CUnicode("").tag(sync=True)
    axis_mappings = traitlets.CUnicode("").tag(sync=True)


def figure_view(df: ReactiveDF, fig: go.Figure) -> FigureView:
    # TODO: validate fig._data against df.columns to confirm they match

    # return view
    return FigureView(
        df_id=df.id,
        figure=pio.to_json(fig),
        axis_mappings=json.dumps(axis_mappings(fig)),
    )


class AxisMappings(TypedDict):
    x: str | None
    y: str | None
    z: str | None


def axis_mappings(fig: go.Figure) -> AxisMappings:
    mappings = {"x": None, "y": None, "z": None}

    # Method 1: Try to get from _px_spec (modern plotly express figures)
    if hasattr(fig, "_px_spec") and fig._px_spec:
        for axis in ["x", "y", "z"]:
            if axis in fig._px_spec:
                mappings[axis] = fig._px_spec[axis]
        return cast(AxisMappings, mappings)

    # Method 2: Look at layout metadata
    for axis in ["x", "y", "z"]:
        axis_obj = getattr(fig.layout, f"{axis}axis", None)
        if axis_obj and hasattr(axis_obj, "title"):
            if hasattr(axis_obj.title, "text") and axis_obj.title.text:
                mappings[axis] = axis_obj.title.text

    # Method 3: Examine the figure data
    for trace in fig.data:
        # Check if this is a 3D trace
        is_3d = hasattr(trace, "type") and trace.type in [
            "scatter3d",
            "surface",
            "mesh3d",
        ]

        if hasattr(trace, "hovertemplate"):
            # Parse the hovertemplate to extract column names
            template = trace.hovertemplate

            for axis in ["x", "y", "z"]:
                if f"%{{{axis}}}" in template and not mappings[axis]:
                    # Try to infer from customdata or other properties
                    for prop in dir(trace):
                        if prop.startswith("custom") and prop != "customdata":
                            # e.g. customdata_x_column
                            if f"_{axis}_" in prop:
                                mappings[axis] = getattr(trace, prop)

        # For 3D plots, trace sometimes has direct access to the column names
        if is_3d:
            for axis in ["x", "y", "z"]:
                meta_key = f"{axis}_column"
                if hasattr(trace, meta_key):
                    mappings[axis] = getattr(trace, meta_key)

    return cast(AxisMappings, mappings)
