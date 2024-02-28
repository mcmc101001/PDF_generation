from textwrap import dedent
from typing import override

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import AlignableTypstObject, TypstObject


@dataclass(frozen=True, kw_only=True)
class HeadingAttrs:
    level: int


@dataclass(frozen=True, kw_only=True)
class Heading(AlignableTypstObject):
    content: list[TypstObject] = Field()
    attrs: HeadingAttrs = Field(default=HeadingAttrs(level=5))

    @override
    def render_internal_block(self) -> str:
        rendered_content = ""
        for ele in self.content:
            rendered_content += f"{ele.render_block()}"
        return dedent(
            f"""\
            #heading(
                level: {self.attrs.level},
                [{rendered_content}]
            )"""
        )
