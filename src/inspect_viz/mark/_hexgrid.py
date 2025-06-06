from typing import Any

from typing_extensions import Unpack

from .._core import Param
from .._util.marshall import dict_remove_none
from ._mark import Mark, MarkOptions


def hexgrid(
    bin_width: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """Create a hexgrid mark that displays a hexagonal grid overlay.

    The hexgrid mark creates a hexagonal grid pattern, typically used as a
    background or reference grid for hexbin visualizations. This is a decoration
    mark that shows the underlying hexagonal structure without requiring data.

    The hexgrid mark is designed to complement hexbin marks by showing the grid
    structure. It's a stroke-only mark where fill is not supported.

    Args:
        bin_width: The distance between centers of neighboring hexagons, in pixels;
            defaults to 20. Should match the bin_width of any corresponding hexbin mark
            for proper alignment.
        **options: Additional mark options from MarkOptions. Note that this is a
            stroke-only mark, so fill options will not be effective.

    Returns:
        A hexgrid mark.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            binWidth=bin_width,
        )
    )

    return Mark("hexgrid", config, options)
