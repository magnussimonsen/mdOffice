# Lektorlaget (Beamer)

A Beamer theme that follows the look of Lektorlaget's PowerPoint template
(`Lektorlaget.presentasjonsmal.pptx`): petrol title slide with the owl
watermark, petrol slide titles over a mint rule, the owl logo top-right and
green arrow bullets. Font: Arial (change it with `mdoffice.font`, see below).

See [`example.md`](example.md) and the built [`beamer/example.pdf`](beamer/example.pdf).

## Usage

```yaml
---
title: "Tittel"
subtitle: "Undertittel"
author: "Forfatter. Rolle."
date: "Dato"
aspectratio: 169
mdoffice:
  make-beamer: true
  beamer-style: "lektorlaget"
  # font: "Fira Sans"   # optional: any installed font instead of Arial
---
```

## Slide types

| Slide | How |
|---|---|
| Title slide | Automatic when `title:` is set |
| Section slide | Automatic for every level-1 heading (`# Section`) |
| Petrol slide | Put `\tealslide` as the first line of a slide, e.g. a closing "Takk!" slide |

## Boxes

```latex
\begin{llbox}{Title} ... \end{llbox}     % petrol title, mint background
\begin{llfocus} ... \end{llfocus}        % mint background, no title
```

Pandoc blocks also use the palette: `### Title` (petrol),
`### Title {.alert}` (red) and `### Title {.example}` (green).

## Colors

`llpetrol` `#008675`, `llgreen` `#28714F`, `llmint` `#D5ECDD`,
`llturquoise` `#00C0AA`, `llblue` `#4174C7`, `llred` `#ED5F54`,
`llyellow` `#FFCB46`, `lltext` `#0A122B`. Use them in LaTeX, e.g.
`\textcolor{llred}{...}`.
