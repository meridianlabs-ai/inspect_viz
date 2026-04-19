import json
import os
import re
import shutil
from pathlib import Path
from typing import cast

from typing_extensions import TypedDict

from inspect_viz._util.notgiven import NOT_GIVEN, NotGiven


def running_in_quarto() -> bool:
    return "QUARTO_FIG_WIDTH" in os.environ.keys()


def quarto_png() -> bool:
    if running_in_quarto():
        execute_info = quarto_execute_info()
        if execute_info is not None:
            return execute_info["format"]["identifier"]["base-format"] not in [
                "html",
                "html4",
                "html5",
                "dashboard",
            ]
        else:
            return os.environ.get("QUARTO_FIG_FORMAT", "") in ["pdf", "svg"]
    else:
        return False


QuartoFormatIdentifier = TypedDict(
    "QuartoFormatIdentifier",
    {"display-name": str, "target-format": str, "base-format": str},
)

QuartoFormat = TypedDict("QuartoFormat", {"identifier": QuartoFormatIdentifier})


QuartoExecuteInfo = TypedDict(
    "QuartoExecuteInfo", {"document-path": str, "format": QuartoFormat}
)

_quarto_execute_info: QuartoExecuteInfo | None | NotGiven = NOT_GIVEN


def quarto_execute_info() -> QuartoExecuteInfo | None:
    global _quarto_execute_info
    if isinstance(_quarto_execute_info, NotGiven):
        execute_info_file = os.environ.get("QUARTO_EXECUTE_INFO", "")
        if execute_info_file:
            _quarto_execute_info = cast(
                QuartoExecuteInfo, json.load(open(execute_info_file))
            )
        else:
            _quarto_execute_info = None
    return _quarto_execute_info


def quarto_immutable_target() -> tuple[Path, str] | None:
    """Return `(absolute_dir, url_prefix)` for inspect-viz immutable assets.

    - `absolute_dir` is the on-disk directory where the content-hashed arrow
      file should be written.
    - `url_prefix` is a URL prefix (no filename) relative to the rendered
      HTML — the caller appends `<hash>.arrow`.

    Under a project render we write to `<output-dir>/site_data/immutable/`
    directly (site-global, dedup across docs) and the URL uses a depth-aware
    `../` prefix. Under a single-doc render we fall back to the per-doc
    `<doc-stem>_files/site_data/immutable/` layout. Returns None outside a
    Quarto render.

    The `site_data/` naming follows the precedent of Quarto's `site_libs/`
    directory. The `/immutable/` subpath signals to HTTP caches that these
    files are content-addressed and safe to `Cache-Control: immutable`.
    """
    info = quarto_execute_info()
    if info is None:
        return None
    doc_path = Path(info["document-path"])

    # project render: site-global dir with depth-aware relative URL
    project_dir_str = os.environ.get("QUARTO_PROJECT_DIR")
    if project_dir_str:
        project_dir = Path(project_dir_str)
        try:
            rel_parent = doc_path.relative_to(project_dir).parent
        except ValueError:
            rel_parent = None
        if rel_parent is not None:
            output_dir_name = _quarto_project_output_dir(project_dir)
            if output_dir_name is not None:
                absolute_dir = project_dir / output_dir_name / "site_data" / "immutable"
                prefix = "../" * len(rel_parent.parts)
                return absolute_dir, f"{prefix}site_data/immutable/"

    # single-doc render fallback: per-doc _files/ next to the source
    stem = doc_path.stem
    absolute_dir = doc_path.parent / f"{stem}_files" / "site_data" / "immutable"
    return absolute_dir, f"{stem}_files/site_data/immutable/"


_QUARTO_OUTPUT_DIR_RE = re.compile(r"^\s*output-dir:\s*(.+?)\s*$", re.MULTILINE)
_QUARTO_BOOK_TYPE_RE = re.compile(r"^\s*type:\s*book\b", re.MULTILINE)


def _quarto_project_output_dir(project_dir: Path) -> str | None:
    """Read `project.output-dir` from `_quarto.yml` (regex-parsed, no pyyaml dep).

    Returns the directory name (e.g. `_site`), or None if no Quarto project
    config exists. Defaults to `_book` for book projects and `_site` for
    everything else when `output-dir` is not explicit.
    """
    for name in ("_quarto.yml", "_quarto.yaml"):
        yml_path = project_dir / name
        if not yml_path.exists():
            continue
        text = yml_path.read_text()
        m = _QUARTO_OUTPUT_DIR_RE.search(text)
        if m:
            val = m.group(1).strip().strip('"').strip("'")
            return val or None
        if _QUARTO_BOOK_TYPE_RE.search(text):
            return "_book"
        # website or custom project types default to _site
        return "_site"
    return None


def quarto_placeholder_target() -> tuple[Path, str] | None:
    """Return `(absolute_dir, url_prefix)` for per-doc placeholder PNGs.

    Unlike `quarto_immutable_target()` (which uses a site-global
    `site_data/immutable/` dir so multiple docs can share data assets), this
    always lays out under the per-doc `<doc-stem>_files/placeholder/` dir:
    PNG placeholders are specific to a document's rendered layout (column
    width, legend position, etc.) and aren't usefully shared across pages.

    Under a project render we write to
    `<output-dir>/<rel-parent>/<stem>_files/placeholder/`; under a single-doc
    render we write source-adjacent to `<stem>_files/placeholder/`. The URL
    prefix is always `<stem>_files/placeholder/` since the rendered HTML is
    co-located with its `_files` directory. Returns None outside a Quarto
    render.
    """
    info = quarto_execute_info()
    if info is None:
        return None
    doc_path = Path(info["document-path"])
    stem = doc_path.stem
    url_prefix = f"{stem}_files/placeholder/"

    # project render: write into <output-dir>/<rel-parent>/<stem>_files/placeholder/
    project_dir_str = os.environ.get("QUARTO_PROJECT_DIR")
    if project_dir_str:
        project_dir = Path(project_dir_str)
        try:
            rel_parent = doc_path.relative_to(project_dir).parent
        except ValueError:
            rel_parent = None
        if rel_parent is not None:
            output_dir_name = _quarto_project_output_dir(project_dir)
            if output_dir_name is not None:
                absolute_dir = (
                    project_dir
                    / output_dir_name
                    / rel_parent
                    / f"{stem}_files"
                    / "placeholder"
                )
                return absolute_dir, url_prefix

    # single-doc fallback: source-adjacent _files/
    absolute_dir = doc_path.parent / f"{stem}_files" / "placeholder"
    return absolute_dir, url_prefix


def quarto_theme_font_css() -> str | None:
    """Compose CSS so a Playwright capture renders fonts like the live Quarto page.

    Tries two sources in order:

    1. The project's compiled Bootstrap CSS at
       `<output-dir>/site_libs/bootstrap/bootstrap-*.min.css`. Most accurate
       since it reflects any user SCSS overrides, but only available after
       Quarto has compiled the theme (i.e. usually not on the very first
       render of a clean project).
    2. The Quarto installation's bootswatch theme SCSS at
       `<share>/formats/html/bootstrap/themes/<theme>.scss`. Handles the
       chicken-and-egg case before the compiled CSS exists.

    Returns the composed CSS string, or None if neither source is available
    (callers should fall back to a built-in system-ui default).
    """
    css = _font_css_from_compiled_bootstrap()
    if css:
        return css
    return _font_css_from_install_theme()


_COMPILED_IMPORT_RE = re.compile(r'@import\s+(?:url\()?["\']([^"\']+)["\']\)?\s*;?')
_COMPILED_BODY_FONT_RE = re.compile(r"--bs-body-font-family:\s*([^;]+);")


def _font_css_from_compiled_bootstrap() -> str | None:
    info = quarto_execute_info()
    if info is None:
        return None
    project_dir_str = os.environ.get("QUARTO_PROJECT_DIR")
    if project_dir_str:
        project_dir = Path(project_dir_str)
        output_dir_name = _quarto_project_output_dir(project_dir)
        if output_dir_name is None:
            return None
        search_dir = project_dir / output_dir_name / "site_libs" / "bootstrap"
    else:
        # Single-doc render: site_libs lives next to the rendered HTML.
        doc_path = Path(info["document-path"])
        search_dir = doc_path.parent / "site_libs" / "bootstrap"
    if not search_dir.exists():
        return None
    candidates = sorted(search_dir.glob("bootstrap-*.min.css"))
    if not candidates:
        return None
    try:
        text = candidates[0].read_text()
    except (OSError, UnicodeError):
        return None
    body_match = _COMPILED_BODY_FONT_RE.search(text)
    if not body_match:
        return None
    body_font = body_match.group(1).strip()
    imports = _COMPILED_IMPORT_RE.findall(text)
    parts = [f'@import url("{imp}");' for imp in imports]
    parts.append(f"html, body {{ font-family: {body_font}; font-size: 16px; }}")
    return "\n".join(parts)


_SCSS_WEB_FONT_RE = re.compile(r'\$web-font-path:\s*"([^"]+)"')
_SCSS_SANS_RE = re.compile(
    r"\$font-family-sans-serif:\s*([^;!]+?)\s*(?:!default)?\s*;",
    re.DOTALL,
)


def _font_css_from_install_theme() -> str | None:
    share_dir = _quarto_share_dir()
    if share_dir is None:
        return None
    theme_name = _quarto_project_theme_name()
    if theme_name is None:
        return None
    theme_scss = (
        share_dir / "formats" / "html" / "bootstrap" / "themes" / f"{theme_name}.scss"
    )
    if not theme_scss.exists():
        return None
    try:
        text = theme_scss.read_text()
    except (OSError, UnicodeError):
        return None
    sans_match = _SCSS_SANS_RE.search(text)
    if not sans_match:
        return None
    parts: list[str] = []
    web_font_match = _SCSS_WEB_FONT_RE.search(text)
    if web_font_match:
        parts.append(f'@import url("{web_font_match.group(1)}");')
    sans_value = " ".join(sans_match.group(1).split())
    parts.append(f"html, body {{ font-family: {sans_value}; font-size: 16px; }}")
    return "\n".join(parts)


def _quarto_share_dir() -> Path | None:
    """Locate the Quarto installation's `share/` directory.

    Tries `QUARTO_SHARE_PATH` (set by Quarto during render), then derives
    from `which quarto` (works for both pip-installed `quarto_cli` and
    the standalone macOS install), then a known-default location.
    """
    env = os.environ.get("QUARTO_SHARE_PATH")
    if env:
        p = Path(env)
        if p.exists():
            return p
    quarto_bin = shutil.which("quarto")
    if quarto_bin:
        derived = Path(quarto_bin).resolve().parent.parent / "share"
        if derived.exists():
            return derived
    standalone = Path("/Applications/quarto/share")
    if standalone.exists():
        return standalone
    return None


_THEME_KEY_RE = re.compile(r"^\s*theme:\s*(.+?)\s*$", re.MULTILINE)


def _quarto_project_theme_name() -> str | None:
    """Find the bootswatch theme name from project / extension YAML.

    Scans `_quarto.yml` and any `_extension.yml` files under `_extensions/`
    for a `theme:` key. Theme value can be a bare name (`cosmo`), a quoted
    string (`"cosmo"`), or a list (`[cosmo, resources/theme.scss]`); we pick
    the first non-`.scss`/`.css` token.
    """
    project_dir_str = os.environ.get("QUARTO_PROJECT_DIR")
    if not project_dir_str:
        return None
    project_dir = Path(project_dir_str)
    yaml_paths: list[Path] = []
    for name in ("_quarto.yml", "_quarto.yaml"):
        p = project_dir / name
        if p.exists():
            yaml_paths.append(p)
    ext_dir = project_dir / "_extensions"
    if ext_dir.exists():
        yaml_paths.extend(ext_dir.rglob("_extension.yml"))
        yaml_paths.extend(ext_dir.rglob("_extension.yaml"))
    for yp in yaml_paths:
        try:
            text = yp.read_text()
        except (OSError, UnicodeError):
            continue
        m = _THEME_KEY_RE.search(text)
        if not m:
            continue
        val = m.group(1).strip().strip("[]")
        for token in val.split(","):
            token = token.strip().strip('"').strip("'")
            if not token:
                continue
            if token.endswith(".scss") or token.endswith(".css"):
                continue
            return token
    return None


def quarto_fig_size() -> tuple[int, int] | None:
    if running_in_quarto():
        fig_width = os.environ.get("QUARTO_FIG_WIDTH", "")
        fig_height = os.environ.get("QUARTO_FIG_HEIGHT", "")
        if fig_width and fig_height:
            return (int(float(fig_width) * 96), int(float(fig_height) * 96))

    return None


def running_in_colab() -> bool:
    try:
        import google.colab  # type: ignore # noqa: F401

        return True
    except ImportError:
        return False


def running_in_notebook() -> bool:
    try:
        from IPython import get_ipython  # type: ignore

        if "IPKernelApp" not in get_ipython().config:  # type: ignore
            return False
    except ImportError:
        return False
    except AttributeError:
        return False
    return True
