"""Generates `_core_v2/doc/frontmatter-reference.md` from the format schemas
declared in `formats/*.py` (via `core/schema.py`).

This replaces a hand-maintained template: as long as every custom or
intercepted key is declared as a `Key(...)` in the schema that reads it, this
script is the only thing that needs to run to keep the docs in sync with the
code. Run via `mdoffice.py docs`, or directly: `python generate_reference.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.schema import GLOBAL_KEYS, FormatSchema, Key  # noqa: E402
from formats import SCHEMAS  # noqa: E402

_INTRO = """\
# mdOffice v2 -- Frontmatter reference

**Generated from `formats/*.py` schemas -- do not hand-edit.**
Run `mdoffice.py docs` (or `python generate_reference.py`) to regenerate
after changing a `SCHEMA` declaration.

Every option below is optional. Two kinds of keys share one YAML frontmatter
block:

- **Pandoc built-in keys** (e.g. `title`, `fontsize`, `logo`) stay at the
  **top level** of the frontmatter, exactly where pandoc expects them. Some
  of these are also read by mdOffice's own code -- for path resolution,
  defaulting, or translating into a CLI flag -- and are marked
  **"intercepted"** below.
- **mdOffice custom keys** -- concepts pandoc has never heard of -- live
  nested under one `mdoffice:` map, e.g.:

```yaml
---
title: My Document
fontsize: 12pt

mdoffice:
  make-pdf: true
  doc-style: standard-pdf
---
```

Any pandoc metadata key not listed here (e.g. `subtitle`, `author`, `toc-depth`,
`colorlinks`, ...) is pure passthrough -- mdOffice's code never touches it.
See pandoc's manual for the writer in question.
"""


def _table(keys: tuple[Key, ...], key_prefix: str = "") -> str:
    if not keys:
        return "_None._\n"
    lines = ["| Key | Type | Default | Description |", "| --- | --- | --- | --- |"]
    for key in sorted(keys, key=lambda k: k.name):
        default = "" if key.default is None else f"`{key.default}`"
        lines.append(f"| `{key_prefix}{key.name}` | {key.type} | {default} | {key.doc} |")
    return "\n".join(lines) + "\n"


def render() -> str:
    sections = [_INTRO]

    sections.append("## Global keys (`mdoffice:`)\n")
    sections.append("Apply regardless of which targets are built.\n")
    sections.append(_table(GLOBAL_KEYS, key_prefix="mdoffice."))

    for target, schema in sorted(SCHEMAS.items()):
        assert isinstance(schema, FormatSchema)
        sections.append(f"## {target}\n")
        sections.append("### `mdoffice:` keys (custom)\n")
        sections.append(_table(schema.custom_keys(), key_prefix="mdoffice."))
        sections.append("### Top-level keys mdOffice also reads (intercepted)\n")
        sections.append(_table(schema.intercepted_keys()))

    return "\n".join(sections)


def write(output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render(), encoding="utf-8")
    return output_path


def main() -> int:
    scripts_dir = Path(__file__).resolve().parent
    output_path = scripts_dir.parent / "doc" / "frontmatter-reference.md"
    write(output_path)
    print(f"Written: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
