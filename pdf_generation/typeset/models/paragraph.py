from typing import override

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import TypstObject


@dataclass(frozen=True, kw_only=True)
class Paragraph(TypstObject):
    content: list[TypstObject] = Field()

    @override
    def render_internal_block(self) -> str:
        rendered_content = ""
        for ele in self.content:
            rendered_content += f"{ele.render_block()} "
        return f"#par({rendered_content})"
