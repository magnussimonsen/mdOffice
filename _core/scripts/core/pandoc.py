from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Sequence


def run_pandoc_command(
    command: Sequence[str],
    md_file: Path,
    temp_files: Sequence[Path] = (),
) -> subprocess.CompletedProcess[str]:
    """Run pandoc and clean up temp helper files afterwards.

    cwd=md_file.parent so relative paths (images, resource-doc, ...) resolve
    the way a user editing that file would expect. Does not touch media-*
    folders pandoc may create — those are legitimate build output, not
    temp files.
    """
    try:
        result = subprocess.run(
            list(command),
            cwd=md_file.parent,
            capture_output=True,
            text=True,
        )
    finally:
        # Always run cleanup, even if pandoc fails or raises an exception.
        # missing_ok=True avoids errors if a temp file is already removed.
        for temp_file in temp_files:
            temp_file.unlink(missing_ok=True)

    return result
