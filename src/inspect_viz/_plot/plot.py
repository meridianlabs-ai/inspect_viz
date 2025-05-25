from inspect_viz._core import Data, Widget
from inspect_viz.mosaic import Plot


def plot(*mark: Widget) -> Widget:
    components = [m.component for m in mark]
    return Widget(component=Plot(plot=components))  # type: ignore[arg-type]
