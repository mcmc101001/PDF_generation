from textwrap import dedent
from typing import override

from pydantic import Field
from pydantic.dataclasses import dataclass

from .base_class import TypstObject

# MUST BE FRONT OF DOCUMENT, POTENTIAL FIX TO THIS WOULD BE TO INHERIT FROM SOME SUBCLASS THTA WILL BE ORDERED


@dataclass(frozen=True)
class Page(TypstObject):
    header: str | TypstObject = Field(alias="header")

    @override
    def _render_internal_block(self) -> str:
        # implement multiline indentation fix
        # multiLineCode = self.header.toTypstCode() if isinstance(self.header, TypstObject) else f"{self.header}"

        # if multiLineCode.count("\n") > 0:
        #     pass

        return dedent(
            f"""\
            #set page(
                header: [
                    {self.header.render_block() if isinstance(
                self.header, TypstObject) else f"{self.header}"}
                ],
            )"""
        )
