from typing import Any, ClassVar, Optional

from pydantic import BaseModel, Field
from shortuuid import uuid


def _param_id() -> str:
    return f"param_{uuid()}"


class Param(BaseModel):
    """Parameter that can be bound from inputs."""

    # Class-level dictionary to store all instances
    _instances: ClassVar[dict[str, "Param"]] = {}

    id: str = Field(default_factory=_param_id)
    """Unique id for parameter."""

    default: int | float | bool | str
    """Default value for parameter."""

    def __str__(self) -> str:
        return f":{self.id}"

    def model_post_init(self, __context: Any) -> None:
        """Hook that is called after the model is initialized."""
        # Store instance in the class-level cache
        Param._instances[self.id] = self

    @classmethod
    def get(cls, param_id: str) -> Optional["Param"]:
        """Get a parameter by its id."""
        return cls._instances.get(param_id)

    @classmethod
    def get_all(cls) -> dict[str, "Param"]:
        """Get all parameters."""
        return cls._instances.copy()


def param(default: int | float | bool | str) -> Param:
    """Create a parameter that can be bound from inputs.

    Args:
       default: Default value.

    Returns:
       Parameter.
    """
    return Param(default=default)
