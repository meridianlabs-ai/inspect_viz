from typing import Any, Type

import inspect_viz.transform as tx
from pydantic import BaseModel

from ._schema import (
    AggregateExpression,
    Argmax,
    Argmin,
    Avg,
    Bin,
    Column,
    Count,
    DateDay,
    DateMonth,
    DateMonthDay,
    First,
    Last,
    Max,
    Median,
    Min,
    Mode,
    Product,
    Quantile,
    SQLExpression,
    Stddev,
    StddevPop,
    Sum,
    Variance,
    VarPop,
)


def test_column_wrapper() -> None:
    check_transform(tx.column("foo"), Column)


def test_bin_wrapper() -> None:
    check_transform(
        tx.bin("foo", interval="hour", step=1, steps=1, nice=True, offset=1), Bin
    )


def test_sql_wrapper() -> None:
    check_transform(tx.sql("foo", label="bar"), SQLExpression)


def test_agg_wrapper() -> None:
    check_transform(tx.agg("foo", label="bar"), AggregateExpression)


def test_date_month_day_wrapper() -> None:
    check_transform(tx.date_month_day("date_column"), DateMonthDay)


def test_date_day_wrapper() -> None:
    check_transform(tx.date_day("date_column"), DateDay)


def test_date_month_wrapper() -> None:
    check_transform(tx.date_month("date_column"), DateMonth)


def test_argmin_wrapper() -> None:
    check_transform(
        tx.argmin(col1="foo", col2="bar", **aggregate_args()),
        Argmin,
    )


def test_argmax_wrapper() -> None:
    check_transform(
        tx.argmax(col1="foo", col2="bar", **aggregate_args()),
        Argmax,
    )


def test_avg_wrapper() -> None:
    check_transform(
        tx.avg(col="foo", **aggregate_args()),
        Avg,
    )


def test_count_wrapper() -> None:
    check_transform(
        tx.count(col=None, **aggregate_args()),
        Count,
        exclude_none=False,
    )


def check_transform(
    transform: tx.Transform, type: Type[BaseModel], exclude_none: bool = True
) -> None:
    model = type.model_validate(transform)
    assert model.model_dump(exclude_none=exclude_none, by_alias=True) == transform


def test_first_wrapper() -> None:
    check_transform(
        tx.first(col="foo", **aggregate_args()),
        First,
    )


def test_last_wrapper() -> None:
    check_transform(
        tx.last(col="foo", **aggregate_args()),
        Last,
    )


def test_max_wrapper() -> None:
    check_transform(
        tx.max(col="foo", **aggregate_args()),
        Max,
    )


def test_min_wrapper() -> None:
    check_transform(
        tx.min(col="foo", **aggregate_args()),
        Min,
    )


def test_median_wrapper() -> None:
    check_transform(
        tx.median(col="foo", **aggregate_args()),
        Median,
    )


def test_mode_wrapper() -> None:
    check_transform(
        tx.mode(col="foo", **aggregate_args()),
        Mode,
    )


def test_product_wrapper() -> None:
    check_transform(
        tx.product(col="foo", **aggregate_args()),
        Product,
    )


def test_stddev_wrapper() -> None:
    check_transform(
        tx.stddev(col="foo", **aggregate_args()),
        Stddev,
    )


def test_sum_wrapper() -> None:
    check_transform(
        tx.sum(col="foo", **aggregate_args()),
        Sum,
    )


def test_variance_wrapper() -> None:
    check_transform(
        tx.variance(col="foo", **aggregate_args()),
        Variance,
    )


def test_stddev_pop_wrapper() -> None:
    check_transform(
        tx.stddev_pop(col="foo", **aggregate_args()),
        StddevPop,
    )


def test_var_pop_wrapper() -> None:
    check_transform(
        tx.var_pop(col="foo", **aggregate_args()),
        VarPop,
    )


def test_quantile_wrapper() -> None:
    check_transform(
        tx.quantile(col="foo", threshold=0.5, **aggregate_args()),
        Quantile,
    )


def aggregate_args() -> dict[str, Any]:
    return dict(
        distinct=True,
        orderby="foo",
        partitionby="foo",
        rows=[None],
        range=[None],
    )
