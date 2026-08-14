"""Declares the vocabulary of frontmatter keys each output format understands.

This is the single source of truth for the pandoc-vs-mdOffice split:

  - "intercepted" keys are pandoc-native names (or pandoc-adjacent, e.g. the
    Beamer `logo` template variable) that mdOffice's Python ALSO reads --
    for path resolution, defaulting, or translating into a CLI flag. They
    stay at the TOP LEVEL of the frontmatter, exactly where pandoc expects
    them.
  - "custom" keys are concepts mdOffice invented; pandoc has never heard of
    them. They live under the nested `mdoffice:` map in the frontmatter.

Each `formats/*.py` module declares one `SCHEMA = FormatSchema(...)`. Three
things read it: the planner itself (`create_plan`), `core/validate.py`
(to warn on unknown `mdoffice:` keys), and `generate_reference.py` (to
generate `doc/frontmatter-reference.md`). Adding or renaming an option means
editing one `Key(...)` line here -- nothing else needs to change to keep the
docs and validator in sync.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Scope = Literal["custom", "intercepted"]
KeyType = Literal["str", "bool", "length", "hexcolor", "path"]


@dataclass(frozen=True)
class Key:
    name: str  # bare key name, e.g. "titlebg" (no "mdoffice." prefix)
    scope: Scope
    type: KeyType
    default: object = None
    doc: str = ""  # one-line description, used to generate the reference doc


@dataclass(frozen=True)
class FormatSchema:
    target: str
    keys: tuple[Key, ...]

    def custom_keys(self) -> tuple[Key, ...]:
        return tuple(key for key in self.keys if key.scope == "custom")

    def intercepted_keys(self) -> tuple[Key, ...]:
        return tuple(key for key in self.keys if key.scope == "intercepted")


# Keys read by `filters/solution_filter.lua`, not by any Python planner --
# shared by every LaTeX-based target (pdf, beamer; see LATEX_TARGETS in
# core/filters.py). Declared once here so pdf.py and beamer.py don't
# duplicate the same four Key(...) lines.
SOLUTION_FILTER_KEYS: tuple[Key, ...] = (
    Key("show-solution", "custom", "bool", default=False,
        doc="Show ::: solution ... ::: blocks (read by solution_filter.lua, not Python)"),
    Key("show-blankbox", "custom", "bool", default=False,
        doc="Show ::: blankbox ... ::: blocks (read by solution_filter.lua, not Python)"),
    Key("solution-text", "custom", "str", default="Solution",
        doc="Label on the solution box frame, e.g. \"Løsning\" (read by solution_filter.lua)"),
    Key("blankbox-text", "custom", "str", default="Write your solution in this box",
        doc="Label on blank answer boxes (read by solution_filter.lua)"),
)

# Global custom keys that aren't specific to one format: they live under
# `mdoffice:` in every document regardless of which targets are enabled.
GLOBAL_KEYS: tuple[Key, ...] = (
    Key("make-pdf", "custom", "bool", default=False, doc="Build the pdf target on `build-all`"),
    Key("make-docx", "custom", "bool", default=False, doc="Build the docx target on `build-all`"),
    Key("make-odt", "custom", "bool", default=False, doc="Build the odt target on `build-all`"),
    Key("make-pptx", "custom", "bool", default=False, doc="Build the pptx target on `build-all`"),
    Key("make-beamer", "custom", "bool", default=False, doc="Build the beamer target on `build-all`"),
    Key("make-epub", "custom", "bool", default=False, doc="Build the epub target on `build-all`"),
    Key(
        "ai-instructions",
        "custom",
        "path",
        doc="Path (or list of paths) to AI-instruction files injected into CLAUDE.md / .continuerules",
    ),
)
