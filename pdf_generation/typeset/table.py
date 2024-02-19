from textwrap import dedent
from typing import override

from pydantic import Field
from pydantic.dataclasses import dataclass

from .base_class import AlignableTypstObject, TypstObject


@dataclass(frozen=True)
class Table(AlignableTypstObject):
    tableData: list[list[str | TypstObject]] = Field(alias="data")
    tableCaption: str | None = Field(default=None, alias="caption")

    @override
    def _render_internal_block(self) -> str:
        content = ""

        for row in self.tableData:
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
                    columns: {len(self.tableData[0])},
                    {content}
                ),
                {self.tableCaption and f"caption: [{self.tableCaption}]"}
            )"""
        )
