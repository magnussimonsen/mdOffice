---
title: "Native Diagrams with TikZ"
fontsize: 12pt
numbersections: false
header-includes: |
  \usepackage{tikz}
  \usetikzlibrary{positioning, arrows.meta}

mdoffice:
  make-pdf: true
  doc-style: exam
---

## From Markdown straight to a vector diagram
A `tikzpicture` block written in the Markdown file is passed through Pandoc
unchanged and compiled by xelatex, so the flowchart below is a real vector
drawing, not a pasted-in image.

\begin{figure}[h]
\centering
\begin{tikzpicture}[
  every node/.style={draw, rounded corners, fill=blue!10, minimum width=2.8cm,
                     minimum height=0.9cm, align=center, font=\small},
  every path/.style={-{Stealth[length=2.5mm]}, thick},
  node distance=1.4cm
]
  \node (md)  {Markdown\\+ TikZ};
  \node (pdc) [right=of md]  {mdoffice.py\\(Pandoc + xelatex)};
  \node (pdf) [right=of pdc] {PDF};

  \draw (md) -- (pdc);
  \draw (pdc) -- (pdf);
\end{tikzpicture}
\caption{One Markdown file, one command, one PDF with the diagram already in it}
\end{figure}



