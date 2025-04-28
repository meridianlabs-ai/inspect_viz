from typing import Any, Protocol

import anywidget
import narwhals as nw
import pyarrow as pa  # type: ignore
import traitlets
from IPython.display import display
from narwhals import DataFrame
from narwhals.typing import IntoDataFrameT
from shortuuid import uuid

from inspect_analysis._util.constants import STATIC_DIR


class SharedDF(Protocol):
    """Shared data frame for use with client side views and inputs."""

    @property
    def id(self) -> str:
        """Unique client side id for shared data frame."""
        ...

    def __narwhals_dataframe__(self) -> object: ...


def shared_df(df: IntoDataFrameT) -> SharedDF:
    """Create a shared data frame for use with linked views and inputs.

    The data frame is synced to the client and mapped to the
    automatically genreated `id`. Pass this object to views and inputs
    that want to share access to it on the client.

    The [narwhals](https://narwhals-dev.github.io/narwhals/) library is
    used to support a variety of data frame types, so any data frame
    supported by narwhals is compatible with `shared_df()`. This includes
    Pandas, Polars, PyArrow, Dask, DuckDB, Ibis, etc.

    Args:
        df: Data frame object.

    Returns:
        Shared data frame.
    """
    # convert to narwhals
    ndf = nw.from_native(df)

    # convert to arrow bytes to send to client/arquero
    reader = pa.ipc.RecordBatchStreamReader.from_stream(ndf)
    table = reader.read_all()
    table_buffer = pa.BufferOutputStream()
    with pa.RecordBatchStreamWriter(table_buffer, table.schema) as writer:
        writer.write_table(table)

    # create and render SharedDFWidget on the client
    class SharedDFWidget(anywidget.AnyWidget):
        _esm = STATIC_DIR / "shared_df.js"
        _df_bytes = traitlets.Bytes(b"").tag(sync=True)
        _id = traitlets.CUnicode("").tag(sync=True)

    sdf = SharedDFWidget()
    sdf._id = uuid()
    sdf._df_bytes = table_buffer.getvalue().to_pybytes()
    display(sdf)  # type: ignore

    # return handle fo SharedDF
    class SharedDFImpl:
        def __init__(self, id: str, ndf: DataFrame[Any]) -> None:
            self._id = id
            self._ndf = ndf

        @property
        def id(self) -> str:
            return self._id

        def __narwhals_dataframe__(self) -> object:
            return self._ndf._compliant_frame

    return SharedDFImpl(id=sdf._id, ndf=ndf)
