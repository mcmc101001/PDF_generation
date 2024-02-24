from typing import override

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import TypstObject


@dataclass(frozen=True, kw_only=True)
class Paragraph(TypstObject):
    content: str | TypstObject = Field()

    @override
    def render_internal_block(self) -> str:
        return f"#par()[{self.content.render_block() if isinstance(self.content, TypstObject) else self.content}]"
