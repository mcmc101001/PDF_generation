from abc import ABC, abstractmethod
from textwrap import dedent
from typing import Literal

from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class TypstObject(ABC):

    @abstractmethod
    def render_internal_block(self) -> str:
        raise NotImplementedError

    def render_block(self) -> str:
        return self.render_internal_block()


type AlignmentType = Literal[  # type: ignore
    "start", "end", "left", "center", "right", "top", "horizon", "bottom"
]


@dataclass(frozen=True, kw_only=True)
class AlignableTypstObject(TypstObject):
    alignment: AlignmentType | None = Field(default=None, alias="align")

    def render_block(self) -> str:
        if self.alignment is None:
            return self.render_block()
        return dedent(
            f"""
            #align({self.alignment})[
                {self.render_internal_block()}
            ]"""
        )
