from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# how to create a custom input:
#
# (1) Add a class to this file that has an `input` field w/ the input type
# (2) Add the class to the `Input` type-alias in the adjacent __init__.py
# (3) Implement the custom input in js/_input (e.g. see radio.ts)
# (4) Add the custom input to CUSTOM_INPUTS in js/input_/index.ts


class Radio(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    input: Literal["radio"] = Field(
        default="radio", description="A radio input widget."
    )
    label: str | None = Field(default=None, description="A text label for this input.")
