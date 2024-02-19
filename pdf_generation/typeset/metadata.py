from typing import override

from pydantic import Field
from pydantic.dataclasses import dataclass

from .base_class import TypstObject

# MUST BE FRONT OF DOCUMENT, POTENTIAL FIX TO THIS WOULD BE TO INHERIT FROM SOME SUBCLASS THTA WILL BE ORDERED


@dataclass(frozen=True)
class Metadata(TypstObject):
    metaDataTitle: str = Field(alias="title")

    @override
    def _render_internal_block(self) -> str:
        return f'#set document(title: "{self.metaDataTitle}")'
