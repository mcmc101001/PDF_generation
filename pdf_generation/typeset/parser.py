from dataclasses import fields
from typing import Type

from pdf_generation.models.request_model import (RequestContentType,
                                                 TypstObjectJson)
from pdf_generation.typeset.models.base_class import TypstObject
from pdf_generation.typeset.models.heading import Heading
from pdf_generation.typeset.models.paragraph import Paragraph
from pdf_generation.typeset.models.table import Table

parser_dict: dict[RequestContentType, Type[TypstObject]] = {
    "heading": Heading,
    "text": Paragraph,
    "table": Table,
}


def parse_if_typst_object(content: str | TypstObjectJson) -> str | TypstObject:
    if isinstance(content, TypstObjectJson):
        return parse_json(content)
    else:
        return content


def parse_2darray(
    array: list[list[str | TypstObjectJson]],
) -> list[list[str | TypstObject]]:
    return [[parse_if_typst_object(i) for i in _] for _ in array]


def parse_json(json_object: TypstObjectJson) -> TypstObject:
    parsed_object_type = parser_dict.get(json_object.type)
    content = json_object.content
    parsed_content: str | TypstObject | list[list[str | TypstObject]] | None = None

    if isinstance(content, str):
        parsed_content = content
    elif isinstance(content, TypstObjectJson):
        parsed_content = parse_json(content)
    elif isinstance(content, list):
        parsed_content = parse_2darray(content)
    else:
        parsed_content = None

    json_to_dict = {}
    for field in fields(json_object):
        if not field.name == "content":
            json_to_dict[field.name] = getattr(json_object, field.name)

    if parsed_object_type is None:
        raise ValueError(f"Invalid type {json_object.type}")
        # return Paragraph(content="")  # return equivalent of None

    parsed_object = parsed_object_type(content=parsed_content, **json_to_dict)  # type: ignore

    if parsed_object is None:
        raise ValueError(f"Invalid type {json_object.type}")
    return parsed_object


def parse_json_array(json_objects: list[TypstObjectJson]) -> list[TypstObject]:
    return [parse_json(obj) for obj in json_objects]
