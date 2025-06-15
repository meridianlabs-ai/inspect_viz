from typing import Any

from inspect_viz._core import Data

from .._core.data import Data
from .._core.param import Param
from .._core.selection import Selection


def label_param(label: str | None) -> dict[str, Any]:
    if label is not None:
        return {"label": f"{label}: "}
    else:
        return {}


def options_params(
    options: list[str] | dict[str, str] | None = None,
    target: Param | Selection | None = None,
) -> dict[str, Any]:
    config: dict[str, Any] = {}
    if options is not None:
        if isinstance(options, list):
            config["options"] = options
        else:
            config["options"] = [dict(label=k, value=v) for k, v in options.items()]
        if target is None:
            raise ValueError("You must pass a target `Param` along with `options`")
        config["as"] = target
    return config


def column_validated(data: Data | None, column: str) -> str:
    if data is not None:
        if column not in data.columns:
            raise ValueError(f"Column '{column}' was not found in the data source.")
    return column


def data_params(
    data: Data | None = None,
    column: str | None = None,
    target: Param | Selection | None = None,
    field: str | None = None,
    filter_by: Selection | None = None,
) -> dict[str, Any]:
    config: dict[str, Any] = {}
    if data is not None:
        config["from"] = data.table

        if target is not None:
            if not isinstance(target, Selection):
                raise ValueError("The passed `target` must be of type `Selection`")
            config["as"] = target
        else:
            config["as"] = data.selection

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

    return config
