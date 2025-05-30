from pydantic import JsonValue

from .._core.param import Param
from ._transform import Transform


def date_month_day(expr: str | Param) -> Transform:
    """Map date/times to a month and day value, all within the same year for comparison.

    The resulting value is still date-typed.
    """
    config: dict[str, JsonValue] = {"dateMonthDay": expr}
    return Transform(config)
