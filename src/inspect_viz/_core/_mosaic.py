from datetime import datetime

from pydantic_core import to_json

from ..mosaic import Param, ParamDate, Selection
from ._param import Param as VizParam
from ._selection import Selection as VizSelection


def mosaic_params() -> dict[str, Param | ParamDate | Selection]:
    all_params: dict[str, Param | ParamDate | Selection] = {}

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


def mosaic_params_json() -> str:
    return to_json(mosaic_params()).decode()
