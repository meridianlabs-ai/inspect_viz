from datetime import datetime
from typing import Any

import traitlets
from anywidget import AnyWidget
from pydantic_core import to_json

from .._core._data import Data
from .._core._param import Param as VizParam
from .._core._selection import Selection as VizSelection
from .._util._constants import STATIC_DIR
from ._schema.schema import Param, ParamDate, PlotAttributes, Selection
from ._types import Component, Params


class MosaicWidget(AnyWidget):
    _esm = STATIC_DIR / "mosaic.js"
    df_id = traitlets.CUnicode("").tag(sync=True)
    spec = traitlets.CUnicode("").tag(sync=True)


def mosaic(
    *,
    data: Data,
    component: Component,
    plot_defaults: PlotAttributes | None = None,
) -> MosaicWidget:
    # base spec
    spec: dict[str, Any] = component.model_dump(by_alias=True, exclude_none=True)

    # add params
    spec["params"] = mosaic_params()

    # add plot defaults
    if plot_defaults is not None:
        spec["plotDefaults"] = plot_defaults.model_dump(
            by_alias=True, exclude_none=True
        )

    # create and return widget
    widget = MosaicWidget()
    widget.df_id = data.id
    widget.spec = to_json(spec).decode()
    return widget


def mosaic_params() -> Params:
    all_params: Params = {}

    for param in VizParam.get_all():
        if isinstance(param.default, datetime):
            all_params[param.id] = ParamDate(date=param.default.isoformat())
        else:
            all_params[param.id] = Param(value=param.default)

    for selection in VizSelection.get_all():
        all_params[selection.id] = Selection(
            select=selection.select, cross=selection.cross, empty=selection.empty
        )

    return all_params
