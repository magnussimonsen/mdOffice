"""`mdoffice.font`: pick the document's font from the frontmatter.

Shared by `formats/pdf.py` and `formats/beamer.py`. Writes a small `.tex`
file that the planner includes AFTER the theme file, so the frontmatter
font wins over whatever font the theme sets -- for every theme, official
or custom, without the theme having to know about the key.

The same font is used as both main (serif slot) and sans font: PDF themes
typeset body text in the main font, Beamer in the sans font, and headings
may use either, so setting both gives one consistent font. If the font
isn't installed, the theme's font is kept instead of failing the build, and
mdOffice warns about it (checked with `fc-list`, which ships with both
MiKTeX and TeX Live and reads the same font database as XeLaTeX).
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from core.tex_sanitize import sanitize_font_name


def font_installed(font: str) -> bool | None:
    """True/False if `fc-list` can tell whether `font` is installed, or None
    if `fc-list` isn't available (then LaTeX's own fallback still applies)."""
    fc_list = shutil.which("fc-list")
    if fc_list is None:
        return None
    try:
        result = subprocess.run(
            [fc_list, f":family={font}", "family"],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return bool(result.stdout.strip())


def write_font_header(output_dir: Path, font: str | None, target: str) -> Path | None:
    """Write `_mdoffice_fonts.tex` for `mdoffice.font`, or return None if
    no (valid) font was given."""
    if not font:
        return None
    safe_font = sanitize_font_name(font)
    if safe_font is None:
        print(f"Warning: [{target}] mdoffice.font contains characters that aren't "
              f"allowed in a font name: {font!r}. Using the theme's font.", file=sys.stderr)
        return None
    if font_installed(safe_font) is False:
        print(f"Warning: [{target}] font not installed: mdoffice.font: {safe_font!r}. "
              f"Using the theme's font.", file=sys.stderr)
        return None

    font_file = output_dir / "_mdoffice_fonts.tex"
    font_file.write_text(
        f"\\IfFontExistsTF{{{safe_font}}}{{%\n"
        f"  \\setmainfont{{{safe_font}}}%\n"
        f"  \\setsansfont{{{safe_font}}}%\n"
        f"}}{{%\n"
        f"  \\typeout{{mdOffice warning: font '{safe_font}' (mdoffice.font) is not installed. Using the theme's font.}}%\n"
        f"}}\n",
        encoding="utf-8",
    )
    return font_file
