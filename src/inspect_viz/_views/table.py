import traitlets
from anywidget import AnyWidget

from .._dataframe.dataframe import DataFrame
from .._dataframe.valdidate import validate_df
from .._util.constants import STATIC_DIR


def table(df: DataFrame) -> AnyWidget:
    validate_df(df)

    class TableView(AnyWidget):
        _esm = STATIC_DIR / "table.js"
        df_id = traitlets.CUnicode("").tag(sync=True)

    view = TableView(df_id=df.id)
    return view
