from typing import Any, Literal, Sequence

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ._channel import Channel, ChannelSpec
from ._mark import Mark, MarkOptions
from ._types import Curve
from ._util import column_param


def area(
    data: Data,
    x1: ChannelSpec | Param,
    y1: ChannelSpec | Param,
    x2: ChannelSpec | Param | None = None,
    y2: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    curve: Curve | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """An area mark defined by a baseline (*x1*, *y1*) and a topline (*x2*, *y2*).

    The **x1** and **y1** channels specify the area's baseline; the **x2** and **y2** channels specify the area's topline. Both the baseline and topline are typically bound to the same scales as their respective dimensions.

    If **x2** is not specified, it defaults to **x1**. If **y2** is not specified, it defaults to **y1**. Typically either **x2** or **y2** is unspecified, creating either a horizontal or vertical area.

    Args:
       data: The data source for the mark.
       x1: The required primary (starting, often left) horizontal position channel, representing the area's baseline, typically bound to the *x* scale.
       x2: The optional secondary (ending, often right) horizontal position channel, representing the area's topline, typically bound to the *x* scale; if not specified, **x1** is used.
       y1: The required primary (starting, often bottom) vertical position channel, representing the area's baseline, typically bound to the *y* scale.
       y2: The optional secondary (ending, often top) vertical position channel, representing the area's topline, typically bound to the *y* scale; if not specified, **y1** is used.
       z: An optional ordinal channel for grouping data into (possibly stacked) series to be drawn as separate areas; defaults to **fill** if a channel, or **stroke** if a channel.
       filter_by: Selection to filter by (defaults to data source selection).
       offset: After stacking, an optional **offset** can be applied to translate and scale stacks, say to produce a streamgraph; defaults to null for a zero baseline (**y** = 0 for stackY, and **x** = 0 for stackX). If the *wiggle* offset is used, the default **order** changes to *inside-out*.
       order: The order in which stacks are layered; one of:

         - null (default) for input order
         - a named stack order method such as *inside-out* or *sum*
         - a field name, for natural order of the corresponding values
         - a function of data, for natural order of the corresponding values
         - an array of explicit **z** values in the desired order

         If the *wiggle* **offset** is used, as for a streamgraph, the default changes to *inside-out*.
       curve: The curve (interpolation) method for connecting adjacent points.
       options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x1=column_param(data, x1),
            x2=column_param(data, x2),
            y1=column_param(data, y1),
            y2=column_param(data, y2),
            z=column_param(data, z),
            offset=offset,
            order=order,
            curve=curve,
        )
    )

    return Mark("area", config, options)


def area_x(
    data: Data,
    x: ChannelSpec | Param,
    x1: ChannelSpec | Param | None = None,
    x2: ChannelSpec | Param | None = None,
    y: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    curve: Curve | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A horizontal area mark.

    The **x** channel specifies the area's length (or width); it is typically bound to the *x* scale. The **y** channel specifies the area's vertical position; it is typically bound to the *y* scale and defaults to the zero-based index of the data [0, 1, 2, …].

    If neither **x1** nor **x2** is specified, an implicit stackX transform is applied and **x** defaults to the identity function, assuming that *data* = [*x₀*, *x₁*, *x₂*, …]. Otherwise, if only one of **x1** or **x2** is specified, the other defaults to **x**, which defaults to zero.

    Args:
       data: The data source for the mark.
       x: The horizontal position (or length) channel, typically bound to the *x* scale. If neither **x1** nor **x2** is specified, an implicit stackX transform is applied and **x** defaults to the identity function, assuming that *data* = [*x₀*, *x₁*, *x₂*, …]. Otherwise, if only one of **x1** or **x2** is specified, the other defaults to **x**, which defaults to zero.
       x1: The required primary (starting, often left) horizontal position channel, representing the area's baseline, typically bound to the *x* scale. For areaX, setting this option disables the implicit stackX transform.
       x2: The optional secondary (ending, often right) horizontal position channel, representing the area's topline, typically bound to the *x* scale; if not specified, **x1** is used. For areaX, setting this option disables the implicit stackX transform.
       y: The vertical position channel, typically bound to the *y* scale; defaults to the zero-based index of the data [0, 1, 2, …].
       z: An optional ordinal channel for grouping data into (possibly stacked) series to be drawn as separate areas; defaults to **fill** if a channel, or **stroke** if a channel.
       filter_by: Selection to filter by (defaults to data source selection).
       offset: After stacking, an optional **offset** can be applied to translate and scale stacks, say to produce a streamgraph; defaults to null for a zero baseline (**y** = 0 for stackY, and **x** = 0 for stackX). If the *wiggle* offset is used, the default **order** changes to *inside-out*.
       order: The order in which stacks are layered; one of:

         - null (default) for input order
         - a named stack order method such as *inside-out* or *sum*
         - a field name, for natural order of the corresponding values
         - a function of data, for natural order of the corresponding values
         - an array of explicit **z** values in the desired order

         If the *wiggle* **offset** is used, as for a streamgraph, the default changes to *inside-out*.
       curve: The curve (interpolation) method for connecting adjacent points.
       options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            x1=column_param(data, x1),
            x2=column_param(data, x2),
            y=column_param(data, y),
            z=column_param(data, z),
            offset=offset,
            order=order,
            curve=curve,
        )
    )

    return Mark("areaX", config, options)


def area_y(
    data: Data,
    y: ChannelSpec | Param,
    y1: ChannelSpec | Param | None = None,
    y2: ChannelSpec | Param | None = None,
    x: ChannelSpec | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    offset: Literal["center", "normalize", "wiggle"] | Param | None = None,
    order: Literal["value", "x", "y", "z", "sum", "appearance", "inside-out"]
    | str
    | Sequence[float | bool]
    | Param
    | None = None,
    curve: Curve | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A vertical area mark.

    The **y** channel specifies the area's height (or length); it is typically bound to the *y* scale. The **x** channel specifies the area's horizontal position; it is typically bound to the *x* scale and defaults to the zero-based index of the data [0, 1, 2, …].

    If neither **y1** nor **y2** is specified, an implicit stackY transform is applied and **y** defaults to the identity function, assuming that *data* = [*y₀*, *y₁*, *y₂*, …]. Otherwise, if only one of **y1** or **y2** is specified, the other defaults to **y**, which defaults to zero.

    Args:
       data: The data source for the mark.
       y: The vertical position (or length) channel, typically bound to the *y* scale. If neither **y1** nor **y2** is specified, an implicit stackY transform is applied and **y** defaults to the identity function, assuming that *data* = [*y₀*, *y₁*, *y₂*, …]. Otherwise, if only one of **y1** or **y2** is specified, the other defaults to **y**, which defaults to zero.
       y1: The required primary (starting, often bottom) vertical position channel, representing the area's baseline, typically bound to the *y* scale. For areaY, setting this option disables the implicit stackY transform.
       y2: The optional secondary (ending, often top) vertical position channel, representing the area's topline, typically bound to the *y* scale; if not specified, **y1** is used. For areaY, setting this option disables the implicit stackY transform.
       x: The horizontal position channel, typically bound to the *x* scale; defaults to the zero-based index of the data [0, 1, 2, …].
       z: An optional ordinal channel for grouping data into (possibly stacked) series to be drawn as separate areas; defaults to **fill** if a channel, or **stroke** if a channel.
       filter_by: Selection to filter by (defaults to data source selection).
       offset: After stacking, an optional **offset** can be applied to translate and scale stacks, say to produce a streamgraph; defaults to null for a zero baseline (**y** = 0 for stackY, and **x** = 0 for stackX). If the *wiggle* offset is used, the default **order** changes to *inside-out*.
       order: The order in which stacks are layered; one of:

         - null (default) for input order
         - a named stack order method such as *inside-out* or *sum*
         - a field name, for natural order of the corresponding values
         - a function of data, for natural order of the corresponding values
         - an array of explicit **z** values in the desired order

         If the *wiggle* **offset** is used, as for a streamgraph, the default changes to *inside-out*.
       curve: The curve (interpolation) method for connecting adjacent points.
       options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            y=column_param(data, y),
            y1=column_param(data, y1),
            y2=column_param(data, y2),
            x=column_param(data, x),
            z=column_param(data, z),
            offset=offset,
            order=order,
            curve=curve,
        )
    )

    return Mark("areaY", config, options)
