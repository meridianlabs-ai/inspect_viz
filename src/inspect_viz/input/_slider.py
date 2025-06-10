from typing import Any

from inspect_viz._util.marshall import dict_remove_none

from .._core import Component, Data, Param, Selection


def slider(
    data: Data | None = None,
    *,
    label: str | None = None,
    column: str | None = None,
    field: str | None = None,
    filter_by: str | None = None,
    selection: Selection | None = None,
    param: Param | None = None,
    value: float | None = None,
    min: float | None = None,
    max: float | None = None,
    step: float | None = None,
    width: float | None = None,
) -> Component:
    """Select input widget.

    Args:
       data: The data source for this widget. Used in conjunction with the `column` property. The minimum and maximum values of the column determine the slider range.
       label: A text label for this input (optional).
       column: The name of a database column whose values determine the slider range. Used in conjunction with the `data` property. The minimum and maximum values of the column determine the slider range.
       field: The database column name to use within generated selection clause predicates. Defaults to the `column` property.
       filter_by: A selection to filter the data source indicated by the `data` property.
       selection: A selection to target with the selected `column` or `field` (defaults to the data source selection).
       param: A parameter to set with the current slider value (if `param` is specified then `field` and `selection` parameters are not used).
       value: The initial slider value.
       min: The minumum slider value.
       max: The maximum slider value.
       step: The slider step, the amount to increment between consecutive values.
       width: The width of the slider in screen pixels.
    """
    menu: dict[str, Any] = dict_remove_none(
        {
            "input": "slider",
            "value": value,
            "min": min,
            "max": max,
            "step": step,
            "width": width,
        }
    )

    if label is not None:
        menu["label"] = f"{label}: "

    if data is not None:
        # set data table and as_
        menu["from"] = data.table
        menu["as"] = param or selection or data.selection

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
    else:
        menu["as"] = param or selection

    # return widget
    return Component(config=menu)
