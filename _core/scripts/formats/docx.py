from __future__ import annotations

from pathlib import Path
from typing import Any

from core.models import TargetPlan
from core.schema import FormatSchema

# docx currently has no custom or intercepted keys -- every option (title,
# reference-doc, toc, ...) is pure pandoc passthrough. The empty schema still
# gets picked up by generate_reference.py, so the reference doc correctly
# shows "no mdOffice-specific keys for docx" instead of omitting the format.
SCHEMA = FormatSchema(target="docx", keys=())


def create_plan(md_file: Path, config: dict[str, Any], scripts_dir: Path) -> TargetPlan:
    _ = config, scripts_dir
    output_dir = md_file.parent / "docx"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{md_file.stem}.docx"

    command = [
        "pandoc",
        str(md_file),
        "-o",
        str(output_file),
        "--resource-path",
        str(md_file.parent),
    ]
    return TargetPlan(target="docx", output_file=output_file, command=command)
