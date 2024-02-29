from abc import ABC, abstractmethod
from textwrap import dedent
from typing import Literal, override

from pydantic import Field
from pydantic.dataclasses import dataclass

type ObjectType = Literal[  # type: ignore
    "heading",
    "image",
    "text",
    "table",
    "paragraph",
    "bulletList",
    "listItem",
    "orderedList",
    "metadata",
    "page",
]


@dataclass(frozen=True)
class BaseTypstObject(ABC):
    type: ObjectType = Field(title="Type of the field")

    @abstractmethod
    def render_internal_block(self) -> str:
        return ""

    def render_block(self) -> str:
        return self.render_internal_block()


type AlignmentType = Literal[  # type: ignore
    "start", "end", "left", "center", "right", "top", "horizon", "bottom"
]


@dataclass(frozen=True, kw_only=True)
class AlignableTypstObject(BaseTypstObject):
    align: AlignmentType | None = Field(default=None)

    @override
    def render_block(self) -> str:
        if self.align is None:
            return self.render_internal_block()
        return dedent(
            f"""
            #align({self.align})[
                {self.render_internal_block()}
            ]"""
        )
