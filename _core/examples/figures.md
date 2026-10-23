---
title: "Figures with TikZ"
subtitle: "Drawing a physics figure directly in Markdown"
fontsize: 12pt
lang: "en-US"
numbersections: false
header-includes: 
  \usepackage{tikz}

mdoffice:
  make-pdf: true
  doc-style: exam-pdf
  page-numbering: true
  show-solution: false
  show-blankbox: false
  ai-instructions:
    - "../ai-instructions/math.md"
    - "../ai-instructions/text.md"
---

## Task 6: Block and hanging weight over a pulley

A block with mass $M = 2.0\,\text{kg}$ lies on a horizontal table. The block is
attached to a hanging weight with mass $m = 0.50\,\text{kg}$ by a massless string
that runs over a frictionless pulley, as shown in the figure. The coefficient of
friction between the block and the table is $\mu = 0.15$. The system is released
from rest.

\begin{center}
\begin{tikzpicture}[thick, scale=1.5, every node/.style={scale=1.3}]
\fill[gray!25] (0,-0.3) rectangle (5,0);
\draw (0,0) -- (5.0,0) -- (5,-0.3);
\draw[fill=blue!10] (1,0) rectangle (2.4,1) node[midway] {$M$};
\draw (5,0) -- (5.3,0.3);
\draw[fill=white] (5.3,0.3) circle (0.3);
\fill (5.3,0.3) circle (1.2pt);
\draw (2.4,0.6) -- (5.3,0.6);
\draw (5.6,0.3) -- (5.6,-1.5);
\draw[fill=red!10] (5.3,-2.2) rectangle (5.9,-1.5) node[midway] {$m$};
\end{tikzpicture}
\end{center}








