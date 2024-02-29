from __future__ import annotations

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.models.typst_object import TypstObject


@dataclass(frozen=True)
class GeneratePdfRequest:
    file_name: str = Field()
    content: tuple[TypstObject, ...] = Field(default_factory=tuple)
