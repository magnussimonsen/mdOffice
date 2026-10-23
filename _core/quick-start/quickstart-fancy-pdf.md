---
# Basic Pandoc metadata (active)
title: "PDF title"
author: "Your name"
date: "2026-08-15"

# Common Pandoc metadata (optional)
# lang: nb-NO
# subtitle: "Optional subtitle"
# toc: true
# numbersections: true

# PDF top-level options (optional)
# fontsize: 11pt
# mainfont: "Times New Roman"
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
  doc-style: "fancy-pdf"

  # PDF options (optional)
  # leftheader: "School name"
  # rightheader: "Course code"
  # page-numbering: true
  # first-page-numbering: false
  # show-solution: false
  # show-blankbox: false
  # solution-text: "Suggested solution"
  # blankbox-text: "Write solution in this box"
---

<!-- Example content: replace everything below the frontmatter with your own text.
Comments like this one are only visible here. They never appear in the PDF. -->

# Colored headings
\blueheader

<!-- Put \blueheader, \redheader, \greenheader, \cyanheader or \grayheader
on the line right after a heading to give it a colored bar. Without a macro
the heading is plain. The color only applies to that one heading. -->

This heading has a blue bar. The next heading has no macro, so it is plain.

## A plain heading

Colors never carry over from one heading to the next.

# Boxes
\greenheader

<!-- Every box comes in blue, red, green, cyan and gray.
  bluebox*  : a box with a title and no number, e.g. \begin{bluebox*}{Title}
  bluebox   : a numbered box. It also takes a label, e.g. \begin{bluebox}{Title}{label}
  bluefocus : a tinted box without a title, for key formulas and remarks
Inside a box, write LaTeX: \textbf{...} for bold and \emph{...} for italic. -->

\begin{bluebox*}{Definition}
A \textbf{prime number} is a whole number greater than 1 that can only be divided by 1 and itself.
\end{bluebox*}

\begin{redbox}{Theorem}{thm:pythagoras}
In a right triangle with legs $a$ and $b$ and hypotenuse $c$:
$$a^2 + b^2 = c^2$$
\end{redbox}

\begin{greenfocus}
\textbf{Tip:} Check your answer by putting it back into the original equation.
\end{greenfocus}

## Two columns
\redheader

<!-- Columns: one outer block with six colons, and one inner block with
three colons per column. The widths should add up to less than 100%.
The same syntax works in fancy-beamer slides.

Code: a block between ``` lines is printed in a monospace font. Write the
language after the first ``` (python, r, javascript, ...) to get colored code.

Graph: change the function in \addplot. width=\linewidth makes the graph fit
its column, and grid=both draws the background grid. -->

:::::: columns
::: {.column width="48%"}
The Python code computes some values of $f(x) = x^2 - 2x - 3$. The graph on the right shows the same function.

```python
def f(x):
    return x**2 - 2*x - 3

for x in range(-1, 4):
    print(x, f(x))
```
:::
::: {.column width="48%"}
\begin{tikzpicture}
\begin{axis}[
  axis lines=middle, grid=both,
  xlabel={$x$}, ylabel={$y$},
  xmin=-2, xmax=4.5, ymin=-5, ymax=5.5,
  xtick distance=1, ytick distance=1,
  ticklabel style={font=\footnotesize},
  width=\linewidth, height=7cm,
  domain=-1.8:3.8, samples=100]
\addplot[thick, blue] {x^2 - 2*x - 3};
\end{axis}
\end{tikzpicture}
:::
::::::

## LaTeX tables
\grayheader

<!-- A LaTeX table gives more control than a Markdown table:
  {|c|p{7cm}|c|}  one letter per column: l = left, c = centered, r = right,
                  p{7cm} = fixed width, the text wraps. | draws a vertical line.
  >{\raggedright\arraybackslash}p{7cm}  the same p column, but with the text
                  left-aligned instead of stretched to fill each line.
  &               moves to the next cell. \\ ends the row.
  \hline          draws a horizontal line.
  \multicolumn{3}{|c|}{Text}  one cell that spans 3 columns.
Math works inside the cells as usual: $x^2$. -->

\begin{center}
\begin{tabular}{|c|>{\raggedright\arraybackslash}p{7cm}|c|}
\hline
\multicolumn{3}{|c|}{\textbf{Plan for the chapter}} \\
\hline
\textbf{Week} & \textbf{Topic} & \textbf{Test} \\
\hline
1 & Linear functions $f(x) = ax + b$ and their graphs & \\
\hline
2 & Quadratic functions: zeros, vertex and the quadratic formula & Yes \\
\hline
\end{tabular}
\end{center}

## Warning and info
\cyanheader

<!-- \warn and \info print a fixed message. The CustomMsg versions take your
own text and an optional color: myblue, myred, mygreen, mycyan or mygray. -->

- \warn
- \info
- \warnCustomMsg{Remember units in every answer}
- \infoCustomMsg[mygreen]{This section is a repetition}
