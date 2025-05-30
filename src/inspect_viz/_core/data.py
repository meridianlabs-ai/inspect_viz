import os
from os import PathLike
from typing import ClassVar

import narwhals as nw
import pandas as pd
import pyarrow as pa
from narwhals import Boolean, String
from narwhals.typing import IntoDataFrame
from pydantic import JsonValue
from shortuuid import uuid

from .param import Param
from .selection import Selection

# data needs to be accumulated like params
# all data needs to be sent with every widget that is printed (subject to collection)
# Widget no longer takes data


class Data:
    def __init__(self, data: IntoDataFrame | str | PathLike[str]) -> None:
        # assign a unique table name
        self._table = uuid()

        # create a default selection
        self._selection = Selection(select="intersect", unique=self._table)

        # convert to pandas if its a path
        if isinstance(data, (str, PathLike)):
            data = _read_df_from_file(data)

        # convert to narwhals
        self._ndf = nw.from_native(data)

        # create buffer
        reader = pa.ipc.RecordBatchStreamReader.from_stream(self._ndf)
        table = reader.read_all()
        buffer = pa.BufferOutputStream()
        with pa.RecordBatchStreamWriter(buffer, table.schema) as writer:
            writer.write_table(table)
        self._data: bytes | None = buffer.getvalue().to_pybytes()

        # track instances
        Data._instances.append(self)

    @property
    def table(self) -> str:
        return self._table

    @property
    def selection(self) -> Selection:
        return self._selection

    def plot_from(self, filter_by: Selection | None = None) -> dict[str, JsonValue]:
        return {"from": self.table, "filterBy": filter_by or f"${self.selection.id}"}

    @property
    def columns(self) -> list[str]:
        return self._ndf.columns

    def validate_column(self, column: str | None) -> str | None:
        if column is not None and column not in self.columns:
            raise ValueError(f"The specified column '{column}' does not exist.")
        return column

    def collect_data(self) -> bytes:
        if self._data:
            buffer = self._data
            self._data = None
            return buffer
        else:
            return bytes()

    def __str__(self) -> str:
        return self._replace_caption(self._ndf.__str__())

    def __repr__(self) -> str:
        return self._replace_caption(self._ndf.__repr__())

    def __len__(self) -> int:
        return self._ndf.__len__()

    def _replace_caption(self, text: str) -> str:
        return text.replace("Narwhals DataFrame", "     Viz Data     ")

    # Class-level dictionary to store all instances
    _instances: ClassVar[list["Data"]] = []

    @classmethod
    def get_all(cls) -> list["Data"]:
        """Get all data."""
        return cls._instances.copy()


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


def validate_data(data: Data) -> None:
    # valdate type for people not using type-checkers
    if not isinstance(data, Data):
        raise TypeError(
            "Passed data is not of type vz.Data. Did you forget to wrap it in vz.Data()?"
        )


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
