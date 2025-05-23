import os
from os import PathLike
from typing import Any

import anywidget
import narwhals as nw
import pandas as pd
import pyarrow as pa
import traitlets
from IPython.display import display
from narwhals.typing import IntoDataFrame
from shortuuid import uuid

from inspect_viz._param.param import Param

from .._util.constants import STATIC_DIR


class DataFrame:
    def __init__(self, data: IntoDataFrame | str | PathLike[str]) -> None:
        # assign a unique id
        self._id = uuid()

        # convert to pandas if its a path
        if isinstance(data, (str, PathLike)):
            data = _read_df_from_file(data)

        # convert to narwhals
        self._ndf = nw.from_native(data)

        # create widget
        self._widget: DataFrameWidget | None = dataframe_widget(self._id, ndf=self._ndf)

    @property
    def id(self) -> str:
        return self._id

    @property
    def columns(self) -> list[str]:
        return self._ndf.columns

    def __str__(self) -> str:
        return self._replace_caption(self._ndf.__str__())

    def __repr__(self) -> str:
        return self._replace_caption(self._ndf.__repr__())

    def __len__(self) -> int:
        return self._ndf.__len__()

    def _replace_caption(self, text: str) -> str:
        return text.replace("Narwhals DataFrame", "     Viz Data     ")

    def _ensure(self) -> None:
        if self._widget is not None:
            display(self._widget)  # type: ignore[no-untyped-call]
            self._widget = None


def _read_df_from_file(path: str | PathLike[str]) -> pd.DataFrame:
    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext == ".csv":
        return pd.read_csv(path)
    elif ext == ".xlsx" or ext == ".xls":
        return pd.read_excel(path)
    elif ext == ".json":
        return pd.read_json(path)
    elif ext == ".parquet":
        return pd.read_parquet(path)
    elif ext == ".feather":
        return pd.read_feather(path)
    elif ext == ".sas7bdat":
        return pd.read_sas(path)
    elif ext == ".dta":
        return pd.read_stata(path)
    elif ext == ".txt" or ext == ".dat":
        # Try to guess the delimiter
        return pd.read_csv(path, sep=None, engine="python")
    elif ext == ".fwf":
        return pd.read_fwf(path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")


# create and render ReactiveDFWidget on the client
class DataFrameWidget(anywidget.AnyWidget):
    _esm = STATIC_DIR / "dataframe.js"
    id = traitlets.CUnicode("").tag(sync=True)
    buffer = traitlets.Bytes(b"").tag(sync=True)
    params = traitlets.CUnicode(Param.get_all_as_json()).tag(sync=True)


# create reactive_df_widget (will be printed on demand)
def dataframe_widget(id: str, ndf: nw.DataFrame[Any]) -> DataFrameWidget:
    # create widget
    widget = DataFrameWidget()
    widget.id = id

    # create arrow ipc buffer
    reader = pa.ipc.RecordBatchStreamReader.from_stream(ndf)
    table = reader.read_all()
    table_buffer = pa.BufferOutputStream()
    with pa.RecordBatchStreamWriter(table_buffer, table.schema) as writer:
        writer.write_table(table)
    widget.buffer = table_buffer.getvalue().to_pybytes()

    # return widget
    return widget
