---
title: "mdOffice: The Office suite in a code editor"
subtitle: "Turn VS Code into your main office workplace using Markdown and LaTeX"
fontsize: 11pt
logo: img/mdOffice_logo_light.png
toc: true
numbersections: false

mdoffice:
  make-pdf: true
  doc-style: exam # Users can make their own doc-style. See doc/frontmatter-reference.md.
  titlebg: "#0bc2cc"
  titlebgpad: 8pt
  header: "A simple mdOffice PDF example with the exam doc style"
  page-numbering: true
---

This PDF is built entirely from the Markdown file that produced it, using small LaTeX blocks for things like **math** and **footnotes**. Standard LaTeX \textbf{references} and \textbf{labels} work too. The logo, colored title block, header, live math, and table of contents are all driven by the frontmatter block[^frontmatter] above and a user customizable doc-style theme.

[^frontmatter]: The frontmatter block has two parts. The top level keys (`title`, `subtitle`, `fontsize`, `logo`, `toc`, `numbersections`) are standard Pandoc keys. The keys nested under `mdoffice:` (`make-pdf`, `doc-style`, `titlebg`, `titlebgpad`, `header`, `page-numbering`) are mdOffice's own keys.

## Use AI to generate template markdown and LaTeX code
Inline math written in LaTeX looks like this: $x^2 - 5x + 6 = 0$. 
\begin{align}
x^2 - 5x + 6 &= 0 \\
x &= \frac{5 \pm \sqrt{(-5)^2 - 4\cdot 1\cdot 6}}{2\cdot 1} \\
x &= 2 \quad \text{or} \quad x = 3
\end{align}

## Built with a few frontmatter keys
Everything you see on this page (the logo, the colored title, the header, the contents list) comes from a handful of keys in the frontmatter block. The `doc-style` theme itself lives in `_core_v2/scripts/themes/exam.tex` and can be edited directly, or copied as a starting point for your own theme.

### Frontmatter keys used here
| Key | What it does |
|---|---|
| `make-pdf: true` | Builds a PDF from this file on save |
| `doc-style: exam` | Selects this theme: logo in the header, colored title block |
| `titlebg` | Sets the title block's background color |
| `titlebgpad` | Sets the padding around the title text inside that colored block |
| `logo` | Places the logo in the header of every page |
| `header` | The right-aligned text at the top of every page |
| `page-numbering: true` | Shows page numbers on every page |
| `toc: true` | Generates the contents list above |
