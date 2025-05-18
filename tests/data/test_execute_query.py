from typing import Any, cast

import narwhals as nw
import numpy as np
import pandas as pd
import pytest
from sqlglot import parse_one
from sqlglot.expressions import Select

from inspect_viz.data._query.execute import execute_query
from inspect_viz.data._query.parser import parse_sql
from inspect_viz.data.reactive_df import ReactiveDF, reactive_df


@pytest.fixture
def sample_dataframe() -> nw.DataFrame[Any]:
    """Create a sample pandas dataframe for testing."""
    data = {
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "age": [25, 30, 35, 40, 45],
        "department": ["HR", "Engineering", "Marketing", "Engineering", "HR"],
        "salary": [60000, 75000, 65000, 80000, 70000],
    }
    return nw.from_native(pd.DataFrame(data))


def test_execute_simple_select(sample_dataframe: nw.DataFrame[Any]) -> None:
    """Test executing a simple SELECT query."""
    query = parse_sql("SELECT name, age FROM data")
    result = execute_query(sample_dataframe, query)

    # Check the result structure
    assert isinstance(result, nw.DataFrame)

    # Check column count and names
    pdf = result.to_pandas()
    assert len(pdf.columns) == 2
    assert "name" in pdf.columns
    assert "age" in pdf.columns

    # Check the data values match original
    original_pdf = sample_dataframe.to_pandas()
    # Use numpy array comparison which returns an array of booleans, then check if all are True
    assert np.all(pdf["name"].values == original_pdf["name"].values)
    assert np.all(pdf["age"].values == original_pdf["age"].values)


def test_execute_where_clause(sample_dataframe: nw.DataFrame[Any]) -> None:
    """Test executing a query with WHERE clause."""
    query = parse_sql("SELECT * FROM data WHERE age > 30")
    result = execute_query(sample_dataframe, query)

    # Convert to pandas for testing
    pdf = result.to_pandas()

    # Check filtered data
    assert len(pdf) == 3  # Charlie, David, Eve
    assert all(age > 30 for age in pdf["age"])
    assert set(pdf["name"].tolist()) == {"Charlie", "David", "Eve"}


def test_execute_aggregation(sample_dataframe: nw.DataFrame[Any]) -> None:
    """Test executing a query with aggregation."""
    query = parse_sql("SELECT department, AVG(salary) as avg_salary FROM data GROUP BY department")
    result = execute_query(sample_dataframe, query)

    # Check result
    pdf = result.to_pandas()
    assert len(pdf) == 3  # 3 departments
    assert "department" in pdf.columns
    assert "avg_salary" in pdf.columns

    # Verify the averages are correct
    hr_row = pdf[pdf["department"] == "HR"]
    eng_row = pdf[pdf["department"] == "Engineering"]

    assert hr_row["avg_salary"].values[0] == 65000.0  # (60000 + 70000) / 2
    assert eng_row["avg_salary"].values[0] == 77500.0  # (75000 + 80000) / 2


def test_execute_order_by(sample_dataframe: nw.DataFrame[Any]) -> None:
    """Test executing a query with ORDER BY clause."""
    query = parse_sql("SELECT name, age FROM data ORDER BY age DESC")
    result = execute_query(sample_dataframe, query)

    pdf = result.to_pandas()
    assert len(pdf) == 5

    # Verify the order is correct (descending by age)
    expected_names = ["Eve", "David", "Charlie", "Bob", "Alice"]
    assert list(pdf["name"]) == expected_names


def test_execute_limit(sample_dataframe: nw.DataFrame[Any]) -> None:
    """Test executing a query with LIMIT clause."""
    query = parse_sql("SELECT * FROM data LIMIT 3")
    result = execute_query(sample_dataframe, query)

    pdf = result.to_pandas()
    assert len(pdf) == 3


def test_execute_parameterized_query(sample_dataframe: nw.DataFrame[Any]) -> None:
    """Test executing a parameterized query."""
    query = parse_sql("SELECT * FROM data WHERE age > :min_age", min_age=30)
    result = execute_query(sample_dataframe, query)

    pdf = result.to_pandas()
    assert len(pdf) == 3
    assert all(age > 30 for age in pdf["age"])


def test_execute_complex_query(sample_dataframe: nw.DataFrame[Any]) -> None:
    """Test executing a more complex query."""
    query_str = """
    SELECT
        department,
        COUNT(*) as employee_count,
        AVG(salary) as avg_salary
    FROM data
    WHERE age >= 30
    GROUP BY department
    HAVING COUNT(*) > 1
    ORDER BY avg_salary DESC
    """

    query = parse_sql(query_str)
    result = execute_query(sample_dataframe, query)

    pdf = result.to_pandas()

    # Only the Engineering department should have more than 1 employee aged >= 30
    assert len(pdf) == 1
    assert pdf["department"].values[0] == "Engineering"
    assert pdf["employee_count"].values[0] == 2
    assert pdf["avg_salary"].values[0] == 77500.0


# Test the ReactiveDF implementation specifically
def test_reactive_df_query_method() -> None:
    """Test the query method of ReactiveDF."""
    # Create a sample dataframe
    data = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 40, 45],
            "department": ["HR", "Engineering", "Marketing", "Engineering", "HR"],
            "salary": [60000, 75000, 65000, 80000, 70000],
        }
    )

    # Create a reactive dataframe
    df = reactive_df(data)

    # Apply a query to the reactive dataframe
    result_df = df.query("SELECT name, age FROM data WHERE age > 30")

    # Since ReactiveDF is a Protocol, we can't directly use isinstance
    # Instead, verify it has the correct methods
    assert hasattr(result_df, "query")
    assert hasattr(result_df, "__dataframe__")
    assert hasattr(result_df, "__narwhals_dataframe__")
    assert hasattr(result_df, "_table")

    # Extract narwhals dataframe from the implementation
    ndf = cast(nw.DataFrame[Any], result_df.__narwhals_dataframe__())

    # Convert to pandas for testing
    pdf = ndf.to_pandas()

    # Check that the query was correctly applied
    assert len(pdf) == 3  # Charlie, David, Eve
    assert all(age > 30 for age in pdf["age"])
    assert set(pdf["name"].tolist()) == {"Charlie", "David", "Eve"}


def test_reactive_df_chained_queries() -> None:
    """Test chaining multiple queries on a ReactiveDF."""
    # Create a sample dataframe
    data = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 40, 45],
            "department": ["HR", "Engineering", "Marketing", "Engineering", "HR"],
            "salary": [60000, 75000, 65000, 80000, 70000],
        }
    )

    # Create a reactive dataframe
    df = reactive_df(data)

    # Apply two chained queries
    filtered_df = df.query("SELECT * FROM data WHERE age > 30")
    result_df = filtered_df.query("SELECT name, department FROM data ORDER BY name")

    # Verify the methods are present
    assert hasattr(result_df, "query")
    assert hasattr(result_df, "__dataframe__")

    # Extract narwhals dataframe from the implementation
    ndf = cast(nw.DataFrame[Any], result_df.__narwhals_dataframe__())

    # Convert to pandas for testing
    pdf = ndf.to_pandas()

    # Check column names
    assert set(pdf.columns) == {"name", "department"}

    # Check the data is correct and sorted by name
    assert len(pdf) == 3
    assert list(pdf["name"]) == ["Charlie", "David", "Eve"]


def test_reactive_df_with_parameterized_query() -> None:
    """Test ReactiveDF with parameterized queries."""
    # Create a sample dataframe
    data = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 40, 45],
            "department": ["HR", "Engineering", "Marketing", "Engineering", "HR"],
            "salary": [60000, 75000, 65000, 80000, 70000],
        }
    )

    # Create a reactive dataframe
    df = reactive_df(data)

    # Apply a parameterized query
    min_age = 35
    result_df = df.query("SELECT * FROM data WHERE age >= :min_age", min_age=min_age)

    # Verify it's a valid ReactiveDF implementation
    assert hasattr(result_df, "query")
    assert hasattr(result_df, "__dataframe__")

    # Extract narwhals dataframe from the implementation
    ndf = cast(nw.DataFrame[Any], result_df.__narwhals_dataframe__())

    # Convert to pandas for testing
    pdf = ndf.to_pandas()

    # Check that the query was correctly applied
    assert len(pdf) == 3  # Charlie, David, Eve
    assert all(age >= min_age for age in pdf["age"])


def test_reactive_df_with_sqlglot_select() -> None:
    """Test ReactiveDF with sqlglot Select object instead of string."""
    # Create a sample dataframe
    data = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 40, 45],
            "department": ["HR", "Engineering", "Marketing", "Engineering", "HR"],
            "salary": [60000, 75000, 65000, 80000, 70000],
        }
    )

    # Create a reactive dataframe
    df = reactive_df(data)

    # Create a sqlglot Select object
    select_obj = parse_one("SELECT name, department FROM data WHERE age > 30")
    assert isinstance(select_obj, Select)  # Ensure it's a Select object

    # Apply the Select object query
    result_df = df.query(select_obj)

    # Verify it's a valid ReactiveDF implementation
    assert hasattr(result_df, "query")
    assert hasattr(result_df, "__dataframe__")

    # Extract narwhals dataframe from the implementation
    ndf = cast(nw.DataFrame[Any], result_df.__narwhals_dataframe__())

    # Convert to pandas for testing
    pdf = ndf.to_pandas()

    assert set(pdf.columns) == {"name", "department"}
    assert len(pdf) == 3  # Charlie, David, Eve with age > 30