from typing import Any, ClassVar, Optional

from pydantic import BaseModel, Field
from shortuuid import uuid

PARAM_ESCAPE = ":"
PARAM_PREFIX = "param_"


class Param(BaseModel):
    """Parameter that can be bound from inputs."""

    default: int | float | bool | str
    """Default value for parameter."""

    id: str = Field(default_factory=lambda: f"{PARAM_PREFIX}{uuid()}")
    """Unique id for parameter."""

    def is_numeric(self) -> bool:
        return isinstance(self.default, (int | float))

    def is_bool(self) -> bool:
        return isinstance(self.default, bool)

    def is_string(self) -> bool:
        return isinstance(self.default, str)

    def __str__(self) -> str:
        return f"{PARAM_ESCAPE}{self.id}"

    # Class-level dictionary to store all instances
    _instances: ClassVar[dict[str, "Param"]] = {}

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
