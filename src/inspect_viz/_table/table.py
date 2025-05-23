import traitlets
from anywidget import AnyWidget

from inspect_viz._core._mosaic import mosaic_params_json

from .._core._data import Data, validate_data
from .._util._constants import STATIC_DIR


def table(data: Data) -> AnyWidget:
    validate_data(data)

    class TableView(AnyWidget):
        _esm = STATIC_DIR / "table.js"
        df_id = traitlets.CUnicode("").tag(sync=True)
        selection = traitlets.CUnicode("").tag(sync=True)
        params = traitlets.CUnicode(mosaic_params_json()).tag(sync=True)

    view = TableView()
    view.df_id = data.id
    view.selection = data.selection.id

    return view
