from __future__ import annotations

from typing import Literal

from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import AlignmentType

type RequestContentType = Literal["heading", "text", "table"]  # type: ignore


@dataclass(config=ConfigDict(extra="allow"))
class TypstObjectJson:
    type: RequestContentType = Field()
    content: str | TypstObjectJson | list[list[str | TypstObjectJson]] | None = Field(
        default=None
    )
    align: AlignmentType | None = Field(default=None)
    caption: str | None = Field(default=None)


@dataclass
class GeneratePdfRequest:
    file_name: str
    content: list[TypstObjectJson]
