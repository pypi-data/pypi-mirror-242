"""FSM Helpers."""

import json
from enum import Enum
from pathlib import Path

from clea import ChoiceByFlag, Directory, File, group
from typing_extensions import Annotated

from open_autonomy_compose.fsm.composition import Composition
from open_autonomy_compose.fsm.specification import FSMSpecification
from open_autonomy_compose.helpers.package import load_packages


DEFAULT_OUTPUT_FILE = Path("./fsm.yaml")


class OutputType(Enum):
    """Output types."""

    JSON = "json"
    YAML = "yaml"


@group
def fsm() -> None:
    """FSM Helpers."""


@fsm.command(name="from-app")
def _from_app(
    app: Annotated[Path, Directory(exists=True, resolve=True)],
    output_type: Annotated[
        OutputType,
        ChoiceByFlag(
            enum=OutputType, default=OutputType.YAML, help="File output type."
        ),
    ],
    output: Annotated[Path, File(help="Path to output file.")] = DEFAULT_OUTPUT_FILE,
) -> None:
    """Generate specification from an ABCI app."""
    load_packages(packages=app.parent.parent.parent)
    spec = FSMSpecification.from_compostion(
        composition=Composition.from_path(
            path=app,
        ),
    )
    if output_type == OutputType.YAML:
        spec.to_yaml(file=output, include_parent=True)
    else:
        data = spec.to_json(include_parent=True)
        with output.open("w+", encoding="utf-8") as fp:
            json.dump(data, fp=fp, indent=2)
