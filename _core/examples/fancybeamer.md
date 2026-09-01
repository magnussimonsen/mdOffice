---
title: "Fancy Beamer — Feature Showcase"
subtitle: "Style and Features"
author: "Your name"
date: "2026"
aspectratio: 169
logo: "img/logo.png"
logo-height: "0.6cm"
fontsize: 11pt

mdoffice:
  make-beamer: true
  beamer-style: "fancybeamer"
  page-numbering: true
---

## Blue — Theorem and Focus Box
\blueheader

:::::: {.columns totalwidth="\textwidth"}
::: {.column width="50%"}
\begin{bluebox*}{Definition}
A \textbf{set} $S$ is \emph{finite} if there exists a bijection
$S \to \{1,\ldots,n\}$ for some $n \in \mathbb{N}$.
\end{bluebox*}

\medskip

\begin{bluebox}{Definition (numbered)}{def:finite}
Same box, numbered and referenceable.
\end{bluebox}
:::
::: {.column width="50%"}
\begin{bluefocus}
\textbf{bluefocus} --- for key formulas or remarks without a formal label.
$$e^{i\pi} + 1 = 0$$
\end{bluefocus}
:::
::::::

## Red — Theorem and Focus Box
\redheader

:::::: {.columns totalwidth="\textwidth"}
::: {.column width="50%"}
\begin{redbox*}{Theorem}
For all $a, b \in \mathbb{R}$:
$$(a + b)^2 = a^2 + 2ab + b^2$$
\end{redbox*}

\medskip

\begin{redbox}{Theorem (numbered)}{thm:binomial}
Counter is shared across all box types.
\end{redbox}
:::
::: {.column width="50%"}
\begin{redfocus}
\textbf{redfocus} --- for warnings or anything that demands immediate attention.

\medskip
Reserve red for critical content, not decoration.
\end{redfocus}
:::
::::::

## Green — Theorem and Focus Box
\greenheader

:::::: {.columns totalwidth="\textwidth"}
::: {.column width="50%"}
\begin{greenbox*}{Example}
Let $f(x) = x^2$. Then $f'(x) = 2x$, so the slope at $x = 3$ is
$$f'(3) = 6.$$
\end{greenbox*}

\medskip

\begin{greenbox}{Example (numbered)}{ex:deriv}
Same box, numbered.
\end{greenbox}
:::
::: {.column width="50%"}
\begin{greenfocus}
\textbf{greenfocus} --- for worked examples, intuition, or positive reinforcement.
\end{greenfocus}
:::
::::::

## Cyan — Theorem and Focus Box
\cyanheader

:::::: {.columns totalwidth="\textwidth"}
::: {.column width="50%"}
\begin{cyanbox*}{Exercise}
Compute $\displaystyle\int_0^1 x^2\,dx$ and verify the answer equals $\tfrac{1}{3}$.
\end{cyanbox*}

\medskip

\begin{cyanbox}{Exercise (numbered)}{ex:integral}
Same box, numbered.
\end{cyanbox}
:::
::: {.column width="50%"}
\begin{cyanfocus}
\textbf{cyanfocus} --- for exercises, tasks, or student prompts without a formal label.
\end{cyanfocus}
:::
::::::

## Gray — Theorem and Focus Box
\grayheader

:::::: {.columns totalwidth="\textwidth"}
::: {.column width="50%"}
\begin{graybox*}{Exploration}
Pick two vectors $u, v \in \mathbb{R}^2$. Compare $\norm{u+v}$ with $\norm{u} + \norm{v}$.
\end{graybox*}

\medskip

\begin{graybox}{Exploration (numbered)}{ex:triangle}
Same box, numbered.
\end{graybox}
:::
::: {.column width="50%"}
\begin{grayfocus}
\textbf{grayfocus} --- for open-ended exploration, background remarks, or supplementary context.
\end{grayfocus}
:::
::::::

## Macros
\blueheader

**Warning and info macros:**

\medskip

- \warn
- \info
- \warnCustomMsg[myblue]{Custom warning in any color}
- \infoCustomMsg[mygreen]{Custom info in any color}

\medskip

**Math macros:**

\medskip

- Norm: $\norm{v} = \sqrt{\langle v, v \rangle}$
- Absolute value: $\abs{x - y} \leq \abs{x} + \abs{y}$
- Combined: $\abs{\langle u, v \rangle} \leq \norm{u}\,\norm{v}$ \quad (Cauchy--Schwarz)
