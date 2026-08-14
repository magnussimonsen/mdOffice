---
title: mdOffice v2 — Docx Example
author: mdOffice

mdoffice:
  make-docx: true
---

# Hello from mdOffice v2

docx has no custom or intercepted keys today — every option here is pure
pandoc passthrough. `mdoffice.make-docx` is the only mdOffice-specific key,
and it's global (declared in `core/schema.py`'s `GLOBAL_KEYS`), not part of
`formats/docx.py`'s own (empty) schema.
