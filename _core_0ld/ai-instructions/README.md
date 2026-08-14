# AI instructions

Reusable knowledge files for an AI assistant working on mdOffice documents —
writing style, citation formats, language rules, and similar reference
material. Content here is meant to be *read by* Claude Code (or another AI
assistant), not rendered into any output document.

Any `.md` document opts into specific files here via its own frontmatter:

```yaml
mdoffice:
  ai-instructions:
    - "../ai-instructions/math.md"
    - "../ai-instructions/norwegian/Norsk-APA.md"
```

Running `mdoffice.py build-ai-instructions <file>` then generates `CLAUDE.md`
(using `@path` imports, which Claude Code loads automatically) and
`.continuerules` (a plain pointer) next to that document — neither file
copies the content, they just reference it here, so this folder stays the
single source of truth.

## Current files

- `math.md` — math formatting and language-level conventions.
- `text.md` — general punctuation and language-level conventions.
- `norwegian/Norsk-APA.md` — APA 7 in-text citation guide (Norwegian).
