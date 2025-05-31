from datetime import datetime
from typing import ClassVar, Sequence, TypeAlias

from shortuuid import uuid

PARAM_PREFIX = "param_"

ParamValue: TypeAlias = (
    int | float | bool | str | datetime | Sequence[int | float | bool | str]
)


class Param(str):
    """Parameter that can be bound from inputs."""

    _id: str
    _default: ParamValue

    def __new__(cls, default: ParamValue) -> "Param":
        # assign a unique id
        id = f"{PARAM_PREFIX}{uuid()}"

        # create the string instance
        instance = super().__new__(cls, f"${id}")

        # bind instance fars
        instance._id = id
        instance._default = default

        # track and return instance
        Param._instances.append(instance)
        return instance

    @property
    def id(self) -> str:
        """Unique id (automatically generated)."""
        return self._id

    @property
    def default(self) -> ParamValue:
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

    def __repr__(self) -> str:
        return f"Param(default={self.default})"

    # Class-level dictionary to store all instances
    _instances: ClassVar[list["Param"]] = []

    @classmethod
    def get_all(cls) -> list["Param"]:
        """Get all parameters."""
        return cls._instances.copy()
