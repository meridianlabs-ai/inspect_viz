from textwrap import dedent

from IPython.display import HTML, display


def ensure_dependencies() -> None:
    global _loaded_dependencies
    if _loaded_dependencies is False:
        html = dedent("""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/3.0.1/plotly.min.js"></script>
        """)

        display(HTML(html))  # type: ignore

        _loaded_dependencies = True


_loaded_dependencies = False
