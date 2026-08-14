---
title: "TikZ Crash Course"
fontsize: 12pt
lang: "en-US"
header-includes: |
  \usepackage{tikz}
  \usetikzlibrary{positioning, arrows.meta}

mdoffice:
  make-pdf: true
  doc-style: standard-pdf
  page-numbering: true
---

# TikZ Crash Course

TikZ is a LaTeX package for drawing directly in a document. Pandoc passes
raw `\begin{tikzpicture}...\end{tikzpicture}` blocks through unchanged to
xelatex, so every diagram below is a real vector drawing, not an image, and
needs no external tools to build.

Every TikZ picture is a list of drawing commands ended with a semicolon,
inside a `tikzpicture` environment. The two commands used most are `\draw`
(paths: lines, shapes, curves) and `\node` (a labeled box, circle, or point
you can refer to by name).

## 1. Coordinates and paths

`\draw` connects coordinates with `--` for straight lines. Shapes like
`circle` and `rectangle` are keywords used after a coordinate.

\begin{figure}[h]
\centering
\begin{tikzpicture}
  \draw[thick] (0,0) -- (2,0) -- (2,1.5) -- (0,1.5) -- cycle;
  \draw[thick, fill=blue!10] (4,0.75) circle (0.75);
  \draw[->, thick] (2.4,0.75) -- (3.1,0.75);
\end{tikzpicture}
\caption{A rectangle, an arrow, and a filled circle}
\end{figure}

## 2. Nodes

A `node` is a piece of content (usually text) with an optional shape drawn
around it. Naming a node with `(name)` lets later commands refer back to
its position.

\begin{figure}[h]
\centering
\begin{tikzpicture}[
  every node/.style={draw, rounded corners, fill=blue!10, minimum width=2.4cm,
                     minimum height=0.9cm, align=center, font=\small}
]
  \node (a) at (0,0) {Node A};
  \node (b) at (3,0) {Node B};
\end{tikzpicture}
\caption{Two independent nodes, placed by explicit coordinates}
\end{figure}

## 3. Connecting nodes into a flowchart

Once nodes are named, `\draw (a) -- (b)` connects them without recomputing
coordinates. Adding `->` (or the sharper `-Stealth`, from the
`arrows.meta` library) turns a line into an arrow, which is how most
flowcharts are built.

\begin{figure}[h]
\centering
\begin{tikzpicture}[
  every node/.style={draw, rounded corners, fill=blue!10, minimum width=2.6cm,
                     minimum height=0.9cm, align=center, font=\small},
  every path/.style={-{Stealth[length=2.5mm]}, thick}
]
  \node (editor)   at (0,0)   {Editor};
  \node (compiler) at (3.2,0) {Compiler};
  \node (preview)  at (6.4,0) {Preview};

  \draw (editor) -- (compiler);
  \draw (compiler) -- (preview);
\end{tikzpicture}
\caption{A simple left-to-right flowchart}
\end{figure}

## 4. Relative positioning

Explicit coordinates get tedious for bigger diagrams. The `positioning`
library adds `below=of`, `right=of`, etc., so a node's location is
described relative to another node instead of measured by hand.

\begin{figure}[h]
\centering
\begin{tikzpicture}[
  every node/.style={draw, rounded corners, fill=blue!10, minimum width=2.4cm,
                     minimum height=0.9cm, align=center, font=\small},
  node distance=0.8cm and 1.6cm,
  every path/.style={->, thick}
]
  \node (start) {Start};
  \node (yes) [below left=of start] {Yes branch};
  \node (no)  [below right=of start] {No branch};

  \draw (start) -- (yes);
  \draw (start) -- (no);
\end{tikzpicture}
\caption{Nodes placed relative to each other, not by coordinates}
\end{figure}

## 5. Repetition with \texttt{\textbackslash foreach}

`\foreach` loops over a list of values, running the same drawing command
for each one. This avoids writing near-identical `\draw` lines by hand.

\begin{figure}[h]
\centering
\begin{tikzpicture}
  \foreach \x in {0,1,2,3,4} {
    \draw[fill=blue!10] (\x, 0) circle (0.3);
  }
\end{tikzpicture}
\caption{Five circles drawn from one loop instead of five \texttt{\textbackslash draw} lines}
\end{figure}

## Where to go from here

These five patterns, coordinates, nodes, connections, relative
positioning, and loops, cover most flowcharts, diagrams, and simple plots
you'll want in a document. The full TikZ & PGF manual documents many more
shapes, libraries, and styling options.
