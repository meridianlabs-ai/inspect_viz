from narwhals import Boolean, String

from .._data.param import Param
from .._data.reactive_df import ReactiveDF


def validate_df(df: ReactiveDF) -> None:
    # valdate type for people not using type-checkers
    if not isinstance(df, ReactiveDF):
        raise TypeError(
            "Passed dataframe is not a ReactiveDF. Did you forget to wrap it in reactive_df?"
        )

    # ensure the df is on the client
    df._ensure()


def validate_bindings(df: ReactiveDF, column: str, param: Param | None = None) -> None:
    def raise_type_error(type: str) -> None:
        raise TypeError(
            f"Parameter passed for column '{column}' must be a {type} type."
        )

    # validate df and ensure it is on the client
    validate_df(df)

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
