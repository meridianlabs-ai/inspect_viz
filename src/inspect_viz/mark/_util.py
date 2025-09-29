from typing import Any

import pandas as pd
from pydantic import JsonValue

from .._core import Data, Param
from ..transform._column import column
from ._channel import ChannelIntervalSpec
from ._mark import Mark, Marks
from ._options import MarkOptions


def column_param(
    data: Data | None, param: ChannelIntervalSpec | Param | None
) -> ChannelIntervalSpec | Param | None:
    if data is not None and isinstance(param, str):
        if not isinstance(param, Param) and param not in data.columns:
            raise ValueError(f"Column '{param}' was not found in the data source.")

        return column(param)
    else:
        return param


def tip_mark(type: str, config: dict[str, JsonValue], options: MarkOptions) -> Mark:
    return Mark(type, config, options, {"tip": True})


def flatten_marks(marks: Marks | None) -> list[Mark]:
    if marks is None:
        return []
    if isinstance(marks, Mark):
        return [marks]

    # Handle list case
    result = []
    for item in marks:
        if isinstance(item, Mark):
            result.append(item)
        else:
            result.extend(item)
    return result


def args_to_data(args: dict[str, Any]) -> Data:
    """Turns a dictionary of key-value pairs into a data object. Key-value pairs with value None are ignored.

    Args:
        args: Dictionary of key-value pairs (e.g., {"x": [0, 1, 2], "y": [0, 1, 2]}).
    """
    return Data.from_dataframe(
        pd.DataFrame({k: v for k, v in args.items() if v is not None})
    )


def check_column_names(data: Data, column_names: list[str]) -> list[str | None]:
    """Checks if column names are in the data source.

    Returns a list of column names that are in the data source in the same order as the input column names.
    If a column name is not in the data source, it is returned as None.

    Args:
        data: The data source to check the column names against.
        column_names: The column names to check against the data source.
    """
    return [col if col in data.columns else None for col in column_names]
