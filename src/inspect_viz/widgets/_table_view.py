import anywidget
import traitlets

from .._util.constants import STATIC_DIR
from ..data.reactive_df import ReactiveDF


class TableView(anywidget.AnyWidget):
    _esm = STATIC_DIR / "table_view.js"
    table = traitlets.CUnicode("").tag(sync=True)


def table_view(df: ReactiveDF) -> TableView:
    view = TableView(table=df._table())
    return view
