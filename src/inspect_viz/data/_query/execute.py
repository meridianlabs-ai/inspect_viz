from typing import Any

import duckdb
import narwhals as nw

from .constants import DEFAULT_TABLE
from .mosaic import MosaicQuery


def execute_query(df: nw.DataFrame[Any], query: MosaicQuery) -> nw.DataFrame[Any]:
    con = duckdb.connect(database=":memory:")
    con.register(DEFAULT_TABLE, df.to_pandas())
    parameters = {k: v.value for k, v in query.parameters.items()}
    pdf = con.execute(query.sql, parameters or None).fetch_df()
    return nw.from_native(pdf)
