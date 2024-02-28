from textwrap import dedent
from typing import override

from pydantic.dataclasses import dataclass
from pydantic.fields import Field

from pdf_generation.typeset.models.base_class import TypstObject


@dataclass(frozen=True, kw_only=True)
class ListItem(TypstObject):
    content: list[TypstObject] = Field()

    @override
    def render_internal_block(self) -> str:
        rendered_content = ""
        for ele in self.content:
            rendered_content += f"{ele.render_block()} "
        return rendered_content


@dataclass
class OrderedListAttrs:
    start: int = Field(default=1)


@dataclass(frozen=True, kw_only=True)
class OrderedList(TypstObject):
    attrs: OrderedListAttrs = Field(default=OrderedListAttrs())
    content: list[ListItem] = Field()

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
class BulletList(TypstObject):
    content: list[ListItem] = Field()

    @override
    def render_internal_block(self) -> str:
        rendered_content = ""
        for ele in self.content:
            rendered_content += f"[{ele.render_block()}], "
        return f"#list({rendered_content})"
