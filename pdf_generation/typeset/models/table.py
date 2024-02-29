from textwrap import dedent
from typing import override

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import (AlignableTypstObject,
                                                      BaseTypstObject)
from pdf_generation.typeset.utils import escape_typst_code


@dataclass(frozen=True, kw_only=True)
class Table(AlignableTypstObject):
    content: list[list[str | BaseTypstObject]] = Field()
    caption: str | None = Field(default=None)

    @override
    def render_internal_block(self) -> str:
        content = ""

        for row in self.content:
            for ele in row:
                content += f"[{ele.render_block() if isinstance(ele, BaseTypstObject) else escape_typst_code(ele)}], "
            content += "\n"

        block = dedent(
            f"""\
            table(
                columns: {len(self.content[0])},
                {content}
            )"""
        )
        if self.caption is None:
            return f"#{block}"
        else:
            return dedent(
                f"""\
                #figure(
                    {block},
                    {self.caption and f"caption: [{escape_typst_code(self.caption)}]"}
                )"""
            )
