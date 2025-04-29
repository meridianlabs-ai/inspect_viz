from textwrap import dedent

from IPython.display import HTML, display


def ensure_dependencies() -> None:
    global _loaded_dependencies
    if _loaded_dependencies is False:
        html = dedent("""
       
        """)

        display(HTML(html))  # type: ignore

        _loaded_dependencies = True


_loaded_dependencies = False
