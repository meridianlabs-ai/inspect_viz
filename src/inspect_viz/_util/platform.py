import json
import os
import re
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
                absolute_dir = (
                    project_dir / output_dir_name / "site_data" / "immutable"
                )
                prefix = "../" * len(rel_parent.parts)
                return absolute_dir, f"{prefix}site_data/immutable/"

    # single-doc render fallback: per-doc _files/ next to the source
    stem = doc_path.stem
    absolute_dir = doc_path.parent / f"{stem}_files" / "site_data" / "immutable"
    return absolute_dir, f"{stem}_files/site_data/immutable/"


_QUARTO_OUTPUT_DIR_RE = re.compile(
    r"^\s*output-dir:\s*(.+?)\s*$", re.MULTILINE
)
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
