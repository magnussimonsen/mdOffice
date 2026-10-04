# Improvement analysis

Analysis date: 2026-10-04. Covers the backend in `_core/scripts/` and overall user friendliness.

The three bugs listed first were reproduced in a scratch folder. Nothing in the repo was changed as part of the analysis.

## Confirmed bugs (highest priority)

1. **Solutions leak into DOCX, ODT and EPUB.**
   The Lua filters, including `solution_filter.lua`, only run for PDF and Beamer (`LATEX_TARGETS` in `core/filters.py`).
   A DOCX built with `show-solution: false` still contains the solution text.
   This matters for exams: enabling Word output hands out the answers.
   The validator also warns that `show-solution` is an "unknown key" for docx, which is misleading.
   *Fix:* run the solution filter for every target. Render the boxes natively in non-LaTeX formats, or just strip the blocks.

2. **Every `media-*` folder next to the document is deleted.**
   `run_pandoc_command` in `core/pandoc.py` deletes every directory matching `media-*` in the document folder after each build.
   A user folder named `media-mystuff`, with files in it, was deleted after an unrelated DOCX build.
   *Fix:* delete only folders this build created (snapshot before and after), or build in a temporary directory.

3. ~~**A list-style `header-includes` breaks the PDF build.**~~ *Fixed 2026-10-04:* `formats/pdf.py` now reads the key with the new `get_text_block()` in `core/frontmatter.py`, which joins list items with newlines. Beamer was not affected, because it lets pandoc read `header-includes` directly.
   YAML lists are the usual way to write this key, for example `header-includes: [ '\usepackage{xcolor}' ]`.
   `get_value()` calls `str()` on the list, so the Python repr `['\\usepackage{xcolor}']` ends up in the LaTeX preamble and xelatex fails.
   *Fix:* in `formats/pdf.py`, and in `formats/beamer.py` if the same thing happens there, join list items with newlines.

## Backend improvements

- **No tests or CI.** A small pytest suite that builds each file in `_core/examples/` would catch the bugs above. Add a GitHub Action running it on Linux and Windows to protect the OneDrive and Windows workarounds.
- **Schema types are never checked.** Every `Key` declares a type (`bool`, `length`, `hexcolor`, `path`), but `validate.py` only checks key names. Bad values like `titlebg: "#zzz"`, `logo-height: big` or `make-pdf: yes` are silently replaced with defaults. The validator should warn on these.
- ~~**A mistyped theme fails silently.**~~ *Fixed 2026-10-04:* `warn_unknown_theme()` in `core/assets.py` now warns from `formats/pdf.py` and `formats/beamer.py` and lists the available themes. The build continues without a theme. The list includes every theme file, since nothing records which format a theme belongs to. If `doc-style` or `beamer-style` names a theme that doesn't exist, `resolve_theme()` returns `None` and the theme is skipped with no warning. Warn, and list the available themes.
- **A missing Pandoc gives a cryptic error.** It surfaces as "Unhandled exception ... No such file or directory". Check `shutil.which("pandoc")` (and `xelatex` for LaTeX targets) up front and print install instructions.
- **LaTeX errors are hard to read.** The raw xelatex stderr ends in things like `l.44 [`. Pick out the line starting with `!` and add a hint, or keep the full log in a file and point to it.
- **Temporary files can collide.** `_mdoffice_defs.tex` and `_mdoffice_header_includes.tex` use fixed names inside the shared `pdf/` folder. Two documents saved quickly in the same folder can overwrite each other's files. Prefix them with the document stem or use `tempfile`.
- **No timeout on Pandoc.** `subprocess.run` has no `timeout`, so a MiKTeX package-install prompt can hang the build on save indefinitely.
- ~~**Stale `_core_v2` paths.**~~ *Fixed 2026-10-04:* all references now point to `_core/`, including the root `CLAUDE.md` imports, which had silently failed to load the math and text AI instructions. The root `CLAUDE.md`, the `mdoffice.py` comments and the pipeline docstrings point to `_core_v2/scripts/...`, but the folder is `_core/`. The command in `CLAUDE.md` fails as written.
- **Packaging.** A `pyproject.toml` with an `mdoffice` console entry point would replace the long `.venv/bin/python _core/scripts/mdoffice.py ...` invocation.
- **Targets build one after another.** Targets are independent, so they could build in parallel to make multi-format saves faster. This is a low priority.

## Usability improvements

- **Lower the Python requirement.** Requiring Python 3.14 (`.python-version`, the install scripts) is the most likely setup failure, and the README admits this. The code needs about 3.12 at most, for `shutil.rmtree(onexc=...)`. The install scripts should then try `python3` / `py -3` automatically instead of asking users to edit `PYTHON_CMD`.
- **Make LaTeX optional in the installer.** `install_linux.sh` exits if xelatex is missing, though the README says DOCX, ODT, PPTX and EPUB don't need LaTeX. Warn and continue.
- **Add a `doctor` command.** It would check Pandoc, xelatex, the LaTeX packages from `latex-required-packages.txt` and the Python version on demand. Reuse the logic from the install scripts.
- **Add a `new` command.** For example `mdoffice new exam my-test.md`, which copies a quick-start template. That is friendlier than finding and copying template files by hand.
- **Generated AI files overwrite existing ones.** `build-ai-instructions` runs on every save and replaces `CLAUDE.md` and `.continuerules` in the document's folder, including hand-written ones. Only overwrite files that contain the `--- CUSTOM AI INSTRUCTIONS ---` marker, or warn first.
- ~~**Build-on-save runs for every Markdown file.**~~ *Fixed 2026-10-04:* `build-all` in `mdoffice.py` now exits silently when the frontmatter has no `mdoffice:` key. Files with the block but no `make-*` flags still print "nothing to build", and frontmatter warnings are still shown. The run-on-save pattern `.*\.md$` also fires on README.md and on notes without frontmatter. This is harmless but noisy. Exit quietly when there is no `mdoffice:` block.
- **Make failures visible.** Build-on-save output only appears in the output panel, so a failed PDF is easy to miss. Consider an option to open the PDF on success and a clear one-line error summary at the end.
- ~~**Keep the solution labels consistent.**~~ *Done 2026-10-04:* the defaults are now "Suggested solution" and "Write solution in this box" in `solution_filter.lua`, `core/schema.py`, the quick-start templates and the regenerated `doc/frontmatter-reference.md`.

## Suggested order

1. Fix the three confirmed bugs.
2. Add a basic test suite that builds the examples, plus CI.
3. Add value type validation, theme warnings and Pandoc/xelatex checks up front.
4. Make the setup easier: lower the Python version, make LaTeX optional, add `doctor` and `new`.
