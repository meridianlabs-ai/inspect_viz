from typing import Any, Literal, Sequence

from typing_extensions import Unpack

from inspect_viz.transform._transform import Transform

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from .channel import Channel
from .mark import Mark, MarkOptions
from .options import Interval


def bar_x(
    data: Data,
    x: Channel | Param,
    x1: Channel | Param | None = None,
    x2: Channel | Param | None = None,
    y: Channel | Param | None = None,
    interval: Interval | None = None,
    filter_by: Selection | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    z: Channel | Param | None = None,
    inset: float | Param | None = None,
    inset_top: float | Param | None = None,
    inset_right: float | Param | None = None,
    inset_bottom: float | Param | None = None,
    inset_left: float | Param | None = None,
    rx: str | float | Param | None = None,
    ry: str | float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A horizontal bar mark.

    The required *x* values should be quantitative or temporal, and the optional *y* values should be ordinal.

    If neither **x1** nor **x2** nor **interval** is specified, an implicit stackX transform is applied and **x** defaults to the identity function, assuming that *data* = [*x₀*, *x₁*, *x₂*, …]. Otherwise if an **interval** is specified, then **x1** and **x2** are derived from **x**, representing the lower and upper bound of the containing interval, respectively. Otherwise, if only one of **x1** or **x2** is specified, the other defaults to **x**, which defaults to zero.

    The optional **y** ordinal channel specifies the vertical position; it is typically bound to the *y* scale, which must be a *band* scale. If the **y** channel is not specified, the bar will span the vertical extent of the plot’s frame.

    If *y* is quantitative, use the rectX mark instead. If *x* is ordinal, use the cell mark instead."

    Args:
       data: The data source for the mark.
       x: The horizontal position (or length/width) channel, typically bound to the *x* scale. If neither **x1** nor **x2** nor **interval** is specified, an implicit stackX transform is applied and **x** defaults to the identity function, assuming that *data* = [*x₀*, *x₁*, *x₂*, …]. Otherwise if an **interval** is specified, then **x1** and **x2** are derived from **x**, representing the lower and upper bound of the containing interval, respectively. Otherwise, if only one of **x1** or **x2** is specified, the other defaults to **x**, which defaults to zero.
       x1: The required primary (starting, often left) horizontal position channel, typically bound to the *x* scale. Setting this option disables the implicit stackX transform. If *x* represents ordinal values, use a cell mark instead.
       x2: The required secondary (ending, often right) horizontal position channel, typically bound to the *x* scale. Setting this option disables the implicit stackX transform. If *x* represents ordinal values, use a cell mark instead.
       y: The optional vertical position of the bar; a ordinal channel typically bound to the *y* scale. If not specified, the bar spans the vertical extent of the frame; otherwise the *y* scale must be a *band* scale. If *y* represents quantitative or temporal values, use a rectX mark instead.
       interval: How to convert a continuous value (**x** for barX, or **y** for barY) into an interval (**x1** and **x2** for barX, or **y1** and **y2** for barY); one of:

         - a named time interval such as *day* (for date intervals)
         - a number (for number intervals), defining intervals at integer multiples of *n*

         Setting this option disables the implicit stack transform (stackX for barX, or stackY for barY).
       filter_by: Selection to filter by (defaults to data source selection).
       offset: After stacking, an optional **offset** can be applied to translate and scale stacks, say to produce a streamgraph; defaults to null for a zero baseline (**y** = 0 for stackY, and **x** = 0 for stackX). If the *wiggle* offset is used, the default **order** changes to *inside-out*.
       order: The order in which stacks are layered; one of:

         - null (default) for input order
         - a named stack order method such as *inside-out* or *sum*
         - a field name, for natural order of the corresponding values
         - a function of data, for natural order of the corresponding values
         - an array of explicit **z** values in the desired order

         If the *wiggle* **offset** is used, as for a streamgraph, the default changes to *inside-out*.
       reverse: If true, reverse the effective order of the stacks.
       z: The **z** channel defines the series of each value in the stack. Used when the **order** is *sum*, *appearance*, *inside-out*, or an explicit array of **z** values.
       inset: Shorthand to set the same default for all four insets.
       inset_top: Insets the top edge by the specified number of pixels. A positive value insets towards the bottom edge (reducing effective area), while a negative value insets away from the bottom edge (increasing it).
       inset_right: Insets the right edge by the specified number of pixels. A positive value insets towards the left edge (reducing effective area), while a negative value insets away from the left edge (increasing it).
       inset_bottom: Insets the bottom edge by the specified number of pixels. A positive value insets towards the top edge (reducing effective area), while a negative value insets away from the top edge (increasing it).
       inset_left: Insets the left edge by the specified number of pixels. A positive value insets towards the right edge (reducing effective area), while a negative value insets away from the right edge (increasing it).
       rx: The rounded corner [*x*-radius](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/rx), either in pixels or as a percentage of the rect width. If **rx** is not specified, it defaults to **ry** if present, and otherwise draws square corners.
       ry: The rounded corner [*y*-radius][], either in pixels or as a percentage of the rect height. If **ry** is not specified, it defaults to **rx** if present, and otherwise draws square corners.
       options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=x if isinstance(x, Transform) else dict(column=x),
            x1=x1,
            x2=x2,
            y=y,
            interval=interval,
            offset=offset,
            order=order,
            z=z,
            inset=inset,
            insetTop=inset_top,
            insetRight=inset_right,
            insetBottom=inset_bottom,
            insetLeft=inset_left,
            rx=rx,
            ry=ry,
        )
    )

    return Mark("barX", config, options)
