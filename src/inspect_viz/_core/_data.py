import os
from os import PathLike
from typing import Any

import anywidget
import narwhals as nw
import pandas as pd
import pyarrow as pa
import traitlets
from inspect_viz._core._mosaic import mosaic_params_json
from IPython.display import display
from narwhals import Boolean, String
from narwhals.typing import IntoDataFrame
from shortuuid import uuid

from .._util._constants import STATIC_DIR
from ._param import Param
from ._selection import Selection


class Data:
    def __init__(self, data: IntoDataFrame | str | PathLike[str]) -> None:
        # assign a unique id
        self._id = uuid()

        # create a default selection
        self._selection = Selection(select="intersect", unique=self._id)

        # convert to pandas if its a path
        if isinstance(data, (str, PathLike)):
            data = _read_df_from_file(data)

        # convert to narwhals
        self._ndf = nw.from_native(data)

        # create widget
        self._widget: DataWidget | None = data_widget(self._id, ndf=self._ndf)

    @property
    def id(self) -> str:
        return self._id

    @property
    def selection(self) -> Selection:
        return self._selection

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


class DataWidget(anywidget.AnyWidget):
    _esm = STATIC_DIR / "data.js"
    id = traitlets.CUnicode("").tag(sync=True)
    buffer = traitlets.Bytes(b"").tag(sync=True)
    params = traitlets.CUnicode(mosaic_params_json()).tag(sync=True)


def data_widget(id: str, ndf: nw.DataFrame[Any]) -> DataWidget:
    # create widget
    widget = DataWidget()
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


def validate_data(data: Data) -> None:
    # valdate type for people not using type-checkers
    if not isinstance(data, Data):
        raise TypeError(
            "Passed data is not of type vz.Data. Did you forget to wrap it in vz.Data()?"
        )

    # ensure the df is on the client
    data._ensure()


def validate_bindings(data: Data, column: str, param: Param | None = None) -> None:
    def raise_type_error(type: str) -> None:
        raise TypeError(
            f"Parameter passed for column '{column}' must be a {type} type."
        )

    # validate df and ensure it is on the client
    validate_data(data)

    # validate that the column in in the data frame
    dtype = data._ndf.schema.get(column, None)
    if dtype is None:
        raise ValueError(
            f"Column '{column}' does not exist in the data (expected one of {', '.join(data.columns)})."
        )

    # if a param is specified ensure that the type matches the column type
    if param is not None:
        if dtype.is_numeric() and not param.is_numeric():
            raise_type_error("numeric")
        elif dtype.is_temporal() and not param.is_datetime():
            raise_type_error("datetime")
        elif isinstance(dtype, Boolean) and not param.is_bool():
            raise_type_error("boolean")
        elif isinstance(dtype, String) and not param.is_string():
            raise_type_error("string")
