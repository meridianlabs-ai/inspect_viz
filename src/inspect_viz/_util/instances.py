import functools
from typing import Any, Literal, TypeAlias, cast

InstanceType: TypeAlias = Literal["data", "param", "selection"]


INSTANCES_VAR = "__inspect_viz_instances__"


def track_instance(type: InstanceType, o: object) -> None:
    get_instances(type).append(o)


def get_instances(type: InstanceType) -> list[object]:
    instances = _instances()
    if type not in instances:
        instances[type] = list()
    return instances[type]


def _instances() -> dict[InstanceType, list[object]]:
    if INSTANCES_VAR not in globals():
        globals()[INSTANCES_VAR] = {}
        _install_reset_hook()
    return cast(dict[InstanceType, list[object]], globals()[INSTANCES_VAR])


# clear instances when %reset is called (this enables things to work
# correctly when quarto re-executes a notebook in preview mode)
def _install_reset_hook() -> None:
    import IPython

    # IPython is typed in some releases and not others; Any suits both
    shell = cast(Any, IPython).get_ipython()
    if shell is None:
        return  # not running inside IPython
    if getattr(shell, "_inspect_viz_reset_hooked", False):
        return  # already patched

    # hook w/ delegation to original %reset
    original_reset = shell.reset

    @functools.wraps(original_reset)
    def reset_with_cleanup(*args: Any, **kwargs: Any) -> Any:
        out = original_reset(*args, **kwargs)
        if INSTANCES_VAR in globals():
            globals().pop(INSTANCES_VAR)
        return out

    shell.reset = reset_with_cleanup
    shell._inspect_viz_reset_hooked = True
