from pydantic import BaseModel, Field
from shortuuid import uuid


class Param(BaseModel):
    """Parameter that can be bound from inputs."""

    id: str = Field(default_factory=uuid)
    """Unique id for parameter."""

    default: int | float | bool | str
    """Default value for parameter."""


def param(default: int | float | bool | str) -> Param:
    """Create a parameter that can be bound from inputs.

    Args:
       default: Default value.

    Returns:
       Parameter.
    """
    return Param(default=default)
