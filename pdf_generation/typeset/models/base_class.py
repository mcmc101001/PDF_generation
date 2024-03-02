from abc import ABC, abstractmethod
from textwrap import dedent
from typing import Literal, override

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.dependencies.dependencies import Dependencies

type ObjectType = Literal[  # type: ignore
    "heading",
    "image",
    "text",
    "paragraph",
    "bulletList",
    "listItem",
    "orderedList",
    "metadata",
    "page",
]


@dataclass(frozen=True, kw_only=True)
class BaseTypstObject(ABC):
    type: ObjectType = Field(title="Type of the field")

    @abstractmethod
    def render_internal_block(self, dependencies: Dependencies) -> str:
        return ""

    def render_block(self, dependencies: Dependencies) -> str:
        return self.render_internal_block(dependencies)


type AlignmentType = Literal[  # type: ignore
    "start", "end", "left", "center", "right", "top", "horizon", "bottom"
]


@dataclass(frozen=True, kw_only=True)
class AlignableTypstObjectAttrs:
    textAlign: AlignmentType | None = Field(default=None)


@dataclass(frozen=True, kw_only=True)
class AlignableTypstObject(BaseTypstObject):
    attrs: AlignableTypstObjectAttrs = Field(
        default=AlignableTypstObjectAttrs(textAlign=None)
    )

    @override
    def render_block(self, dependencies: Dependencies) -> str:
        if self.attrs.textAlign is None:
            return self.render_internal_block(dependencies)
        return dedent(
            f"""
            #align({self.attrs.textAlign})[
                {self.render_internal_block(dependencies)}
            ]"""
        )
