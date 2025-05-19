import traitlets
from anywidget import AnyWidget

from inspect_viz._data.param import Param

from .._data.reactive_df import ReactiveDF
from .._util.constants import STATIC_DIR


def slider_input(df: ReactiveDF, column: str, param: Param | None = None) -> AnyWidget:
    df._ensure()

    class SliderInput(AnyWidget):
        _esm = STATIC_DIR / "slider_input.js"
        df_id = traitlets.CUnicode("").tag(sync=True)
        column = traitlets.CUnicode("").tag(sync=True)
        param = traitlets.CUnicode("").tag(sync=True)

    return SliderInput(df_id=df.id, column=column, param=param.id if param else "")
