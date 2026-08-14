from __future__ import annotations

from pathlib import Path

LATEX_TARGETS = {"pdf", "beamer"}


def apply_lua_filters(command: list[str], target: str, scripts_dir: Path) -> None:
    """Append existing Lua filters to pandoc command for a given target."""
    filter_names: list[str] = []

    if target in LATEX_TARGETS:
        filter_names.extend([
            "math_env_normalize.lua",
            "solution_filter.lua",
        ])

    for name in filter_names:
        filter_path = scripts_dir / "filters" / name
        if filter_path.exists():
            command += ["--lua-filter", str(filter_path)]
