from __future__ import annotations

from pathlib import Path
from shutil import copy2
from tempfile import NamedTemporaryFile, _TemporaryFileWrapper, gettempdir
from textwrap import dedent
from typing import IO

from pydantic import Field
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.base_class import AlignableTypstObject, AlignmentType
from pdf_generation.typeset.utils import escape_typst_code

"""
https://stackoverflow.com/questions/77682563/image-from-hyperlink-in-typst
typst images do not support internet or absolute paths.
"""


class ImageFactory:
    def __init__(self, temp_files: list[IO] = []):
        self.temp_files = temp_files

    def generate(
        self,
        image_url: str,
        width_percentage: float | None = None,
        height_percentage: float | None = None,
        caption: str | None = None,
        align: AlignmentType | None = None,
    ) -> Image:
        file = NamedTemporaryFile(delete=True, delete_on_close=True)
        copy2(image_url, file.name)

        tempdir = gettempdir()
        temp_file_relative_path = Path(file.name).relative_to(tempdir)

        self.temp_files.append(file)

        return Image(
            image_url=str(temp_file_relative_path),
            width_percentage=width_percentage,
            height_percentage=height_percentage,
            caption=caption,
            align=align,
        )

    def remove_temp_image_files(self):
        for file in self.temp_files:
            file.close()  # Delete on close is True, so this will delete the temp file


@dataclass(frozen=True, kw_only=True)
class Image(AlignableTypstObject):
    image_url: str = Field(alias="image_url")
    width_percentage: float | None = Field(default=None, alias="width_percentage")
    height_percentage: float | None = Field(default=None, alias="height_percentage")
    caption: str | None = Field(default=None, alias="caption")

    def render_internal_block(self) -> str:
        if self.caption is None:
            return dedent(
                f"""\
                #image("{self.image_url}"{f", width: {self.width_percentage}%" if self.width_percentage else ""}{f", height: {self.height_percentage}%" if self.height_percentage else ""})"""
            )
        else:
            return dedent(
                f"""\
                #figure(
                    image("{self.image_url}"{f", width: {self.width_percentage}%" if self.width_percentage else ""}{f", height: {self.height_percentage}%" if self.height_percentage else ""}),
                    {f"caption: [{escape_typst_code(self.caption)}]" if self.caption else ""}
                )"""
            )
