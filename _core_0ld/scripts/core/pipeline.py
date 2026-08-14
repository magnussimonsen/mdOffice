"""Core build pipeline: turns a markdown file into one or more output documents.

For each requested target (pdf, docx, pptx, beamer, epub) this:
  1. Validates the file's `mdoffice:` frontmatter keys against that target's
     schema, printing warnings for anything unrecognized (never fatal).
  2. Asks the matching "planner" (in `formats/`) to build a pandoc command.
  3. Runs that command via pandoc.
  4. Records success/failure for each target in a BuildReport.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable

from core.frontmatter import get_custom, get_flag, load_frontmatter
from core.models import BuildReport, TargetResult
from core.pandoc import run_pandoc_command
from core.validate import validate_custom_keys
from formats import PLANNERS, SCHEMAS

# All output formats this tool knows how to produce.
SUPPORTED_TARGETS = ("pdf", "docx", "odt", "pptx", "beamer", "epub")


def _target_flag(target: str) -> str:
    """`mdoffice:` key used to enable a target, e.g. "pdf" -> "make-pdf"."""
    return f"make-{target}"


def enabled_targets(config: dict[str, object]) -> list[str]:
    """Return the targets whose `mdoffice.make-<target>: true` flag is set."""
    custom = get_custom(config)
    return [target for target in SUPPORTED_TARGETS if get_flag(custom, _target_flag(target), False)]


def build_document(
    md_path: str | Path,
    requested_targets: Iterable[str] | None = None,
    scripts_dir: Path | None = None,
) -> BuildReport:
    """Build the given markdown file for each requested target.

    If `requested_targets` is None (the "build-all" CLI command), the targets
    are instead taken from the `mdoffice.make-<target>` flags in the file's
    frontmatter. `scripts_dir` is the _core_v2/scripts directory, used by
    planners to find filters, themes, and other supporting files.
    """
    md_file = Path(md_path).resolve()
    report = BuildReport(source_file=md_file)

    if not md_file.exists() or md_file.suffix.lower() != ".md":
        report.results.append(
            TargetResult(target="input", success=False, error=f"Invalid markdown file: {md_path}")
        )
        return report

    config = load_frontmatter(md_file)
    selected = enabled_targets(config) if requested_targets is None else list(requested_targets)

    if not selected:
        report.results.append(
            TargetResult(target="none", success=True, error="No enabled targets; nothing to build")
        )
        return report

    # Default to the scripts/ directory two levels up from this file
    # (core/pipeline.py -> core/ -> scripts/).
    runner_root = scripts_dir or Path(__file__).resolve().parents[1]
    custom = get_custom(config)

    for target in selected:
        # Each target has its own "planner" function that builds the pandoc
        # command and lists any temp files it creates along the way.
        planner = PLANNERS.get(target)
        if planner is None:
            report.results.append(
                TargetResult(target=target, success=False, error=f"Unknown target: {target}")
            )
            continue

        schema = SCHEMAS.get(target)
        if schema is not None:
            for warning in validate_custom_keys(schema, custom, target):
                print(f"Warning: {warning}", file=sys.stderr)

        plan = None
        try:
            plan = planner(md_file, config, runner_root)
            result = run_pandoc_command(plan.command, md_file, plan.temp_files)

            if result.returncode != 0:
                report.results.append(
                    TargetResult(
                        target=target,
                        success=False,
                        output_file=plan.output_file,
                        error=result.stderr.strip() or f"pandoc failed with exit code {result.returncode}",
                    )
                )
                continue

            if not plan.output_file.exists():
                report.results.append(
                    TargetResult(
                        target=target,
                        success=False,
                        output_file=plan.output_file,
                        error=f"Output file not created: {plan.output_file}",
                    )
                )
                continue

            report.results.append(TargetResult(target=target, success=True, output_file=plan.output_file))
        except Exception as exc:
            # Catch-all so one failing target doesn't abort the whole build;
            # the error is recorded and the next target is still attempted.
            report.results.append(
                TargetResult(
                    target=target,
                    success=False,
                    output_file=None if plan is None else plan.output_file,
                    error=f"Unhandled exception while building target '{target}': {exc}",
                )
            )
            continue

    return report
