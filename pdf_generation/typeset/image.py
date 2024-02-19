from textwrap import dedent

from pydantic import Field
from pydantic.dataclasses import dataclass
from tempfile import NamedTemporaryFile, gettempdir
from shutil import copy2

from pathlib import Path

from pdf_generation.typeset.base_class import AlignableTypstObject

"""
https://stackoverflow.com/questions/77682563/image-from-hyperlink-in-typst
typst images do not support internet or absolute paths.
"""

@dataclass(frozen=True)
class Image(AlignableTypstObject):
    image_URL: str = Field(alias="image_URL")
    width_percentage: float | None = Field(default=None, alias="width_percentage")
    height_percentage: float | None = Field(default=None, alias="height_percentage")
    caption: str | None = Field(default=None, alias="caption")
    
    def __post_init__(self):
        file = NamedTemporaryFile(delete=True, delete_on_close=True)
        copy2(self.image_URL, file.name)
        object.__setattr__(self, 'temp_file', file) # set temp_file attribute of frozen dataclass
        
        tempdir = gettempdir()
        temp_file_relative_path = Path(self.temp_file.name).relative_to(tempdir)
        object.__setattr__(self, 'image_relative_URL', temp_file_relative_path) # set imageURL attribute of frozen dataclass
    
    def __del__(self):
        self.temp_file.close()
        

    def render_internal_block(self) -> str:
        if self.temp_file is None or self.image_relative_URL is None:
            raise ValueError("Image temp_file is not generated!")
        if self.caption is None:
            return dedent(
                f"""\
                #image("{self.image_relative_URL}"{f", width: {self.width_percentage}%" if self.width_percentage else ""}{f", height: {self.height_percentage}%" if self.height_percentage else ""})"""
            )
        else:
            return dedent(
                f"""\
                #figure(
                    image("{self.image_relative_URL}"{f", width: {self.width_percentage}%" if self.width_percentage else ""}{f", height: {self.height_percentage}%" if self.height_percentage else ""}),
                    {f"caption: [{self.caption}]" if self.caption else ""}
                )"""
            )
