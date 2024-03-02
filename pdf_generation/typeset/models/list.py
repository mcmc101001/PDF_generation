from textwrap import dedent
from typing import TYPE_CHECKING, override

from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import (
    AlignableTypstObject,
    AlignableTypstObjectAttrs,
    BaseTypstObject,
    ObjectType,
)

if TYPE_CHECKING:
    from pdf_generation.typeset.models.typst_object import TypstObject


@dataclass(frozen=True, kw_only=True)
class ListItem(BaseTypstObject):
    type: ObjectType = "listItem"
    content: tuple["TypstObject", ...] = Field()

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: ObjectType):
        expected_type = "listItem"
        if v != type:
            raise ValueError(f"Expected type to be {expected_type}, got {v} instead.")

    @override
    def render_internal_block(self, dependencies) -> str:
        rendered_content = ""
        for ele in self.content:
            rendered_content += f"{ele.render_block(dependencies)} "
        return rendered_content


@dataclass(frozen=True, kw_only=True)
class OrderedListAttrs(AlignableTypstObjectAttrs):
    start: int = Field(default=1)


@dataclass(frozen=True, kw_only=True)
class OrderedList(AlignableTypstObject):
    type: ObjectType = "orderedList"
    attrs: OrderedListAttrs = Field(default=OrderedListAttrs())
    content: tuple[ListItem, ...] = Field()

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: ObjectType):
        expected_type = "orderedList"
        if v != type:
            raise ValueError(f"Expected type to be {expected_type}, got {v} instead.")

    @override
    def render_internal_block(self, dependencies) -> str:
        rendered_content = ""
        for ele in self.content:
            rendered_content += f"[{ele.render_block(dependencies)}], "
        return dedent(
            f"""\
            #enum(
                start: {self.attrs.start},
                {rendered_content}
            )
            """
        )


@dataclass(frozen=True, kw_only=True)
class BulletList(AlignableTypstObject):
    type: ObjectType = "bulletList"
    content: tuple[ListItem, ...] = Field()

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: ObjectType):
        expected_type = "bulletList"
        if v != type:
            raise ValueError(f"Expected type to be {expected_type}, got {v} instead.")

    @override
    def render_internal_block(self, dependencies) -> str:
        rendered_content = ""
        for ele in self.content:
            rendered_content += f"[{ele.render_block(dependencies)}], "
        return f"#list({rendered_content})"
