from typing import Any

from inspect_viz._core import Component, Data


def select(
    label: str | None = None,
    data: Data | None = None,
    *,
    column: str | None = None,
    field: str | None = None,
    param: str | None = None,
    filter_by: str | None = None,
    options: list[str] | dict[str, str] | None = None,
) -> Component:
    """Select input widget.

    Args:
       label: A text label for this input (optional).
       data: The data source for input selections (used in conjunction with the `column` property). If `data` is not specified, you must provide explcit `options`.
       column: The name of a column from which to pull options. The unique column values are used as options. Used in conjunction with the `data` property.
       field: The data column name to use within generated selection clause predicates. Defaults to the `column` property.
       param: A parameter to set with the currently selected menu option (if `param` is specified then `field` is not used).
       filter_by: A selection to filter the data source indicated by the `data` property.
       options: A `list` or `dict` of options (provide a `dict` if you want values to map to alternate labels). If `options` is not specified you must pass a `data` argument.
    """
    menu: dict[str, Any] = {"input": "menu"}

    if label is not None:
        menu["label"] = f"{label}: "

    if options is not None:
        if isinstance(options, list):
            menu["options"] = options
        else:
            menu["options"] = [dict(label=k, value=v) for k, v in options.items()]
        if param is None:
            raise ValueError("You must pass a `param` value along with `options`")
        menu["as"] = param

    elif data is not None:
        # set data table and as_
        menu["from"] = data.table
        menu["as"] = data.selection

        # validate and set column
        if column is None:
            raise ValueError("You must pass a `column` value along with `data`")
        menu["column"] = column

        # set field (optional, defaults to column)
        if field is not None:
            menu["field"] = field

        # set filter_by
        if filter_by is not None:
            menu["filterBy"] = filter_by

    # return widget
    return Component(config=menu)
