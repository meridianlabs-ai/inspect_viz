import hashlib
import os
from os import PathLike
from typing import Any, Union, cast

import narwhals as nw
import pandas as pd
import pyarrow as pa
from narwhals import Boolean, String
from narwhals.typing import IntoDataFrame
from pydantic import JsonValue
from shortuuid import uuid

from .._util.instances import get_instances, track_instance
from .._util.platform import quarto_immutable_target, running_in_quarto
from .param import Param
from .selection import Selection


class Data:
    """Data source for visualizations.

    Data sources can be created from any standard Python data frame (e.g. Pandas, Polars, etc.) or from a path pointing to a data file in a standard format (e.g. csv, parquet, etc.)
    """

    @classmethod
    def from_dataframe(cls, df: IntoDataFrame) -> "Data":
        """Create `Data` from a standard Python data frame (e.g. Pandas, Polars, PyArrow, etc.).

        Args:
           df: Data frame to read.
        """
        return Data(df)

    @classmethod
    def from_file(cls, file: Union[str, PathLike[str]]) -> "Data":
        """Create `Data` from a data file (e.g. csv, parquet, feather, etc.).

        Args:
           file: File to read data from. Supported formats include csv, json, xslx, parquet, feather, sas7bdat, dta, and fwf.
        """
        return Data(file)

    def __init__(self, data: Union[IntoDataFrame, str, PathLike[str]]) -> None:
        # assign a unique table name
        self._table = uuid()

        # create a default selection
        self._selection = Selection(select="intersect", unique=self._table)

        # convert to pandas if its a path
        if isinstance(data, (str, PathLike)):
            data = _read_df_from_file(data)

        # convert to narwhals
        self._ndf = nw.from_native(data)

        # serialize to an uncompressed Arrow IPC stream. DuckDB-WASM's Arrow
        # build does not include zstd/lz4 codecs, so stream-level compression
        # isn't available; we rely on HTTP transport compression for the
        # external-file path and the raw layout suffices for inline transport.
        reader = pa.ipc.RecordBatchStreamReader.from_stream(self._ndf)
        table = reader.read_all()
        buffer = pa.BufferOutputStream()
        with pa.ipc.RecordBatchStreamWriter(buffer, table.schema) as writer:
            writer.write_table(table)
        raw_bytes = buffer.getvalue().to_pybytes()

        # Under Quarto static render, write bytes to a content-hashed file
        # under the project's `<output-dir>/site_data/immutable/` (shared
        # across all docs in the site) and ship only a URL. Outside Quarto
        # keep bytes inline for live-kernel binary-buffer transport.
        self._data_url: str | None = None
        self._data: bytes = raw_bytes
        target = quarto_immutable_target() if running_in_quarto() else None
        if target is not None:
            immutable_dir, url_prefix = target
            digest = hashlib.sha256(raw_bytes).hexdigest()[:16]
            filename = f"{digest}.arrow"
            file_path = immutable_dir / filename
            if not file_path.exists():
                immutable_dir.mkdir(parents=True, exist_ok=True)
                file_path.write_bytes(raw_bytes)
            self._data_url = f"{url_prefix}{filename}"
            # NOTE: keep `self._data` populated even when a URL is written.
            # The Quarto render path prefers `_data_url` over the bytes
            # (see `_get_data` / `_collect_data`), so the bytes are never
            # embedded in the HTML — but the in-process PNG path needs them
            # to inline data into a Playwright-renderable snippet.

        # track whether we have been collected
        self._collected = False

        # track instances
        track_instance("data", self)

    @property
    def table(self) -> str:
        return self._table

    @property
    def selection(self) -> Selection:
        return self._selection

    @property
    def columns(self) -> list[str]:
        """Column names for data source."""
        return self._ndf.columns

    def column_unique(self, column: str) -> list[Any]:
        return self._ndf[column].unique().to_list()

    def column_min(self, column: str) -> Any:
        return self._ndf[column].min()

    def column_max(self, column: str) -> Any:
        return self._ndf[column].max()

    def _plot_from(self, filter_by: Selection | None = None) -> dict[str, JsonValue]:
        return {"from": self.table, "filterBy": filter_by or f"${self.selection.id}"}

    def _get_data(self) -> bytes | str:
        return self._data_url if self._data_url is not None else self._data

    def _collect_data(self) -> bytes | str:
        if not self._collected:
            self._collected = True
            return self._get_data()
        else:
            # sibling widgets get an empty payload and waitForTable on the
            # client side; shape must match the normal payload shape
            return "" if self._data_url is not None else b""

    def __str__(self) -> str:
        lines = [
            f"Viz Data ({len(self._ndf):,} rows x {len(self._ndf.columns):,} columns)",
            "-" * 80,
        ]
        for col_name, dtype in self._ndf.schema.items():
            lines.append(f"{col_name:<40} {str(dtype):<40}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return self._ndf.__len__()

    @classmethod
    def _get_all(cls) -> list["Data"]:
        """Get all data."""
        return cast(list["Data"], get_instances("data"))


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
        if dtype.is_numeric() and not param._is_numeric():
            raise_type_error("numeric")
        elif dtype.is_temporal() and not param._is_datetime():
            raise_type_error("datetime")
        elif isinstance(dtype, Boolean) and not param._is_bool():
            raise_type_error("boolean")
        elif isinstance(dtype, String) and not param._is_string():
            raise_type_error("string")
