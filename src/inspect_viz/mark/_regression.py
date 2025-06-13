from typing import Any

from typing_extensions import Unpack

from .._core import Data, Param, Selection
from .._util.marshall import dict_remove_none
from ._channel import Channel
from ._mark import Mark, MarkOptions
from ._util import column_param


def regression_y(
    data: Data,
    x: Channel | Param | None = None,
    y: Channel | Param | None = None,
    z: Channel | Param | None = None,
    filter_by: Selection | None = None,
    ci: float | Param | None = None,
    precision: float | Param | None = None,
    **options: Unpack[MarkOptions],
) -> Mark:
    """A vertical regression mark.

    The regressionY mark draws a regression line with optional confidence bands
    showing the relationship between variables. The x variable is the independent
    variable and y is the dependent variable.

    Args:
        data: The data source for the mark.
        x: The independent variable horizontal position channel (defaults to zero-based index).
        y: The dependent variable vertical position channel (defaults to identity function).
        z: An optional ordinal channel for grouping data into series, producing independent regressions for each group.
        filter_by: Selection to filter by (defaults to data source selection).
        ci: The confidence interval in (0, 1), or 0 to hide bands; defaults to 0.95.
        precision: The distance in pixels between samples of the confidence band; defaults to 4.
        options: Additional `MarkOptions`.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            data=data.plot_from(filter_by),
            x=column_param(data, x),
            y=column_param(data, y),
            z=column_param(data, z),
            ci=ci,
            precision=precision,
        )
    )

    return Mark("regressionY", config, options)
