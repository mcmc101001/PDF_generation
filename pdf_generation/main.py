from fastapi import FastAPI, Response

from pdf_generation.typeset.base_class import TypstObject
from pdf_generation.typeset.image import Image
from pdf_generation.typeset.metadata import Metadata
from pdf_generation.typeset.page import Page
from pdf_generation.typeset.table import Table
from pdf_generation.typeset.typst_formatter import TypstFormatter

# PYTHONPATH=.


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/generate", tags=["typst"])
def generate(file_name: str = "my_file"):

    document = TypstFormatter()
    document.addObject(Metadata(title=file_name))

    logo = Image(
        imageURL="./images/logo-512x512.png", heightPercentage=80, align="left"
    )

    document.addObject(Page(header=logo))
    document.addLoremIpsum()

    place_table_content: list[list[str | TypstObject]] = [
        ["*Name*", "*Type*", "*Distance*"],
        ["McDonalds", "Fast Food", "0.5 miles"],
        ["Burger King", "Fast Food", "0.7 miles"],
        ["Subway", "Fast Food", "0.8 miles"],
        ["Taco Bell", "Fast Food", "1.0 miles"],
        ["Wendy's", "Fast Food", "1.2 miles"],
    ]

    document.addObject(
        Table(data=place_table_content, caption="Nearby Places to eat", align="right")
    )

    document.addObject(
        Image(imageURL="./images/logo-512x512.png", heightPercentage=20, align="right")
    )

    pdf_bytes = document.generatePDF()

    headers = {"Content-Disposition": f"inline; filename={file_name}.pdf"}

    response = Response(
        content=pdf_bytes, media_type="application/pdf", headers=headers
    )

    return response
