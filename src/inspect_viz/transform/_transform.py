from pydantic import JsonValue


class Transform(dict[str, JsonValue]):
    """Column transformation operation."""

    def __init__(self, config: dict[str, JsonValue]) -> None:
        super().__init__(config)
