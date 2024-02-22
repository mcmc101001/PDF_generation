from fastapi.testclient import TestClient

from pdf_generation.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


class TestGeneratePDF:
    def test_pdf_generated(self):
        response = client.get("/generate")
        assert response.status_code == 200
        assert response.headers.get("Content-Type") == "application/pdf"

    def test_pdf_name_customisation(self):
        response = client.get("/generate?file_name=custom_name")
        assert response.status_code == 200
        assert response.headers.get("Content-Type") == "application/pdf"
        assert (
            response.headers.get("Content-Disposition")
            == 'inline; filename="custom_name.pdf"'
        )
