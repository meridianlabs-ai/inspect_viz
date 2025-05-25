from datetime import datetime
from typing import Any

import traitlets
from anywidget import AnyWidget
from pydantic_core import to_json

from .._util._constants import STATIC_DIR
from ..mosaic import Component, Param, ParamDate, Params, Selection
from ._data import Data
from ._param import Param as VizParam
from ._selection import Selection as VizSelection


class Widget(AnyWidget):
    """Visualization widget (input, plot, table, etc.)."""

    _esm = STATIC_DIR / "mosaic.js"
    df_id = traitlets.CUnicode("").tag(sync=True)
    df_buffer = traitlets.Bytes(b"").tag(sync=True)
    spec = traitlets.CUnicode("").tag(sync=True)

    def __init__(self, component: Component, data: Data | None = None) -> None:
        """Create a visualization widget.

        Args:
            component: Visualization component wrapped by the widget.
            data: Data source for wiget (optional).

        Returns:
            Visualization widget.
        """
        super().__init__()
        self._component = component
        self._data = data

    @property
    def component(self) -> Component:
        """Mosaic component."""
        return self.component

    def _repr_mimebundle_(
        self, **kwargs: Any
    ) -> tuple[dict[str, Any], dict[str, Any]] | None:
        # ensure data
        if self._data is not None:
            self.df_id = self._data.id
            self.df_buffer = self._data.collect_buffer()

        # ensure spec
        if not self.spec:
            # base spec
            spec: dict[str, Any] = self._component.model_dump(
                by_alias=True, exclude_none=True
            )

            # add current params
            spec["params"] = mosaic_params()

            # to json
            self.spec = to_json(spec).decode()

        return super()._repr_mimebundle_(**kwargs)


# class MosaicWidget(AnyWidget):
#     _esm = STATIC_DIR / "mosaic.js"
#     df_id = traitlets.CUnicode("").tag(sync=True)
#     df_buffer = traitlets.Bytes(b"").tag(sync=True)
#     spec = traitlets.CUnicode("").tag(sync=True)


# def mosaic_widget(
#     *,
#     data: Data,
#     component: Component,
# ) -> MosaicWidget:
#     # base spec
#     spec: dict[str, Any] = component.model_dump(by_alias=True, exclude_none=True)

#     # add current params
#     spec["params"] = mosaic_params()

#     # create and return widget
#     widget = MosaicWidget()
#     widget.df_id = data.id
#     widget.df_buffer = data.collect_buffer()
#     widget.spec = to_json(spec).decode()
#     return widget


def mosaic_params() -> Params:
    all_params: Params = {}

    for param in VizParam.get_all():
        if isinstance(param.default, datetime):
            all_params[param.id] = ParamDate(date=param.default.isoformat())
        else:
            all_params[param.id] = Param(value=param.default)

    for selection in VizSelection.get_all():
        all_params[selection.id] = Selection(
            select=selection.select, cross=selection.cross, empty=selection.empty
        )

    return all_params
