import os
from contextlib import contextmanager
from types import SimpleNamespace
from typing import Iterator, Literal, TypedDict

from typing_extensions import Unpack

_VALID_OUTPUT_FORMATS: tuple[Literal["auto", "js", "png", "js+png"], ...] = (
    "auto",
    "js",
    "png",
    "js+png",
)


class OptionsArgs(TypedDict):
    output_format: Literal["auto", "js", "png", "js+png"]


class Options(SimpleNamespace):
    """Inspect Viz global options."""

    output_format: Literal["auto", "js", "png", "js+png"]
    """Output format for components.

    Defaults to "auto", which resolves to "js" (interactive plots and tables)
    in all contexts except Quarto PDF output (which uses "png"). Specify
    "png" to always write static PNG images instead (interactive features will
    be disabled in this case).

    Specify "js+png" for hybrid output in Quarto HTML: a static PNG is
    rendered as a placeholder/fallback and the interactive widget is overlaid
    on top once it loads. If the JS pipeline fails (e.g. CDN blocked), the
    PNG remains visible. Falls back to "png" for Quarto PDF and "js" in
    notebook contexts (where the failure-mode value does not apply).

    The initial value is read from the `INSPECT_VIZ_OUTPUT_FORMAT` environment
    variable when set to one of the valid values; programmatic assignment
    (and `options_context`) still overrides at runtime.
    """


def _initial_output_format() -> Literal["auto", "js", "png", "js+png"]:
    env = os.environ.get("INSPECT_VIZ_OUTPUT_FORMAT", "").strip()
    for v in _VALID_OUTPUT_FORMATS:
        if env == v:
            return v
    return "auto"


options: Options = Options(output_format=_initial_output_format())
"""Inspect Viz global options."""


@contextmanager
def options_context(**kwargs: Unpack[OptionsArgs]) -> Iterator[None]:
    """Context manager for temporarily overriding global options.

    Args:
        **kwargs: Options to override within the context.
    """
    global options
    options_backup = Options(**vars(options))
    try:
        for k, v in kwargs.items():
            setattr(options, k, v)
        yield
    finally:
        options = options_backup
