# ParamRef is string
# ChannelValue is Channel
# ChannelValueSpec is Channel
# SortOrder is SortOrder (ignore/exclude ChannelDomainSort)

# ignore tip for now


from typing import Any, Literal, TypedDict

from pydantic import JsonValue

from .._core._component import Component
from .._core._param import Param
from .._util.casing import snake_to_camel
from .channel import Channel, SortOrder


class MarkOptions(TypedDict, total=False):
    """Shared options for all marks."""

    filter: Channel
    """Applies a transform to filter the mark’s index according to the given channel values; only truthy values are retained."""

    select: Literal[
        "first",
        "last",
        "maxX",
        "maxY",
        "minX",
        "minY",
        "nearest",
        "nearestX",
        "nearestY",
    ]
    """Applies a filter transform after data is loaded to highlight selected values only. For example, `first` and `last` select the first or last values of series only (using the *z* channel to separate series).  Meanwhile, `nearestX` and `nearestY` select the point nearest to the pointer along the *x* or *y* channel dimension. Unlike Mosaic selections, a mark level *select* is internal to the mark only, and does not populate a param or selection value to be shared across clients."""

    reverse: bool | Param
    """Applies a transform to reverse the order of the mark’s index, say for reverse input order."""

    sort: SortOrder
    """Sort order for a plot mark's index."""

    fx: Channel
    """The horizontal facet position channel, for mark-level faceting, bound to the *fx* scale"""

    fy: Channel
    """The vertical facet position channel, for mark-level faceting, bound to the *fy* scale."""

    facet: Literal["auto", "include", "exclude", "super"] | bool | None | Param
    """Whether to enable or disable faceting.

    - *auto* (default) - automatically determine if this mark should be faceted
    - *include* (or `True`) - draw the subset of the mark’s data in the current facet
    - *exclude* - draw the subset of the mark’s data *not* in the current facet
    - *super* - draw this mark in a single frame that covers all facets
    - null (or `False`) - repeat this mark’s data across all facets (*i.e.*, no faceting)

    When a mark uses *super* faceting, it is not allowed to use position scales
    (*x*, *y*, *fx*, or *fy*); *super* faceting is intended for decorations,
    such as labels and legends.

    When top-level faceting is used, the default *auto* setting is equivalent
    to *include* when the mark data is strictly equal to the top-level facet
    data; otherwise it is equivalent to null. When the *include* or *exclude*
    facet mode is chosen, the mark data must be parallel to the top-level facet
    data: the data must have the same length and order. If the data are not
    parallel, then the wrong data may be shown in each facet. The default
    *auto* therefore requires strict equality for safety, and using the
    facet data as mark data is recommended when using the *exclude* facet mode.

    When mark-level faceting is used, the default *auto* setting is equivalent
    to *include*: the mark will be faceted if either the **fx** or **fy**
    channel option (or both) is specified. The null or false option will
    disable faceting, while *exclude* draws the subset of the mark’s data *not*
    in the current facet."""

    facet_anchor: (
        Literal[
            "top",
            "right",
            "bottom",
            "left",
            "top-left",
            "top-right",
            "bottom-leftbottom-right",
            "top-empty",
            "right-empty",
            "bottom-empty",
            "left-empty",
            "empty",
        ]
        | None
        | Param
    )
    """How to place the mark with respect to facets.

    - `None` (default for most marks) - display the mark in each non-empty facet
    - *top*, *right*, *bottom*, or *left* - display the mark only in facets on the given side
    - *top-empty*, *right-empty*, *bottom-empty*, or *left-empty* (default for axis marks) - display the mark only in facets that have empty space on the given side: either the margin, or an empty facet
    - *empty* - display the mark in empty facets only
    """

    margin: float | Param
    """Shorthand to set the same default for all four mark margins."""

    margin_top: float | Param
    """The mark’s top margin."""

    margin_right: float | Param
    """The mark’s right margin."""

    margin_bottom: float | Param
    """The mark’s bottom margin."""

    margin_left: float | Param
    """The mark’s left margin."""

    aria_description: str | Param
    """ARIA description (<https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-description>)."""

    aria_hidden: str | Param
    """ARIA hidden (<https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-hidden>)."""

    aria_label: str | Param
    """ARIA label (<https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-label/>)."""

    pointer_events: str | Param
    """Pointer events (<https://developer.mozilla.org/en-US/docs/Web/CSS/pointer-events>)."""

    title: Channel
    """The title; a channel specifying accessible, short textual descriptions as strings (possibly with newlines). If the `tip` option is specified, the title will be displayed with an interactive tooltip instead of using the SVG title element."""

    tip: (
        bool
        | Literal[
            "first",
            "last",
            "maxX",
            "maxY",
            "minX",
            "minY",
            "nearest",
            "nearestX",
            "nearestY",
        ]
        | Param
    )
    """Whether to generate a tooltip for this mark."""

    channels: dict[str, str]
    """Additional named channels, for example to include in a tooltip."""

    clip: Literal["frame", "sphere"] | bool | None | Param
    """How to clip the mark.

    - *frame* or `True` - clip to the plot’s frame (inner area)
    - *sphere* - clip to the projected sphere (*e.g.*, front hemisphere)
    - `None` or `False` - do not clip

    The *sphere* clip option requires a geographic projection.
    """

    dx: float | Param
    """The horizontal offset in pixels; a constant option. On low-density screens, an additional 0.5px offset may be applied for crisp edges."""

    dy: float | Param
    """The vertical offset in pixels; a constant option. On low-density screens, an additional 0.5px offset may be applied for crisp edges."""

    fill: Channel | Param
    """A constant CSS color string, or a channel typically bound to the *color* scale. If all channel values are valid CSS colors, by default the channel will not be bound to the *color* scale, interpreting the colors literally."""

    fill_opacity: Channel | Param
    """A constant number between 0 and 1, or a channel typically bound to the *opacity* scale. If all channel values are numbers in [0, 1], by default the channel will not be bound to the *opacity* scale, interpreting the opacities literally."""

    stroke: Channel | Param
    """A constant CSS color string, or a channel typically bound to the *color* scale. If all channel values are valid CSS colors, by default the channel will not be bound to the *color* scale, interpreting the colors literally.
    """

    stroke_dasharray: str | float | Param
    """A constant number indicating the length in pixels of alternating dashes and gaps, or a constant string of numbers separated by spaces or commas (_e.g._, *10 2* for dashes of 10 pixels separated by gaps of 2 pixels), or *none* (the default) for no dashing.
    """

    stroke_dashoffset: str | float | Param
    """A constant indicating the offset in pixels of the first dash along the stroke; defaults to zero."""

    stroke_linecap: str | Param
    """A constant specifying how to cap stroked paths, such as *butt*, *round*, or *square* (<https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linecap>).
    """

    stroke_linejoin: str | Param
    """A constant specifying how to join stroked paths, such as *bevel*, *miter*, *miter-clip*, or *round* (<https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linejoin>)
    """

    stroke_miterlimit: float | Param
    """A constant number specifying how to limit the length of *miter* joins on stroked paths."""

    stroke_opacity: Channel
    """A constant between 0 and 1, or a channel typically bound to the *opacity* scale. If all channel values are numbers in [0, 1], by default the channel will not be bound to the *opacity* scale, interpreting the opacities literally."""

    stroke_width: Channel
    """A constant number in pixels, or a channel."""

    opacity: Channel
    """A constant between 0 and 1, or a channel typically bound to the *opacity* scale. If all channel values are numbers in [0, 1], by default the channel will not be bound to the *opacity* scale, interpreting the opacities literally. For faster rendering, prefer the **stroke_opacity** or **fill_opacity** option.
    """

    mix_blend_mode: str | Param
    """A constant string specifying how to blend content such as *multiply* (<https://developer.mozilla.org/en-US/docs/Web/CSS/filter>)."""

    image_filter: str | Param
    """A constant string used to adjust the rendering of images, such as *blur(5px)* (<https://developer.mozilla.org/en-US/docs/Web/CSS/filter>)."""

    paint_order: str | Param
    """A constant string specifying the order in which the * **fill**, **stroke**, and any markers are drawn; defaults to *normal*, which draws the fill, then stroke, then markers; defaults to *stroke* for the text mark to create a "halo" around text to improve legibility.
    """

    shape_rendering: str | Param
    """A constant string such as *crispEdges* (<https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/shape-rendering>)."""

    href: Channel
    """a channel specifying URLs for clickable links. May be used in conjunction with the **target** option to open links in another window."""

    target: str | Param
    """A constant string specifying the target window (_e.g. *_blank*) for clickable links; used in conjunction with the **href** option (<https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/target>)."""


class Mark(Component):
    def __init__(
        self, type: str, config: dict[str, JsonValue], options: MarkOptions
    ) -> None:
        super().__init__({"mark": type} | config | mark_options_to_camel(options))


def mark_options_to_camel(options: MarkOptions) -> dict[str, Any]:
    return {snake_to_camel(key): value for key, value in options.items()}
