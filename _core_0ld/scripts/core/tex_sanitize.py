from __future__ import annotations

import re

# Characters that frequently break TeX macro arguments if inserted raw.
# We only escape what we currently inject from frontmatter text fields.
_TEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "%": r"\%",
    "#": r"\#",
    "&": r"\&",
    "_": r"\_",
    "$": r"\$",
}

# Accept strict TeX length tokens only (for values like logo-height/titlebgpad).
# This avoids injecting arbitrary TeX commands through a "length" field.
_VALID_TEX_LENGTH = re.compile(r"^\d+(?:\.\d+)?(?:pt|mm|cm|in|em|ex|bp|pc|dd|cc|sp)$")

# Colors are passed into TeX color macros as plain hex, so enforce 6 hex digits.
_VALID_HEX_COLOR = re.compile(r"^[0-9A-Fa-f]{6}$")


def escape_tex_text(value: str) -> str:
    """Escape TeX-special characters in user-provided text."""
    # Character-by-character escaping keeps unknown characters untouched
    # while protecting known TeX metacharacters.
    return "".join(_TEX_ESCAPES.get(char, char) for char in value)


def sanitize_tex_length(value: str | None, default: str) -> str:
    """Return a safe TeX length literal, or default if invalid."""
    if value is None:
        return default
    text = value.strip()
    if _VALID_TEX_LENGTH.fullmatch(text):
        return text
    return default


def sanitize_hex_color(value: str | None) -> str | None:
    """Return a 6-digit hex color without '#', or None if invalid."""
    if value is None:
        return None
    text = value.strip().lstrip("#")
    if _VALID_HEX_COLOR.fullmatch(text):
        return text
    return None


def sanitize_tex_path(value: str) -> str | None:
    """Wrap a filesystem path so TeX treats special characters literally, or
    None if that isn't possible.

    \\detokenize{...}'s argument is delimited by ordinary TeX brace matching,
    which happens before \\detokenize itself ever runs -- so an unescaped
    `{`/`}` inside `value` can't be neutralized from in here; it would just
    close the group early (or fail to balance) and corrupt the surrounding
    LaTeX. Filenames can't contain braces on Windows, but they can on
    Linux/macOS, so this is refused rather than silently producing broken
    TeX.
    """
    if "{" in value or "}" in value:
        return None
    # We normalize to forward slashes for cross-platform TeX compatibility.
    return r"\detokenize{" + value.replace("\\", "/") + "}"
