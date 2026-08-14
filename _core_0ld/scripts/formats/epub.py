from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from core.assets import resolve_asset
from core.frontmatter import get_custom, get_flag, get_value
from core.models import TargetPlan
from core.schema import FormatSchema, Key

SCHEMA = FormatSchema(
    target="epub",
    keys=(
        Key("epub-css", "custom", "path",
            doc="Stylesheet applied to the epub; mdOffice resolves the path and passes it as --css"),
        Key("toc", "intercepted", "bool", default=False,
            doc="Pandoc-vocabulary name, but the epub writer needs an explicit --toc flag, so mdOffice reads it"),
        Key("cover-image", "intercepted", "path",
            doc="Pandoc-vocabulary name; mdOffice resolves the path and passes --epub-cover-image"),
    ),
)


def create_plan(md_file: Path, config: dict[str, Any], scripts_dir: Path) -> TargetPlan:
    output_dir = md_file.parent / "epub"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{md_file.stem}.epub"
    custom = get_custom(config)

    command = [
        "pandoc",
        str(md_file),
        "-o",
        str(output_file),
        "--resource-path",
        str(md_file.parent),
        # Without this, pandoc falls back to raw TeX for math it can't
        # convert (e.g. \frac), leaving literal "$...$" in the output.
        "--mathml",
    ]

    if get_flag(config, "toc", default=False):
        command += ["--toc"]

    cover_image = get_value(config, "cover-image")
    if cover_image:
        resolved = resolve_asset(md_file, cover_image)
        if resolved is not None:
            command += ["--epub-cover-image", str(resolved)]
        else:
            print(f"Warning: [epub] cover-image file not found: {cover_image}", file=sys.stderr)
            # `cover-image` is a real pandoc epub metadata field: if left
            # unresolved, pandoc's own writer would try to open the same
            # missing raw path itself and crash the build. Override it to
            # an empty string (CLI --metadata wins over doc frontmatter);
            # epub_cover_image.lua then turns that empty value into a fully
            # absent key, since the epub writer treats an empty-but-present
            # value as "open this path" too, not as "no cover".
            command += ["--metadata", "cover-image="]

    cover_filter = scripts_dir / "filters" / "epub_cover_image.lua"
    if cover_filter.exists():
        command += ["--lua-filter", str(cover_filter)]

    # `mdoffice.epub-css` (custom): mdOffice's own name for the epub stylesheet.
    epub_css = get_value(custom, "epub-css")
    if epub_css:
        resolved = resolve_asset(md_file, epub_css)
        if resolved is not None:
            command += ["--css", str(resolved)]
        else:
            print(f"Warning: [epub] epub-css file not found: {epub_css}", file=sys.stderr)

    return TargetPlan(target="epub", output_file=output_file, command=command)
