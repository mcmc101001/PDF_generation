from __future__ import annotations

from typing import Literal

from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import AlignmentType
from pdf_generation.typeset.models.heading import HeadingAttrs
from pdf_generation.typeset.models.text import Mark
from pdf_generation.typeset.models.list import OrderedListAttrs

type RequestContentType = Literal["heading", "text", "table", "paragraph", "bulletList", "listItem", "orderedList"]  # type: ignore
type Attributes = HeadingAttrs | OrderedListAttrs | None  # type: ignore


@dataclass(config=ConfigDict(extra="allow"))
class TypstObjectJson:
    type: RequestContentType = Field()
    content: (
        str
        | TypstObjectJson
        | list[TypstObjectJson]
        # | list[list[str | TypstObjectJson]]
        | None
    ) = Field(default=None)
    align: AlignmentType | None = Field(default=None)
    caption: str | None = Field(default=None)
    attrs: Attributes | None = Field(default=None)
    text: str | None = Field(default=None)
    marks: list[Mark] | None = Field(default=None)


@dataclass
class GeneratePdfRequest:
    file_name: str
    content: list[TypstObjectJson]
