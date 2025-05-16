import anywidget
import traitlets

from .._util.constants import STATIC_DIR
from ._shared_df import SharedDF


class TableView(anywidget.AnyWidget):
    _esm = STATIC_DIR / "table_view.js"
    table = traitlets.CUnicode("").tag(sync=True)


def table_view(df: SharedDF) -> TableView:
    view = TableView(table=df._table())
    return view
