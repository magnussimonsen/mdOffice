---
# Basic Pandoc metadata (active)
title: "EPUB title"
author: "Your name"
date: "2026-08-15"

# Common Pandoc metadata (optional)
# lang: nb-NO
# subtitle: "Optional subtitle"
# toc: true
# numbersections: true

# EPUB top-level options (optional)
# cover-image: "img/cover.png"

mdoffice:
  make-epub: true

  # EPUB options (optional)
  # epub-css: "styles/epub.css"

  # Optional extra outputs
  # make-docx: true
  # make-odt: true
---

<!-- Example content: replace everything below the frontmatter with your own text.
Comments like this one are only visible here. They never appear in the book.
Each "#" heading starts a new chapter. -->

# First chapter

This is a paragraph. Write *italic*, **bold** and `code` straight in the text. Leave an empty line between paragraphs.

## A section

- A bullet point
- Another bullet point

1. First step
2. Second step

> A quote starts with `>` at the beginning of the line.

# Second chapter

## Tables

| Planet | Moons |
|--------|-------|
| Earth  | 1     |
| Mars   | 2     |

## Math

Inline math such as $a^2 + b^2 = c^2$ sits inside the sentence. Display math gets its own line:

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

A footnote is marked in the text like this.[^1]

[^1]: In an e-book, the footnote text is shown as a pop-up or at the end of the chapter.
