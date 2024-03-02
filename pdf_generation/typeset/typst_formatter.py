from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import typst

from pdf_generation.typeset.dependencies.dependencies import Dependencies
from pdf_generation.typeset.dependencies.image_factory import ImageFactory
from pdf_generation.typeset.models.base_class import BaseTypstObject


class TypstFormatter:
    def __init__(
        self,
        temp_dir: TemporaryDirectory,
        image_dir_path: Path,
        content: list[BaseTypstObject] | None = None,
    ):
        if content is None:
            content = []
        self.content = content
        self.temp_dir = temp_dir
        self.dependencies = Dependencies(
            image_factory=ImageFactory(
                temp_dir_path=Path(self.temp_dir.name), image_dir_path=image_dir_path
            )
        )

    def add_object(self, obj: BaseTypstObject):
        self.content.append(obj)

    def remove_temp_image_files(self):
        self.dependencies.image_factory.remove_temp_image_files()

    def render_block(self) -> str:
        return "\n".join([obj.render_block(self.dependencies) for obj in self.content])

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
