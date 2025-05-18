import os
from os import PathLike
from typing import Any, Protocol, runtime_checkable

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


@runtime_checkable
class ReactiveDF(Protocol):
    """Reactive dataframe for use with views and inputs."""

    def query(self, sql: str | Select, **parameters: Any) -> "ReactiveDF":
        """Apply a query to this dataframe to yield another dataframe.

        Args:
            sql: SQL string or `Select` statement created via `select()`.
            **parameters: Default values for query parameters.

        Returns:
            Reactive dataframe resulting from running the specified query.
        """
        ...

    # interoperate with libraries that take the dataframe protocol
    def __dataframe__(self) -> object: ...

    # interoperate with libraries that take narwhals (e.g. plotly)
    def __narwhals_dataframe__(self) -> object: ...

    # internal: unique id
    def _id(self) -> str: ...


def reactive_df(data: IntoDataFrame | str | PathLike[str]) -> ReactiveDF:
    """Create a reactive dataframe for use with linked views and inputs.

    Pass this object to views and inputs that want to share access to it.
    Changes in inputs will flow to the dataframe causing view updates.

    Input is the path to a data file (csv, parquet, etc.) or any Python
    dataframe (the [narwhals](https://narwhals-dev.github.io/narwhals/)
    library is used to support a variety of data frame types including
    Pandas, Polars, PyArrow, Dask, DuckDB, Ibis, etc.

    Args:
        data: Path to a data file or Python dataframe object.

    Returns:
        Reactive dataframe for use in linked views and inputs.
    """
    # convert to pandas if its a path
    if isinstance(data, (str, PathLike)):
        data = _read_df_from_file(data)

    # convert to narwhals
    ndf = nw.from_native(data)

    # dataframe id
    id = uuid()

    # convert to arrow bytes to send to client/arquero
    reader = pa.ipc.RecordBatchStreamReader.from_stream(ndf)
    table = reader.read_all()
    table_buffer = pa.BufferOutputStream()
    with pa.RecordBatchStreamWriter(table_buffer, table.schema) as writer:
        writer.write_table(table)

    # create and render ReactiveDFWidget on the client
    class ReactiveDFWidget(anywidget.AnyWidget):
        _esm = STATIC_DIR / "reactive_df.js"
        id = traitlets.CUnicode("").tag(sync=True)
        buffer = traitlets.Bytes(b"").tag(sync=True)
        queries = traitlets.CUnicode("").tag(sync=True)

    # publish reactive_df to client
    def publish_reactive_df(*, queries: str = "") -> None:
        widget = ReactiveDFWidget()
        widget.id = id
        widget.buffer = table_buffer.getvalue().to_pybytes()
        widget.queries = queries
        display(widget)  # type: ignore

    publish_reactive_df()

    # return handle fo ReactiveDF
    class ReactiveDFImpl:
        def __init__(self, *, queries: list[MosaicQuery], ndf: DataFrame[Any]) -> None:
            self._ndf = ndf
            self._queries = queries

        def query(self, sql: str | Select, **parameters: Any) -> ReactiveDF:
            # parse query and add it to the stack of queries
            query = parse_sql(sql, **parameters)
            queries = self._queries + [query]

            # push to client (note that underlying ndf is the same, queries change)
            publish_reactive_df(queries=to_json(queries).decode())

            # execute the query and yield a new ndf
            ndf = execute_query(self._ndf, query)

            # return handle with updated ndf and queries
            return ReactiveDFImpl(queries=queries, ndf=ndf)

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

        def _id(self) -> str:
            return id

    return ReactiveDFImpl(queries=[], ndf=ndf)


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
