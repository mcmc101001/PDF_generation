from textwrap import dedent

from pydantic import Field
from pydantic.dataclasses import dataclass

from .base_class import AlignableTypstObject


@dataclass(frozen=True)
class Image(AlignableTypstObject):
    imageURL: str = Field(alias="imageURL")
    widthPercentage: float | None = Field(default=None, alias="widthPercentage")
    heightPercentage: float | None = Field(default=None, alias="heightPercentage")
    caption: str | None = Field(default=None, alias="caption")

    def _render_internal_block(self) -> str:
        if self.caption is None:
            return dedent(
                f"""\
                #image("{self.imageURL}"{f", width: {self.widthPercentage}%" if self.widthPercentage else ""}{f", height: {self.heightPercentage}%" if self.heightPercentage else ""})"""
            )
        else:
            return dedent(
                f"""\
                #figure(
                    image("{self.imageURL}"{f", width: {self.widthPercentage}%" if self.widthPercentage else ""}{f", height: {self.heightPercentage}%" if self.heightPercentage else ""}),
                    {f"caption: [{self.caption}]" if self.caption else ""}
                )"""
            )
