from typing import Any, Literal

from inspect_viz._util.marshall import dict_remove_none

from .._core import Component, Data, Param, Selection


def slider(
    data: Data | None = None,
    *,
    filter_by: str | None = None,
    label: str | None = None,
    column: str | None = None,
    field: str | None = None,
    selection: Selection | None = None,
    select: Literal["point", "interval"] | None = None,
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
       filter_by: A selection to filter the data source indicated by the `data` property.
       label: A text label for this input (optional).
       column: The name of a database column whose values determine the slider range. Used in conjunction with the `data` property. The minimum and maximum values of the column determine the slider range.
       field: The database column name to use within generated selection clause predicates. Defaults to the `column` property.
       selection: A selection to target with the selected `column` or `field` (defaults to the data source selection).
       select: The type of selection clause predicate to generate when `selection` is specified. If `'point'` (the default), the selection predicate is an equality check for the slider value. If `'interval'`, the predicate checks an interval from the minimum to the current slider value.
       param: A parameter to set with the current slider value (if `param` is specified then `field`, `selection`, and `select` are ignored.
       value: The initial slider value.
       min: The minumum slider value.
       max: The maximum slider value.
       step: The slider step, the amount to increment between consecutive values.
       width: The width of the slider in screen pixels.
    """
    config: dict[str, Any] = dict_remove_none(
        {
            "input": "slider",
            "select": select,
            "value": value,
            "min": min,
            "max": max,
            "step": step,
            "width": width,
        }
    )

    if label is not None:
        config["label"] = f"{label}: "

    if data is not None:
        # set data table and as_
        config["from"] = data.table
        config["as"] = param or selection or data.selection

        # validate and set column
        if column is None:
            raise ValueError("You must pass a `column` value along with `data`")
        config["column"] = column

        # set field (optional, defaults to column)
        if field is not None:
            config["field"] = field

        # set filter_by
        if filter_by is not None:
            config["filterBy"] = filter_by
    else:
        config["as"] = param or selection

    # return widget
    return Component(config=config)
