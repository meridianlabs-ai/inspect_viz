from typing import Type

import inspect_viz.transform as tx
from pydantic import BaseModel

from ._schema import AggregateExpression, SQLExpression


def test_sql_wrapper() -> None:
    check_transform(tx.sql("foo", label="bar"), SQLExpression)


def test_agg_wrapper() -> None:
    check_transform(tx.agg("foo", label="bar"), AggregateExpression)


def check_transform(transform: tx.Transform, type: Type[BaseModel]) -> None:
    model = type.model_validate(transform)
    assert model.model_dump(exclude_none=True, by_alias=True) == transform
