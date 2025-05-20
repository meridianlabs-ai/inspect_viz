import subprocess
from pathlib import Path


def generate_mosaic_models() -> None:
    dir = Path(__file__).parent
    schema = (dir / "v0.16.2.json").as_posix()
    models = (dir / "mosaic.py").as_posix()
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
        ]
    )


if __name__ == "__main__":
    generate_mosaic_models()
