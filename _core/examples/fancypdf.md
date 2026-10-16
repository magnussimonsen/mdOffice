---
title: "Fancy PDF: Feature Showcase"
subtitle: "The document companion to fancybeamer"
author: "Your name"
date: "2026"
fontsize: 11pt

mdoffice:
  make-pdf: true
  doc-style: "fancypdf"
  header: "fancypdf example"
  page-numbering: true
---

## Plain heading (the default)

Headings have no background color unless you ask for one. Write a color macro on the line right after a heading, exactly as in fancybeamer, to give that one heading a colored bar.

## Blue: theorem and focus box
\blueheader

\begin{bluebox*}{Definition}
A \textbf{set} $S$ is \emph{finite} if there exists a bijection
$S \to \{1,\ldots,n\}$ for some $n \in \mathbb{N}$.
\end{bluebox*}

\begin{bluebox}{Definition (numbered)}{def:finite}
Same box, numbered and referenceable.
\end{bluebox}

\begin{bluefocus}
\textbf{bluefocus}: for key formulas or remarks without a formal label.
$$e^{i\pi} + 1 = 0$$
\end{bluefocus}

## Red: theorem and focus box
\redheader

\begin{redbox*}{Theorem}
For all $a, b \in \mathbb{R}$:
$$(a + b)^2 = a^2 + 2ab + b^2$$
\end{redbox*}

\begin{redfocus}
\textbf{redfocus}: for warnings or anything that demands immediate attention.
\end{redfocus}

## Back to plain

The previous heading was red, but this one is plain again. Colors never carry over to the next heading.

## Green: theorem and focus box
\greenheader

\begin{greenbox}{Example (numbered)}{ex:deriv}
Let $f(x) = x^2$. Then $f'(x) = 2x$, so the slope at $x = 3$ is $f'(3) = 6$.
\end{greenbox}

\begin{greenfocus}
\textbf{greenfocus}: for worked examples or intuition.
\end{greenfocus}

### Cyan subheading
\cyanheader

\begin{cyanbox*}{Exercise}
Compute $\displaystyle\int_0^1 x^2\,dx$.
\end{cyanbox*}

\begin{cyanfocus}
\textbf{cyanfocus}: for exercises or student prompts.
\end{cyanfocus}

### Gray subheading
\grayheader
Text can start on the line right after the macro.

\begin{graybox*}{Exploration}
Compare $\norm{u+v}$ with $\norm{u} + \norm{v}$.
\end{graybox*}

\begin{grayfocus}
\textbf{grayfocus}: for background remarks.
\end{grayfocus}

## Macros

- \warn
- \info
- \warnCustomMsg[myblue]{Custom warning in any color}
- \infoCustomMsg[mygreen]{Custom info in any color}
