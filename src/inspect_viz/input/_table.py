from typing import Literal

from pydantic import JsonValue

from inspect_viz._util.marshall import dict_remove_none
from inspect_viz.mark._util import column_validated

from .._core import Component, Data
from .._core.selection import Selection


def table(
    data: Data,
    filter_by: Selection | None = None,
    columns: list[str] | None = None,
    selection: Selection | None = None,
    align: dict[str, Literal["left", "right", "center", "justify"]] | None = None,
    width: float | dict[str, float] | None = None,
    max_width: float | None = None,
    height: float | None = None,
    row_batch: int | None = None,
) -> Component:
    """Tabular display of data.

    Args:
       data: The data source for the table.
       filter_by: Selection to filter by (defaults to data source selection).
       columns: A list of column names to include in the table grid. If unspecified, all table columns are included.
       selection: The output selection. A selection clause is added for each currently selected table row
       align: A dict of per-column alignment values. Column names should be object keys, which map to alignment values. Valid alignment values are: `"left"`, `"right"`, `"center"`, and `"justify"`. By default, numbers are right-aligned and other values are left-aligned.
       width: If a number, sets the total width of the table widget, in pixels. If an object, provides per-column pixel width values. Column names should be object keys, mapped to numeric width values.
       max_width: The maximum width of the table widget, in pixels.
       height: The height of the table widget, in pixels.
       row_batch: The number of rows load in a new batch upon table scroll.
    """
    config: dict[str, JsonValue] = dict_remove_none(
        {
            "input": "table",
            "from": data.table,
            "filterBy": filter_by or data.selection,
            "columns": [column_validated(data, c) for c in columns]
            if columns
            else None,
            "as": selection,
            "align": {column_validated(data, k): v for k, v in align.items()}
            if isinstance(align, dict)
            else align,
            "width": {column_validated(data, k): v for k, v in width.items()}
            if isinstance(width, dict)
            else width,
            "maxWidth": max_width,
            "height": height,
            "rowBatch": row_batch,
        }
    )

    return Component(config=config)
