import re

import traitlets
from anywidget import AnyWidget
from pydantic_core import to_json

from .._dataframe.dataframe import DataFrame
from .._param.param import PARAM_ESCAPE, PARAM_PREFIX
from .._param.param import Param as VizParam
from .._util.constants import STATIC_DIR
from ..plot import HConcat, Plot, VConcat


class PlotWidget(AnyWidget):
    _esm = STATIC_DIR / "plot.js"
    df_id = traitlets.CUnicode("").tag(sync=True)
    plot = traitlets.CUnicode("").tag(sync=True)
    params = traitlets.CUnicode("").tag(sync=True)


def plot(df: DataFrame, plot: Plot | HConcat | VConcat) -> PlotWidget:
    # convert plot to json
    plot_json = plot.model_dump_json(by_alias=True, exclude_none=True)

    # find param references and populate params
    plot_params = extract_param_references(plot_json)
    params = {param: VizParam.get(param) for param in plot_params}
    params_json = to_json(params).decode()

    # create and return widget
    widget = PlotWidget()
    widget.df_id = df.id
    widget.plot = plot_json
    widget.params = params_json
    return widget


def extract_param_references(plot_json: str) -> list[str]:
    prefix = f"{PARAM_ESCAPE}{PARAM_PREFIX}"
    pattern = prefix + r"[0-9a-zA-Z]{22}"
    return re.findall(pattern, plot_json)
