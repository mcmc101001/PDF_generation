import uvicorn

if __name__ == "__main__":
    uvicorn.run("pdf_generation.main:app", reload=True, port=8000)
