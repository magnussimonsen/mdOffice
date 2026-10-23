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
# fontsize: 12pt
# geometry: a4paper,top=2.00cm,bottom=2.00cm,left=2.54cm,right=2.54cm
# mainfont: "Times New Roman"
# sansfont: "Fira Sans"
# sansfont options: "Open Sans", "Source Sans Pro", "Arial", "Calibri", "DejaVu Sans"
# note: choose a font installed on your machine (Arial/Calibri common on Windows, DejaVu Sans common on Linux)
# logo: "img/logo.png"
# logo-height: 1.2cm

# Extra LaTeX packages
header-includes: |
  \usepackage{tikz}             % drawings
  % \usepackage{pgfplots}       % function graphs (see the exam-pdf template)
  % \pgfplotsset{compat=1.18}
  % Remove the % at the start of a line to use that package:
  % \usepackage{siunitx}        % numbers and units: \qty{9.81}{m/s^2}, \num{12345.6}
  % \usetikzlibrary{angles, quotes, calc, arrows.meta}  % geometry: marked angles, arrows
  % \usepackage{mhchem}         % chemistry: \ce{2H2 + O2 -> 2H2O}
  % \usepackage{circuitikz}     % electrical circuits

mdoffice:
  make-pdf: true
  doc-style: "standard-pdf"

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

# Introduction

This page shows the most common Markdown formatting. Write *italic*, **bold** and `code` straight in the text. Leave an empty line between paragraphs.

## Lists

- A bullet point
- Another bullet point
    - Indent with four spaces for a sub-point

1. First step
2. Second step

## Math

<!-- Inline math goes between single dollar signs: $...$
Display math goes between double dollar signs: $$...$$
Wrap align blocks in $$ as well. -->

Inline math such as $a^2 + b^2 = c^2$ sits inside the sentence. Display math gets its own line:

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

Use `align` to line up the steps of a calculation. The `&` marks where the lines line up, and `\\` ends a line:

$$
\begin{align*}
(x + 3)^2 &= x^2 + 2 \cdot 3 \cdot x + 3^2 \\
&= x^2 + 6x + 9
\end{align*}
$$

## Tables

| Shape     | Area        |
|-----------|-------------|
| Square    | $s^2$       |
| Rectangle | $l \cdot w$ |
| Circle    | $\pi r^2$   |

Markdown tables are quick to write. For more control, such as merged cells, lines between cells and text that wraps inside a cell, write the table in LaTeX:

<!-- A LaTeX table gives more control than a Markdown table:
  {|l|c|p{6cm}|}  one letter per column: l = left, c = centered, r = right,
                  p{6cm} = fixed width, the text wraps. | draws a vertical line.
  >{\raggedright\arraybackslash}p{6cm}  the same p column, but with the text
                  left-aligned instead of stretched to fill each line.
  &               moves to the next cell. \\ ends the row.
  \hline          draws a horizontal line.
  \multicolumn{3}{|c|}{Text}  one cell that spans 3 columns.
Math works inside the cells as usual: $x^2$. -->

\begin{center}
\begin{tabular}{|l|c|>{\raggedright\arraybackslash}p{6cm}|}
\hline
\multicolumn{3}{|c|}{\textbf{Common shapes}} \\
\hline
\textbf{Shape} & \textbf{Area} & \textbf{Note} \\
\hline
Square & $s^2$ & All four sides have the same length $s$. \\
\hline
Circle & $\pi r^2$ & $r$ is the radius, which is half the diameter. \\
\hline
\end{tabular}
\end{center}

## Drawings with TikZ

<!-- A TikZ drawing is made from coordinates (x,y), measured in cm from (0,0).
The light grid and the numbers on the axes show the coordinate system, so it
is easy to see where each point goes. Delete the grid and number lines when
the drawing is finished. Lines starting with % are LaTeX comments. -->

\begin{center}
\begin{tikzpicture}
  % Background grid and axes
  \draw[help lines] (0,0) grid (6,4);
  \draw[thick, ->] (0,0) -- (6.4,0) node[right] {$x$};
  \draw[thick, ->] (0,0) -- (0,4.4) node[above] {$y$};
  \foreach \x in {1,...,6} \node[below] at (\x,0) {\x};
  \foreach \y in {1,...,4} \node[left] at (0,\y) {\y};
  % The drawing: a triangle and a marked point
  \draw[thick, blue, fill=blue!15] (1,1) -- (5,1) -- (5,3) -- cycle;
  \fill[red] (5,3) circle (2pt) node[above right] {$(5,3)$};
\end{tikzpicture}
\end{center}

## Quotes and footnotes

> A quote starts with `>` at the beginning of the line.

A footnote is marked in the text like this.[^1]

[^1]: The footnote text is printed at the bottom of the page.
