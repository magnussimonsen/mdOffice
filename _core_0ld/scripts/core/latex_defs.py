"""Shared helper for the "frontmatter value -> LaTeX macro" bridge.

A markdown file's YAML frontmatter (e.g. `logo:`, `mdoffice.titlebg:`) has no
meaning to LaTeX on its own. The pattern used by `formats/pdf.py` and
`formats/beamer.py` is:

  1. Read a frontmatter value.
  2. If present, define a `\\macro{...}` for it.
  3. Write every macro defined this way into ONE `.tex` file and add it to
     the pandoc command with `--include-in-header`, so it's spliced into the
     LaTeX preamble BEFORE the theme file (scripts/themes/{doc-style}.tex).
  4. The theme file then does `\\ifdefined\\macro ... \\else ... \\fi` to
     check whether a macro was defined, and styles itself accordingly.

`LatexDefWriter` collapses the "one `.tex` file per option" boilerplate
(`_logo_def.tex`, `_header_def.tex`, ...) into a single accumulated
`_mdoffice_defs.tex` per build. Callers are responsible for sanitizing
values (see `core/tex_sanitize.py`) before passing them in -- this class
only formats and writes.
"""

from __future__ import annotations

from pathlib import Path


class LatexDefWriter:
    def __init__(self, output_dir: Path, filename: str = "_mdoffice_defs.tex") -> None:
        self._path = output_dir / filename
        self._lines: list[str] = []

    def define(self, macro: str, value: str) -> None:
        """Add `\\def\\macro{value}`. `value` should already be sanitized."""
        self._lines.append(f"\\def\\{macro}{{{value}}}")

    def flag(self, macro: str) -> None:
        """Add `\\def\\macro{1}`, for macros used only as a presence check."""
        self._lines.append(f"\\def\\{macro}{{1}}")

    def write(self) -> Path | None:
        """Write the accumulated defs to disk, or return None if none were added."""
        if not self._lines:
            return None
        self._path.write_text("\n".join(self._lines) + "\n", encoding="utf-8")
        return self._path
