import anywidget
import traitlets

from .._util.constants import STATIC_DIR
from ..data.reactive_df import ReactiveDF


class MenuInput(anywidget.AnyWidget):
    _esm = STATIC_DIR / "menu_input.js"
    table = traitlets.CUnicode("").tag(sync=True)
    column = traitlets.CUnicode("").tag(sync=True)


def menu_input(df: ReactiveDF, column: str) -> MenuInput:
    input = MenuInput(table=df._table(), column=column)
    return input
