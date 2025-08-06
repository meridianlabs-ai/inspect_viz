import json
import subprocess
import sys
import tempfile
from contextlib import asynccontextmanager
from io import BytesIO
from pathlib import Path
from textwrap import dedent
from typing import Any, AsyncIterator

import ipywidgets  # type: ignore
from ipywidgets.embed import embed_data, escape_script  # type: ignore
from PIL import Image, ImageChops, ImageOps
from typing_extensions import overload

from inspect_viz._util._async import current_async_backend, run_coroutine

from .. import Component


def to_html(component: Component, dependencies: bool = True) -> str:
    """Genreate an HTML snippet for a plot or other component.

    Args:
       component: Compontent to export.
       dependencies: Include JavaScript dependencies required for Jupyter widget rendering.
          Dependencies should only be included once per web-page, so if you already have
          them on a page you might want to disable including them when generating HTML.
    """
    # realize the widget data and state
    component._mimebundle(collect=False)
    widget_data = embed_data(views=[component], drop_defaults=False)
    widget_state = escape_script(json.dumps(widget_data["manager_state"], indent=2))

    # create views
    widget_view_template = dedent("""
    <script type="application/vnd.jupyter.widget-view+json">
    {view_spec}
    </script>
    """)
    widget_views = "\n".join(
        widget_view_template.format(view_spec=escape_script(json.dumps(view_spec)))
        for view_spec in widget_data["view_specs"]
    )

    # create runtime dependencies
    html_manager_version = ipywidgets._version.__html_manager_version__
    jupyter_dependencies = (
        dedent(f"""

    <!--[jupyter_widget_dependencies]-->
    <script src="https://cdn.jsdelivr.net/npm/requirejs@2.3.6/require.min.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@jupyter-widgets/html-manager@{html_manager_version}/dist/embed-amd.js" crossorigin="anonymous"></script>
    <!--[/jupyter_widget_dependencies]-->
    """)
        if dependencies
        else ""
    )

    return HTML_SNIPPET_TEMPLATE.format(
        dependencies=jupyter_dependencies,
        widget_state=widget_state,
        widget_views=widget_views,
    )


HTML_SNIPPET_TEMPLATE = """
<div>{dependencies}
<script type="application/vnd.jupyter.widget-state+json">
{widget_state}
</script>
{widget_views}
</div>
"""


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
    with tempfile.NamedTemporaryFile("w", suffix=".html") as temp_file:
        # write the component as HTML
        write_html(temp_file.name, component=component)

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

            # eliminate scrolling
            w = await page.evaluate("document.documentElement.scrollWidth")
            h = await page.evaluate("document.documentElement.scrollHeight")
            await page.set_viewport_size({"width": w, "height": h})

            # take screenshot and crop image
            background_color = "white"
            image_bytes = await page.screenshot(
                scale="device",
                style="body { background-color: " + background_color + "; }",
            )
            img = _crop_image(image_bytes, padding, scale, background_color)
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
        try:
            browser = await p.chromium.launch(headless=True)
            try:
                yield browser
            finally:
                await browser.close()
        except Error as e:
            if "Executable doesn't exist" in str(e) and sys.stdin.isatty():
                if _confirm_install():
                    _install()
                    print(
                        "Playwright installed. Please try the write_png() function again."
                    )
                yield None
            else:
                raise e


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


def _crop_image(
    image_bytes: bytes, pad: int, scale: int, background_color: str
) -> Image.Image:
    # open image
    img: Image.Image = Image.open(BytesIO(image_bytes))

    # build an image filled with the background colour of the top-left pixel
    bg = Image.new(img.mode, img.size, background_color)

    # compute difference and locate the bounding box of non-bg pixels
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()  # returns (left, upper, right, lower) or None

    if bbox:
        img_cropped = img.crop(bbox)
        img_fill = img.getpixel((0, 0))

        if img_fill is not None:
            # we read the pixel, resolve the fill_value
            if isinstance(img_fill, float):
                # Convert float (grayscale) to int for compatibility
                img_cropped = ImageOps.expand(
                    img_cropped, border=pad * scale, fill=int(img_fill)
                )
            else:
                img_cropped = ImageOps.expand(
                    img_cropped, border=pad * scale, fill=img_fill
                )
        else:
            # no value for the top left pixel, use background color
            img_cropped = ImageOps.expand(
                img_cropped, border=pad * scale, fill=background_color
            )
        img.close()
        img = img_cropped

    # return image
    return img
