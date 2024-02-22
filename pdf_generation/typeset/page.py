from textwrap import dedent
from typing import override

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.base_class import TypstObject
from pdf_generation.typeset.utils import escape_typst_code

# MUST BE FRONT OF DOCUMENT, POTENTIAL FIX TO THIS WOULD BE TO INHERIT FROM SOME SUBCLASS THTA WILL BE ORDERED


@dataclass(frozen=True, kw_only=True)
class Page(TypstObject):
    header: str | TypstObject = Field(alias="header")

    @override
    def render_internal_block(self) -> str:

        return dedent(
            f"""\
            #set page(
                header: [
                    {self.header.render_block() if isinstance(
                self.header, TypstObject) else f"{escape_typst_code(self.header)}"}
                ],
            )"""
        )
