from typing import TYPE_CHECKING, override

from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import AlignableTypstObject, ObjectType

if TYPE_CHECKING:
    from pdf_generation.typeset.models.typst_object import TypstObject


@dataclass(frozen=True, kw_only=True)
class Paragraph(AlignableTypstObject):
    type: ObjectType = "paragraph"
    content: tuple["TypstObject", ...] = Field()

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: ObjectType):
        expected_type = "paragraph"
        if v != type:
            raise ValueError(f"Expected type to be {expected_type}, got {v} instead.")

    @override
    def render_internal_block(self, dependencies) -> str:
        rendered_content = ""
        for ele in self.content:
            rendered_content += f"{ele.render_block(dependencies)}"
        return f"#par()[{rendered_content}]"
