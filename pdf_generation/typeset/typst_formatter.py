from __future__ import annotations

import os
from tempfile import NamedTemporaryFile, _TemporaryFileWrapper

import typst
from pydantic import BaseModel

from pdf_generation.typeset.base_class import TypstObject
from pdf_generation.typeset.lorem import LoremIpsum
from pdf_generation.typeset.image import Image


class GenerateDocumentRequest(BaseModel):
    latitude: float
    longitude: float
    file_name: str | None = "my_file"


class TypstFormatter:
    def __init__(self, objects: list[TypstObject] = [], image_temp_files: list[_TemporaryFileWrapper[bytes]] = []):
        self.objects = objects
        self.image_temp_files= image_temp_files

    def add_object(self, obj: TypstObject):
        self.objects.append(obj)
        if isinstance(obj, Image):
            self.image_temp_files.append(obj.temp_file)
            
    def remove_temp_image_files(self):
        for file in self.image_temp_files:
            file.close() # Delete on close is True, so this will delete the temp file

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
        return pdf_bytes
