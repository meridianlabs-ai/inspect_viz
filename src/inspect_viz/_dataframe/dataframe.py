import os
from os import PathLike
from typing import Any, Optional

import anywidget
import duckdb
import narwhals as nw
import pandas as pd
import pyarrow as pa
import traitlets
from IPython.display import display
from narwhals.typing import IntoDataFrame
from pydantic_core import to_json
from shortuuid import uuid
from sqlglot.expressions import Select

from .._util.constants import STATIC_DIR
from .constants import DEFAULT_TABLE
from .parse_sql import parse_sql
from .query import MosaicQuery


class DataFrame:
    def __init__(self, data: IntoDataFrame | str | PathLike[str]) -> None:
        # convert to pandas if its a path
        if isinstance(data, (str, PathLike)):
            data = _read_df_from_file(data)

        # convert to narwhals
        self._ndf = nw.from_native(data)

        # bind members
        id = uuid()
        self._bind(
            id=id,
            queries=[],
            widget=dataframe_widget(source_id=id, ndf=self._ndf),
        )

    def _bind(
        self,
        id: str,
        queries: list[MosaicQuery],
        widget: "DataFrameWidget",
        parent: Optional["DataFrame"] = None,
    ) -> None:
        self._id = id
        self._queries = queries
        self._widget: DataFrameWidget | None = widget
        self._parent = parent

    @property
    def id(self) -> str:
        return self._id

    @property
    def columns(self) -> list[str]:
        return self._ndf.columns

    @property
    def schema(self) -> nw.Schema:
        """Schema for dataframe."""
        return self._ndf.schema

    def query(self, sql: str | Select) -> "DataFrame":
        # parse query and add it to the stack of queries
        query = parse_sql(sql)
        queries = self._queries + [query]

        # create widget
        id = uuid()
        widget = dataframe_widget(
            source_id=self._id, id=id, ndf=self._ndf, queries=to_json(queries).decode()
        )

        # execute the query and yield a new ndf
        ndf = _execute_query(self._ndf, query)

        # return handle with updated ndf and queries
        df = DataFrame(ndf)
        df._bind(id=id, queries=queries, widget=widget, parent=self)
        return df

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
            return native.__dataframe__(nan_as_null=nan_as_null, allow_copy=allow_copy)

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
        return text.replace("Narwhals DataFrame", "Reactive DataFrame")

    def _ensure(self) -> None:
        if self._widget is not None:
            if self._parent is not None:
                self._parent._ensure()
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
    source_id = traitlets.CUnicode("").tag(sync=True)
    buffer = traitlets.Bytes(b"").tag(sync=True)
    queries = traitlets.CUnicode("").tag(sync=True)


# create reactive_df_widget (will be printed on demand)
def dataframe_widget(
    *,
    source_id: str,
    id: str | None = None,
    ndf: nw.DataFrame[Any],
    queries: str = "",
) -> DataFrameWidget:
    # create widget
    widget = DataFrameWidget()
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

    # return widget
    return widget


def _execute_query(df: nw.DataFrame[Any], query: MosaicQuery) -> nw.DataFrame[Any]:
    con = duckdb.connect(database=":memory:")
    con.register(DEFAULT_TABLE, df.to_pandas())
    parameters = {k: v.default for k, v in query.parameters.items()}
    pdf = con.execute(query.sql, parameters or None).fetch_df()
    return nw.from_native(pdf)
