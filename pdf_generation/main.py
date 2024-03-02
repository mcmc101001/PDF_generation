from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Annotated
from urllib.parse import quote

from fastapi import Depends, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from pdf_generation.models.request_model import GeneratePdfRequest
from pdf_generation.typeset.models.image import Image, ImageAttrs
from pdf_generation.typeset.models.metadata import Metadata
from pdf_generation.typeset.models.page import Page
from pdf_generation.typeset.models.text import Text
from pdf_generation.typeset.typst_formatter import TypstFormatter

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:4173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.post("/generate", tags=["typst"])
def generate(
    request: GeneratePdfRequest,
    temp_dir: Annotated[TemporaryDirectory, Depends(TemporaryDirectory)],
):
    image_dir_path = Path(__file__).parent / "images"
    document = TypstFormatter(temp_dir=temp_dir, image_dir_path=image_dir_path)
    document.add_object(Metadata(title=request.file_name))

    logo = Image(attrs=ImageAttrs(id="logo"), height_percentage=80)

    document.add_object(Page(header=logo))

    if len(request.content) == 0:
        document.add_object(Text(type="text", text="No content provided"))
    for object in request.content:
        document.add_object(object)

    pdf_bytes = document.generate_pdf()

    safe_file_name = quote(request.file_name)

    headers = {"Content-Disposition": f'inline; filename="{safe_file_name}.pdf"'}

    response = Response(
        content=pdf_bytes, media_type="application/pdf", headers=headers
    )

    return response
