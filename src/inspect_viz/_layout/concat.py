from .._core import Widget
from ..mosaic import HConcat, VConcat


def vconcat(*widget: Widget) -> Widget:
    """Vertically concatenate widgets in a column layout.

    Args:
        *widget: Widgets to concatenate.
    """
    components = [w.component for w in widget]
    return Widget(VConcat(vconcat=components))  # type: ignore[arg-type]


def hconcat(*widget: Widget) -> Widget:
    """Horizontally concatenate widgets in a row layout.

    Args:
        *widget: Widgets to layout.
    """
    components = [w.component for w in widget]
    return Widget(HConcat(hconcat=components))  # type: ignore[arg-type]
