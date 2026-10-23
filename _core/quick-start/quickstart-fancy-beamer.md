---
# Basic Pandoc metadata (active)
title: "Slide deck title"
author: "Your name"
date: "2026-08-15"

# Beamer top-level options (optional)
# aspectratio: 169
# fontsize: 12pt
# sansfont: "Fira Sans"
# sansfont options: "Open Sans", "Source Sans Pro", "Arial", "Calibri", "DejaVu Sans"
# note: choose a font installed on your machine (Arial/Calibri common on Windows, DejaVu Sans common on Linux)
# logo: "img/logo.png"
# logo-height: 0.8cm

# Common Pandoc metadata (optional)
# lang: nb-NO

mdoffice:
  make-beamer: true
  beamer-style: "fancy-beamer"

  # Beamer options (optional)
  # page-numbering: true
  # show-solution: false
  # show-blankbox: false
  # solution-text: "Suggested solution"
  # blankbox-text: "Write solution in this box"

  # Optional extra outputs
  # make-pdf: true
  # make-pptx: true
---

## Welcome
\blueheader

<!-- Example content: replace everything below the frontmatter with your own slides.
Comments like this one are only visible here. They never appear in the slides.
Nothing may come before the first "##" heading, or you get an empty slide.

Each "##" heading starts a new slide. Put \blueheader, \redheader,
\greenheader, \cyanheader or \grayheader on the line right after the slide
title to color the header bar. -->

- Each `##` heading starts a new slide
- Bullet points are written as normal Markdown
- Math works too: $a^2 + b^2 = c^2$

## Boxes
\greenheader

<!-- Every box comes in blue, red, green, cyan and gray.
  bluebox*  : a box with a title and no number, e.g. \begin{bluebox*}{Title}
  bluebox   : a numbered box. It also takes a label, e.g. \begin{bluebox}{Title}{label}
  bluefocus : a tinted box without a title, for key formulas and remarks
Inside a box, write LaTeX: \textbf{...} for bold and \emph{...} for italic. -->

\begin{bluebox*}{Definition}
A \textbf{prime number} is a whole number greater than 1 that can only be divided by 1 and itself.
\end{bluebox*}

\begin{greenfocus}
\textbf{Example:} 2, 3, 5, 7 and 11 are the first five prime numbers.
\end{greenfocus}

## Two columns
\cyanheader

<!-- Columns: one outer block with six colons, and one inner block with
three colons per column. The widths should add up to less than 100%. -->

:::::: {.columns totalwidth="\textwidth"}
::: {.column width="48%"}
**Left column**

- Text, lists and math
- or boxes, as on the right
:::
::: {.column width="48%"}
\begin{cyanfocus}
\textbf{Exercise:} Solve $3x - 4 = 11$.
\end{cyanfocus}
:::
::::::

## LaTeX tables
\grayheader

<!-- A LaTeX table gives more control than a Markdown table:
  {|c|c|c|}       one letter per column: l = left, c = centered, r = right,
                  p{3cm} = fixed width, the text wraps. | draws a vertical line.
  &               moves to the next cell. \\ ends the row.
  \hline          draws a horizontal line.
  \multicolumn{6}{|c|}{Text}  one cell that spans 6 columns.
  \arraystretch   makes the rows taller (1.4 = 40 % taller).
Math works inside the cells as usual: $x^2$. -->

The values of $f(x) = x^2 - 2x - 3$:

\begin{center}
\renewcommand{\arraystretch}{1.4}
\begin{tabular}{|c|c|c|c|c|c|}
\hline
\multicolumn{6}{|c|}{\textbf{Value table}} \\
\hline
$x$ & $-1$ & $0$ & $1$ & $2$ & $3$ \\
\hline
$f(x)$ & $0$ & $-3$ & $-4$ & $-3$ & $0$ \\
\hline
\end{tabular}
\end{center}

## Warning and info
\redheader

<!-- \warn and \info print a fixed message. The CustomMsg versions take your
own text and an optional color: myblue, myred, mygreen, mycyan or mygray. -->

- \warn
- \info
- \warnCustomMsg{Remember units in every answer}
- \infoCustomMsg[mygreen]{This slide is a repetition}
