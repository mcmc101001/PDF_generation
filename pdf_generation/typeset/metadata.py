from typing import override

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.base_class import TypstObject
from pdf_generation.typeset.utils import escape_typst_code

# MUST BE FRONT OF DOCUMENT, POTENTIAL FIX TO THIS WOULD BE TO INHERIT FROM SOME SUBCLASS THTA WILL BE ORDERED


@dataclass(frozen=True, kw_only=True)
class Metadata(TypstObject):
    metadata_title: str = Field(alias="title")

    @override
    def render_internal_block(self) -> str:
        return f'#set document(title: "{escape_typst_code(self.metadata_title)}")'
