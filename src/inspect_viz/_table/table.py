import traitlets
from anywidget import AnyWidget

from .._core._data import Data, validate_data
from .._util._constants import STATIC_DIR


def table(data: Data) -> AnyWidget:
    validate_data(data)

    class TableView(AnyWidget):
        _esm = STATIC_DIR / "table.js"
        df_id = traitlets.CUnicode("").tag(sync=True)
        selection = traitlets.CUnicode("").tag(sync=True)

    view = TableView()
    view.df_id = data.id
    view.selection = data.selection.id

    return view
