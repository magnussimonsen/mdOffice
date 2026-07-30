---
title: mdOffice v2 — Pptx Example
author: mdOffice

mdoffice:
  make-pptx: true
---

# Hello from mdOffice v2

- pptx's only mdOffice-specific key is `reference-doc`, which stays
  top-level (**intercepted**) because it's pandoc's own CLI option name —
  mdOffice just resolves the path relative to this file.
- Not set here, so pandoc uses its built-in default template.
