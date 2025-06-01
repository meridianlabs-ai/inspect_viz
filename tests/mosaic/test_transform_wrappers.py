from typing import Type

import inspect_viz.transform as tx
from pydantic import BaseModel

from ._schema import (
    AggregateExpression,
    DateDay,
    DateMonth,
    DateMonthDay,
    SQLExpression,
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


def check_transform(transform: tx.Transform, type: Type[BaseModel]) -> None:
    model = type.model_validate(transform)
    assert model.model_dump(exclude_none=True, by_alias=True) == transform
