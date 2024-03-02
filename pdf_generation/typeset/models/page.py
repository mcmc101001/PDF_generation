from textwrap import dedent
from typing import override

from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import BaseTypstObject, ObjectType


@dataclass(frozen=True, kw_only=True)
class Page(BaseTypstObject):
    type: ObjectType = "page"
    header: BaseTypstObject = Field()

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: ObjectType):
        expected_type = "page"
        if v != expected_type:
            raise ValueError(f"Expected type to be {expected_type}, got {v} instead.")

    @override
    def render_internal_block(self, dependencies) -> str:
        return dedent(
            f"""\
            #set page(
                header: [
                    {self.header.render_block(dependencies)}
                ],
            )"""
        )
