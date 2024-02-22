from __future__ import annotations

from tempfile import NamedTemporaryFile
from typing import IO

import typst
from pydantic import BaseModel

from pdf_generation.typeset.base_class import TypstObject
from pdf_generation.typeset.image import Image, ImageFactory
from pdf_generation.typeset.lorem import LoremIpsum


class GenerateDocumentRequest(BaseModel):
    latitude: float
    longitude: float
    file_name: str | None = "my_file"


class TypstFormatter:
    def __init__(self, objects: list[TypstObject] = []):
        self.objects = objects
        self.image_factory = ImageFactory()

    def add_object(self, obj: TypstObject):
        self.objects.append(obj)

    def remove_temp_image_files(self):
        self.image_factory.remove_temp_image_files()

    def render_block(self) -> str:
        return "\n".join([obj.render_block() for obj in self.objects])

    def add_lorem_ipsum(self):
        self.add_object(LoremIpsum())

    def generate_pdf(self) -> bytes:
        with NamedTemporaryFile(
            suffix=".typ", delete=True, delete_on_close=False
        ) as file:
            file.write(self.render_block().encode("utf-8"))
            file.close()  # need to close file before calling typst.compile
            pdf_bytes = typst.compile(file.name)
        self.remove_temp_image_files()
        return pdf_bytes
