import anywidget
import traitlets

from .._util.constants import STATIC_DIR
from ._shared_df import SharedDF


class MenuInput(anywidget.AnyWidget):
    _esm = STATIC_DIR / "menu_input.js"
    table = traitlets.CUnicode("").tag(sync=True)
    column = traitlets.CUnicode("").tag(sync=True)


def menu_input(df: SharedDF, column: str) -> MenuInput:
    input = MenuInput(table=df.table, column=column)
    return input
