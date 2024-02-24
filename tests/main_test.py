from io import BytesIO

import pikepdf
from fastapi.testclient import TestClient

from pdf_generation.main import app

client = TestClient(app)

sample_json = {
    "file_name": "test",
    "content": [],
}


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_pdf_generated():
    response = client.post("/generate", json=sample_json)
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "application/pdf"


def test_pdf_name_customisation():
    response = client.post(
        "/generate",
        json={
            "file_name": "custom_name",
            "content": [],
        },
    )
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "application/pdf"
    assert (
        response.headers.get("Content-Disposition")
        == 'inline; filename="custom_name.pdf"'
    )


def test_pdf_name_escape_characters():
    response = client.post(
        "/generate",
        json={
            "file_name": "!@$%^*()_+-={}[]:\";'<>,./|\\~#&?",
            "content": [],
        },
    )
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "application/pdf"
    with pikepdf.open(BytesIO(response.content)) as pdf:
        assert str(pdf.docinfo["/Title"]) == "!@$%^*()_+-={}[]:\";'<>,./|\\~#&?"


# FAILED
def test_pdf_exact_output():
    response = client.post(
        "/generate",
        json={
            "file_name": "custom_name",
            "content": [],
        },
    )
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "application/pdf"
    with open("tests/pdfs/reference.pdf", "rb") as f:
        expected_pdf = f.read()
    assert response.content == expected_pdf
