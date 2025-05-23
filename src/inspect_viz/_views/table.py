import traitlets
from anywidget import AnyWidget

from inspect_viz._param.param import Param

from .._data import Data, validate_data
from .._util.constants import STATIC_DIR


def table(data: Data) -> AnyWidget:
    validate_data(data)

    class TableView(AnyWidget):
        _esm = STATIC_DIR / "table.js"
        df_id = traitlets.CUnicode("").tag(sync=True)
        params = traitlets.CUnicode(Param.get_all_as_json()).tag(sync=True)

    view = TableView(df_id=data.id)
    return view
