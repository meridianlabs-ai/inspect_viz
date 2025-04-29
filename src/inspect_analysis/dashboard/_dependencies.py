from textwrap import dedent

from IPython.display import HTML, display


def ensure_dependencies() -> None:
    global _loaded_dependencies
    if _loaded_dependencies is False:
        html = dedent("""
        <script>window.backupDefine = window.define; window.define = undefined;</script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/3.0.1/plotly.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/arquero@8.0.1"></script>
        <script>window.define = window.backupDefine; window.backupDefine = undefined;</script>
        """)

        display(HTML(html))  # type: ignore

        _loaded_dependencies = True


_loaded_dependencies = False
