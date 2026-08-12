from __future__ import annotations

import os
import stat
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Sequence


def _clear_readonly_and_retry(func, path, _exc: BaseException) -> None:
    """Allow rmtree to retry when OneDrive marks files/directories read-only."""
    try:
        os.chmod(path, stat.S_IWRITE)
    except OSError:
        return
    func(path)


def _remove_tree_with_retries(path: Path, attempts: int = 6, base_delay: float = 0.1) -> bool:
    """Best-effort recursive delete with backoff for transient Windows locks."""
    last_error: Exception | None = None

    for attempt in range(1, attempts + 1):
        try:
            shutil.rmtree(path, onexc=_clear_readonly_and_retry)
            return True
        except FileNotFoundError:
            return True
        except Exception as exc:  # pragma: no cover - platform/IO dependent
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(base_delay * attempt)

    if path.exists():
        print(
            f"Warning: could not remove temporary folder '{path}': {last_error}",
            file=sys.stderr,
        )
    return False


def run_pandoc_command(
    command: Sequence[str],
    md_file: Path,
    temp_files: Sequence[Path] = (),
) -> subprocess.CompletedProcess[str]:
    """Run pandoc and clean up temp helper files afterwards.

    cwd=md_file.parent so relative paths (images, resource-doc, ...) resolve
    the way a user editing that file would expect. Any media-* folders in that
    directory are treated as temporary build output and removed after the
    command finishes.
    """
    work_dir = md_file.parent

    try:
        result = subprocess.run(
            list(command),
            cwd=work_dir,
            capture_output=True,
            text=True,
        )
    finally:
        # Remove all media-* directories so stale folders from earlier runs
        # don't linger forever.
        for media_dir in work_dir.glob("media-*"):
            if not media_dir.is_dir():
                continue
            _remove_tree_with_retries(media_dir)

        # Always run cleanup, even if pandoc fails or raises an exception.
        # missing_ok=True avoids errors if a temp file is already removed.
        for temp_file in temp_files:
            temp_file.unlink(missing_ok=True)

    return result
