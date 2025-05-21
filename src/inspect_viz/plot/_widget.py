import traitlets
from anywidget import AnyWidget

from inspect_viz._dataframe.dataframe import DataFrame
from inspect_viz._util.constants import STATIC_DIR
from inspect_viz.plot import Plot


class PlotWidget(AnyWidget):
    _esm = STATIC_DIR / "plot.js"
    df_id = traitlets.CUnicode("").tag(sync=True)
    plot = traitlets.CUnicode("").tag(sync=True)
    params = traitlets.CUnicode("").tag(sync=True)


def plot_widget(df: DataFrame, plot: Plot) -> PlotWidget:
    plot_json = plot.model_dump_json()

    # TODO: find param references and populate params
    params_json = "[]"

    widget = PlotWidget()
    widget.df_id = df.id
    widget.plot = plot_json
    widget.params = params_json

    return widget
