"""Helper for locating asset files (images, logos, etc.) referenced by a
markdown file's frontmatter, e.g. `logo: assets/logo.png`."""

from __future__ import annotations

import sys
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


CUSTOM_THEME_ENTRY = "theme.tex"


def official_themes_dir(scripts_dir: Path) -> Path:
    """mdOffice's own themes: `_core/scripts/themes/<name>.tex`."""
    return scripts_dir / "themes"


def custom_themes_dir(scripts_dir: Path) -> Path:
    """User themes: `custom_themes/<name>/theme.tex` in the repository root.

    Kept outside `_core/` so syncing mdOffice's core never touches them.
    """
    return scripts_dir.parent.parent / "custom_themes"


def _resolve_official_theme(themes_dir: Path, style_name: str) -> Path | None:
    themes_dir = themes_dir.resolve()
    candidate = (themes_dir / f"{style_name}.tex").resolve()
    if candidate.parent != themes_dir or not candidate.exists():
        return None
    return candidate


def _resolve_custom_theme(themes_dir: Path, style_name: str) -> Path | None:
    themes_dir = themes_dir.resolve()
    candidate = (themes_dir / style_name / CUSTOM_THEME_ENTRY).resolve()
    if candidate.parent.parent != themes_dir or not candidate.exists():
        return None
    return candidate


def resolve_theme(scripts_dir: Path, style_name: str, target: str) -> Path | None:
    """Resolve `mdoffice.doc-style` / `mdoffice.beamer-style` to a theme file.

    Looks first for a self-contained custom theme folder
    (`custom_themes/<name>/theme.tex`), then for an official theme
    (`_core/scripts/themes/<name>.tex`). A custom theme with the same name
    as an official one overrides it, with a note on stderr.

    `style_name` is meant to be a bare theme name like "standard-pdf", but
    it's user-controlled frontmatter text; without this check a value like
    "../../../../some/other/file" would let a document `--include-in-header`
    an arbitrary `.tex` file elsewhere on disk. Refuses anything that
    resolves outside the themes directories (`../` segments, absolute
    paths, nested folders, etc.) by checking the resolved file's location.
    """
    custom = _resolve_custom_theme(custom_themes_dir(scripts_dir), style_name)
    official = _resolve_official_theme(official_themes_dir(scripts_dir), style_name)
    if custom is not None:
        if official is not None:
            print(f"Note: [{target}] custom theme {style_name!r} overrides the official "
                  f"mdOffice theme with the same name ({custom.parent}).", file=sys.stderr)
        return custom
    return official


def available_themes(scripts_dir: Path) -> list[str]:
    """Names of all official and custom themes, sorted. Custom themes are
    marked "(custom)"."""
    official = {path.stem for path in official_themes_dir(scripts_dir).glob("*.tex")}
    custom_dir = custom_themes_dir(scripts_dir)
    custom = {path.parent.name for path in custom_dir.glob(f"*/{CUSTOM_THEME_ENTRY}")} if custom_dir.is_dir() else set()
    return sorted(
        f"{name} (custom)" if name in custom else name
        for name in official | custom
    )


def warn_unknown_theme(scripts_dir: Path, style_name: str, target: str, key: str) -> None:
    """Warn that `mdoffice.<key>` named a theme that doesn't exist.

    The build continues without a theme (pandoc's plain look), so without
    this a typo like `doc-style: exma` would silently produce an unstyled
    document.
    """
    names = ", ".join(available_themes(scripts_dir)) or "(none found)"
    print(
        f"Warning: [{target}] theme not found: mdoffice.{key}: {style_name!r}. "
        f"Available themes: {names}. Building without a theme.",
        file=sys.stderr,
    )
