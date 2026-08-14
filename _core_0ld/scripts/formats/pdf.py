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
from core.tex_sanitize import escape_tex_text, sanitize_hex_color, sanitize_tex_length, sanitize_tex_path

# Fallback values used only when "fontsize"/"geometry" aren't set in frontmatter.
# Theme files (scripts/themes/*.tex) are included after these and may call
# \geometry{...} again, overriding margins set here (paper size is kept).
DEFAULT_FONTSIZE = "12pt"
DEFAULT_GEOMETRY = "a4paper,top=2.00cm,bottom=2.00cm,left=2.54cm,right=2.54cm"

DEFAULT_DOC_STYLE = "standard-pdf"

SCHEMA = FormatSchema(
    target="pdf",
    keys=(
        Key("doc-style", "custom", "str", default=DEFAULT_DOC_STYLE,
            doc="Theme to load from scripts/themes/, e.g. standard-pdf, exam"),
        Key("header", "custom", "str",
            doc="Small text shown top-right on every page"),
        Key("titlebg", "custom", "hexcolor",
            doc="6-digit hex color (no '#') for a block behind the title (theme-dependent: exam.tex uses it, standard-pdf.tex doesn't)"),
        Key("titlebgpad", "custom", "length",
            doc="Padding around the title text inside that colored block (see titlebg)"),
        Key("page-numbering", "custom", "bool", default=True,
            doc="false = hide page numbers everywhere"),
        Key("first-page-numbering", "custom", "bool", default=False,
            doc="true = also number the title/first page (theme-dependent: exam.tex has no separate title page, so this has no effect there)"),
        Key("logo", "intercepted", "path",
            doc="Logo image path; mdOffice resolves it relative to the doc and sanitizes it for TeX"),
        Key("logo-height", "intercepted", "length", default="1.2cm",
            doc="Logo height"),
        Key("subtitle", "intercepted", "str",
            doc="Pandoc-vocabulary name; mdOffice defines \\mdsubtitle since pandoc's own subtitle mechanism doesn't survive a custom \\maketitle"),
        Key("fontsize", "intercepted", "str", default=DEFAULT_FONTSIZE,
            doc="mdOffice supplies this default if the key is absent"),
        Key("geometry", "intercepted", "str", default=DEFAULT_GEOMETRY,
            doc="mdOffice supplies this default if the key is absent"),
        *SOLUTION_FILTER_KEYS,
    ),
)


def create_plan(md_file: Path, config: dict[str, Any], scripts_dir: Path) -> TargetPlan:
    output_dir = md_file.parent / "pdf"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{md_file.stem}.pdf"
    temp_files: list[Path] = []
    custom = get_custom(config)

    command = [
        "pandoc",
        str(md_file),
        "-o",
        str(output_file),
        "--pdf-engine=xelatex",
        "--resource-path",
        str(md_file.parent),
    ]

    apply_lua_filters(command, target="pdf", scripts_dir=scripts_dir)

    # `header-includes` (top-level, pandoc built-in): normally pandoc splices
    # this YAML metadata field into the preamble itself, but as soon as ANY
    # `--include-in-header` file is passed on the command line (which is
    # true for every build below, since at least one mdOffice def is always
    # written), pandoc silently replaces the metadata-derived header-includes
    # with only the command-line ones, dropping the user's content entirely.
    # Re-routing it through its own `-H` file sidesteps that.
    user_header_includes = get_value(config, "header-includes")
    if user_header_includes:
        header_includes_file = output_dir / "_mdoffice_header_includes.tex"
        header_includes_file.write_text(user_header_includes + "\n", encoding="utf-8")
        temp_files.append(header_includes_file)
        command += ["--include-in-header", str(header_includes_file)]

    # All \def macros below must be defined before the theme file is
    # included, since the theme uses \ifdefined checks while it is loaded.
    defs = LatexDefWriter(output_dir)

    # `logo` (top-level, intercepted): pandoc has no built-in article/report
    # logo concept, but mdOffice resolves/sanitizes the path and defines
    # \logopath/\logoheight, which the loaded theme file consumes via \ifdefined.
    left_logo = get_value(config, "logo")
    if left_logo:
        logo_abs = resolve_asset(md_file, left_logo)
        if logo_abs is not None:
            safe_logo_path = sanitize_tex_path(logo_abs.as_posix())
            if safe_logo_path is not None:
                logo_height = sanitize_tex_length(get_value(config, "logo-height"), default="1.2cm")
                defs.define("logopath", safe_logo_path)
                defs.define("logoheight", logo_height)
            else:
                print(f"Warning: [pdf] logo path contains '{{' or '}}', which "
                      f"can't be safely embedded in LaTeX: {logo_abs}", file=sys.stderr)
        else:
            print(f"Warning: [pdf] logo file not found: {left_logo}", file=sys.stderr)

    # `subtitle` (top-level, intercepted): pandoc's own subtitle mechanism
    # (`\apptocmd{\@title}{...}`) only survives the DEFAULT \maketitle: our
    # themes fully redefine \maketitle and read \thetitle, not \@title, so
    # pandoc's subtitle text would silently never appear. mdOffice instead
    # defines \mdsubtitle directly; themes that support it check \ifdefined.
    subtitle = get_value(config, "subtitle")
    if subtitle:
        defs.define("mdsubtitle", escape_tex_text(subtitle))

    # `mdoffice.header` (custom): a small right-aligned header line.
    right_header = get_value(custom, "header")
    if right_header:
        defs.define("rightheader", escape_tex_text(right_header))

    # `mdoffice.titlebg` (+ optional `mdoffice.titlebgpad`) (custom): switches
    # \maketitle from a plain bold title to a colored background block.
    safe_title_bg = sanitize_hex_color(get_value(custom, "titlebg"))
    if safe_title_bg:
        defs.define("titlebgcolor", safe_title_bg)
        title_bg_pad = get_value(custom, "titlebgpad")
        if title_bg_pad:
            defs.define("titlebgpad", sanitize_tex_length(title_bg_pad, default="0pt"))

    # `mdoffice.page-numbering: false` (custom): hide page numbers everywhere.
    if not get_flag(custom, "page-numbering", default=True):
        defs.flag("hidepagenumbers")

    # `mdoffice.first-page-numbering` (custom): documents with a title get an
    # unnumbered, re-styled title page by default; this opts back in.
    has_title = bool(get_value(config, "title"))
    if not get_flag(custom, "first-page-numbering", default=not has_title):
        defs.flag("hidefirstpagenumber")

    # `mdoffice.doc-style` (custom): picks WHICH theme file to load (default
    # "standard-pdf" -> scripts/themes/standard-pdf.tex). Computed here
    # (rather than just before the theme is loaded) because the
    # `numbersections` default below depends on it.
    doc_style = get_value(custom, "doc-style", DEFAULT_DOC_STYLE) or DEFAULT_DOC_STYLE

    # `numbersections` (top-level, pandoc-native): pandoc's own template
    # already sets secnumdepth from this key before header-includes are
    # spliced in. Exam documents are numbered by default (their body
    # headings are the task list), but an explicit `numbersections: false`
    # should still be able to opt out, so this only tells exam.tex to force
    # numbering back on when the user hasn't said otherwise.
    if doc_style == "exam" and get_flag(config, "numbersections", default=True):
        defs.flag("forcenumbersections")

    def_file = defs.write()
    if def_file is not None:
        temp_files.append(def_file)
        command += ["--include-in-header", str(def_file)]

    theme_file = resolve_theme(scripts_dir / "themes", doc_style)
    if theme_file is not None:
        command += ["--include-in-header", str(theme_file)]

    if not get_value(config, "fontsize"):
        command += ["--variable", f"fontsize={DEFAULT_FONTSIZE}"]
    if not get_value(config, "geometry"):
        command += ["--variable", f"geometry={DEFAULT_GEOMETRY}"]

    return TargetPlan(target="pdf", output_file=output_file, command=command, temp_files=temp_files)
