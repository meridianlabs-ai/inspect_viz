import subprocess
from pathlib import Path

# mypy: disable-error-code="type-arg"
# ruff: noqa: D200, D301, W605, D205

# from builtins import float as float_aliased

# re-order spec / hconcat / remove not plot types


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
            "--use-schema-description",
            "--use-standard-collections",
        ]
    )


if __name__ == "__main__":
    generate_mosaic_models()
