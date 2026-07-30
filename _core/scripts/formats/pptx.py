from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from core.assets import resolve_asset
from core.frontmatter import get_value
from core.models import TargetPlan
from core.schema import FormatSchema, Key

SCHEMA = FormatSchema(
    target="pptx",
    keys=(
        Key("reference-doc", "intercepted", "path",
            doc="pandoc's own option; mdOffice resolves the path relative to the doc"),
    ),
)


def create_plan(md_file: Path, config: dict[str, Any], scripts_dir: Path) -> TargetPlan:
    _ = scripts_dir
    output_dir = md_file.parent / "pptx"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{md_file.stem}.pptx"

    command = [
        "pandoc",
        str(md_file),
        "-o",
        str(output_file),
        "--resource-path",
        str(md_file.parent),
    ]

    reference_doc = get_value(config, "reference-doc")
    if reference_doc:
        resolved = resolve_asset(md_file, reference_doc)
        if resolved is not None:
            command += ["--reference-doc", str(resolved)]
        else:
            print(f"Warning: [pptx] reference-doc file not found: {reference_doc}", file=sys.stderr)

    return TargetPlan(target="pptx", output_file=output_file, command=command)
