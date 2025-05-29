from typing import Any


def snake_to_camel(snake_str: str) -> str:
    """Convert a snake_case string to camelCase."""
    components = snake_str.split("_")
    return components[0] + "".join(word.capitalize() for word in components[1:])


def dict_to_camel(d: dict[str, Any]) -> dict[str, Any]:
    return {snake_to_camel(key): value for key, value in d.items()}
