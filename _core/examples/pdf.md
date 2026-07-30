---
title: "mdOffice - The Office suite in a code editor"
subtitle: "Turn VS Code into your main office workplace using Markdown and LaTeX"
fontsize: 11pt
logo: img/mdOffice_logo_light.png
toc: true
numbersections: true
header-includes: |
  \usepackage{pgfplots}
  \pgfplotsset{compat=1.18}

mdoffice:
  make-pdf: true
  doc-style: exam # Users can make their own doc-style. See doc/frontmatter-reference.md.
  titlebg: "#00b5c0"
  titlebgpad: 8pt
  header: "mdOffice PDF Example"
  page-numbering: true
---

This PDF is built entirely from the Markdown file that produced it, no design tool, no manual export required. The logo, colored title block, header, live math, and table of contents are all driven by the frontmatter block above and a customizable doc-style theme.

## Use AI to generate template markdown and LaTeX code
Inline math looks like this: $x^2 - 5x + 6 = 0$ has two real roots. Solve it and plot it side by side, in the same PDF, with no separate diagramming tool:

\begin{figure}[h]
\centering
\begin{minipage}[c]{0.42\textwidth}
\begin{align*}
x^2 - 5x + 6 &= 0 \\
x &= \frac{5 \pm \sqrt{(-5)^2 - 4\cdot 1\cdot 6}}{2\cdot 1} \\
x &= 2 \quad \text{or} \quad x = 3
\end{align*}
\end{minipage}
\hfill
\begin{minipage}[c]{0.5\textwidth}
\centering
\begin{tikzpicture}
\begin{axis}[axis lines=middle, xlabel={$x$}, ylabel={$y$}, xmin=-1, xmax=6,
  ymin=-3, ymax=8, width=6cm, height=6cm, domain=-0.5:5.5, samples=100]
\addplot[thick, blue] {x^2 - 5*x + 6};
\addplot[only marks, mark=*, red] coordinates {(2,0) (3,0)};
\end{axis}
\end{tikzpicture}
\end{minipage}
\caption{Solving $x^2 - 5x + 6 = 0$ and its graph, side by side}
\end{figure}

## Built with a few frontmatter keys
Everything you see on this page (the logo, the colored title, the header, the contents list) comes from a handful of keys in the frontmatter block. The `doc-style` theme itself lives in `_core_v2/scripts/themes/exam.tex` and can be edited directly, or copied as a starting point for your own theme.

### Frontmatter keys used here
| Key | What it does |
|---|---|
| `doc-style: exam` | Selects this theme: logo in the header, colored title block |
| `titlebg` | Sets the title block's background color |
| `logo` | Places the logo in the header of every page |
| `header` | The right-aligned text at the top of every page |
| `toc: true` | Generates the contents list above |
