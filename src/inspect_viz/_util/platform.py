import json
import os
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
