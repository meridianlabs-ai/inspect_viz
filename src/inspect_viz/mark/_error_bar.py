from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ._channel import Channel
from ._mark import Mark, MarkOptions
from ._types import Marker
from ._util import column_param


def error_bar_x(
    data: Data,
    x: Channel | Param,
    y: Channel | Param | None = None,
    ci: float | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A horizontal error bar mark.

    The errorBarX mark draws horizontal error bars showing confidence intervals or uncertainty
    around data points. The error bars extend horizontally from the central value.

    Args:
        data: The data source for the mark.
        x: The dependent variable horizontal position channel (required).
        y: The independent variable vertical position channel (optional).
        ci: The confidence interval in (0, 1); defaults to 0.95.
        z: An optional ordinal channel for grouping data into series.
        filter_by: Selection to filter by (defaults to data source selection).
        marker: The marker symbol to use at all positions along the error bar.
        marker_start: The marker symbol to use at the start of the error bar.
        marker_mid: The marker symbol to use at the middle of the error bar.
        marker_end: The marker symbol to use at the end of the error bar.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            ci=ci,
            z=column_param(data, z),
            marker=marker,
            markerStart=marker_start,
            markerMid=marker_mid,
            markerEnd=marker_end,
        )
    )

    return Mark("errorbarX", config, options)


def error_bar_y(
    data: Data,
    y: Channel | Param,
    x: Channel | Param | None = None,
    ci: float | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    marker: Marker | bool | Param | None = None,
    marker_start: Marker | bool | Param | None = None,
    marker_mid: Marker | bool | Param | None = None,
    marker_end: Marker | bool | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A vertical error bar mark.

    The errorBarY mark draws vertical error bars showing confidence intervals or uncertainty
    around data points. The error bars extend vertically from the central value.

    Args:
        data: The data source for the mark.
        y: The dependent variable vertical position channel (required).
        x: The independent variable horizontal position channel (optional).
        ci: The confidence interval in (0, 1); defaults to 0.95.
        z: An optional ordinal channel for grouping data into series.
        filter_by: Selection to filter by (defaults to data source selection).
        marker: The marker symbol to use at all positions along the error bar.
        marker_start: The marker symbol to use at the start of the error bar.
        marker_mid: The marker symbol to use at the middle of the error bar.
        marker_end: The marker symbol to use at the end of the error bar.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            y=column_param(data, y),
            x=column_param(data, x),
            ci=ci,
            z=column_param(data, z),
            marker=marker,
            markerStart=marker_start,
            markerMid=marker_mid,
            markerEnd=marker_end,
        )
    )

    return Mark("errorbarY", config, options)
