import sys
import anywidget
import plotly.graph_objects as go
import plotly.io as pio
import traitlets

from inspect_analysis._util.constants import STATIC_DIR

from ._shared_df import SharedDF


class FigureView(anywidget.AnyWidget):
    _esm = STATIC_DIR / "figure_view.js"
    _css = STATIC_DIR / "figure_view.css"
    df_id = traitlets.CUnicode("").tag(sync=True)
    figure_json = traitlets.CUnicode("").tag(sync=True)


def figure_view(df: SharedDF, fig: go.Figure) -> FigureView:
    # TODO: validate fig._data against df.columns to confirm they match

    # fig_dict = fig.to_dict()
    # fig_dict['layout']
    # fig_dict['config']
    # to_json_plotly to git into order for the client

    view = FigureView()
    view.df_id = df.id
    view.figure_json = pio.to_json(fig)
    return view
