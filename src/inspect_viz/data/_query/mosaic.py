from typing import Literal, Union

from pydantic import BaseModel


class FunctionExpression(BaseModel):
    type: Literal["function"] = "function"
    name: str
    args: list["Expression"]


class BinaryExpression(BaseModel):
    type: str  # eq, neq, gt, gte, lt, lte, and, or, add, sub, mul, div
    left: "Expression"
    right: "Expression"


class LogicalExpression(BaseModel):
    type: Literal["and", "or"]
    expressions: list["Expression"]


class GroupByField(BaseModel):
    field: str | FunctionExpression


class ParameterExpression(BaseModel):
    type: Literal["parameter"] = "parameter"
    name: str


class UnknownExpression(BaseModel):
    type: Literal["unknown"] = "unknown"
    expression: str


class OrderByItem(BaseModel):
    field: str
    order: Literal["asc", "desc"]


class SelectField(BaseModel):
    expression: str | FunctionExpression | BinaryExpression | UnknownExpression


class Parameter(BaseModel):
    name: str
    value: int | float | bool | str
    type: str


class MosaicQuery(BaseModel):
    sql: str
    parameters: dict[str, Parameter]
    select: dict[
        str, Union[str, FunctionExpression, BinaryExpression, UnknownExpression]
    ]
    distinct: bool | None = None
    sample: float | int | None = None
    where: BinaryExpression | LogicalExpression | UnknownExpression | None = None
    groupby: list[str | GroupByField] | None = None
    having: BinaryExpression | LogicalExpression | UnknownExpression | None = None
    orderby: list[OrderByItem] | None = None
    limit: int | None = None


Expression = Union[
    str,
    int,
    float,
    bool,
    BinaryExpression,
    LogicalExpression,
    FunctionExpression,
    ParameterExpression,
    UnknownExpression,
]
