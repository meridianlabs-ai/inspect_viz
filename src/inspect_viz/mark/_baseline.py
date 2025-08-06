from typing import Literal, TypedDict, cast

from typing_extensions import NotRequired

from inspect_viz._core.data import Data
from inspect_viz._core.param import Param
from inspect_viz.mark._channel import Channel
from inspect_viz.mark._mark import Mark
from inspect_viz.mark._rule import rule_x, rule_y
from inspect_viz.mark._text import text
from inspect_viz.mark._types import FrameAnchor, LineAnchor
from inspect_viz.transform._transform import Transform


def baseline(
    value: Channel,
    *,
    orientation: Literal["x", "y"] = "x",
    label: str | None = None,
    label_position: Literal["start", "middle", "end"] = "end",
    label_inset: int | float | None = None,
    color: str | None = "#000000",
    width: int | float | None = 1,
    dasharray: str | float | Param = "2,4",
    data: Data | None = None,
    filter: Transform | None = None,
) -> list[Mark]:
    """Create a plot baseline mark.

    Adds a title at the top of the plot frame.

    Args:
       value: The channel where the baseline will be positioned on the chart's scale.
       orientation: The orientation on which the value for the baseline will be drawn. Defaults to "y" for vertical baselines.
       label: The display text that appears alongside the baseline line.
       label_position: Controls where the label text appears relative to the baseline line. "top" places the label above the line, "bottom" places it below. Defaults to the "top" position.
       label_inset: The inset distance in pixels for the label from the edge of the plot frame. This argument has no effect for middle label positions.
       color: The color of the baseline line and label. Can be any valid CSS color value (hex, rgb, named colors, etc.). If None, defaults to black.
       width: The thickness of the baseline line in pixels. Defaults to 1.
       dasharray: SVG dash pattern for the line (e.g., "5,5" for dashed line, "2,3,5,3" for dash-dot pattern). Defaults to "2,4" (a dashed line).
       data: The data source for the baseline mark. If None, the baseline will not be bound to any data.
       filter: A Transform to filter the data used for the baseline. If None, no filtering is applied.
    """
    """Generate baseline marks from a list of Baseline dictionaries."""
    # Prepare the baseline marks
    components = []

    # resolve the baseline itself
    baseline_line = (
        rule_x(
            data,
            x=value,
            stroke=color,
            stroke_dasharray=dasharray,
            stroke_width=width,
            filter=filter,
        )
        if orientation == "x"
        else rule_y(
            data,
            y=value,
            stroke=color,
            stroke_dasharray=dasharray,
            stroke_width=width,
            filter=filter,
        )
    )
    components.append(baseline_line)

    # resolve the baseline label
    if label is not None:
        # resolve the label position
        anchor = label_anchoring(
            orientation=orientation,
            label_position=label_position,
            label_inset=label_inset,
        )

        # create the label text mark
        baseline_label = text(
            data,
            x=value if orientation == "x" else None,
            y=value if orientation == "y" else None,
            frame_anchor=anchor["frame"],
            line_anchor=anchor["line"],
            dy=anchor.get("dy", 0),
            dx=anchor.get("dx", 3),
            text=[label],
            fill=color,
            rotate=anchor.get("rotate", 0),
            filter=filter,
        )

        components.append(baseline_label)
    return components


class LabelAnchor(TypedDict):
    """Label anchor configuration for baseline labels."""

    frame: FrameAnchor
    line: LineAnchor
    dx: NotRequired[int | float]
    dy: NotRequired[int | float]
    rotate: NotRequired[int | float]


def label_anchoring(
    orientation: Literal["x", "y"] = "y",
    label_position: Literal["start", "middle", "end"] = "start",
    label_inset: int | float | None = None,
) -> LabelAnchor:
    """Resolve the anchor position."""
    if orientation == "x":
        frame_mapping = {
            "start": "top",
            "middle": "middle",
            "end": "bottom",
        }
        frame = cast(FrameAnchor, frame_mapping[label_position])
        line: LineAnchor = "bottom"
        dy = label_inset or (30 if label_position == "start" else -30)
        return {"frame": frame, "line": line, "dy": dy, "rotate": 90, "dx": 3}
    else:
        frame_mapping = {
            "start": "left",
            "middle": "middle",
            "end": "right",
        }
        frame = cast(FrameAnchor, frame_mapping[label_position])
        line = "bottom"
        dx = label_inset or (-5 if label_position != "start" else 5)
        return {"frame": frame, "line": line, "dx": dx, "dy": -3}
