from textwrap import dedent
from typing import override

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import (AlignableTypstObject,
                                                      TypstObject)
from pdf_generation.typeset.utils import escape_typst_code


@dataclass(frozen=True, kw_only=True)
class Heading(AlignableTypstObject):
    content: str | TypstObject = Field()
    level: int = Field(default=1)

    @override
    def render_internal_block(self) -> str:
        return dedent(
            f"""\
            #heading(
                level: {self.level},
                [{self.content.render_block() if isinstance(self.content, TypstObject) else escape_typst_code(self.content)}]
            )"""
        )
