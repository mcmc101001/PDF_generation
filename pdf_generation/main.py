from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, Response

from pdf_generation.models.request_model import GeneratePdfRequest
from pdf_generation.typeset.models.heading import Heading
from pdf_generation.typeset.models.metadata import Metadata
from pdf_generation.typeset.models.page import Page
from pdf_generation.typeset.parser import parse_json_array
from pdf_generation.typeset.typst_formatter import TypstFormatter

cwd = Path.cwd()

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.post("/generate", tags=["typst"])
def generate(request: GeneratePdfRequest):

    document = TypstFormatter()
    document.add_object(Metadata(title=request.file_name))

    p = Path(cwd) / "pdf_generation" / "images" / "logo-512x512.png"

    logo = document.image_factory.generate(
        image_url=p, height_percentage=80, align="left"
    )

    document.add_object(Page(header=logo))

    document.add_object(Heading(content="hello"))

    objects = parse_json_array(request.content)
    for object in objects:
        document.add_object(object)

    pdf_bytes = document.generate_pdf()

    safe_file_name = quote(request.file_name)

    headers = {"Content-Disposition": f'inline; filename="{safe_file_name}.pdf"'}

    response = Response(
        content=pdf_bytes, media_type="application/pdf", headers=headers
    )

    return response
