---
title: "Introduction to Italian Grammar and Calculus of Limits"
subtitle: "A Short EPUB Example"
author: "Name"
date: "2026"
lang: "en-US"
toc: true
cover-image: "./img/logo.png"

mdoffice:
  make-epub: true
---

# Introduction

This is a short example showing how mdOffice converts a Markdown file into an
EPUB ebook. It covers headings, lists, tables, images, basic formatting, and
LaTeX math, all common elements in a set of lecture notes.

# Sounds and Pronunciation (IPA)

Italian pronunciation is fairly regular: most letters and letter combinations
correspond to a single sound.

## Vowels

Italian has seven vowel sounds, written with five letters:

| Letter | IPA   | Example      |
| ------ | ----- | ------------ |
| a      | /a/   | *casa* (house) |
| e      | /e/, /ɛ/ | *sera* (evening) |
| i      | /i/   | *vino* (wine)  |
| o      | /o/, /ɔ/ | *sole* (sun)  |
| u      | /u/   | *luna* (moon)  |

## Consonants

A few consonant combinations have special pronunciations:

- **gli** — like the "lli" in *million*, e.g. *famiglia* (family)
- **gn** — like the "ny" in *canyon*, e.g. *bagno* (bathroom)
- **sc** before *e* or *i* — like "sh" in *fish*, e.g. *pesce* (fish)

# Articles

## Definite articles

The Italian definite article ("the") agrees with the noun in gender and
number:

1. **il** — masculine singular (*il libro* — the book)
2. **lo** — masculine singular before *s+consonant*, *z*, *gn*, *ps* (*lo
   studente* — the student)
3. **la** — feminine singular (*la casa* — the house)
4. **i** — masculine plural (*i libri* — the books)
5. **le** — feminine plural (*le case* — the houses)

## Indefinite articles

> "A language is not just a set of rules. It is also a habit of mind, a way
> of looking at the world."

- **un** — masculine (*un libro*)
- **uno** — masculine before *s+consonant*, *z*, *gn*, *ps* (*uno studente*)
- **una** — feminine (*una casa*)

# Verbs: Present Tense

Regular verbs fall into three conjugations, identified by their infinitive
ending: `-are`, `-ere`, and `-ire`.

```text
parlare (to speak)  ->  parlo, parli, parla, parliamo, parlate, parlano
```

# Calculus of Limits

## The formal definition

We say that

$$\lim_{x \to a} f(x) = L$$

if for every $\varepsilon > 0$ there exists a $\delta > 0$ such that

$$0 < |x - a| < \delta \implies |f(x) - L| < \varepsilon.$$

## Epsilon-delta

A useful example for understanding the epsilon-delta definition:

If you are buying epsilon-soda for one delta-dollar per litre, then for
every amount of epsilon-soda you want to buy, there exists an amount of
delta-dollars you can use to buy that much epsilon-soda. In symbols, for
every $\varepsilon > 0$ there is a $\delta > 0$ (here $\delta = \varepsilon$)
such that $\varepsilon$ litres of soda costs $\delta$ dollars.

But if you instead try to buy epsilon-kittens, and the price of one
epsilon-kitten is one delta-dollar, then this breaks down: for some small
amounts of epsilon-kittens (say, half a kitten), there is **no** amount of
delta-dollars you can use to buy exactly that much, because kittens can only
be bought as whole units. This is why limits are defined for continuous
quantities like real numbers, not discrete ones.

## Worked example

Show that $\displaystyle\lim_{x \to 2} (3x - 1) = 5$.

Given $\varepsilon > 0$, choose $\delta = \frac{\varepsilon}{3}$. Then
whenever $0 < |x - 2| < \delta$:

$$
|(3x - 1) - 5| = |3x - 6| = 3|x - 2| < 3\delta = \varepsilon.
$$

# Conclusion

This file can be extended with more chapters — each top-level heading (`#`)
becomes a new chapter in the generated EPUB.
