"""The mdOffice version, read from `_core/VERSION`.

That file is the only place the number is written down. `mdoffice.py
--version`, `mdoffice.py docs` (frontmatter reference and website) and the
VS Code extension (via `build-vsix.py`) all read it from there.
"""

from __future__ import annotations

from pathlib import Path

VERSION_FILE = Path(__file__).resolve().parents[2] / "VERSION"
MDOFFICE_VERSION = VERSION_FILE.read_text(encoding="utf-8").strip()
