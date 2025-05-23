from typing import Any

import anywidget
import narwhals as nw
import pyarrow as pa
import traitlets
from inspect_viz._constants import STATIC_DIR
from inspect_viz._param import Param


class DataWidget(anywidget.AnyWidget):
    _esm = STATIC_DIR / "data.js"
    id = traitlets.CUnicode("").tag(sync=True)
    buffer = traitlets.Bytes(b"").tag(sync=True)
    params = traitlets.CUnicode(Param.get_all_as_json()).tag(sync=True)


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
