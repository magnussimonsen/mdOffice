"""Helpers for reading a markdown file's YAML frontmatter (the `---` block at
the top of the file) and pulling typed values out of it.

Two kinds of keys live in that one YAML block, and this module deliberately
doesn't try to keep them apart -- `load_frontmatter()` returns the whole
thing, because pandoc itself reads the exact same block directly from the
file. What separates "pandoc built-in" from "mdOffice custom" is WHERE in
that dict a planner looks:

    config = load_frontmatter(md_file)      # top-level: pandoc / intercepted keys
    custom = get_custom(config)              # config["mdoffice"]: custom keys

Example frontmatter:

    ---
    title: My Document      # pandoc built-in -> read from `config`
    fontsize: 12pt           # pandoc built-in, mdOffice also defaults it -> `config`
    mdoffice:
      make-pdf: true         # mdOffice custom -> read from `custom`
    ---
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

# A `---` delimited block at the very start of the file.
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)

# Just the opening fence, used to distinguish "no frontmatter block at all"
# from "opened a block but never closed it" when _FRONTMATTER_RE fails to match.
_OPENING_FENCE_RE = re.compile(r"^---\s*\n")


def load_frontmatter(md_file: Path) -> dict[str, Any]:
    """Load YAML frontmatter from a markdown file, or return an empty dict."""
    try:
        # utf-8-sig also strips a leading BOM if the file has one (common
        # when files are saved/edited on Windows).
        content = md_file.read_text(encoding="utf-8-sig")
    except OSError as exc:
        print(f"Error reading {md_file}: {exc}", file=sys.stderr)
        return {}

    match = _FRONTMATTER_RE.match(content)
    if not match:
        if _OPENING_FENCE_RE.match(content):
            # Looks like the user meant to write frontmatter (opened a `---`
            # fence) but never closed it -- warn instead of silently
            # building as if none of the mdoffice.* flags were set.
            print(
                f"Warning: {md_file} starts with '---' but no closing '---' "
                "fence was found; treating it as having no frontmatter.",
                file=sys.stderr,
            )
        # No frontmatter block: treat as "no config", not an error.
        return {}

    raw = match.group(1)
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        print(f"Warning: invalid frontmatter in {md_file}: {exc}", file=sys.stderr)
        return {}

    # Guard against frontmatter that's valid YAML but not a mapping
    # (e.g. just a list or a scalar value).
    return data if isinstance(data, dict) else {}


def get_custom(config: dict[str, Any]) -> dict[str, Any]:
    """Return the nested `mdoffice:` map holding all custom keys.

    Guards against `mdoffice:` being present but not a mapping (e.g. a user
    accidentally wrote `mdoffice: true`), which would otherwise blow up
    every `get_value(custom, ...)` call downstream.
    """
    custom = config.get("mdoffice")
    return custom if isinstance(custom, dict) else {}


def get_flag(config: dict[str, Any], key: str, default: bool = False) -> bool:
    """Read a boolean flag from a frontmatter dict, e.g. `page-numbering: true`.

    Accepts real YAML booleans as well as the strings "true"/"false"
    (case-insensitive), since users sometimes quote them in YAML.
    Anything else falls back to `default`.
    """
    value = config.get(key, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"true", "false"}:
            return text == "true"
    return default


def get_value(config: dict[str, Any], key: str, default: str | None = None) -> str | None:
    """Read a string value from a frontmatter dict, e.g. `title: My Document`.

    Returns `default` if the key is missing or its value is `None`;
    otherwise the value is converted to a stripped string.
    """
    if key not in config:
        return default
    value = config.get(key)
    if value is None:
        return default
    return str(value).strip()
