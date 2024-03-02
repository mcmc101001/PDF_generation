from typing import Literal, override

from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import BaseTypstObject, ObjectType
from pdf_generation.typeset.utils import escape_typst_code

type MarkType = Literal["bold", "italic", "strike"]  # type: ignore


@dataclass(frozen=True, kw_only=True)
class Mark:
    type: MarkType

    def modify_text(self, text) -> str:
        if self.type == "bold":
            return f"#strong[{text}]"
        elif self.type == "italic":
            return f"#emph[{text}]"
        elif self.type == "strike":
            return f"#strike[{text}]"
        else:
            raise ValueError(f"Invalid mark type {self.type}")


@dataclass(frozen=True, kw_only=True)
class Text(BaseTypstObject):
    type: ObjectType = "text"
    text: str = Field()
    marks: tuple[Mark] | None = Field(default=None)

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: ObjectType):
        if v != "text":
            raise ValueError(f"Expected type to be text, got {v} instead.")

    @override
    def render_internal_block(self, dependencies) -> str:
        modified_text = escape_typst_code(self.text)
        if self.marks is not None:
            for mark in self.marks:
                modified_text = mark.modify_text(modified_text)
        return modified_text
