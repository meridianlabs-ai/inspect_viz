import traitlets
from anywidget import AnyWidget

from .._data.reactive_df import ReactiveDF
from .._util.constants import STATIC_DIR


def table_view(df: ReactiveDF) -> AnyWidget:
    df._ensure()

    class TableView(AnyWidget):
        _esm = STATIC_DIR / "table_view.js"
        df_id = traitlets.CUnicode("").tag(sync=True)

    view = TableView(df_id=df.id)
    return view
