"""Plain data containers shared across the build pipeline.

A `@dataclass` is a Python decorator that auto-generates the boilerplate for
a class that mainly just holds data: it writes `__init__`, `__repr__`, and
`__eq__` for you based on the fields you declare. So instead of writing
`def __init__(self, target, output_file, ...): self.target = target ...`,
you just list the fields with their types and `@dataclass` does the rest.

`field(default_factory=list)` is the dataclass way of giving a field a
default value of `[]` (a plain `= []` default would be shared between all
instances, which is a classic Python pitfall).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TargetPlan:
    """Everything needed to build one output target: the pandoc command to
    run, where its output will end up, and any temp files to clean up after."""

    target: str
    output_file: Path
    command: list[str]
    temp_files: list[Path] = field(default_factory=list)


@dataclass
class TargetResult:
    """Outcome of building a single target (e.g. "pdf")."""

    target: str
    success: bool
    output_file: Path | None = None
    # Holds the failure reason on error, or an informational message on a
    # successful no-op (e.g. "target skipped").
    error: str | None = None


@dataclass
class BuildReport:
    """Aggregate result of a `build_document` call across all requested targets."""

    source_file: Path
    results: list[TargetResult] = field(default_factory=list)

    @property
    def success(self) -> bool:
        """True only if every target in `results` succeeded."""
        return all(result.success for result in self.results)
