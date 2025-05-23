from datetime import datetime
from typing import ClassVar

from shortuuid import uuid

PARAM_PREFIX = "param_"


class Param:
    """Parameter that can be bound from inputs."""

    def __init__(self, *, default: int | float | bool | str | datetime) -> None:
        self._id = f"{PARAM_PREFIX}{uuid()}"
        self._default = default
        Param._instances.append(self)

    @property
    def id(self) -> str:
        """Unique id (automatically generated)."""
        return self._id

    @property
    def default(self) -> int | float | bool | str | datetime:
        """Default value."""
        return self._default

    def is_numeric(self) -> bool:
        """Is this a numeric parameter?"""
        return isinstance(self.default, (int | float))

    def is_bool(self) -> bool:
        """Is this a boolean parameter?"""
        return isinstance(self.default, bool)

    def is_string(self) -> bool:
        """Is this a string parameter?"""
        return isinstance(self.default, str)

    def is_datetime(self) -> bool:
        """Is this a datetime parameter?"""
        return isinstance(self.default, datetime)

    # Class-level dictionary to store all instances
    _instances: ClassVar[list["Param"]] = []

    @classmethod
    def get_all(cls) -> list["Param"]:
        """Get all parameters."""
        return cls._instances.copy()
