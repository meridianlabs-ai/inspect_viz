import re
import subprocess
from pathlib import Path
from textwrap import dedent

# we don't define params in the spec we send....in case we need to here are the aliases:

# ParamLiteral: TypeAlias = None | str | int | float | bool
# ParamValue: TypeAlias = ParamLiteral | list[ParamLiteral | ParamRef]
# ParamDefinition: TypeAlias = ParamValue | Param | ParamDate | Selection
# Params: TypeAlias = dict[str, ParamDefinition]


def generate_mosaic_models() -> None:
    dir = Path(__file__).parent
    schema = (dir / "v0.16.2.json").as_posix()
    models = (dir / "plot.py").as_posix()
    subprocess.run(
        [
            "datamodel-codegen",
            "--input",
            schema,
            "--output",
            models,
            "--input-file-type",
            "jsonschema",
            "--output-model-type",
            "pydantic_v2.BaseModel",
            "--target-python-version",
            "3.10",
            "--use-standard-collections",
            "--enum-field-as-literal=all",
            "--use-one-literal-as-default",
            "--use-union-operator",
            "--use-default-kwarg",
            "--collapse-root-models",
        ]
    )

    # apply fixups
    with open(models, "r", encoding="utf-8") as file:
        models_content = file.read()
    with open(models, "w", encoding="utf-8") as file:
        # float aliased
        typing_import = "from typing import Any, Literal"
        float_alised = "from builtins import float as float_aliased"
        models_content = models_content.replace(
            typing_import, f"{float_alised}\n{typing_import}"
        )

        # strip spec classes
        spec_pattern = r"^class\s+Spec\d+\([^)]*BaseModel[^)]*\):.*?(?=^class\s|\Z)"
        models_content = re.sub(
            spec_pattern, "", models_content, flags=re.MULTILINE | re.DOTALL
        )

        # strip unwanted classes
        unwanted_pattern = r"^class\s+(?:Config|Meta|Data\w*|Model)\s*(?:\([^)]*\))?\s*:.*?(?=^class\s|\Z)"
        models_content = re.sub(
            unwanted_pattern, "", models_content, flags=re.MULTILINE | re.DOTALL
        )
        models_content = models_content.replace("\nModel.model_rebuild()", "", 1)
        models_content = models_content.replace("AnyUrl, ", "", 1)

        # tip classes
        models_content = consolidate_tip_classes(models_content)

        # ignores
        ignores = dedent("""
        # mypy: disable-error-code="type-arg"
        # ruff: noqa: D200, D301, W605, D205
        """).lstrip()
        file.write(ignores + "\n" + models_content)


def consolidate_tip_classes(content: str) -> str:
    # Find all Tip class definitions with their positions
    tip_class_pattern = (
        r"^(class\s+Tip\d+\s*\([^)]*BaseModel[^)]*\):.*?)(?=^class\s|\Z)"
    )
    matches = list(
        re.finditer(tip_class_pattern, content, flags=re.MULTILINE | re.DOTALL)
    )

    if not matches:
        return content

    # Get the first match and its content
    first_match = matches[0]
    first_class_content = first_match.group(1)

    # Rename the first class content
    renamed_first_class = re.sub(
        r"^class\s+Tip\d+\b", "class Tip", first_class_content, flags=re.MULTILINE
    )

    # Now remove ALL Tip class definitions (including the first one)
    content_without_tips = re.sub(
        tip_class_pattern, "", content, flags=re.MULTILINE | re.DOTALL
    )

    # Insert the renamed class back at the original position of the first match
    start_pos = first_match.start()
    final_content = (
        content_without_tips[:start_pos]
        + renamed_first_class
        + content_without_tips[start_pos:]
    )

    # Replace all references to numbered Tip classes with just "Tip"
    tip_reference_pattern = r"\bTip\d+\b"
    final_content = re.sub(tip_reference_pattern, "Tip", final_content)

    # remove the second leftover Tip class
    tip_pattern = r"^class\s+Tip\s*(?:\([^)]*\))?\s*:.*?(?=^class\s|\Z)"
    matches = list(
        re.finditer(tip_pattern, final_content, flags=re.MULTILINE | re.DOTALL)
    )
    second_match = matches[1]
    final_content = (
        final_content[: second_match.start()] + final_content[second_match.end() :]
    )

    return final_content


if __name__ == "__main__":
    generate_mosaic_models()
