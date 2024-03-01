from __future__ import annotations

from pathlib import Path
from shutil import copy2
from tempfile import NamedTemporaryFile
from textwrap import dedent
from typing import IO, override

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.models.base_class import BaseTypstObject, ObjectType
from pdf_generation.typeset.utils import escape_typst_code

"""
https://stackoverflow.com/questions/77682563/image-from-hyperlink-in-typst
typst images do not support internet or absolute paths.
"""


class ImageFactory:
    def __init__(
        self,
        temp_dir_path: Path,
        image_dir_path: Path,
        temp_files: list[IO] | None = None,
    ):
        if temp_files is None:
            temp_files = []
        self.temp_files = temp_files
        self.temp_dir_path = temp_dir_path
        self.image_dir_path = image_dir_path

    def generate(
        self,
        id: str,
        width_percentage: float | None = None,
        height_percentage: float | None = None,
        caption: str | None = None,
    ) -> Image:
        file = NamedTemporaryFile(
            delete=True, delete_on_close=True, dir=self.temp_dir_path
        )

        # Find the image file with the given id without knowing the file extension
        images: list[Path] = list(self.image_dir_path.rglob("*.jpeg")) + list(
            self.image_dir_path.glob("*.png")
        )
        for image in images:
            if image.stem == id:
                file_path = image
                break

        copy2(file_path, file.name)
        temp_file_relative_path = Path(file.name).relative_to(self.temp_dir_path)

        self.temp_files.append(file)

        return Image(
            image_url=temp_file_relative_path,
            width_percentage=width_percentage,
            height_percentage=height_percentage,
            caption=caption,
        )

    def remove_temp_image_files(self):
        for file in self.temp_files:
            file.close()  # Delete on close is True, so this will delete the temp file


@dataclass(frozen=True, kw_only=True)
class ImageAttrs:
    id: int = Field(default=0)


@dataclass(frozen=True, kw_only=True)
class Image(BaseTypstObject):
    type: ObjectType = "image"
    attrs: ImageAttrs = Field(default_factory=ImageAttrs)
    image_url: Path = Field()
    width_percentage: float | None = Field(default=None)
    height_percentage: float | None = Field(default=None)
    caption: str | None = Field(default=None)

    @override
    def render_internal_block(self) -> str:
        block = dedent(
            f"""\
                image("{self.image_url}"{f", width: {self.width_percentage}%" if self.width_percentage else ""}{f", height: {self.height_percentage}%" if self.height_percentage else ""})"""
        )
        if self.caption is None:
            return f"#{block}"
        else:
            return dedent(
                f"""\
                #figure(
                    {block},
                    {f"caption: [{escape_typst_code(self.caption)}]" if self.caption else ""}
                )"""
            )
