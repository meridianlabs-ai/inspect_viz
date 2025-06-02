from typing import Literal

Interval = (
    Literal[
        "second",
        "minute",
        "hour",
        "day",
        "week",
        "month",
        "year",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    | float
    | int
)
