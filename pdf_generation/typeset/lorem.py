from typing import override

from .base_class import TypstObject


class LoremIpsum(TypstObject):
    def __init__(self):
        pass

    @override
    def _render_internal_block(self) -> str:
        return f"#lorem(30)"
