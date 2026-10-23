# Naming conventions

Rules for naming themes, files and frontmatter keys in mdOffice. Follow them
when adding something new, so names stay predictable for users.

General rule: lowercase words joined by hyphens (kebab-case), for example
`exam-pdf` or `show-solution`.

## Themes

Name themes `<style>-<output>`:

| Theme | Output | Set with |
|---|---|---|
| `standard-pdf` | PDF | `mdoffice.doc-style` |
| `exam-pdf` | PDF | `mdoffice.doc-style` |
| `fancy-pdf` | PDF | `mdoffice.doc-style` |
| `fancy-beamer` | Beamer | `mdoffice.beamer-style` |
| `beamer` | Beamer | `mdoffice.beamer-style` |

Exception: `beamer` keeps its plain name, since Beamer is a standard in its
own right.

Theme files are named exactly like the theme:

- Official themes: `_core/scripts/themes/<theme>.tex`
- Custom themes: `custom_themes/<theme>/theme.tex`

## Quick-start templates

Name them `quickstart-<theme>.md` in `_core/quick-start/`, for example
`quickstart-fancy-pdf.md`. Templates that are not tied to one theme use the
output format instead: `quickstart-epub.md`.

Built output is named after the source file (`pdf/quickstart-fancy-pdf.pdf`),
so renaming a template also means renaming its built output.

The VS Code extension lists every `quickstart-*.md` automatically. A template
with its own menu item also needs an entry in
`_core/vscode-extension/mdoffice-insert/extension.js` and `package.json`.

## Frontmatter keys

- Keys that mdOffice invents live under `mdoffice:` and use kebab-case:
  `add-answer-sheet`, `show-solution`, `page-numbering`.
- Output switches are named `make-<format>`: `make-pdf`, `make-docx`.
- Pandoc's own keys (`title`, `fontsize`, `logo`, ...) stay at the top level
  with pandoc's names. Never move or rename them.

Known exceptions, from before this rule: `leftheader`, `rightheader`,
`titlebg` and `titlebgpad`. Leave them as they are unless they are renamed
with backwards compatibility, as described below.

## Renaming something users already write

Users have the old name in their documents, so a rename must not break them:

1. Add the old name to `THEME_ALIASES` in `_core/scripts/core/assets.py`.
   Old names then still work, and the build log tells the user the new name.
   Keys have no alias table yet: add one before renaming a key.
2. Search the whole repo for the old name: examples, quick-start files,
   READMEs, `docs/`, the VS Code extension and code that compares names
   (for example `doc_style == "exam-pdf"` in `formats/pdf.py`).
3. Regenerate the reference: `python _core/scripts/mdoffice.py docs`.
4. Rebuild and reinstall the VS Code extension if its labels or file names
   changed.

## What not to rename

- Internal LaTeX macro names such as `\fancypdf@headcolor`. Users never see
  them, and LaTeX does not allow `-` in macro names.
- Screenshot file names in `docs/img/`.
