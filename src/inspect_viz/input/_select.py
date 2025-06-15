from typing import Any

from .._core import Component, Data, Param, Selection
from ._params import data_params, label_param, options_params


def select(
    data: Data | None = None,
    *,
    column: str | None = None,
    options: list[str] | dict[str, str] | None = None,
    target: Param | Selection | None = None,
    field: str | None = None,
    label: str | None = None,
    filter_by: Selection | None = None,
) -> Component:
    """Select input.

    Select inputs can be populated either from a database table (via the `data` and `column` parameters) or from a static set of options (via the `options` parameter).

    Select inputs have a `target` which is either a `Param` or `Selection`. In the latter case,
    the `field` parameter determines the data column name to use within generated selection
    clause predicates (defaulting to `column`). If no `target` is specified then the data
    source's selection is used as the target.

    The intitial selected value will be "All" when `target` is a `Selection` (indicating select all records) and the param value when `target` is a `Param`.

    Args:
       data: The data source for input selections (used in conjunction with the `column` parameter). If `data` is not specified, you must provide explcit `options`.
       column: The name of a column from which to pull options. The unique column values are used as options. Used in conjunction with the `data` parameter.
       options: A `list` or `dict` of options (provide a `dict` if you want values to map to alternate labels). Alternative to populating options from a database column via `data` and `column`.
       target: A `Param` or `Selection` that this select input should update. For a `Param`, the selected value is set to be the new param value. For a `Selection`, a predicate of the form column = value will be added to the selection.
       field: The data column name to use within generated selection clause predicates. Defaults to the `column` parameter.
       label: A text label for the input. If unspecified, the column name (if provided) will be used by default.
       filter_by: A selection to filter the data source indicated by the `data` parameter.
    """
    config: dict[str, Any] = {"input": "menu"}

    config = (
        config
        | label_param(label)
        | options_params(options, target)
        | data_params(data, column, target, field, filter_by)
    )

    return Component(config=config)
