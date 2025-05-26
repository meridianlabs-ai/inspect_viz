from typing import Any

from inspect_viz._core import Data, Widget
from inspect_viz.mosaic import Table


def table(data: Data) -> Widget:
    table_args: dict[str, Any] = {"from_": data.table, "filterBy": data.selection}
    return Widget(Table(**table_args))
