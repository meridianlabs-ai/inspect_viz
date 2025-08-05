import base64
from datetime import datetime
from pathlib import Path
from typing import Any, Literal, cast

import traitlets
from anywidget import AnyWidget
from pydantic import JsonValue
from pydantic_core import to_json, to_jsonable_python

from .._util.constants import WIDGETS_DIR
from .._util.marshall import dict_remove_none
from .._util.platform import quarto_png, running_in_colab, running_in_quarto
from ._options import options
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
    """Data visualization component (input, plot, mark, table, layout, etc.).

    Visualization components are Jupyter widgets that can be used in
    any notebook or Jupyter based publishing system.

    See the documentation on inputs, plots, marks, and interactors for
    details on available components.
    """

    _css_initialized = False

    def __init__(
        self,
        config: dict[str, JsonValue],
        *,
        bind_spec: bool = False,
        bind_tables: bool | Literal["empty"] = False,
    ) -> None:
        # one time config of default css
        if not Component._css_initialized:
            Component._css_initialized = True
            css_paths = [self._css_base, self._css_nouislider]
            if running_in_quarto():
                css_paths.append(self._css_quarto)
                css_paths.append(self._css_tomselect_bs5)
            else:
                css_paths.append(self._css_tomselect)
            css_paths.append(self._css_tomselect_viz)
            css_paths.append(self._css_aggrid)
            css_paths.append(self._css_tooltips)
            css_paths.append(self._css_legend)
            for css in css_paths:
                with open(css, "r") as f:
                    Component._css = f"{self._css}\n\n{f.read()}"

        # only send css once for quarto
        elif running_in_quarto():
            self._css = ""

        super().__init__()
        self._config = config

        # eager bind as requested -- basically, in any environment where
        # _repr_mimebundle_ might is not called (e.g. colab) we need to
        # eagerly bind anything which might appear at the top level
        # (as there will be no opportunity for late binding)
        if running_in_colab():
            if bind_spec:
                self.spec = self._create_spec()
            if bind_tables:
                if bind_tables is True:
                    self.tables = all_tables(collect=False)
                else:
                    self.tables = all_tables_empty()

    @property
    def config(self) -> dict[str, JsonValue]:
        return self._config

    def _repr_mimebundle_(
        self, **kwargs: Any
    ) -> tuple[dict[str, Any], dict[str, Any]] | None:
        # if we are configured for png output then do that
        if options.output_format == "png" or (
            options.output_format == "auto" and quarto_png()
        ):
            from inspect_viz.plot._write import write_png

            SCALE = 2
            result = write_png(None, self, scale=SCALE)
            if result is not None:
                image_bytes, width, height = result
                b64_data = base64.b64encode(image_bytes).decode("ascii")
                data = {"image/png": b64_data}
                metadata = {
                    "image/png": {"width": width / SCALE, "height": height / SCALE}
                }
                return data, metadata
            else:
                return None

        # standard js output
        else:
            return self._mimebundle(collect=running_in_quarto(), **kwargs)

    def _mimebundle(
        self, *, collect: bool, **kwargs: Any
    ) -> tuple[dict[str, Any], dict[str, Any]] | None:
        # set current tables
        self.tables = all_tables(collect=collect)

        # ensure spec
        if not self.spec:
            self.spec = self._create_spec()

        return super()._repr_mimebundle_(**kwargs)

    _esm = WIDGETS_DIR / "mosaic.js"
    _css: str = ""
    _css_base: Path = WIDGETS_DIR / "mosaic.css"
    _css_nouislider: Path = WIDGETS_DIR / "nouislider.css"
    _css_tomselect: Path = WIDGETS_DIR / "tomselect.css"
    _css_tomselect_bs5: Path = WIDGETS_DIR / "tomselect-bs5.css"
    _css_tomselect_viz: Path = WIDGETS_DIR / "tomselect-viz.css"
    _css_quarto: Path = WIDGETS_DIR / "quarto.css"
    _css_aggrid: Path = WIDGETS_DIR / "ag-grid.css"
    _css_tooltips: Path = WIDGETS_DIR / "tooltips.css"
    _css_legend: Path = WIDGETS_DIR / "legend.css"

    tables = TablesData({}).tag(sync=True)
    spec = traitlets.CUnicode("").tag(sync=True)

    def _create_spec(self) -> str:
        from ..plot._defaults import plot_defaults_as_camel

        # base spec
        spec = self._config.copy()

        # add plot defaults
        spec["plotDefaults"] = plot_defaults_as_camel()

        # add current params
        spec["params"] = all_params()

        # to json
        return to_json(spec, exclude_none=True).decode()


def all_tables(*, collect: bool) -> dict[str, str | bytes]:
    all_data: dict[str, str | bytes] = {}
    for data in Data._get_all():
        all_data[data.table] = data._collect_data() if collect else data._get_data()
    return all_data


def all_tables_empty() -> dict[str, str | bytes]:
    all_data: dict[str, str | bytes] = {}
    for data in Data._get_all():
        all_data[data.table] = bytes()
    return all_data


def all_params() -> dict[str, JsonValue]:
    all_params: dict[str, Any] = {}

    for param in VizParam._get_all():
        if isinstance(param.default, datetime):
            all_params[param.id] = dict(select="value", date=param.default.isoformat())
        else:
            all_params[param.id] = dict(select="value", value=param.default)

    for selection in VizSelection._get_all():
        all_params[selection.id] = dict_remove_none(
            dict(
                select=selection.select,
                cross=selection.cross,
                empty=selection.empty,
                include=selection.include,
            )
        )

    return cast(dict[str, JsonValue], to_jsonable_python(all_params, exclude_none=True))
