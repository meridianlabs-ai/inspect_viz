from typing import Any

from pydantic import JsonValue, RootModel

from inspect_viz._core.param import Param


class Transform(RootModel[dict[str, JsonValue]]):
    """Column transformation operation."""

    def __init__(self, config: dict[str, JsonValue] | None = None) -> None:
        super().__init__(config or {})

    def __getitem__(self, key: str) -> JsonValue:
        return self.root[key]

    def __setitem__(self, key: str, value: JsonValue) -> None:
        self.root[key] = value

    def __delitem__(self, key: str) -> None:
        del self.root[key]

    def __contains__(self, key: str) -> bool:
        return key in self.root

    def __iter__(self) -> Any:
        return iter(self.root)

    def __len__(self) -> int:
        return len(self.root)

    def keys(self) -> Any:
        return self.root.keys()

    def values(self) -> Any:
        return self.root.values()

    def items(self) -> Any:
        return self.root.items()

    def get(self, key: str, default: JsonValue = None) -> JsonValue:
        return self.root.get(key, default)

    def pop(self, key: str, default: JsonValue = None) -> JsonValue:
        return self.root.pop(key, default)

    def popitem(self) -> tuple[str, JsonValue]:
        return self.root.popitem()

    def clear(self) -> None:
        self.root.clear()

    def update(self, other: dict[str, JsonValue]) -> None:
        self.root.update(other)

    def setdefault(self, key: str, default: JsonValue = None) -> JsonValue:
        return self.root.setdefault(key, default)


TransformArg = str | float | bool | Param | list[str | float | bool | Param]
