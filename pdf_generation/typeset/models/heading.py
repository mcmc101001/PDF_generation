from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING, override

from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import (
    AlignableTypstObject,
    ObjectType,
    AlignableTypstObjectAttrs,
)

if TYPE_CHECKING:
    from pdf_generation.models.typst_object import TypstObject


@dataclass(frozen=True, kw_only=True)
class HeadingAttrs(AlignableTypstObjectAttrs):
    level: int


@dataclass(frozen=True, kw_only=True)
class Heading(AlignableTypstObject):
    content: tuple["TypstObject", ...] = Field()
    attrs: HeadingAttrs = Field(default=HeadingAttrs(level=1, textAlign=None))

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: ObjectType):
        if v != "heading":
            raise ValueError(f"Expected type to be heading, got {v} instead.")

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
