from typing import Any, Literal

from inspect_viz._core.param import Param

from .._core import Component, Data, Selection
from ._params import column_validated


def search(
    data: Data,
    *,
    filter_by: str | None = None,
    type: Literal["contains", "prefix", "suffix", "regexp"] | None = None,
    label: str | None = None,
    column: str | None = None,
    field: str | None = None,
    selection: Selection | None = None,
    param: Param | None = None,
) -> Component:
    """Text search input widget

    Args:
       data: The data source for input selections (used in conjunction with the `column` property).
       filter_by: A selection to filter the data source indicated by the `data` property.
       type: The type of text search query to perform. One of:
          - `"contains"` (default): the query string may appear anywhere in the text
          - `"prefix"`: the query string must appear at the start of the text
          - `"suffix"`: the query string must appear at the end of the text
          - `"regexp"`: the query string is a regular expression the text must match
       label: A text label for this input (optional).
       column: TThe name of a database column from which to pull valid search results. The unique column values are used as search autocomplete values. Used in conjunction with the `data` property.
       field: The data column name to use within generated selection clause predicates. Defaults to the `column` property.
       selection: The output selection. A selection clause is added for the current text search query. Defaults to the data source selection.
       param: A parameter to set with the current search value (if `param` is specified then `field` and `selection` are ignored.
    """
    config: dict[str, Any] = {"input": "search"}

    if label is not None:
        config["label"] = f"{label}: "

    if type is not None:
        config["type"] = type

    # set data table and as_
    config["from"] = data.table
    config["as"] = param or selection or data.selection

    # validate and set column
    if column is None:
        raise ValueError("You must pass a `column` value along with `data`")
    config["column"] = column_validated(data, column)

    # set field (optional, defaults to column)
    if field is not None:
        config["field"] = column_validated(data, field)

    # set filter_by
    if filter_by is not None:
        config["filterBy"] = filter_by

    # return widget
    return Component(config=config)
