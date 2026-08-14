"""Helper for locating asset files (images, logos, etc.) referenced by a
markdown file's frontmatter, e.g. `logo: assets/logo.png`."""

from __future__ import annotations

from pathlib import Path


def resolve_asset(md_file: Path, asset_path: str) -> Path | None:
    """Resolve an asset path relative to the markdown file or its parent tree.

    First tries the path next to the markdown file itself. If not found
    there, walks up through each ancestor directory (e.g. so a shared
    `assets/` folder higher up the project tree can also be found).
    Returns None if the asset can't be found anywhere.
    """
    candidate = md_file.parent / asset_path
    if candidate.exists():
        return candidate.resolve()

    for parent in md_file.parents:
        fallback = parent / asset_path
        if fallback.exists():
            return fallback.resolve()

    return None


def resolve_theme(themes_dir: Path, style_name: str) -> Path | None:
    """Resolve `mdoffice.doc-style` / `mdoffice.beamer-style` to a `.tex`
    file directly inside `themes_dir`.

    `style_name` is meant to be a bare theme name like "standard-pdf", but
    it's user-controlled frontmatter text; without this check a value like
    "../../../../some/other/file" would let a document `--include-in-header`
    an arbitrary `.tex` file elsewhere on disk. Refuses anything that
    resolves outside `themes_dir` (`../` segments, absolute paths, etc.) by
    requiring the resolved file's parent to be exactly `themes_dir`.
    """
    themes_dir = themes_dir.resolve()
    candidate = (themes_dir / f"{style_name}.tex").resolve()
    if candidate.parent != themes_dir or not candidate.exists():
        return None
    return candidate
