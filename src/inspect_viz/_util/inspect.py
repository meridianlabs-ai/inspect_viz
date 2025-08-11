# This is a file with vendored code from inspect_ai. If we ever can take a dependenchy on that, we should remove this code
from typing import Callable, Mapping, Sequence, Union

CORRECT = "C"
"""Value to assign for correct answers."""

INCORRECT = "I"
"""Value to assign for incorrect answers."""

PARTIAL = "P"
"""Value to assign for partial credit."""

NOANSWER = "N"
"""Value to assign for no answer or refusal to answer."""


Value = Union[
    str | int | float | bool,
    Sequence[str | int | float | bool],
    Mapping[str, str | int | float | bool | None],
]
"""Value provided by a score.

Use the methods of `Score` to easily treat
the `Value` as a simple scalar of various types.
"""

ValueToFloat = Callable[[Value], float]
"""Function used by metrics to translate from a Score value to a float value."""


def value_to_float(
    correct: Value = CORRECT,
    incorrect: Value = INCORRECT,
    partial: Value = PARTIAL,
    noanswer: Value = NOANSWER,
) -> ValueToFloat:
    """Create a ValueToFloat function.

    Create a ValueToFloat function that maps scalar values of
    different types into floats. For strings, common boolean
    representations (e.g. 'yes', 'no', 'true', 'false') are
    mapped to 1 and 0. In addition, the specified correct,
    incorrect, partial, and noanswer values (by default "C"
    "I", "P", and "N") are mapped to 1, 0, 0.5, and 0. Note that
    those are the default literal values, but they can be
    customized. Strings with only numbers are converted, and
    numeric values are cast to float. Arrays and dictionaries
    give a warning and return 0.

    Args:
       correct (Value): Value that represents a correct answer (1)
       incorrect (Value): Value that represents an incorrect answer (0)
       partial (Value): Value to assign partial credit for (0.5)
       noanswer (Value): Value for refusals to answer (0)

    Returns:
        ValueToFloat function.
    """

    def to_float(value: Value) -> float:
        if isinstance(value, int | float | bool):
            return float(value)
        elif value == correct:
            return 1.0
        elif value == partial:
            return 0.5
        elif value == incorrect or value == noanswer:
            return 0
        elif isinstance(value, str):
            value = value.lower()
            if value in ["yes", "true"]:
                return 1.0
            elif value in ["no", "false"]:
                return 0.0
            elif value.replace(".", "").isnumeric():
                return float(value)

        # couldn't extract a value
        return 0.0

    return to_float
