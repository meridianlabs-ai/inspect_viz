import anywidget
import traitlets

from inspect_analysis._util.constants import STATIC_DIR


class FigureView(anywidget.AnyWidget):
    _esm = STATIC_DIR / "figure_view.js"
    _css = STATIC_DIR / "figure_view.css"
    value = traitlets.Int(0).tag(sync=True)
