from pydantic import JsonValue

from .._core.param import Param
from ._transform import Transform


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
