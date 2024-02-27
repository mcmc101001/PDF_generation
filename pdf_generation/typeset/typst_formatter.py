from __future__ import annotations

from tempfile import NamedTemporaryFile, TemporaryDirectory

import typst

from pathlib import Path

from pdf_generation.typeset.models.base_class import TypstObject
from pdf_generation.typeset.models.image import ImageFactory


class TypstFormatter:
    def __init__(self, objects: list[TypstObject] | None = None):
        if objects is None:
            objects = []
        self.objects = objects
        self.temp_dir = TemporaryDirectory()
        self.image_factory = ImageFactory(Path(self.temp_dir.name))

    def add_object(self, obj: TypstObject):
        self.objects.append(obj)

    def remove_temp_image_files(self):
        self.image_factory.remove_temp_image_files()

    def render_block(self) -> str:
        return "\n".join([obj.render_block() for obj in self.objects])

    def generate_pdf(self) -> bytes:
        with NamedTemporaryFile(
            suffix=".typ",
            delete=True,
            delete_on_close=False,
            dir=Path(self.temp_dir.name),
        ) as file:
            file.write(self.render_block().encode("utf-8"))
            file.close()  # need to close file before calling typst.compile
            pdf_bytes = typst.compile(file.name)
        self.remove_temp_image_files()
        self.temp_dir.cleanup()
        return pdf_bytes
