from narwhals import Boolean, String

from .._data.dataframe import DataFrame
from .._data.param import Param


def validate_df(df: DataFrame) -> None:
    # valdate type for people not using type-checkers
    if not isinstance(df, DataFrame):
        raise TypeError(
            "Passed dataframe is not an Inspect Viz DataFrame. Did you forget to call vz.dataframe()?"
        )

    # ensure the df is on the client
    df._ensure()


def validate_bindings(df: DataFrame, column: str, param: Param | None = None) -> None:
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
