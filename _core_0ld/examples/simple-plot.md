---
title: "Native Plots with pgfplots"
fontsize: 12pt
numbersections: false
header-includes: |
  \usepackage{pgfplots}
  \pgfplotsset{compat=1.18}

mdoffice:
  make-pdf: true
  doc-style: exam
---

## Solving and plotting a quadratic

Consider the function $f(x) = x^2 - 2x - 3$. Factoring gives:

\begin{align*}
f(x) &= x^2 - 2x - 3 \\
     &= (x - 3)(x + 1)
\end{align*}

Setting $f(x) = 0$ shows that this function has two roots, at $x = -1$ and
$x = 3$.

\begin{figure}[h]
\centering
\begin{tikzpicture}
\begin{axis}[axis lines=middle, xlabel={$x$}, ylabel={$y$}, xmin=-4, xmax=6,
  ymin=-5, ymax=8, width=8cm, height=8cm, domain=-3.2:5.2, samples=100]
\addplot[thick, blue] {x^2 - 2*x - 3};
\addplot[only marks, mark=*, red] coordinates {(-1,0) (3,0)};
\end{axis}
\end{tikzpicture}
\caption{The graph of $f(x) = x^2 - 2x - 3$ crossing the $x$-axis at its two roots}
\end{figure}









