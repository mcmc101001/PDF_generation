from pdf_generation.models.request_model import GeneratePdfRequest
from pdf_generation.typeset.parser import parse_json_array

# Tests: heading, markup
complex_json = {
    "file_name": "test",
    "content": [
        {
            "type": "heading",
            "attrs": {"level": 1},
            "content": [
                {"type": "text", "text": "This is my "},
                {"type": "text", "marks": [{"type": "italic"}], "text": "title"},
            ],
        },
        {
            "type": "orderedList",
            "attrs": {"start": 3},
            "content": [
                {"type": "listItem", "content": [{"type": "text", "text": "Item 1"}]},
                {"type": "listItem", "content": [{"type": "text", "text": "Item 2"}]},
            ],
        },
        {
            "type": "bulletList",
            "attrs": {"start": 1},
            "content": [
                {"type": "listItem", "content": [{"type": "text", "text": "Item 1"}]},
                {"type": "listItem", "content": [{"type": "text", "text": "Item 2"}]},
            ],
        },
    ],
}


def test_parser_complex_with_nesting():
    objects = parse_json_array(GeneratePdfRequest(**complex_json).content)
    assert len(objects) == 3
