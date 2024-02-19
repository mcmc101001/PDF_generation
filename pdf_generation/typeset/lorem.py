from typing import override

from pdf_generation.typeset.base_class import TypstObject


class LoremIpsum(TypstObject):
    def __init__(self):
        pass

    @override
    def render_internal_block(self) -> str:
        return f"#lorem(30)"
