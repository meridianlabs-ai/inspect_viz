import base64
from datetime import datetime
from typing import Any, cast

import traitlets
from anywidget import AnyWidget
from pydantic import JsonValue
from pydantic_core import to_json, to_jsonable_python

from .._util.constants import WIDGETS_DIR
from .._util.marshall import dict_remove_none
from .data import Data
from .param import Param as VizParam
from .selection import Selection as VizSelection


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


class Component(AnyWidget):
    """Viz component (input, plot, table, etc.)."""

    def __init__(self, config: dict[str, JsonValue]) -> None:
        """Create a visualization component.

        Args:
            config: Component configuration.

        Returns:
            Visualization component.
        """
        super().__init__()
        self._config = config

    @property
    def config(self) -> dict[str, JsonValue]:
        """Component config."""
        return self._config

    def _repr_mimebundle_(
        self, **kwargs: Any
    ) -> tuple[dict[str, Any], dict[str, Any]] | None:
        from ..options._defaults import plot_defaults_as_camel

        # set current tables
        self.tables = all_tables()

        # ensure spec
        if not self.spec:
            # base spec
            spec = self._config.copy()

            # add plot defaults
            spec["plotDefaults"] = plot_defaults_as_camel()

            # add current params
            spec["params"] = all_params()

            # to json
            self.spec = to_json(spec, exclude_none=True).decode()

        return super()._repr_mimebundle_(**kwargs)

    _esm = WIDGETS_DIR / "mosaic.js"
    tables = TablesData({}).tag(sync=True)
    spec = traitlets.CUnicode("").tag(sync=True)


def all_tables() -> dict[str, str | bytes]:
    all_data: dict[str, str | bytes] = {}
    for data in Data.get_all():
        all_data[data.table] = data.collect_data()
    return all_data


def all_params() -> dict[str, JsonValue]:
    all_params: dict[str, Any] = {}

    for param in VizParam.get_all():
        if isinstance(param.default, datetime):
            all_params[param.id] = dict(select="value", date=param.default.isoformat())
        else:
            all_params[param.id] = dict(select="value", value=param.default)

    for selection in VizSelection.get_all():
        all_params[selection.id] = dict_remove_none(
            dict(
                select=selection.select,
                cross=selection.cross,
                empty=selection.empty,
                include=selection.include,
            )
        )

    return cast(dict[str, JsonValue], to_jsonable_python(all_params, exclude_none=True))
