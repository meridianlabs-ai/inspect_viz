import os
from os import PathLike
from typing import Any, Protocol, runtime_checkable

import anywidget
import duckdb
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
from .constants import DEFAULT_TABLE
from .parse_sql import parse_sql
from .query import MosaicQuery


@runtime_checkable
class ReactiveDF(Protocol):
    """Reactive dataframe for use with views and inputs."""

    @property
    def id(self) -> str:
        """Unique identifier for dataframe."""
        ...

    @property
    def columns(self) -> list[str]:
        """Column names for dataframe."""
        ...

    def query(self, sql: str | Select) -> "ReactiveDF":
        """Apply a query to this dataframe to yield another dataframe.

        Args:
            sql: SQL string or `Select` statement created via `select()`.

        Returns:
            Reactive dataframe resulting from running the specified query.
        """
        ...

    # interoperate with libraries that take the dataframe protocol
    def __dataframe__(self) -> object: ...

    # interoperate with libraries that take narwhals (e.g. plotly)
    def __narwhals_dataframe__(self) -> object: ...


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

    # dataframe source id (all derivative dataframes will also carry this)
    source_id = uuid()

    # create and render ReactiveDFWidget on the client
    class ReactiveDFWidget(anywidget.AnyWidget):
        _esm = STATIC_DIR / "reactive_df.js"
        id = traitlets.CUnicode("").tag(sync=True)
        source_id = traitlets.CUnicode("").tag(sync=True)
        buffer = traitlets.Bytes(b"").tag(sync=True)
        queries = traitlets.CUnicode("").tag(sync=True)

    # publish reactive_df to client
    def publish_reactive_df(*, id: str | None = None, queries: str = "") -> None:
        # create widget
        widget = ReactiveDFWidget()
        widget.id = id or source_id
        widget.source_id = source_id
        widget.queries = queries

        # include arrow ipc buffer if this is the source data
        if id is None:
            # convert to arrow bytes
            reader = pa.ipc.RecordBatchStreamReader.from_stream(ndf)
            table = reader.read_all()
            table_buffer = pa.BufferOutputStream()
            with pa.RecordBatchStreamWriter(table_buffer, table.schema) as writer:
                writer.write_table(table)
            widget.buffer = table_buffer.getvalue().to_pybytes()

        # push to client
        display(widget)  # type: ignore

    publish_reactive_df()

    # return handle fo ReactiveDF
    class ReactiveDFImpl:
        def __init__(
            self, *, id: str, queries: list[MosaicQuery], ndf: DataFrame[Any]
        ) -> None:
            self._id = id
            self._queries = queries
            self._ndf = ndf

        @property
        def id(self) -> str:
            return self._id

        @property
        def columns(self) -> list[str]:
            return self._ndf.columns

        def query(self, sql: str | Select) -> ReactiveDF:
            # parse query and add it to the stack of queries
            query = parse_sql(sql)
            queries = self._queries + [query]

            # allocate a new id
            id = uuid()

            # push to client
            publish_reactive_df(id=id, queries=to_json(queries).decode())

            # execute the query and yield a new ndf
            ndf = execute_query(self._ndf, query)

            # return handle with updated ndf and queries
            return ReactiveDFImpl(id=id, queries=queries, ndf=ndf)

        def __str__(self) -> str:
            return self._replace_caption(self._ndf.__str__())

        def __repr__(self) -> str:
            return self._replace_caption(self._ndf.__repr__())

        def __len__(self) -> int:
            return self._ndf.__len__()

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

        def _replace_caption(self, text: str) -> str:
            return text.replace("Narwhals DataFrame", "Reactive Dataframe")

    return ReactiveDFImpl(id=source_id, queries=[], ndf=ndf)


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


def execute_query(df: nw.DataFrame[Any], query: MosaicQuery) -> nw.DataFrame[Any]:
    con = duckdb.connect(database=":memory:")
    con.register(DEFAULT_TABLE, df.to_pandas())
    parameters = {k: v.value for k, v in query.parameters.items()}
    pdf = con.execute(query.sql, parameters or None).fetch_df()
    return nw.from_native(pdf)
