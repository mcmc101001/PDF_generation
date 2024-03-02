from textwrap import dedent
from typing import override

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import BaseTypstObject, ObjectType


@dataclass(frozen=True, kw_only=True)
class Page(BaseTypstObject):
    type: ObjectType = "page"
    header: BaseTypstObject = Field()

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
