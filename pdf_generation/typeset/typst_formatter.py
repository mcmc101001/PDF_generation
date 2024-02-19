import os

import typst
from pydantic import BaseModel

from .base_class import TypstObject
from .lorem import LoremIpsum


class GenerateDocumentRequest(BaseModel):
    latitude: float
    longitude: float
    file_name: str | None = "my_file"


class TypstFormatter:
    def __init__(self):
        self.objects: list[TypstObject] = []

    def addObject(self, obj: TypstObject):
        self.objects.append(obj)

    def __toTypstCode(self) -> str:
        return "\n".join([obj.render_block() for obj in self.objects])

    def addLoremIpsum(self):
        self.addObject(LoremIpsum())

    def __generateTypstFile(self):
        filename = os.path.dirname(__file__) + "/typst_files/doc.typ"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.__toTypstCode())

    def generatePDF(self) -> bytes:
        self.__generateTypstFile()
        filename = os.path.dirname(__file__) + "/typst_files/doc.typ"
        return typst.compile(filename, root=os.path.dirname(__file__))
