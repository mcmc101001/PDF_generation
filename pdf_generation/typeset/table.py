from textwrap import dedent
from typing import override

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.base_class import AlignableTypstObject, TypstObject


@dataclass(frozen=True, kw_only=True)
class Table(AlignableTypstObject):
    table_data: list[list[str | TypstObject]] = Field(alias="data")
    table_caption: str | None = Field(default=None, alias="caption")

    @override
    def render_internal_block(self) -> str:
        content = ""

        for row in self.table_data:
            for ele in row:
                content += (
                    f"[{ele.render_block() if isinstance(
                        ele, TypstObject) else ele}], "
                )
            content += "\n"

        return dedent(
            f"""\
            #figure(
                table(
                    columns: {len(self.table_data[0])},
                    {content}
                ),
                {self.table_caption and f"caption: [{self.table_caption}]"}
            )"""
        )
