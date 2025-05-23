import re

import traitlets
from anywidget import AnyWidget

from .._dataframe.dataframe import DataFrame
from .._param.param import Param
from .._util.constants import STATIC_DIR
from ..plot import HConcat, Plot, VConcat


class PlotWidget(AnyWidget):
    _esm = STATIC_DIR / "plot.js"
    df_id = traitlets.CUnicode("").tag(sync=True)
    plot = traitlets.CUnicode("").tag(sync=True)
    params = traitlets.CUnicode(Param.get_all_as_json()).tag(sync=True)


def plot(df: DataFrame, plot: Plot | HConcat | VConcat) -> PlotWidget:
    # convert plot to json
    plot_json = plot.model_dump_json(by_alias=True, exclude_none=True)

    # create and return widget
    widget = PlotWidget()
    widget.df_id = df.id
    widget.plot = plot_json
    return widget
