from typing import Any

import traitlets
from anywidget import AnyWidget
from pydantic_core import to_json

from .._core._data import Data
from .._core._param import Param
from .._util._constants import STATIC_DIR
from ..mosaic import HConcat, Plot, PlotAttributes, VConcat


class SpecWidget(AnyWidget):
    _esm = STATIC_DIR / "spec.js"
    df_id = traitlets.CUnicode("").tag(sync=True)
    spec = traitlets.CUnicode("").tag(sync=True)
    params = traitlets.CUnicode(Param.get_all_as_json()).tag(sync=True)


def spec(
    data: Data,
    root: Plot | HConcat | VConcat,
    plot_defaults: PlotAttributes | None = None,
) -> SpecWidget:
    # base spec
    spec: dict[str, Any] = root.model_dump(by_alias=True, exclude_none=True)

    # params
    spec["params"] = {param.id: param.default for param in Param.get_all()}

    # plot defaults
    if plot_defaults is not None:
        spec["plotDefaults"] = plot_defaults.model_dump(
            by_alias=True, exclude_none=True
        )

    # create and return widget
    widget = SpecWidget()
    widget.df_id = data.id
    widget.spec = to_json(spec).decode()
    return widget
