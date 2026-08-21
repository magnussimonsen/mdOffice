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
  beamer-style: "fancybeamer"

  # Beamer options (optional)
  # page-numbering: true
  # show-solution: false
  # show-blankbox: false
  # solution-text: "Solution"
  # blankbox-text: "Write your solution in this box"

  # Optional extra outputs
  # make-pdf: true
  # make-pptx: true
---

# First slide
\blueheader
## Agenda

- Topic 1
- Topic 2
- Topic 3

# Secons slide {.t}
\greenheader
Two columnas with (blue box  then focusbox cyan left) and same right 

:::::: {.columns totalwidth="\textwidth"}
::: {.column width="48%"}
\begin{bluebox*}{Definition}
A \textbf{set} $S$ is \emph{finite} if there exists a bijection
$S \to \{1,\ldots,n\}$ for some $n \in \mathbb{N}$.
\end{bluebox*}

\medskip

\begin{cyanfocus}
\textbf{cyanfocus} --- for exercises, tasks, or student prompts without a formal label.
\end{cyanfocus}
:::
::: {.column width="48%"}
\begin{bluebox*}{Definition}
A \textbf{set} $S$ is \emph{finite} if there exists a bijection
$S \to \{1,\ldots,n\}$ for some $n \in \mathbb{N}$.
\end{bluebox*}

\medskip

\begin{cyanfocus}
\textbf{cyanfocus} --- for exercises, tasks, or student prompts without a formal label.
\end{cyanfocus}
:::
::::::
