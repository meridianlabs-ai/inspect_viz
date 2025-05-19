from sqlglot.expressions import ExpOrStr, Select
from sqlglot.expressions import select as sg_select

__all__ = ["Select", "select"]


def select(*expressions: ExpOrStr) -> Select:
    """Create a SQL select statement.

    Args:
       *expressions: Columns to select.

    Returns:
       Select object that can be further qualified with where(), group_by(), etc.
    """
    return sg_select(*expressions, dialect="duckdb")
