from .._core import Data, Param
from ..transform._column import column
from ._channel import Channel


def column_param(
    data: Data | None, param: Channel | Param | None
) -> Channel | Param | None:
    if data is not None and isinstance(param, str):
        if not isinstance(param, Param) and param not in data.columns:
            raise ValueError(f"Column '{param}' was not found in the data source.")

        return column(param)
    else:
        return param
