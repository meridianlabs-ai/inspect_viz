from typing import ClassVar, Literal, Union

from shortuuid import uuid

SELECTION_PREFIX = "selection_"


class Selection(str):
    """Selection that can be filtered by inputs and other selections."""

    _id: str
    _select: Literal["crossfilter", "intersect", "single", "union"]
    _cross: bool | None
    _empty: bool | None
    _include: Union["Selection", list["Selection"] | None]

    def __new__(
        cls,
        select: Literal["crossfilter", "intersect", "single", "union"],
        *,
        cross: bool | None = None,
        empty: bool | None = None,
        unique: str | None = None,
        include: Union["Selection", list["Selection"] | None] = None,
    ) -> "Selection":
        # assign a unique id
        id = f"{SELECTION_PREFIX}{unique or uuid()}"

        # create the string instance
        instance = super().__new__(cls, f"${id}")

        # bind instance vars
        instance._id = id
        instance._select = select
        instance._cross = cross
        instance._empty = empty
        instance._include = include

        # track and return instance
        Selection._instances.append(instance)
        return instance

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

    @property
    def include(self) -> Union["Selection", list["Selection"] | None]:
        """Upstream selections whose clauses should be included as part of this selection.

        Any clauses or activations published to the upstream selections will be relayed to this selection.
        """
        return self._include

    def __repr__(self) -> str:
        # start with selection
        repr = f"Selection(select={self.select}"

        # include non-default cross
        if (self.cross is True and self.select != "crossfilter") or (
            self.cross is False and self.select == "crossfilter"
        ):
            repr = f"{repr},cross={self.cross}"

        # include empty if specified
        if self.empty is not None:
            repr = f"{repr},empty={self.empty}"

        if self._include is not None:
            include = (
                self._include if isinstance(self._include, list) else [self._include]
            )
            repr = f"{repr},selection={','.join(include)}"

        # close out and return
        return f"{repr})"

    # Class-level dictionary to store all instances
    _instances: ClassVar[list["Selection"]] = []

    @classmethod
    def get_all(cls) -> list["Selection"]:
        """Get all selections."""
        return cls._instances.copy()
