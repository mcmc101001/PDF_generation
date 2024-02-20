import os
# PYTHONPATH=.
from pathlib import PurePath

from fastapi import FastAPI, Response

from pdf_generation.typeset.base_class import TypstObject
from pdf_generation.typeset.image import ImageFactory
from pdf_generation.typeset.metadata import Metadata
from pdf_generation.typeset.page import Page
from pdf_generation.typeset.table import Table
from pdf_generation.typeset.typst_formatter import TypstFormatter

dir_path = os.path.dirname(os.path.realpath(__file__))

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/generate", tags=["typst"])
def generate(file_name: str = "my_file"):

    document = TypstFormatter(objects=[])
    document.add_object(Metadata(title=file_name))

    p = PurePath(dir_path) / "images" / "logo-512x512.png"
    print(p)

    logo = document.image_factory.generate(
        image_url=str(p), height_percentage=80, align="left"
    )

    document.add_object(Page(header=logo))
    document.add_lorem_ipsum()

    place_table_content: list[list[str | TypstObject]] = [
        ["*Name*", "*Type*", "*Distance*"],
        ["McDonalds", "Fast Food", "0.5 miles"],
        ["Burger King", "Fast Food", "0.7 miles"],
        ["Subway", "Fast Food", "0.8 miles"],
        ["Taco Bell", "Fast Food", "1.0 miles"],
        ["Wendy's", "Fast Food", "1.2 miles"],
    ]

    document.add_object(
        Table(data=place_table_content, caption="Nearby Places to eat", align="right")
    )

    # document.add_object(
    #     Image(imageURL="./images/logo-512x512.png", heightPercentage=20, align="right")
    # )

    pdf_bytes = document.generate_pdf()

    headers = {"Content-Disposition": f'inline; filename="{file_name}.pdf"'}

    response = Response(
        content=pdf_bytes, media_type="application/pdf", headers=headers
    )

    return response
