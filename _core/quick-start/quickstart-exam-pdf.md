---
# Basic Pandoc metadata (active)
title: "Exam title"
author: "Your name"
date: "2026-08-15"

# Common Pandoc metadata (optional)
# lang: nb-NO
# subtitle: "Optional subtitle"
# toc: false
# numbersections: true

# PDF top-level options (optional)
# fontsize: 12pt
# geometry: a4paper,top=2.00cm,bottom=2.00cm,left=2.54cm,right=2.54cm
# sansfont: "Fira Sans"
# sansfont options: "Open Sans", "Source Sans Pro", "Arial", "Calibri", "DejaVu Sans"
# note: choose a font installed on your machine (Arial/Calibri common on Windows, DejaVu Sans common on Linux)
# logo: "img/logo.png"
# logo-height: 1.2cm

# Extra LaTeX packages
header-includes: |
  \usepackage{pgfplots}         % function graphs (also loads TikZ for drawings)
  \pgfplotsset{compat=1.18}
  % Remove the % at the start of a line to use that package:
  % \usepackage{siunitx}        % numbers and units: \qty{9.81}{m/s^2}, \num{12345.6}
  % \usetikzlibrary{angles, quotes, calc, arrows.meta}  % geometry: marked angles, arrows
  % \usepackage{mhchem}         % chemistry: \ce{2H2 + O2 -> 2H2O}
  % \usepackage{circuitikz}     % electrical circuits

mdoffice:
  make-pdf: true
  doc-style: "exam-pdf"

  # Exam-friendly options (optional)
  # header: "MAT101"
  # page-numbering: true
  # add-answer-sheet: 2   # grid answer sheets (front + back) at the end
  # add-draft-sheet: 1    # grid draft sheets after the answer sheets
  # titlebg color examples:
  # titlebg: "D9EEF9"      # blue
  # titlebg: "D6E8CF"    # green
  # titlebg: "#ffa073"   # orange/red (same as norwegian_highshool_exam_template.md)
  # titlebg: "D9D9D9"    # gray
  # titlebg: "#00b5c0"   # cyan
  titlebg: "#d8b4fe"   # purple
  titlebgpad: "6pt"

  # Solution/blankbox toggles
  show-solution: false   # true = print the solutions (answer key)
  show-blankbox: true    # false = hide the answer boxes
  # solution-text: "Suggested solution"
  # blankbox-text: "Write solution in this box"
---

<!-- Example content: replace everything below the frontmatter with your own exam.
Comments like this one are only visible here. They never appear in the PDF.

How this template works:
- Each "##" heading is one task. Tasks are numbered automatically.
- "::: blankbox" makes an empty box for handwritten answers. The number
  inside is the height in lines. Boxes are shown when show-blankbox is true.
- "::: solution" holds the solution. It is hidden unless show-solution is
  true. Build once with false (student version) and once with true (answer key). -->

Allowed aids: calculator and writing materials. Write your answers in the boxes.

## Equations

**a)** Solve the equation $2x + 3 = 11$.

::: blankbox
6
:::

::: solution
Subtract 3 from both sides, then divide by 2:

$$
\begin{align*}
2x + 3 &= 11 \\
2x &= 8 \\
x &= 4
\end{align*}
$$

**Answer:** $x = 4$.
:::

**b)** Solve the equation $x^2 - 5x + 6 = 0$.

::: blankbox
8
:::

::: solution
Applying the quadratic formula with $a = 1$, $b = -5$ and $c = 6$:

$$
\begin{align*}
x &= \frac{5 \pm \sqrt{(-5)^2 - 4 \cdot 1 \cdot 6}}{2 \cdot 1} \\
&= \frac{5 \pm 1}{2}
\end{align*}
$$

**Answer:** $x = 2$ or $x = 3$.
:::

## Graph

The figure shows the graph of the function $f(x) = x^2 - 2x - 3$.

<!-- Graph template (pgfplots). Change the function in \addplot, and the
visible window with xmin, xmax, ymin and ymax. domain is the x-interval the
function is drawn on. grid=both draws the background grid. -->

\begin{center}
\begin{tikzpicture}
\begin{axis}[
  axis lines=middle, grid=both,
  xlabel={$x$}, ylabel={$y$},
  xmin=-3, xmax=5.5, ymin=-5, ymax=6.5,
  xtick distance=1, ytick distance=1,
  ticklabel style={font=\footnotesize},
  width=9cm, height=8cm,
  domain=-2.5:4.5, samples=100]
\addplot[thick, blue] {x^2 - 2*x - 3};
\end{axis}
\end{tikzpicture}
\end{center}

**a)** Complete the value table for $f$.

<!-- A LaTeX table gives more control than a Markdown table:
  {|c|c|p{1cm}|}  one letter per column: l = left, c = centered, r = right,
                  p{1cm} = fixed width, here leaving room to write. | draws a vertical line.
  &               moves to the next cell. \\ ends the row.
  \hline          draws a horizontal line.
  \multicolumn{3}{|c|}{Text}  one cell that spans 3 columns.
  \arraystretch   makes the rows taller (1.6 = 60 % taller).
Math works inside the cells as usual: $x^2$. -->

\begin{center}
\renewcommand{\arraystretch}{1.6}
\begin{tabular}{|c|p{1cm}|p{1cm}|p{1cm}|p{1cm}|p{1cm}|}
\hline
$x$ & $-1$ & $0$ & $1$ & $2$ & $3$ \\
\hline
$f(x)$ & & & & & \\
\hline
\end{tabular}
\end{center}

::: solution
Put each $x$ value into $f(x) = x^2 - 2x - 3$. For example $f(-1) = 1 + 2 - 3 = 0$.

\begin{center}
\begin{tabular}{|c|c|c|c|c|c|}
\hline
$x$ & $-1$ & $0$ & $1$ & $2$ & $3$ \\
\hline
$f(x)$ & $0$ & $-3$ & $-4$ & $-3$ & $0$ \\
\hline
\end{tabular}
\end{center}

**Answer:** The values are $0$, $-3$, $-4$, $-3$ and $0$.
:::

**b)** Use the graph to find the zeros of $f$.

::: blankbox
4
:::

::: solution
The zeros are where the graph crosses the $x$-axis. Reading the graph, this happens at $x = -1$ and $x = 3$.

**Answer:** The zeros of $f$ are $x = -1$ and $x = 3$.
:::

## Word problem

A rectangle is 3 cm longer than it is wide. The perimeter is 26 cm. How wide is the rectangle?

<!-- Another way to set the height of a box: -->
::: {.blankbox lines=10}
:::

::: solution
Call the width $w$. The length is then $w + 3$, and the perimeter is two widths plus two lengths:

$$
\begin{align*}
2w + 2(w + 3) &= 26 \\
4w + 6 &= 26 \\
w &= 5
\end{align*}
$$

**Answer:** The rectangle is 5 cm wide.
:::
