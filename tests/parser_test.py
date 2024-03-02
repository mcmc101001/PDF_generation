from pdf_generation.models.request_model import GeneratePdfRequest

heading_json = {
    "file_name": "test",
    "content": [
        {
            "type": "heading",
            "attrs": {"level": 1},
            "content": [
                {"type": "text", "text": "This is my "},
                {"type": "text", "marks": [{"type": "italic"}], "text": "title"},
            ],
        }
    ],
}


def test_heading_parsed():
    assert GeneratePdfRequest(**heading_json).content[0].type == "heading"
