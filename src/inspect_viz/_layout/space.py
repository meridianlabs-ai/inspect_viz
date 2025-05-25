from inspect_viz._core import Widget
from inspect_viz.mosaic import HSpace, VSpace


def hspace(hspace: float | str) -> Widget:
    """Horizontal space to place between widgets.

    Args:
        hspace: Amount of space. Number values indicate screen pixels. String values may use CSS units (em, pt, px, etc).
    """
    return Widget(HSpace(hspace=hspace))


def vspace(vspace: float | str) -> Widget:
    """Veritcal space to place between widgets.

    Args:
        vspace: Amount of space. Number values indicate screen pixels. String values may use CSS units (em, pt, px, etc).
    """
    return Widget(VSpace(vspace=vspace))
