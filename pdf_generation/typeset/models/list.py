from textwrap import dedent
from typing import TYPE_CHECKING, override

from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import BaseTypstObject, ObjectType

if TYPE_CHECKING:
    from pdf_generation.models.typst_object import TypstObject


@dataclass(frozen=True, kw_only=True)
class ListItem(BaseTypstObject):
    content: tuple["TypstObject", ...] = Field()

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: ObjectType):
        if v != "listItem":
            raise ValueError(f"Expected type to be listItem, got {v} instead.")

    @override
    def render_internal_block(self) -> str:
        rendered_content = ""
        for ele in self.content:
            rendered_content += f"{ele.render_block()} "
        return rendered_content


@dataclass(frozen=True, kw_only=True)
class OrderedListAttrs:
    start: int = Field(default=1)


@dataclass(frozen=True, kw_only=True)
class OrderedList(BaseTypstObject):
    attrs: OrderedListAttrs = Field(default=OrderedListAttrs())
    content: tuple[ListItem, ...] = Field()

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: ObjectType):
        if v != "orderedList":
            raise ValueError(f"Expected type to be orderedList, got {v} instead.")

    @override
    def render_internal_block(self) -> str:
        rendered_content = ""
        for ele in self.content:
            rendered_content += f"[{ele.render_block()}], "
        return dedent(
            f"""\
            #enum(
                start: {self.attrs.start},
                {rendered_content}
            )
            """
        )


@dataclass(frozen=True, kw_only=True)
class BulletList(BaseTypstObject):
    content: tuple[ListItem, ...] = Field()

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: ObjectType):
        if v != "bulletList":
            raise ValueError(f"Expected type to be bulletList, got {v} instead.")

    @override
    def render_internal_block(self) -> str:
        rendered_content = ""
        for ele in self.content:
            rendered_content += f"[{ele.render_block()}], "
        return f"#list({rendered_content})"
