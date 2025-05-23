import traitlets
from anywidget import AnyWidget

from inspect_viz._param.param import Param

from .._dataframe.dataframe import DataFrame
from .._dataframe.valdidate import validate_df
from .._util.constants import STATIC_DIR


def table(df: DataFrame) -> AnyWidget:
    validate_df(df)

    class TableView(AnyWidget):
        _esm = STATIC_DIR / "table.js"
        df_id = traitlets.CUnicode("").tag(sync=True)
        params = traitlets.CUnicode(Param.get_all_as_json()).tag(sync=True)

    view = TableView(df_id=df.id)
    return view
