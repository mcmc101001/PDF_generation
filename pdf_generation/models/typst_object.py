from pdf_generation.typeset.models.heading import Heading
from pdf_generation.typeset.models.list import BulletList, ListItem, OrderedList
from pdf_generation.typeset.models.paragraph import Paragraph
from pdf_generation.typeset.models.text import Text

from typing import Union

TypstObject = Union[Heading, Text, Paragraph, BulletList, ListItem, OrderedList]
