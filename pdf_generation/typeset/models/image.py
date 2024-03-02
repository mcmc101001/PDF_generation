from __future__ import annotations

from textwrap import dedent
from typing import override

from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.dependencies.image_factory import ImageFactory
from pdf_generation.typeset.models.base_class import BaseTypstObject, ObjectType
from pdf_generation.typeset.utils import escape_typst_code

"""
https://stackoverflow.com/questions/77682563/image-from-hyperlink-in-typst
typst images do not support internet or absolute paths.
"""


@dataclass(frozen=True, kw_only=True)
class ImageAttrs:
    id: str = Field(default="1")
    src: str | None = Field(default=None)


@dataclass(frozen=True, kw_only=True)
class Image(BaseTypstObject):
    type: ObjectType = "image"
    attrs: ImageAttrs = Field(default=ImageAttrs())
    width_percentage: float | None = Field(default=None)
    height_percentage: float | None = Field(default=None)
    caption: str | None = Field(default=None)

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: ObjectType):
        expected_type = "image"
        if v != expected_type:
            raise ValueError(f"Expected type to be {expected_type}, got {v} instead.")

    def generate_image_url(self, factory: ImageFactory) -> str:
        return factory.generate_image_path(id=self.attrs.id).as_posix()

    @override
    def render_internal_block(self, dependencies) -> str:
        image_url = self.generate_image_url(dependencies.image_factory)

        block = dedent(
            f"""\
                image("{image_url}"{f", width: {self.width_percentage}%" if self.width_percentage else ""}{f", height: {self.height_percentage}%" if self.height_percentage else ""})"""
        )
        if self.caption is None:
            return f"#{block}"
        else:
            return dedent(
                f"""\
                #figure(
                    {block},
                    {f"caption: [{escape_typst_code(self.caption)}]" if self.caption else ""}
                )"""
            )
