from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Radio(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    input: Literal["radio"] = Field(
        default="radio", description="A radio input widget."
    )
    label: str | None = Field(default=None, description="A text label for this input.")
