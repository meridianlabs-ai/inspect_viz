import traitlets
from anywidget import AnyWidget

from .._data.param import Param
from .._data.reactive_df import ReactiveDF
from .._util.constants import STATIC_DIR
from .valdidate import validate_bindings


def menu_input(df: ReactiveDF, column: str, param: Param | None = None) -> AnyWidget:
    validate_bindings(df, column, param)

    class MenuInput(AnyWidget):
        _esm = STATIC_DIR / "menu_input.js"
        df_id = traitlets.CUnicode("").tag(sync=True)
        column = traitlets.CUnicode("").tag(sync=True)
        param = traitlets.CUnicode("").tag(sync=True)

    return MenuInput(df_id=df.id, column=column, param=param.id if param else "")
