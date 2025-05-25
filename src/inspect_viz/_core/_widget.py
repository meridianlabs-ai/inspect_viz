import base64
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


class TablesData(traitlets.TraitType[dict[str, str], dict[str, str | bytes]]):
    """Custom traitlet for handling multiple table/data pairs.

    Accepts a dict of {table_name: bytes_data} and serializes it as JSON
    with base64-encoded data values for transmission to the frontend.
    """

    info_text = "a dict of table names to data bytes"

    def validate(self, obj: Any, value: Any) -> dict[str, str]:
        if not isinstance(value, dict):
            self.error(obj, value)

        # Convert bytes values to base64 strings for JSON serialization
        serialized = {}
        for key, data in value.items():
            if isinstance(data, bytes):
                serialized[key] = base64.b64encode(data).decode("utf-8")
            elif isinstance(data, str):
                # Already base64 encoded
                serialized[key] = data
            else:
                self.error(obj, value)

        return serialized


class Widget(AnyWidget):
    """Visualization widget (input, plot, table, etc.)."""

    _esm = STATIC_DIR / "mosaic.js"
    tables = TablesData({}).tag(sync=True)
    spec = traitlets.CUnicode("").tag(sync=True)

    def __init__(self, component: Component, data: Data | None = None) -> None:
        """Create a visualization widget.

        Args:
            component: Visualization component wrapped by the widget.
            data: Data source(s) for widget (optional). Can be a single Data object or list of Data objects.

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
        # collect data from all Data objects
        if self._data:
            tables_data_dict: dict[str, str | bytes] = {}
            tables_data_dict[self._data.table] = self._data.collect_data()
            self.tables = tables_data_dict

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
