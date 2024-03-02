from typing import Literal, Union

from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from pdf_generation.typeset.dependencies.image_factory import ImageFactory

type DependencyType = Union[ImageFactory]  # type: ignore
type DependencyLabel = Literal["image_factory"]  # type: ignore


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Dependencies:
    image_factory: ImageFactory
