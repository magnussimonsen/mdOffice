"""Command-line entry point for mdoffice v2.

Converts a markdown file into one or more output formats (pdf, docx, odt,
pptx, beamer, epub) using the conversion pipeline in `core/pipeline.py`. This
is the script invoked by the "Run on Save" VS Code task and from the command
line.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from core.assets import resolve_asset
from core.frontmatter import get_custom, load_frontmatter
from core.pipeline import SUPPORTED_TARGETS, build_document, enabled_targets
from core.validate import validate_custom_keys
from formats import SCHEMAS


def _parse_targets(raw: str) -> list[str]:
    """Turn a comma-separated string like "pdf,docx" into a validated list of targets."""
    targets = [part.strip() for part in raw.split(",") if part.strip()]
    invalid = [target for target in targets if target not in SUPPORTED_TARGETS]
    if invalid:
        raise ValueError(f"Unsupported targets: {', '.join(invalid)}")
    return targets


def _print_report(exit_source: str, report) -> int:
    """Print one line per build result and return the process exit code (0 = success, 2 = failure)."""
    for result in report.results:
        if result.success and result.output_file is not None:
            print(f"[{result.target}] OK -> {result.output_file}")
        elif result.success:
            # Successful but skipped/no-op builds report their reason via `error`.
            print(f"[{result.target}] OK -> {result.error}")
        else:
            print(f"[{result.target}] FAIL -> {result.error}", file=sys.stderr)

    if report.success:
        print(f"Build completed: {exit_source}")
        return 0

    print(f"Build failed: {exit_source}", file=sys.stderr)
    return 2


_AI_INSTRUCTIONS_HEADER = """\
# mdOffice — AI instructions

This file contains general instructions for working with mdOffice documents.

"""

_AI_INSTRUCTIONS_MARKER = "--- CUSTOM AI INSTRUCTIONS ---"


def _ai_instruction_paths(md_file: Path) -> list[str]:
    """Read `mdoffice.ai-instructions` (string or list) from frontmatter."""
    config = load_frontmatter(md_file)
    raw = get_custom(config).get("ai-instructions")

    if isinstance(raw, str):
        return [raw.strip()] if raw.strip() else []
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if item is not None and str(item).strip()]
    return []


def _cmd_build_ai_instructions(md_path: str) -> int:
    """Create AI-tool files next to the document that POINT AT the referenced
    ai-instructions files, rather than inlining their content. Avoids writing
    the same combined text twice (once for CLAUDE.md, once for
    .continuerules) -- the instruction files themselves stay the single
    source of truth on disk.
    """
    md_file = Path(md_path).resolve()
    if not md_file.exists() or md_file.suffix.lower() != ".md":
        print(f"Invalid markdown file: {md_path}", file=sys.stderr)
        return 1

    paths = _ai_instruction_paths(md_file)
    if not paths:
        return 0

    output_dir = md_file.parent
    exit_code = 0
    relative_paths: list[str] = []

    for raw_path in paths:
        resolved = resolve_asset(md_file, raw_path)
        if resolved is None:
            print(f"Warning: ai-instructions file not found: {raw_path}", file=sys.stderr)
            exit_code = 1
            continue
        # Relative to output_dir, since that's where CLAUDE.md/.continuerules
        # are written -- makes the pointer paths resolvable from there.
        relative_paths.append(os.path.relpath(resolved, output_dir).replace("\\", "/"))

    if not relative_paths:
        return exit_code

    # Claude Code: `@path` is a real import syntax -- each referenced file is
    # pulled in automatically as context. No content is duplicated here.
    claude_content = (
        _AI_INSTRUCTIONS_HEADER + _AI_INSTRUCTIONS_MARKER + "\n\n"
        + "\n".join(f"@{path}" for path in relative_paths) + "\n"
    )
    claude_file = output_dir / "CLAUDE.md"
    claude_file.write_text(claude_content, encoding="utf-8")
    print(f"Written: {claude_file}")

    # Continue's .continuerules has no confirmed equivalent auto-import, so
    # this is a plain textual pointer -- advisory, not guaranteed followed.
    continue_content = (
        _AI_INSTRUCTIONS_HEADER + _AI_INSTRUCTIONS_MARKER + "\n\n"
        "See the following files for this document's AI instructions:\n"
        + "\n".join(f"- {path}" for path in relative_paths) + "\n"
    )
    continue_file = output_dir / ".continuerules"
    continue_file.write_text(continue_content, encoding="utf-8")
    print(f"Written: {continue_file}")

    return exit_code


def _cmd_get_ai_instructions(md_path: str) -> int:
    """Read ai-instructions paths from frontmatter and print the combined content."""
    md_file = Path(md_path).resolve()
    if not md_file.exists() or md_file.suffix.lower() != ".md":
        print(f"Invalid markdown file: {md_path}", file=sys.stderr)
        return 1

    paths = _ai_instruction_paths(md_file)
    if not paths:
        print("No ai-instructions defined in frontmatter.", file=sys.stderr)
        return 0

    exit_code = 0
    sections: list[str] = []

    for raw_path in paths:
        resolved = resolve_asset(md_file, raw_path)
        if resolved is None:
            print(f"Warning: ai-instructions file not found: {raw_path}", file=sys.stderr)
            exit_code = 1
            continue
        sections.append(resolved.read_text(encoding="utf-8"))

    if sections:
        print("\n\n".join(sections))

    return exit_code


def _cmd_validate(md_path: str) -> int:
    """Print any unrecognized `mdoffice:` keys for a file's enabled targets, without building."""
    md_file = Path(md_path).resolve()
    if not md_file.exists() or md_file.suffix.lower() != ".md":
        print(f"Invalid markdown file: {md_path}", file=sys.stderr)
        return 1

    config = load_frontmatter(md_file)
    custom = get_custom(config)
    targets = enabled_targets(config)
    if not targets:
        print("No `mdoffice.make-<target>` flags set; nothing to validate.")
        return 0

    warnings: list[str] = []
    for target in targets:
        schema = SCHEMAS.get(target)
        if schema is not None:
            warnings.extend(validate_custom_keys(schema, custom, target))

    if not warnings:
        print(f"OK: no unrecognized mdoffice.* keys for target(s) {', '.join(targets)}.")
        return 0

    for warning in warnings:
        print(f"Warning: {warning}", file=sys.stderr)
    return 1


def _cmd_docs() -> int:
    """Regenerate doc/frontmatter-reference.md from the format schemas."""
    import generate_reference

    scripts_dir = Path(__file__).resolve().parent
    output_path = scripts_dir.parent / "doc" / "frontmatter-reference.md"
    generate_reference.write(output_path)
    print(f"Written: {output_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="mdoffice v2 converter")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # `build-all`: read the markdown file's frontmatter to decide which
    # targets are enabled (e.g. `mdoffice.make-pdf: true` in the YAML header).
    build_all = subparsers.add_parser("build-all", help="Build all enabled targets from frontmatter flags")
    build_all.add_argument("markdown_file", help="Path to markdown file")

    # `build`: ignore frontmatter flags and build exactly the targets given
    # via --targets, e.g. `--targets pdf,docx`.
    build = subparsers.add_parser("build", help="Build specific targets")
    build.add_argument("markdown_file", help="Path to markdown file")
    build.add_argument("--targets", required=True, help="Comma-separated list: pdf,docx,odt,pptx,beamer,epub")

    # `get-ai-instructions`: read ai-instructions from frontmatter and print
    # the combined content of all listed instruction files to stdout.
    get_ai = subparsers.add_parser("get-ai-instructions", help="Print combined AI instruction files for a document")
    get_ai.add_argument("markdown_file", help="Path to markdown file")

    # `build-ai-instructions`: create an AI instructions file next to the document
    # with the ai-instructions content injected under the custom instructions marker.
    build_claude = subparsers.add_parser("build-ai-instructions", help="Generate an AI instructions file for a document")
    build_claude.add_argument("markdown_file", help="Path to markdown file")

    # `validate`: print unrecognized mdoffice.* keys for a document's enabled
    # targets, without building anything.
    validate = subparsers.add_parser("validate", help="Check a document's mdoffice: keys against the schema")
    validate.add_argument("markdown_file", help="Path to markdown file")

    # `docs`: regenerate doc/frontmatter-reference.md from the schemas.
    subparsers.add_parser("docs", help="Regenerate doc/frontmatter-reference.md from the format schemas")

    args = parser.parse_args()

    # The pipeline needs this directory to locate Pandoc filters/themes that
    # live alongside this script under _core_v2/scripts/.
    scripts_dir = Path(__file__).resolve().parent

    if args.command == "get-ai-instructions":
        return _cmd_get_ai_instructions(args.markdown_file)

    if args.command == "build-ai-instructions":
        return _cmd_build_ai_instructions(args.markdown_file)

    if args.command == "validate":
        return _cmd_validate(args.markdown_file)

    if args.command == "docs":
        return _cmd_docs()

    if args.command == "build-all":
        report = build_document(args.markdown_file, requested_targets=None, scripts_dir=scripts_dir)
        return _print_report("build-all", report)

    try:
        targets = _parse_targets(args.targets)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    report = build_document(args.markdown_file, requested_targets=targets, scripts_dir=scripts_dir)
    return _print_report("build", report)


if __name__ == "__main__":
    # Exit with the code returned by main() so CI / Run-on-Save can detect failures.
    sys.exit(main())
