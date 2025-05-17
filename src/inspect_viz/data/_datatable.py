import os
from os import PathLike
from typing import Any, Protocol

import anywidget
import narwhals as nw
import pandas as pd
import pyarrow as pa
import traitlets
from IPython.display import display
from narwhals import DataFrame
from narwhals.typing import IntoDataFrame
from pydantic_core import to_json
from shortuuid import uuid
from sqlglot.expressions import Select

from .._util.constants import STATIC_DIR
from ._query.execute import execute_query
from ._query.mosaic import MosaicQuery
from ._query.parser import parse_sql


class Datatable(Protocol):
    """Datatable for use with views and inputs."""

    def query(self, sql: str | Select, **parameters: Any) -> "Datatable":
        """Apply a query to this datatable to yield another datatable.

        Args:
            sql: SQL string or `Select` statement created via `select()`.
            **parameters: Default values for query parameters.

        Returns:
            Datatable resulting from running the specified query.
        """
        ...

    # interoperate with libraries that take the dataframe protocol
    def __dataframe__(self) -> object: ...

    # interoperate with libraries that take narwhals (e.g. plotly)
    def __narwhals_dataframe__(self) -> object: ...

    # internal: name of table on the client
    def _table(self) -> str: ...


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
    class DatatableWidget(anywidget.AnyWidget):
        _esm = STATIC_DIR / "datatable.js"
        table = traitlets.CUnicode("").tag(sync=True)
        buffer = traitlets.Bytes(b"").tag(sync=True)
        queries = traitlets.CUnicode("").tag(sync=True)

    # function so we can do it again in response to .query()
    def create_shared_df(*, table: str, queries: str = "") -> DatatableWidget:
        sdf = DatatableWidget()
        sdf.table = table
        sdf.buffer = table_buffer.getvalue().to_pybytes()
        sdf.queries = queries
        display(sdf)  # type: ignore
        return sdf

    sdf = create_shared_df(table=uuid())

    # return handle fo Datatable
    class DatatableImpl:
        def __init__(
            self, *, table: str, queries: list[MosaicQuery], ndf: DataFrame[Any]
        ) -> None:
            self._tbl = table
            self._ndf = ndf
            self._queries = queries

        def query(self, sql: str | Select, **parameters: Any) -> "Datatable":
            # parse query and add it to the stack of queries
            query = parse_sql(sql, **parameters)
            queries = self._queries + [query]

            # push to client (note that underlying ndf is the same, queries change)
            create_shared_df(table=self._tbl, queries=to_json(queries).decode())

            # execute the query and yield a new ndf
            ndf = execute_query(self._ndf, query)

            # return handle with updated ndf and queries
            return DatatableImpl(table=self._tbl, queries=queries, ndf=ndf)

        def __dataframe__(
            self,
            *,
            nan_as_null: bool = False,
            allow_copy: bool = True,
        ) -> object:
            ndf = self._ndf

            # fast-path: narwhals frame already supports the protocol
            if hasattr(ndf, "__dataframe__"):
                return ndf.__dataframe__(nan_as_null=nan_as_null, allow_copy=allow_copy)

            # try the native backend
            native = ndf.to_native()
            if hasattr(native, "__dataframe__"):
                return native.__dataframe__(
                    nan_as_null=nan_as_null, allow_copy=allow_copy
                )

            # final fallback: arrow (may involve a copy)
            if allow_copy:
                arrow_tbl = ndf.to_arrow()
                return arrow_tbl.__dataframe__(nan_as_null=nan_as_null, allow_copy=True)
            else:
                raise RuntimeError(
                    "Zero-copy __dataframe__ export is not available for this backend "
                    "and allow_copy=False was requested."
                )

        def __narwhals_dataframe__(self) -> object:
            return self._ndf._compliant_frame

        def _table(self) -> str:
            return self._tbl

    return DatatableImpl(table=sdf.table, queries=[], ndf=ndf)


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
