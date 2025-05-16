import anywidget
import plotly.graph_objects as go
import plotly.io as pio
import traitlets

from .._util.constants import STATIC_DIR
from ._shared_df import SharedDF


class FigureView(anywidget.AnyWidget):
    _esm = STATIC_DIR / "figure_view.js"
    table = traitlets.CUnicode("").tag(sync=True)
    figure_json = traitlets.CUnicode("").tag(sync=True)


def figure_view(df: SharedDF, fig: go.Figure) -> FigureView:
    # TODO: validate fig._data against df.columns to confirm they match

    view = FigureView(table=df._table, figure_json=pio.to_json(fig))
    return view
