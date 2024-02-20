from typing import override

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.base_class import TypstObject

# MUST BE FRONT OF DOCUMENT, POTENTIAL FIX TO THIS WOULD BE TO INHERIT FROM SOME SUBCLASS THTA WILL BE ORDERED


@dataclass(frozen=True, kw_only=True)
class Metadata(TypstObject):
    metaData_title: str = Field(alias="title")

    @override
    def render_internal_block(self) -> str:
        return f'#set document(title: "{self.metaData_title}")'
