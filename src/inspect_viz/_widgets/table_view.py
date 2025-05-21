import traitlets
from anywidget import AnyWidget

from .._data.dataframe import DataFrame
from .._util.constants import STATIC_DIR
from .valdidate import validate_df


def table_view(df: DataFrame) -> AnyWidget:
    validate_df(df)

    class TableView(AnyWidget):
        _esm = STATIC_DIR / "table_view.js"
        df_id = traitlets.CUnicode("").tag(sync=True)

    view = TableView(df_id=df.id)
    return view
