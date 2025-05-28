from pydantic import JsonValue

from .._core import Component


def vconcat(*component: Component) -> Component:
    """Vertically concatenate components in a column layout.

    Args:
        *component: Components to concatenate.
    """
    components: list[JsonValue] = [w.config for w in component]
    return Component(config=dict(vconcat=components))


def hconcat(*component: Component) -> Component:
    """Horizontally concatenate components in a row layout.

    Args:
        *component: Components to concatenate.
    """
    components: list[JsonValue] = [w.config for w in component]
    return Component(config=dict(hconcat=components))
