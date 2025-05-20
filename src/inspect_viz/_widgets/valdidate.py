from narwhals import Boolean, String

from .._data.param import Param
from .._data.reactive_df import ReactiveDF


def validate_bindings(df: ReactiveDF, column: str, param: Param | None = None) -> None:
    def raise_type_error(type: str) -> None:
        raise TypeError(
            f"Parameter passed for column '{column}' must be a {type} type."
        )

    # ensure the df is on the client
    df._ensure()

    # validate that the column in in the data frame
    dtype = df.schema.get(column, None)
    if dtype is None:
        raise ValueError(
            f"Column '{column}' does not exist in the dataframe (expected one of {', '.join(df.columns)})."
        )

    # if a param is specified ensure that the type matches the column type
    if param is not None:
        if dtype.is_numeric() and not param.is_numeric():
            raise_type_error("numeric")
        elif isinstance(dtype, Boolean) and not param.is_bool():
            raise_type_error("boolean")
        elif isinstance(dtype, String) and not param.is_string():
            raise_type_error("string")
