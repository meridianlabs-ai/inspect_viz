import os
from os import PathLike
from typing import Any, Protocol

import anywidget
import narwhals as nw
import pandas as pd
import pyarrow as pa
import traitlets
from inspect_viz.data._query.mosaic import MosaicQuery
from inspect_viz.data._query.parser import parse_sql
from IPython.display import display
from narwhals import DataFrame
from narwhals.typing import IntoDataFrame
from shortuuid import uuid

from .._util.constants import STATIC_DIR
from ..data import Select


class Datatable(Protocol):
    """Datatable for use with views and inputs."""

    def query(self, sql: str | Select) -> "Datatable":
        """Apply a query to this datatable to yield another datatable.

        Args:
            sql: SQL string or `Select` statement created via `select()`.

        Returns:
            Datatable resulting from running the specified query.
        """
        ...

    def to_pandas(self) -> pd.DataFrame:
        """Provide a pandas representation of the datatable."""
        ...

    # internal: name of table on the client
    def _table(self) -> str: ...

    # interoperate with libraries that take narwhals (e.g. plotly)
    def __narwhals_dataframe__(self) -> object: ...


def datatable(data: IntoDataFrame | str | PathLike[str]) -> Datatable:
    """Create a datatable for use with linked views and inputs.

    Pass this object to views and inputs that want to share access to it.

    The [narwhals](https://narwhals-dev.github.io/narwhals/) library is
    used to support a variety of data frame types, so any data frame
    supported by narwhals is compatible with `datatable()`. This includes
    Pandas, Polars, PyArrow, Dask, DuckDB, Ibis, etc.

    Args:
        data: Dataframe object or path to file to read data from.

    Returns:
        Datatable for use in linked views and inputs.
    """
    # convert to pandas if its a path
    if isinstance(data, (str, PathLike)):
        data = _read_datatable_from_file(data)

    # convert to narwhals
    ndf = nw.from_native(data)

    # convert to arrow bytes to send to client/arquero
    reader = pa.ipc.RecordBatchStreamReader.from_stream(ndf)
    table = reader.read_all()
    table_buffer = pa.BufferOutputStream()
    with pa.RecordBatchStreamWriter(table_buffer, table.schema) as writer:
        writer.write_table(table)

    # create and render SharedDFWidget on the client
    class SharedDFWidget(anywidget.AnyWidget):
        _esm = STATIC_DIR / "datatable.js"
        table = traitlets.CUnicode("").tag(sync=True)
        buffer = traitlets.Bytes(b"").tag(sync=True)

    sdf = SharedDFWidget()
    sdf.table = uuid()
    sdf.buffer = table_buffer.getvalue().to_pybytes()
    display(sdf)  # type: ignore

    # return handle fo SharedDF
    class DatatableImpl:
        def __init__(
            self, table: str, ndf: DataFrame[Any], query: MosaicQuery | None
        ) -> None:
            self._tbl = table
            self._ndf = ndf

        def query(self, sql: str | Select) -> "Datatable":
            query = parse_sql(sql)
            return self

        def to_pandas(self) -> pd.DataFrame:
            return self._ndf._compliant_frame.to_pandas()

        def _table(self) -> str:
            return self._tbl

        def __narwhals_dataframe__(self) -> object:
            return self._ndf._compliant_frame

    return DatatableImpl(table=sdf.table, ndf=ndf, query=None)


def _read_datatable_from_file(path: str | PathLike[str]) -> pd.DataFrame:
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
