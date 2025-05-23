from typing import ClassVar, Literal

from shortuuid import uuid

SELECTION_PREFIX = "selection_"


class Selection:
    def __init__(
        self,
        *,
        select: Literal["crossfilter", "intersect", "single", "union"],
        cross: bool | None = None,
        empty: bool | None = None,
        unique: str = uuid(),
    ) -> None:
        self._id = f"{SELECTION_PREFIX}{unique}"
        self._select = select
        self._cross = cross
        self._empty = empty
        Selection._instances.append(self)

    @property
    def id(self) -> str:
        """Unique id (automatically generated)."""
        return self._id

    @property
    def select(self) -> Literal["crossfilter", "intersect", "single", "union"]:
        """Selection type:

        One of:

        - `"intersect"` for a `Selection` that intersects clauses (logical "and")
        - `"union"` for a `Selection` that unions clauses (logical "or")
        - `"single"` for a `Selection` that retains a single clause only
        - `"crossfilter"` for a cross-filtered intersection `Selection`'
        """
        return self._select

    @property
    def cross(self) -> bool | None:
        """A flag for cross-filtering, where selections made in a plot filter others but not oneself (default `False`, except for `crossfilter` selections)."""
        return self._cross

    @property
    def empty(self) -> bool | None:
        """A flag for setting an initial empty selection state.

        If true, a selection with no clauses corresponds to an empty selection with no records. If false, a selection with no clauses selects all values.
        """
        return self._empty

    # Class-level dictionary to store all instances
    _instances: ClassVar[list["Selection"]] = []

    @classmethod
    def get_all(cls) -> list["Selection"]:
        """Get all selections."""
        return cls._instances.copy()
