from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from core.assets import resolve_asset, resolve_theme
from core.filters import apply_lua_filters
from core.frontmatter import get_custom, get_flag, get_value
from core.latex_defs import LatexDefWriter
from core.models import TargetPlan
from core.schema import SOLUTION_FILTER_KEYS, FormatSchema, Key
from core.tex_sanitize import sanitize_tex_length, sanitize_tex_path

DEFAULT_ASPECTRATIO = "169"
DEFAULT_FONTSIZE = "12pt"

SCHEMA = FormatSchema(
    target="beamer",
    keys=(
        Key("beamer-style", "custom", "str",
            doc="mdOffice theme to load from scripts/themes/, e.g. beamer, fancybeamer"),
        Key("page-numbering", "custom", "bool", default=True,
            doc="false = hide the frame-number footline"),
        Key("logo", "intercepted", "path",
            doc="Logo image; mdOffice resolves/sanitizes the path (see note below)"),
        Key("logo-height", "intercepted", "length", default="0.8cm",
            doc="Logo height"),
        Key("aspectratio", "intercepted", "str", default=DEFAULT_ASPECTRATIO,
            doc="mdOffice supplies this default if the key is absent"),
        Key("fontsize", "intercepted", "str", default=DEFAULT_FONTSIZE,
            doc="mdOffice supplies this default if the key is absent"),
        *SOLUTION_FILTER_KEYS,
    ),
)

# Note -- `logo` and `theme`/`colortheme`/`fonttheme`/etc. are real pandoc
# Beamer template variables, read directly by pandoc's own beamer template.
# `logo` is ALSO read here by mdOffice (to resolve/sanitize the path), and
# both `logo` and the theme-* family are effectively overridden by the
# mdOffice theme file (scripts/themes/{beamer-style}.tex), which is included
# LAST and sets \logo{...}/\usetheme{...} again inside \AtBeginDocument, so
# it always wins. Use `mdoffice.beamer-style` to choose between mdOffice's
# own theme files -- it's unrelated to pandoc's `theme:`.


def create_plan(md_file: Path, config: dict[str, Any], scripts_dir: Path) -> TargetPlan:
    output_dir = md_file.parent / "beamer"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{md_file.stem}.pdf"
    temp_files: list[Path] = []
    custom = get_custom(config)

    command = [
        "pandoc",
        str(md_file),
        "-o",
        str(output_file),
        "--to=beamer",
        "--pdf-engine=xelatex",
        "--resource-path",
        str(md_file.parent),
    ]
    apply_lua_filters(command, target="beamer", scripts_dir=scripts_dir)

    defs = LatexDefWriter(output_dir)

    left_logo = get_value(config, "logo")
    if left_logo:
        logo_abs = resolve_asset(md_file, left_logo)
        if logo_abs is not None:
            safe_logo_path = sanitize_tex_path(logo_abs.as_posix())
            if safe_logo_path is not None:
                logo_height = sanitize_tex_length(get_value(config, "logo-height"), default="0.8cm")
                defs.define("logopath", safe_logo_path)
                defs.define("logoheight", logo_height)
            else:
                print(f"Warning: [beamer] logo path contains '{{' or '}}', which "
                      f"can't be safely embedded in LaTeX: {logo_abs}", file=sys.stderr)
        else:
            print(f"Warning: [beamer] logo file not found: {left_logo}", file=sys.stderr)
            # `logo` is a real pandoc Beamer template variable (see note
            # above): if left unresolved, pandoc's own template would try
            # to open the same missing raw path itself and crash the
            # build. Clear it via metadata override rather than just
            # skipping the mdOffice-side \def.
            command += ["--metadata", "logo="]

    # `mdoffice.page-numbering: false` (custom): hide the slide-number footline.
    if not get_flag(custom, "page-numbering", default=True):
        defs.flag("hidepagenumbers")

    def_file = defs.write()
    if def_file is not None:
        temp_files.append(def_file)
        command += ["--include-in-header", str(def_file)]

    # `mdoffice.beamer-style` (custom): picks WHICH mdOffice theme file to
    # load. Included after the defs above so its \ifdefined checks see them,
    # and after pandoc's own beamer template so it wins the `logo`/`theme`
    # race described in the note above.
    beamer_style = get_value(custom, "beamer-style")
    if beamer_style:
        theme_file = resolve_theme(scripts_dir / "themes", beamer_style)
        if theme_file is not None:
            command += ["--include-in-header", str(theme_file)]

    if not get_value(config, "aspectratio"):
        command += ["--variable", f"aspectratio={DEFAULT_ASPECTRATIO}"]
    if not get_value(config, "fontsize"):
        command += ["--variable", f"fontsize={DEFAULT_FONTSIZE}"]

    return TargetPlan(target="beamer", output_file=output_file, command=command, temp_files=temp_files)
