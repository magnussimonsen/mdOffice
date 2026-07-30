"""Warn (never fail) on `mdoffice:` keys that aren't recognized by any schema.

Deliberately scoped to the `mdoffice:` sub-map only. Top-level frontmatter
keys are NOT validated here -- pandoc's own metadata vocabulary is
open-ended (any template can define its own `$variable$`), so a strict
allowlist there would produce false positives. The `mdoffice:` map is the
one namespace mdOffice fully owns, so it's the one namespace it can check.
"""

from __future__ import annotations

from typing import Any

from core.schema import GLOBAL_KEYS, FormatSchema


def validate_custom_keys(schema: FormatSchema, custom: dict[str, Any], target: str) -> list[str]:
    """Return one warning string per `mdoffice.<key>` not declared for this target."""
    known = {key.name for key in schema.custom_keys()} | {key.name for key in GLOBAL_KEYS}
    warnings = []
    for key in custom:
        if key not in known:
            warnings.append(
                f"[{target}] Unknown key 'mdoffice.{key}' -- not read by any mdOffice code "
                f"for this target. Typo? Run `mdoffice.py docs` to see valid keys."
            )
    return warnings
