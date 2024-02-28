from typing import Literal, override

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import TypstObject
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
class Text(TypstObject):
    text: str = Field()
    marks: list[Mark] | None = Field(default=None)

    @override
    def render_internal_block(self) -> str:
        modified_text = escape_typst_code(self.text)
        if self.marks is not None:
            for mark in self.marks:
                modified_text = mark.modify_text(modified_text)
        return modified_text
