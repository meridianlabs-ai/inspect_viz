import pytest
from inspect_viz.data._query.mosaic import (
    BinaryExpression,
    FunctionExpression,
    LogicalExpression,
    MosaicQuery,
    OrderByItem,
    ParameterExpression,
)
from inspect_viz.data._query.parser import parse_sql


def test_simple_select() -> None:
    """Test a simple SELECT statement."""
    sql: str = "SELECT name, age FROM users"
    result: MosaicQuery = parse_sql(sql)

    assert result.select
    assert "name" in result.select
    assert "age" in result.select


def test_where_clause() -> None:
    """Test conversion of WHERE clause."""
    sql: str = "SELECT * FROM users WHERE age > 30"
    result: MosaicQuery = parse_sql(sql)

    assert result.where is not None
    assert isinstance(result.where, BinaryExpression)
    binary_expr = result.where
    assert binary_expr.type == "gt"
    assert binary_expr.left == "age"
    assert binary_expr.right == 30


def test_group_by() -> None:
    """Test conversion of GROUP BY clause."""
    sql: str = (
        "SELECT department, COUNT(*) as emp_count FROM employees GROUP BY department"
    )
    result: MosaicQuery = parse_sql(sql)

    assert result.groupby is not None
    assert "department" in result.groupby
    assert result.select
    assert "department" in result.select
    assert "emp_count" in result.select


def test_order_by() -> None:
    """Test conversion of ORDER BY clause."""
    sql: str = "SELECT name FROM users ORDER BY age DESC"
    result: MosaicQuery = parse_sql(sql)

    assert result.orderby is not None
    assert len(result.orderby) >= 1

    # Find the orderby entry for 'age'
    age_orderby = next((o for o in result.orderby if o.field == "age"), None)
    assert age_orderby is not None, "Should have an ORDER BY entry for 'age'"
    assert age_orderby.order == "desc"


def test_limit() -> None:
    """Test conversion of LIMIT clause."""
    sql: str = "SELECT * FROM users LIMIT 10"
    result: MosaicQuery = parse_sql(sql)

    assert result.limit == 10


def test_aggregate_function() -> None:
    """Test handling of aggregate functions."""
    sql: str = "SELECT AVG(salary) as avg_sal FROM employees"
    result: MosaicQuery = parse_sql(sql)

    assert result.select
    assert "avg_sal" in result.select
    assert isinstance(result.select["avg_sal"], FunctionExpression)
    func_expr = result.select["avg_sal"]
    assert func_expr.type == "function"
    assert func_expr.name == "AVG"


def test_complex_where_clause() -> None:
    """Test handling of complex WHERE clauses with AND/OR operators."""
    sql: str = "SELECT * FROM products WHERE category = 'electronics' AND (price < 500 OR featured = true)"
    result: MosaicQuery = parse_sql(sql)

    assert result.where is not None
    assert isinstance(result.where, LogicalExpression)
    logical_expr = result.where
    assert logical_expr.type == "and"
    assert len(logical_expr.expressions) == 2

    # Check nested OR expression
    or_expr = logical_expr.expressions[1]
    assert isinstance(or_expr, LogicalExpression)
    or_logical = or_expr
    assert or_logical.type == "or"
    assert len(or_logical.expressions) > 0


def test_multiple_where_conditions() -> None:
    """Test handling of multiple WHERE conditions with nesting."""
    sql: str = """
    SELECT * FROM orders
    WHERE
        (status = 'shipped' OR status = 'delivered')
        AND
        (
            (order_date > '2023-01-01' AND total > 100)
            OR
            customer_type = 'premium'
        )
    """
    result: MosaicQuery = parse_sql(sql)

    assert result.where is not None
    assert isinstance(result.where, LogicalExpression)
    logical_expr = result.where
    assert logical_expr.type == "and"
    assert len(logical_expr.expressions) == 2

    # First part: status = 'shipped' OR status = 'delivered'
    first_clause = logical_expr.expressions[0]
    assert isinstance(first_clause, LogicalExpression)
    first_logical = first_clause
    assert first_logical.type == "or"
    assert len(first_logical.expressions) == 2

    # Second part: complex nested clause
    second_clause = logical_expr.expressions[1]
    assert isinstance(second_clause, LogicalExpression)
    second_logical = second_clause
    assert second_logical.type == "or"
    assert len(second_logical.expressions) == 2

    # Verify nested AND condition
    nested_and = second_logical.expressions[0]
    assert isinstance(nested_and, LogicalExpression)
    nested_logical = nested_and
    assert nested_logical.type == "and"
    assert len(nested_logical.expressions) == 2


def test_multiple_group_by() -> None:
    """Test handling of multiple GROUP BY fields."""
    sql: str = "SELECT category, region, COUNT(*) as count FROM sales GROUP BY category, region"
    result: MosaicQuery = parse_sql(sql)

    assert result.groupby is not None
    assert len(result.groupby) == 2
    assert "category" in result.groupby
    assert "region" in result.groupby


def test_complex_select_expressions() -> None:
    """Test handling of complex SELECT expressions."""
    sql: str = """SELECT
        name,
        price * quantity as total_cost,
        CASE WHEN quantity > 10 THEN 'bulk' ELSE 'retail' END as purchase_type,
        AVG(price) OVER (PARTITION BY category) as avg_category_price
        FROM purchases"""
    result: MosaicQuery = parse_sql(sql)

    assert result.select
    assert "name" in result.select
    assert "total_cost" in result.select
    assert "purchase_type" in result.select
    assert "avg_category_price" in result.select

    # Verify the binary expression in total_cost
    assert isinstance(result.select["total_cost"], BinaryExpression)
    total_cost_expr = result.select["total_cost"]
    assert total_cost_expr.type == "mul"
    assert total_cost_expr.left == "price"
    assert total_cost_expr.right == "quantity"


def test_model_validation() -> None:
    """Test that models correctly validate and handle complex nested structures."""
    # Create a complex query structure with nested expressions
    query: MosaicQuery = MosaicQuery(
        sql="",
        parameters={},
        select={
            "name": "name",
            "price": "price",
            "discounted_price": BinaryExpression(type="mul", left="price", right=0.9),
        },
        where=LogicalExpression(
            type="and",
            expressions=[
                BinaryExpression(type="eq", left="category", right="electronics"),
                LogicalExpression(
                    type="or",
                    expressions=[
                        BinaryExpression(type="lt", left="price", right=500),
                        BinaryExpression(type="eq", left="featured", right=True),
                    ],
                ),
            ],
        ),
        groupby=["category"],
        orderby=[OrderByItem(field="price", order="desc")],
        limit=10,
    )

    # Verify the model attributes (no from_ assertion)
    assert query.select
    assert "name" in query.select
    assert "price" in query.select
    assert "discounted_price" in query.select

    # Verify the nested WHERE structure
    assert query.where is not None
    assert isinstance(query.where, LogicalExpression)
    logical_expr = query.where
    assert logical_expr.type == "and"
    assert len(logical_expr.expressions) == 2

    # Verify JSON serialization
    json_data: str = query.model_dump_json()
    # No "from" assertion - FROM clauses are not supported
    assert "where" in json_data

    # Verify deserialization
    restored_query: MosaicQuery = MosaicQuery.model_validate_json(json_data)
    # No "from_" equality check - FROM clauses are not supported
    assert restored_query.limit == query.limit

    # Verify the nested expressions were correctly deserialized
    assert restored_query.where is not None
    assert isinstance(restored_query.where, LogicalExpression)
    restored_logical = restored_query.where
    assert restored_logical.type == "and"
    assert len(restored_logical.expressions) == 2


def test_parameterized_query() -> None:
    """Test handling of parameterized queries."""
    # Test both parameter formats that DuckDB supports
    styles = [
        # Test with $ format
        "SELECT * FROM products WHERE category = $category AND price < $max_price",
        # Test with : format
        "SELECT * FROM products WHERE category = :category AND price < :max_price",
    ]

    # Use the first style for our main test
    sql: str = styles[0]

    # Convert without parameter values
    result: MosaicQuery = parse_sql(sql, category="color", max_price=10)

    # Check the parameter references were captured in the WHERE clause
    assert result.where is not None
    assert isinstance(result.where, LogicalExpression)
    logical_expr = result.where
    assert logical_expr.type == "and"

    # Find the category parameter reference
    category_condition = logical_expr.expressions[0]
    assert isinstance(category_condition, BinaryExpression)
    cat_binary = category_condition
    assert cat_binary.type == "eq"
    assert cat_binary.left == "category"

    # Check that the parameter was recognized
    assert isinstance(cat_binary.right, ParameterExpression)
    category_param = cat_binary.right
    assert category_param.type == "parameter"
    assert category_param.name == "category"

    # Find the price parameter reference
    price_condition = logical_expr.expressions[1]
    assert isinstance(price_condition, BinaryExpression)
    price_binary = price_condition
    assert price_binary.type == "lt"
    assert price_binary.left == "price"

    # Check that the parameter was recognized
    assert isinstance(price_binary.right, ParameterExpression)
    price_param = price_binary.right
    assert price_param.type == "parameter"
    assert price_param.name == "max_price"


def test_query_without_from() -> None:
    """Test handling of queries without FROM clauses."""
    # SQL without a FROM clause
    sql: str = "SELECT 1 + 1 as result"

    # Parse and convert without error
    result: MosaicQuery = parse_sql(sql)

    # Verify that SELECT works correctly without needing a FROM clause
    assert result.select is not None
    assert "result" in result.select


def test_distinct() -> None:
    """Test handling of DISTINCT clause."""
    # SQL with DISTINCT keyword
    sql: str = "SELECT DISTINCT category FROM products"

    # Convert the SQL
    result: MosaicQuery = parse_sql(sql)

    # Verify that DISTINCT was recognized
    assert result.distinct is True
    assert result.select
    assert "category" in result.select


def test_having() -> None:
    """Test handling of HAVING clause."""
    # SQL with HAVING clause
    sql: str = """
    SELECT
        department,
        AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
    HAVING AVG(salary) > 50000
    """

    # Convert the SQL
    result: MosaicQuery = parse_sql(sql)

    # Verify GROUP BY and HAVING clauses
    assert result.groupby == ["department"]
    assert result.having is not None
    assert isinstance(result.having, BinaryExpression)
    having_expr = result.having
    assert having_expr.type == "gt"

    # Check that the HAVING condition is correctly parsed
    assert isinstance(having_expr.left, FunctionExpression)
    func_expr = having_expr.left
    assert func_expr.type == "function"
    assert func_expr.name == "AVG"
    assert having_expr.right == 50000
