import base64
import json
import secrets
from datetime import datetime
from pathlib import Path
from typing import Any, Literal, cast

import traitlets
from anywidget import AnyWidget
from pydantic import JsonValue
from pydantic_core import to_json, to_jsonable_python

from .._util.constants import WIDGETS_DIR
from .._util.marshall import dict_remove_none
from .._util.platform import (
    quarto_execute_info,
    quarto_png,
    running_in_colab,
    running_in_quarto,
)
from ._options import options
from .data import Data
from .param import Param as VizParam
from .selection import Selection as VizSelection


class TablesData(traitlets.TraitType[dict[str, bytes | str], dict[str, bytes | str]]):
    """Custom traitlet for handling multiple table/data pairs.

    Each value is either bytes (shipped as a binary buffer via ipywidgets'
    comm layer — no base64) or a URL string pointing to a Quarto
    `site_data/immutable/` asset the browser will fetch.
    """

    info_text = "a dict of table names to data bytes or URL strings"

    def validate(self, obj: Any, value: Any) -> dict[str, bytes | str]:
        if not isinstance(value, dict):
            self.error(obj, value)

        normalized: dict[str, bytes | str] = {}
        for key, data in value.items():
            if isinstance(data, bytes):
                normalized[key] = data
            elif isinstance(data, (bytearray, memoryview)):
                normalized[key] = bytes(data)
            elif isinstance(data, str):
                normalized[key] = data
            else:
                self.error(obj, value)

        return normalized


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

        # Quarto HTML render: emit pure text/html so Quarto does not detect a
        # Jupyter widget MIME and auto-inject the ~3.5 MB embed-amd.js bundle.
        if running_in_quarto():
            self.tables = all_tables(collect=True)
            if not self.spec:
                self.spec = self._create_spec()
            return {"text/html": self._quarto_html()}, {}

        # Notebook / Colab / live-kernel: standard anywidget output.
        return self._mimebundle(collect=False, **kwargs)

    def _mimebundle(
        self, *, collect: bool, **kwargs: Any
    ) -> tuple[dict[str, Any], dict[str, Any]] | None:
        # set current tables
        self.tables = all_tables(collect=collect)

        # ensure spec
        if not self.spec:
            self.spec = self._create_spec()

        return super()._repr_mimebundle_(**kwargs)

    # Per-document state: only the first widget on a given document carries
    # the full ESM + CSS; subsequent widgets reference them by DOM id.
    _quarto_assets_embedded_for_doc: "str | None" = None

    def _placeholder_info(self) -> dict[str, Any] | None:
        """Info for constructing a loading placeholder, or None to skip.

        Returns `{"w", "h", "legend_kind", "prefix_height"}`:
        - `w`, `h`: plot spec dimensions.
        - `legend_kind`: `"none"` / `"inset"` / `"horizontal"` / `"vertical"`.
        - `prefix_height`: pixels to reserve above the plot for input rows
          and vspace gaps (for `vconcat(*inputs, vspace(), plot)` layouts).

        Handles three top-level shapes:
        1. Plain plot — `{"plot": ...}`.
        2. Plot + legend — `{"hconcat": [{"plot": ...}, {"legend": ...}]}`.
        3. Inputs + plot — `{"vconcat": [{"input": ...}, ..., {"vspace": ...},
           {"plot": ...} OR {"hconcat": [{"plot": ...}, {"legend": ...}]}]}`.

        Returns None for non-plot widgets (standalone inputs/tables/legends),
        unclassifiable specs, and Quarto dashboard output.
        """
        info = quarto_execute_info()
        if info is not None:
            try:
                if info["format"]["identifier"]["base-format"] == "dashboard":
                    return None
            except (KeyError, TypeError):
                pass

        try:
            spec = json.loads(self.spec) if isinstance(self.spec, str) else None
        except json.JSONDecodeError:
            return None
        if not isinstance(spec, dict):
            return None

        plot_node, siblings, prefix_height, suffix_height = _find_plot_node(spec)
        if plot_node is None:
            return None

        w = plot_node.get("width")
        h = plot_node.get("height")
        if not w or not h:
            defaults = spec.get("plotDefaults")
            if isinstance(defaults, dict):
                w = w if w else defaults.get("width")
                h = h if h else defaults.get("height")
        if not w or not h:
            return None

        # Classify the most-space-intrusive legend sibling.
        legend_kind = "none"
        rank = {"none": 0, "inset": 1, "vertical": 2, "horizontal": 3}
        for sib in siblings:
            if "legend" not in sib:
                continue
            anchor = sib.get("_frame_anchor") or ""
            if anchor in ("left", "right"):
                kind = "horizontal"
            elif anchor in ("top", "bottom"):
                kind = "vertical"
            else:
                kind = "inset"
            if rank[kind] > rank[legend_kind]:
                legend_kind = kind

        try:
            return {
                "w": int(w),
                "h": int(h),
                "legend_kind": legend_kind,
                "prefix_height": prefix_height,
                "suffix_height": suffix_height,
            }
        except (TypeError, ValueError):
            return None

    def _quarto_html(self, tables_override: dict[str, bytes] | None = None) -> str:
        """Self-contained HTML output for a single widget.

        Used for two paths:
        - Quarto HTML render (`tables_override=None`): `self.tables` carries
          URL strings pointing to `site_data/immutable/<hash>.arrow` assets.
        - PNG / `to_html` (`tables_override={name: bytes}`): bytes get
          base64-inlined so Playwright can render in a file:// context.

        The first widget on each document inlines the widget ESM (our
        `mosaic.js` bundle) and merged CSS inside `<script id="iv-esm">`
        and `<style id="iv-css">` blocks. Subsequent widgets reference them
        by id so the ESM text appears once per page.
        """
        widget_id = f"iv-{secrets.token_hex(8)}"

        # PNG / to_html paths bypass the per-doc dedup — each invocation
        # is a fresh, self-contained snippet and needs its own assets block.
        if tables_override is not None:
            include_assets = True
        else:
            info = quarto_execute_info()
            doc_path = info["document-path"] if info else ""
            include_assets = Component._quarto_assets_embedded_for_doc != doc_path
            if include_assets:
                Component._quarto_assets_embedded_for_doc = doc_path

        # Normalise `tables`: URL strings pass through; bytes get base64-
        # encoded for inlining. The bootstrap decodes to DataView at load.
        tables_source: dict[str, bytes | str] = (
            cast(dict[str, bytes | str], tables_override)
            if tables_override is not None
            else self.tables
        )
        tables_payload: dict[str, JsonValue] = {}
        for name, val in tables_source.items():
            if isinstance(val, bytes):
                tables_payload[name] = {
                    "__iv_bytes__": True,
                    "data": base64.b64encode(val).decode("ascii"),
                }
            else:
                tables_payload[name] = val

        state_json = json.dumps(
            {"spec": self.spec, "tables": tables_payload},
            separators=(",", ":"),
        ).replace("</", "<\\/")

        assets = ""
        if include_assets:
            esm_text = _escape_script_content((WIDGETS_DIR / "mosaic.js").read_text())
            css_text = _escape_script_content(Component._css or "")

            assets_parts = []
            if css_text.strip():
                assets_parts.append(f'<style id="iv-css">{css_text}</style>')
            assets_parts.append(
                f'<script id="iv-esm" type="text/plain">{esm_text}</script>'
            )
            assets = "".join(assets_parts)

        # Reserve placeholder space so the plot doesn't "snap in" when it
        # finishes loading. The placeholder DOM mirrors the plot's eventual
        # layout (flex row/column with plot + optional legend sibling) so the
        # browser computes a height that matches the rendered SVG's height at
        # the current column width. The bootstrap then pins that height as
        # `min-height` on the widget div so Mosaic's `innerHTML = ''` inside
        # `render()` doesn't collapse the widget while the SVG is being built.
        # A MutationObserver clears the pin on SVG insertion.
        placeholder_info = self._placeholder_info()
        placeholder_inner = _placeholder_inner_html(placeholder_info)

        bootstrap = f"""<script type="module">
(() => {{
  const state = {state_json};
  for (const k in state.tables) {{
    const v = state.tables[k];
    if (v && typeof v === 'object' && v.__iv_bytes__) {{
      const bin = atob(v.data);
      const bytes = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
      state.tables[k] = new DataView(bytes.buffer);
    }}
  }}
  const el = document.getElementById({json.dumps(widget_id)});
  const model = {{
    get: k => state[k], set: () => {{}}, on: () => {{}}, off: () => {{}},
    save_changes: () => {{}}, send: () => {{}}, widget_manager: null,
  }};
  window.__inspectVizHost = window.__inspectVizHost || (async () => {{
    const esmEl = document.getElementById('iv-esm');
    if (!esmEl) throw new Error('inspect-viz ESM block not found');
    const url = URL.createObjectURL(new Blob([esmEl.textContent], {{type:'text/javascript'}}));
    const mod = await import(url);
    URL.revokeObjectURL(url);
    return typeof mod.default === 'function' ? await mod.default() : mod.default;
  }})();
  if (el.firstElementChild && el.firstElementChild.dataset.ivPlaceholder) {{
    // Pin the browser-computed placeholder height so Mosaic's innerHTML=''
    // can't collapse the widget during the async render window. The pin is
    // a floor (min-height), not a cap: if the final rendered content is
    // taller, the widget grows naturally; if shorter, the pin holds at the
    // reserved height so content below stays put. The widget div already
    // carries `.mosaic-widget` from the initial HTML so its 10 px margin-top
    // / 0.5 rem margin-bottom are baked into the document flow before the
    // pin is measured — Mosaic's own `classList.add('mosaic-widget')` later
    // becomes a no-op and no layout shift occurs when it runs.
    const pinH = el.clientHeight;
    if (pinH > 0) el.style.minHeight = pinH + 'px';
  }}
  window.__inspectVizHost
    .then(w => w.render({{model, el}}))
    .catch(e => console.error('inspect-viz render failed', e));
}})();
</script>"""

        return (
            f"{assets}"
            f'<div id="{widget_id}" class="lm-Widget jupyter-widgets-disconnected mosaic-widget">{placeholder_inner}</div>'
            f"{bootstrap}"
        )

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


# Per-kind flex-basis estimates for external legends. Tuned against an
# observed horizontal-legend page (557 px widget, 451 px plot, 55 px legend +
# 51 px flex gap = 106 px → round up to 110 px). Vertical legends add roughly
# one line of labels plus padding. If legends in practice differ from these
# estimates by ±30 px the placeholder will over/under-reserve by ~15 px,
# which is an acceptable layout-shift budget.
_HORIZONTAL_LEGEND_PX = 110
_VERTICAL_LEGEND_PX = 35

# Height estimate per input row (select, checkbox_group, etc.) when a widget
# wraps its plot in `vconcat(*inputs, vspace(), plot)` — inspect-viz views
# like `scores_timeline` do this. Structural breakdown:
#   - Bootstrap form control (.form-select / .form-control) is ~38 px:
#     16 px font × 1.5 line-height + 12 px vertical padding + 2 px border.
#   - `.mosaic-widget label { margin-bottom: 10px }` in `mosaic.css` adds
#     another 10 px below each label.
# Total ≈ 48 px. The release logic uses a tolerance window so being within
# a few px of final height doesn't hold the pin longer than needed.
_INPUT_ROW_PX = 48

# Default vspace height if a `vspace()` entry's `vspace` value can't be
# parsed as an integer (matches the helper's own default).
_VSPACE_DEFAULT_PX = 10


def _find_plot_node(
    spec: dict[str, Any],
) -> tuple[dict[str, Any] | None, list[dict[str, Any]], int, int]:
    """Locate the plot node within a top-level widget spec.

    Returns `(plot_node, legend_siblings, prefix_height, suffix_height)`:
    - `plot_node`: the dict whose `"plot"` key holds the marks, or None.
    - `legend_siblings`: legend dicts sharing the plot's hconcat row.
    - `prefix_height`: pixels to reserve *above* the plot for input rows +
      vspace gaps that appear before the plot inside a top-level vconcat.
    - `suffix_height`: same, for inputs / vspace *below* the plot (when the
      user writes `vconcat(plot, vspace(), *inputs)`).

    Both are zero when the plot sits at top level or in a plain hconcat.
    """
    # Case 1: plot at top level.
    if "plot" in spec:
        return spec, [], 0, 0

    # Case 2: hconcat of plot + optional legends.
    hconcat = spec.get("hconcat")
    if (
        isinstance(hconcat, list)
        and len(hconcat) >= 1
        and isinstance(hconcat[0], dict)
        and "plot" in hconcat[0]
    ):
        siblings = [s for s in hconcat[1:] if isinstance(s, dict)]
        return hconcat[0], siblings, 0, 0

    # Case 3: vconcat — plot may be anywhere (inputs above and/or below).
    vconcat = spec.get("vconcat")
    if isinstance(vconcat, list):
        plot_idx: int | None = None
        plot_node: dict[str, Any] | None = None
        v_siblings: list[dict[str, Any]] = []

        # First pass: find the plot's index in the vconcat.
        for i, item in enumerate(vconcat):
            if not isinstance(item, dict):
                continue
            if "plot" in item:
                plot_idx = i
                plot_node = item
                break
            if "hconcat" in item:
                sub = item.get("hconcat")
                if (
                    isinstance(sub, list)
                    and len(sub) >= 1
                    and isinstance(sub[0], dict)
                    and "plot" in sub[0]
                ):
                    plot_idx = i
                    plot_node = sub[0]
                    v_siblings = [s for s in sub[1:] if isinstance(s, dict)]
                    break

        if plot_node is None or plot_idx is None:
            return None, [], 0, 0

        # Second pass: sum input/vspace heights on each side of the plot.
        prefix_h = 0
        suffix_h = 0
        for i, item in enumerate(vconcat):
            if i == plot_idx or not isinstance(item, dict):
                continue
            add = 0
            if "input" in item:
                add = _INPUT_ROW_PX
            elif "vspace" in item:
                try:
                    add = int(item["vspace"])
                except (TypeError, ValueError):
                    add = _VSPACE_DEFAULT_PX
            if i < plot_idx:
                prefix_h += add
            else:
                suffix_h += add

        return plot_node, v_siblings, prefix_h, suffix_h

    return None, [], 0, 0


def _placeholder_inner_html(info: dict[str, Any] | None) -> str:
    """Build the responsive placeholder DOM that goes inside the widget div.

    Shapes by legend kind:

    - `"none"` / `"inset"`: a single `aspect-ratio` child that sizes itself
      from the widget's width (plot fills widget, no legend sibling space).
    - `"horizontal"`: a flex row with a `flex:1` aspect-ratio plot sibling +
      a fixed-width legend spacer; widget height = plot-placeholder height.
    - `"vertical"`: a flex column with an aspect-ratio plot sibling + a
      fixed-height legend spacer; widget height = plot + spacer.

    Each aspect-ratio plot child also has `max-width: {specW}px` so the
    placeholder stops growing at the plot's natural (spec) width — mirroring
    Observable Plot's output which uses `max-width: 100%` on an SVG whose
    width attribute is the spec width. Without this cap, on wide columns
    our placeholder would keep growing even though the rendered plot caps
    at its spec dimensions.

    Every element is tagged with `data-iv-placeholder` so the bootstrap can
    detect whether a placeholder is present.
    """
    if info is None:
        return ""
    w, h = info["w"], info["h"]
    kind = info["legend_kind"]
    prefix_h = info.get("prefix_height", 0)
    suffix_h = info.get("suffix_height", 0)

    plot_aspect = f"aspect-ratio:{w} / {h}"
    shimmer = '<div class="iv-loading"></div>'

    # "Plot row": the element(s) occupying the plot's horizontal band.
    if kind == "horizontal":
        plot_row = (
            '<div style="display:flex;align-items:flex-start">'
            f'<div style="flex:1 1 0;min-width:0;{plot_aspect}"></div>'
            f'<div style="flex:0 0 {_HORIZONTAL_LEGEND_PX}px"></div>'
            "</div>"
        )
        outer_max = w + _HORIZONTAL_LEGEND_PX
    else:
        # "none" / "inset" / "vertical" — plot fills the row; vertical legend
        # is handled as a separate sibling below.
        plot_row = f'<div style="{plot_aspect}"></div>'
        outer_max = w

    prefix = f'<div style="flex:0 0 {prefix_h}px"></div>' if prefix_h > 0 else ""
    suffix = f'<div style="flex:0 0 {suffix_h}px"></div>' if suffix_h > 0 else ""
    vertical_legend = (
        f'<div style="flex:0 0 {_VERTICAL_LEGEND_PX}px"></div>'
        if kind == "vertical"
        else ""
    )

    # If the placeholder is just the plot (no prefix/suffix, no vertical
    # legend), use the single aspect-ratio root. Otherwise wrap in a flex
    # column that stacks prefix + plot + legend/suffix.
    if not prefix and not suffix and kind != "vertical":
        return (
            '<div data-iv-placeholder="1" '
            f'style="{plot_aspect};max-width:{w}px;position:relative">'
            f"{shimmer}</div>"
            if kind != "horizontal"
            else '<div data-iv-placeholder="1" '
            f'style="display:flex;align-items:flex-start;'
            f'max-width:{outer_max}px;position:relative">'
            f'<div style="flex:1 1 0;min-width:0;{plot_aspect}"></div>'
            f'<div style="flex:0 0 {_HORIZONTAL_LEGEND_PX}px"></div>'
            f"{shimmer}"
            "</div>"
        )

    return (
        '<div data-iv-placeholder="1" '
        f'style="display:flex;flex-direction:column;'
        f'max-width:{outer_max}px;position:relative">'
        f"{prefix}{plot_row}{vertical_legend}{suffix}{shimmer}"
        "</div>"
    )


def _escape_script_content(text: str) -> str:
    r"""Escape ``</`` sequences so they don't close an enclosing tag.

    HTML parsers look for the literal ``</`` bytes when scanning for the end
    of a ``<script>`` or ``<style>`` block. Replacing ``</`` with ``<\/`` is
    safe inside both JavaScript and JSON bodies.
    """
    return text.replace("</", "<\\/")


def all_tables(*, collect: bool) -> dict[str, bytes | str]:
    all_data: dict[str, bytes | str] = {}
    for data in Data._get_all():
        all_data[data.table] = data._collect_data() if collect else data._get_data()
    return all_data


def all_tables_empty() -> dict[str, bytes | str]:
    all_data: dict[str, bytes | str] = {}
    for data in Data._get_all():
        # match the payload shape: URL-backed → empty string, bytes-backed → empty bytes
        payload = data._get_data()
        all_data[data.table] = "" if isinstance(payload, str) else b""
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
