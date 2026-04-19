import subprocess
import sys
import tempfile
from contextlib import asynccontextmanager
from io import BytesIO
from pathlib import Path
from typing import Any, AsyncIterator

from PIL import Image, ImageOps
from typing_extensions import overload

from inspect_viz._core.data import Data
from inspect_viz._util._async import current_async_backend, run_coroutine
from inspect_viz._util.platform import quarto_theme_font_css

from .. import Component

# Font fallback used when no Quarto theme font CSS is available — keeps
# Playwright captures from rendering plot text in headless Chromium's bundled
# serif default. We override only `font-family`; injecting an explicit
# `font-size` makes Plot's `<text>` elements inherit a larger size than the
# live widget would and the rendered plot grows on both axes.
_DEFAULT_FONT_CSS = (
    "html, body { "
    'font-family: system-ui, -apple-system, "Segoe UI", Roboto, '
    '"Helvetica Neue", "Noto Sans", "Liberation Sans", Arial, sans-serif; '
    "}"
)


def to_html(
    component: Component,
    dependencies: bool = True,
    *,
    extra_head: str = "",
) -> str:
    """Generate a self-contained HTML snippet for a plot or other component.

    The returned snippet embeds the inspect-viz widget ESM plus a small
    bootstrap inline — no external Jupyter-widget (`embed-amd.js`,
    `requirejs`, `jquery`) dependencies. Suitable for Playwright headless
    rendering (`write_png`) and general embedding.

    Args:
       component: Component to export.
       dependencies: Accepted for backward compatibility; the returned
          snippet is always self-contained, so this parameter has no
          effect.
       extra_head: Optional HTML to inject inside the document `<head>`
          (e.g. a `<style>` block setting the page font so the rendered
          plot inherits it).
    """
    del dependencies  # snippet is always self-contained

    # Populate widget state (tables + spec).
    component._mimebundle(collect=False)

    # Under Quarto render, `_mimebundle` set tables to URL strings pointing
    # at `site_data/immutable/*.arrow` — unreachable from a Playwright
    # file:// temp page. Force inline-bytes for every tracked Data so the
    # snippet renders in isolation.
    tables_bytes: dict[str, bytes] = {
        data.table: data._data for data in Data._get_all() if data._data
    }
    snippet = component._quarto_html(tables_override=tables_bytes)
    return (
        "<!doctype html><html><head>"
        '<meta charset="utf-8">'
        f"{extra_head}"
        f"</head><body>{snippet}</body></html>"
    )


def write_html(
    file: str | Path, component: Component, dependencies: bool = True
) -> None:
    """Write an HTML file for a plot or other component.

    Args:
       file: Target filename.
       component: Compontent to export.
       dependencies: Include JavaScript dependencies required for Jupyter widget rendering.
          Dependencies should only be included once per web-page, so if you already have
          them on a page you might want to disable including them when generating HTML.
    """
    with open(file, "w") as f:
        f.write(to_html(component, dependencies))


@overload
def write_png(
    file: None, component: Component, scale: int = 2, padding: int = 8
) -> tuple[bytes, int, int] | None: ...


@overload
def write_png(
    file: str | Path, component: Component, scale: int = 2, padding: int = 8
) -> tuple[int, int] | None: ...


def write_png(
    file: str | Path | None, component: Component, scale: int = 2, padding: int = 8
) -> tuple[bytes, int, int] | tuple[int, int] | None:
    """Export a plot or table to a PNG.

    Args:
       file: Target filename (pass `None` to return the image as bytes)
       component: Component to export.
       scale: Device scale to capture plot at. Use 2 (the default) for retina quality images suitable for high resolution displays or print output)
       padding: Padding (in pixels) around plot.

    Returns:
       Tuple with (width, height) of image or (bytes,width,height) of image if no `file` was passed. Returns `None` if no image was saved.
    """
    if current_async_backend() == "trio":
        raise RuntimeError("Use write_png_async() when running under trio")

    return run_coroutine(write_png_async(file, component, scale, padding))


@overload
async def write_png_async(
    file: None, component: Component, scale: int = 2, padding: int = 8
) -> tuple[bytes, int, int] | None: ...


@overload
async def write_png_async(
    file: str | Path, component: Component, scale: int = 2, padding: int = 8
) -> tuple[int, int] | None: ...


async def write_png_async(
    file: str | Path | None, component: Component, scale: int = 2, padding: int = 8
) -> tuple[bytes, int, int] | tuple[int, int] | None:
    """Export a plot or table to a PNG.

    Args:
       file: Target filename (pass `None` to return the image as bytes)
       component: Component to export.
       scale: Device scale to capture plot at. Use 2 (the default) for retina quality images suitable for high resolution displays or print output)
       padding: Padding (in pixels) around plot.

    Returns:
       Tuple with (width, height) of image or (bytes,width,height) of image if no `file` was passed. Returns `None` if no image was saved.
    """
    # Pick up the Quarto site's theme fonts when available so the captured
    # PNG matches what the live widget renders; fall back to a system-ui
    # stack so headless Chromium doesn't fall through to its serif default.
    theme_font_css = quarto_theme_font_css() or _DEFAULT_FONT_CSS
    # Force the widget element to size to its content rather than fill the
    # viewport, so a locator screenshot of `.mosaic-widget` captures exactly
    # the widget's natural bounds — matching what the live widget will
    # occupy on a Quarto page.
    # - `vertical-align: top` removes the inline-block baseline descender
    #   space (otherwise the captured frame includes a few px of whitespace
    #   above content, which shifts everything down/right when overlaid).
    # - `margin: 0` on `.mosaic-widget` neutralises the 10 px top / 0.5 rem
    #   bottom margins that the class normally applies — the locator capture
    #   uses border-box bounds, but the SVG inside has internal alignment
    #   that can be affected by surrounding flow whitespace.
    # - Resetting `html, body` margin removes any default body padding
    #   contribution to the rendered widget's positioning.
    sizing_css = (
        "html, body { margin: 0; padding: 0; }\n"
        ".mosaic-widget {"
        " display: inline-block; width: auto;"
        " vertical-align: top;"
        " margin: 0;"
        " }"
    )
    # Match the typical Bootswatch theme font smoothing (Cosmo, Flatly,
    # Litera, etc. all apply `-webkit-font-smoothing: antialiased`).
    # Without this, capture text renders with macOS's default subpixel AA
    # (darker) while the live page uses grayscale AA (lighter) — producing
    # a visible lightness shift at the PNG → SVG crossfade. The property
    # is inherited, so it propagates to SVG `<text>` for free. On
    # Linux/Windows these rules are silently ignored.
    font_smoothing_css = (
        "html, body {"
        " -webkit-font-smoothing: antialiased;"
        " -moz-osx-font-smoothing: grayscale;"
        " }"
    )
    extra_head = (
        f"<style>{theme_font_css}\n{font_smoothing_css}\n{sizing_css}</style>"
    )

    with tempfile.NamedTemporaryFile("w", suffix=".html") as temp_file:
        # write the component as HTML
        temp_file.write(to_html(component, extra_head=extra_head))
        temp_file.flush()

        # launch the browser
        async with _with_browser() as b:
            from playwright.async_api import Browser

            # browser can be None if playwright wasn't installed yet
            if not isinstance(b, Browser):
                return None

            # create and load page
            ctx = await b.new_context(device_scale_factor=scale)
            page = await ctx.new_page()
            file_uri = Path(temp_file.name).resolve().as_uri()
            await page.goto(file_uri, wait_until="networkidle")
            await page.wait_for_function(
                '() => !!window.document.querySelector("svg") || !!window.document.querySelector(".inspect-viz-table")',
                polling=100,
            )
            # Wait for any web fonts referenced in `extra_head` (e.g. a
            # Google Font from a Bootswatch theme) to finish loading so the
            # screenshot doesn't capture a fallback-font frame.
            await page.evaluate("() => document.fonts.ready")
            # Give Mosaic's throttled post-render hooks (legend handler,
            # text-collision adjuster, etc., all on a 25 ms throttle) time
            # to finish settling the layout before we capture. Without this
            # the captured PNG can be vertically offset relative to what
            # the live widget eventually renders.
            await page.wait_for_timeout(300)

            # Capture the widget element directly. This gives the exact
            # CSS-box dimensions the live widget will occupy (no overflow
            # text included via cropping; no full-viewport white margins).
            background_color = "white"
            locator = page.locator(".mosaic-widget").first
            image_bytes = await locator.screenshot(
                style="body { background-color: " + background_color + "; }",
            )
            img = Image.open(BytesIO(image_bytes))
            if padding > 0:
                img = ImageOps.expand(img, border=padding * scale, fill=background_color)
            size = img.size
            if file:
                img.save(file, dpi=(scale * 96, scale * 96))
                img.close()
                return size
            else:
                image_buffer = BytesIO()
                img.save(image_buffer, format="PNG")
                img.close()
                return (image_buffer.getvalue(), size[0], size[1])


@asynccontextmanager
async def _with_browser() -> AsyncIterator[Any | None]:
    # ensure we have playwright
    try:
        from playwright.async_api import Error, async_playwright
    except ImportError:
        sys.stderr.write(
            "ERROR: The write_png() function requires the playwright package. Install with:\n\npip install playwright\n\n"
        )
        yield None

    # try to launch the browser
    async with async_playwright() as p:
        # Prefer the user's installed Chrome over the bundled headless
        # Chromium — Chromium ships with a different font stack and
        # different anti-aliasing defaults, so PNGs captured under it can
        # render text noticeably heavier/lighter than what users see in
        # their actual Chrome browser. Falls through to bundled Chromium
        # if Chrome isn't installed.
        browser = None
        try:
            browser = await p.chromium.launch(headless=True, channel="chrome")
        except Error:
            try:
                browser = await p.chromium.launch(headless=True)
            except Error as e:
                if "Executable doesn't exist" in str(e) and sys.stdin.isatty():
                    if _confirm_install():
                        _install()
                        print(
                            "Playwright installed. Please try the write_png() function again."
                        )
                    yield None
                    return
                else:
                    raise e
        try:
            yield browser
        finally:
            await browser.close()


def _confirm_install() -> bool:
    prompt = "Playwright can’t find Chromium, which is required for writing PNG files. Install it now? [Y/n] "
    try:
        reply = input(prompt).strip().lower()
        return reply in {"", "y", "yes"}
    except EOFError:  # e.g. piped stdin
        return False


def _install() -> None:
    """Run the idempotent CLI installer (cheap when up-to-date)."""
    subprocess.run(["playwright", "install", "chromium"], check=True)


