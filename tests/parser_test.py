from pdf_generation.models.request_model import GeneratePdfRequest
from pdf_generation.typeset.parser import parse_json_array

simple_json = {
    "file_name": "test",
    "content": [{"type": "heading", "level": 1, "content": "This is my title"}],
}

complex_json = {
    "file_name": "test",
    "content": [
        {"type": "heading", "level": 1, "content": "This is my title"},
        {"type": "text", "content": "Here is a sentence"},
        {
            "type": "table",
            "caption": "Whatever",
            "content": [
                ["hey", "idk", "this"],
                [
                    {"type": "heading", "level": 1, "content": "This is another title"},
                    "hey2",
                    "hey3",
                ],
            ],
        },
        {
            "type": "heading",
            "level": 1,
            "content": "This is my other title",
            "align": "center",
        },
    ],
}


def test_parser_simple():
    objects = parse_json_array(GeneratePdfRequest(**simple_json).content)
    assert len(objects) == 1


def test_parser_complex_with_nesting():
    objects = parse_json_array(GeneratePdfRequest(**complex_json).content)
    assert len(objects) == 4
    assert objects[2].content[1][0].level == 1
    assert objects[2].content[1][0].content == "This is another title"
    assert objects[2].content[1][1] == "hey2"
    assert objects[2].caption == "Whatever"
