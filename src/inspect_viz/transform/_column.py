from typing import Any, Literal, Sequence

from pydantic import JsonValue

from inspect_viz._util.marshall import dict_remove_none

from .._core.param import Param
from ._transform import Transform


def bin(
    bin: str | float | bool | Param | Sequence[str | float | bool | Param],
    interval: Literal[
        "date",
        "number",
        "millisecond",
        "second",
        "minute",
        "hour",
        "day",
        "month",
        "year",
    ]
    | None,
    step: float | None = None,
    steps: float | None = None,
    minstep: float | None = None,
    nice: bool | None = None,
    offset: float | None = None,
) -> Transform:
    """Bin a continuous variable into discrete intervals.

    Args:
       bin: specifies a data column or expression to bin. Both
          numerical and temporal (date/time) values are supported.
       interval: The interval bin unit to use, typically used to
          indicate a date/time unit for binning temporal values, such
          as `hour`, `day`, or `month`. If `date`, the extent of data
          values is used to automatically select an interval for
          temporal data. The value `number` enforces normal numerical
          binning, even over temporal data. If unspecified, defaults to
          `number` for numerical data and `date` for temporal data.
       step: The step size to use between bins. When binning numerical
          values (or interval type `number`), this setting specifies the
          numerical step size. For data/time intervals, this indicates
          the number of steps of that unit, such as hours, days, or years.
       steps: The target number of binning steps to use. To accommodate
          human-friendly ("nice") bin boundaries, the actual number of bins
          may diverge from this exact value. This option is ignored when
          step is specified.
       minstep: The minimum allowed bin step size (default 0) when performing
          numerical binning. For example, a setting of 1 prevents step sizes
          less than 1. This option is ignored when step is specified.
       nice: A flag (default true) requesting "nice" human-friendly end points
          and step sizes when performing numerical binning. When step is
          specified, this option affects the binning end points (e.g., origin) only.
       offset: Offset for computed bins (default 0). For example, a value of 1
          will result in using the next consecutive bin boundary.
    """
    config: dict[str, Any] = dict_remove_none(
        dict(
            bin=bin,
            interval=interval,
            step=step,
            steps=steps,
            minstep=minstep,
            nice=nice,
            offset=offset,
        )
    )
    return Transform(config)


def column(column: str | Param) -> Transform:
    """Intpret a string or param-value as a column reference.

    Args:
       column: Column name or paramameter.
    """
    config: dict[str, JsonValue] = {"column": column}
    return Transform(config)


def date_month_day(expr: str | Param) -> Transform:
    """Map date/times to a month and day value, all within the same year for comparison.

    The resulting value is still date-typed.
    """
    config: dict[str, JsonValue] = {"dateMonthDay": expr}
    return Transform(config)


def date_day(expr: str | Param) -> Transform:
    """Transform a Date value to a day of the month for cyclic comparison.

    Year and month values are collapsed to enable comparison over days only.
    """
    config: dict[str, JsonValue] = {"dateDay": expr}
    return Transform(config)


def date_month(expr: str | Param) -> Transform:
    """Transform a Date value to a month boundary for cyclic comparison.

    Year values are collapsed to enable comparison over months only.
    """
    config: dict[str, JsonValue] = {"dateMonth": expr}
    return Transform(config)
