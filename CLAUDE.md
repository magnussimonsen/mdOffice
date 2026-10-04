# mdOffice — Claude Code instructions

This file contains general instructions for working with mdOffice documents.
Per-document AI instructions are injected below the marker at the bottom by
running `.venv/bin/python _core/scripts/mdoffice.py build-ai-instructions <file.md>` (Linux) or `.venv\Scripts\python.exe _core/scripts/mdoffice.py build-ai-instructions <file.md>` (Windows), which
generates a `CLAUDE.md` in the document's own directory. Claude Code loads
both files automatically.

--- CUSTOM AI INSTRUCTIONS ---

@_core/ai-instructions/math.md
@_core/ai-instructions/text.md
