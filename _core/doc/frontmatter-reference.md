# mdOffice v2 -- Frontmatter reference

**Generated from `formats/*.py` schemas -- do not hand-edit.**
Run `mdoffice.py docs` (or `python generate_reference.py`) to regenerate
after changing a `SCHEMA` declaration.

Every option below is optional. Two kinds of keys share one YAML frontmatter
block:

- **Pandoc built-in keys** (e.g. `title`, `fontsize`, `logo`) stay at the
  **top level** of the frontmatter, exactly where pandoc expects them. Some
  of these are also read by mdOffice's own code -- for path resolution,
  defaulting, or translating into a CLI flag -- and are marked
  **"intercepted"** below.
- **mdOffice custom keys** -- concepts pandoc has never heard of -- live
  nested under one `mdoffice:` map, e.g.:

```yaml
---
title: My Document
fontsize: 12pt

mdoffice:
  make-pdf: true
  doc-style: standard-pdf
---
```

Any pandoc metadata key not listed here (e.g. `subtitle`, `author`, `toc-depth`,
`colorlinks`, ...) is pure passthrough -- mdOffice's code never touches it.
See pandoc's manual for the writer in question.

## Global keys (`mdoffice:`)

Apply regardless of which targets are built.

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `mdoffice.ai-instructions` | path |  | Path (or list of paths) to AI-instruction files injected into CLAUDE.md / .continuerules |
| `mdoffice.make-beamer` | bool | `False` | Build the beamer target on `build-all` |
| `mdoffice.make-docx` | bool | `False` | Build the docx target on `build-all` |
| `mdoffice.make-epub` | bool | `False` | Build the epub target on `build-all` |
| `mdoffice.make-odt` | bool | `False` | Build the odt target on `build-all` |
| `mdoffice.make-pdf` | bool | `False` | Build the pdf target on `build-all` |
| `mdoffice.make-pptx` | bool | `False` | Build the pptx target on `build-all` |

## beamer

### `mdoffice:` keys (custom)

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `mdoffice.beamer-style` | str |  | mdOffice theme to load from scripts/themes/, e.g. beamer, fancybeamer |
| `mdoffice.blankbox-text` | str | `Write your solution in this box` | Label on blank answer boxes (read by solution_filter.lua) |
| `mdoffice.page-numbering` | bool | `True` | false = hide the frame-number footline |
| `mdoffice.show-blankbox` | bool | `False` | Show ::: blankbox ... ::: blocks (read by solution_filter.lua, not Python) |
| `mdoffice.show-solution` | bool | `False` | Show ::: solution ... ::: blocks (read by solution_filter.lua, not Python) |
| `mdoffice.solution-text` | str | `Solution` | Label on the solution box frame, e.g. "Løsning" (read by solution_filter.lua) |

### Top-level keys mdOffice also reads (intercepted)

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `aspectratio` | str | `169` | mdOffice supplies this default if the key is absent |
| `fontsize` | str | `12pt` | mdOffice supplies this default if the key is absent |
| `logo` | path |  | Logo image; mdOffice resolves/sanitizes the path (see note below) |
| `logo-height` | length | `0.8cm` | Logo height |

## docx

### `mdoffice:` keys (custom)

_None._

### Top-level keys mdOffice also reads (intercepted)

_None._

## epub

### `mdoffice:` keys (custom)

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `mdoffice.epub-css` | path |  | Stylesheet applied to the epub; mdOffice resolves the path and passes it as --css |

### Top-level keys mdOffice also reads (intercepted)

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `cover-image` | path |  | Pandoc-vocabulary name; mdOffice resolves the path and passes --epub-cover-image |
| `toc` | bool | `False` | Pandoc-vocabulary name, but the epub writer needs an explicit --toc flag, so mdOffice reads it |

## odt

### `mdoffice:` keys (custom)

_None._

### Top-level keys mdOffice also reads (intercepted)

_None._

## pdf

### `mdoffice:` keys (custom)

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `mdoffice.blankbox-text` | str | `Write your solution in this box` | Label on blank answer boxes (read by solution_filter.lua) |
| `mdoffice.doc-style` | str | `standard-pdf` | Theme to load from scripts/themes/, e.g. standard-pdf, exam |
| `mdoffice.first-page-numbering` | bool | `False` | true = also number the title/first page (theme-dependent: exam.tex has no separate title page, so this has no effect there) |
| `mdoffice.header` | str |  | Small text shown top-right on every page |
| `mdoffice.page-numbering` | bool | `True` | false = hide page numbers everywhere |
| `mdoffice.show-blankbox` | bool | `False` | Show ::: blankbox ... ::: blocks (read by solution_filter.lua, not Python) |
| `mdoffice.show-solution` | bool | `False` | Show ::: solution ... ::: blocks (read by solution_filter.lua, not Python) |
| `mdoffice.solution-text` | str | `Solution` | Label on the solution box frame, e.g. "Løsning" (read by solution_filter.lua) |
| `mdoffice.titlebg` | hexcolor |  | 6-digit hex color (no '#') for a block behind the title (theme-dependent: exam.tex uses it, standard-pdf.tex doesn't) |
| `mdoffice.titlebgpad` | length |  | Padding around the title text inside that colored block (see titlebg) |

### Top-level keys mdOffice also reads (intercepted)

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `fontsize` | str | `12pt` | mdOffice supplies this default if the key is absent |
| `geometry` | str | `a4paper,top=2.00cm,bottom=2.00cm,left=2.54cm,right=2.54cm` | mdOffice supplies this default if the key is absent |
| `logo` | path |  | Logo image path; mdOffice resolves it relative to the doc and sanitizes it for TeX |
| `logo-height` | length | `1.2cm` | Logo height |
| `subtitle` | str |  | Pandoc-vocabulary name; mdOffice defines \mdsubtitle since pandoc's own subtitle mechanism doesn't survive a custom \maketitle |

## pptx

### `mdoffice:` keys (custom)

_None._

### Top-level keys mdOffice also reads (intercepted)

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `reference-doc` | path |  | pandoc's own option; mdOffice resolves the path relative to the doc |
