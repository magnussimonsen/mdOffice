from __future__ import annotations

from .beamer import SCHEMA as BEAMER_SCHEMA
from .beamer import create_plan as create_beamer_plan
from .docx import SCHEMA as DOCX_SCHEMA
from .docx import create_plan as create_docx_plan
from .epub import SCHEMA as EPUB_SCHEMA
from .epub import create_plan as create_epub_plan
from .odt import SCHEMA as ODT_SCHEMA
from .odt import create_plan as create_odt_plan
from .pdf import SCHEMA as PDF_SCHEMA
from .pdf import create_plan as create_pdf_plan
from .pptx import SCHEMA as PPTX_SCHEMA
from .pptx import create_plan as create_pptx_plan

PLANNERS = {
    "pdf": create_pdf_plan,
    "docx": create_docx_plan,
    "odt": create_odt_plan,
    "pptx": create_pptx_plan,
    "beamer": create_beamer_plan,
    "epub": create_epub_plan,
}

# Every format's schema, keyed the same way as PLANNERS. This is what
# `core/validate.py` and `generate_reference.py` iterate over.
SCHEMAS = {
    "pdf": PDF_SCHEMA,
    "docx": DOCX_SCHEMA,
    "odt": ODT_SCHEMA,
    "pptx": PPTX_SCHEMA,
    "beamer": BEAMER_SCHEMA,
    "epub": EPUB_SCHEMA,
}
