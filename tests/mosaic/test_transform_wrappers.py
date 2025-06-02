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
    SQLExpression,
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


def aggregate_args() -> dict[str, Any]:
    return dict(
        distinct=True,
        orderby="foo",
        partitionby="foo",
        rows=[None],
        range=[None],
    )
