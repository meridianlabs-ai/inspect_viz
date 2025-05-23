import traitlets
from anywidget import AnyWidget

from .._data import Data, validate_bindings
from .._param.param import Param
from .._util.constants import STATIC_DIR


def menu(df: Data, column: str, param: Param | None = None) -> AnyWidget:
    validate_bindings(df, column, param)

    class MenuInput(AnyWidget):
        _esm = STATIC_DIR / "menu.js"
        df_id = traitlets.CUnicode("").tag(sync=True)
        column = traitlets.CUnicode("").tag(sync=True)
        param = traitlets.CUnicode("").tag(sync=True)
        params = traitlets.CUnicode(Param.get_all_as_json()).tag(sync=True)

    return MenuInput(df_id=df.id, column=column, param=param.id if param else "")
