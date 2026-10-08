---
title: "Tittel på presentasjonen"
subtitle: "Undertittel"
author: "Forfatter. Rolle."
date: "Oktober 2026"
aspectratio: 169
lang: nb-NO

mdoffice:
  make-beamer: true
  beamer-style: "lektorlaget"
---

# Første del

## Slide-tittel

- Første punkt med en grønn pil som punkttegn
- Andre punkt
  - Underpunkt
  - Enda et underpunkt
- Tredje punkt

## To kolonner

:::::: {.columns}
::: {.column width="48%"}
**Venstre kolonne**

1. Nummerert punkt
2. Neste punkt
3. Siste punkt
:::
::: {.column width="48%"}
\begin{llbox}{Viktig}
En boks med petrol tittel og mint bakgrunn.
\end{llbox}

\begin{llfocus}
En fokusboks uten tittel: $a^2 + b^2 = c^2$
\end{llfocus}
:::
::::::

# Andre del

## Pandoc-blokker

### Blokk

Vanlig blokk i temaets farger.

### Advarsel {.alert}

Varselblokk i rødt.

### Eksempel {.example}

Eksempelblokk i grønt.

## En lang slide-tittel som går over to linjer for å teste hvordan tittelområdet oppfører seg

Brødtekst rett under en lang tittel.

## Takk for oppmerksomheten

\tealslide

Spørsmål?
