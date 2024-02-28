# PDF_generation

## Todo

- [x] python dependencies: poetry
- [x] use dataclasses
- [x] Clean code: isort + black
- [x] .dockerignore might me missing some stuff
- [ ] for env managment: environs
- [x] Check tempfile (from the std)
- [x] check pathlib
- [x] How to escape typst code
- [x] Check the performance (replace / regex)
- [x] Snake case methods
- [x] Makefile to start the project / build the docker image, etc.
- [x] Commit / push your code
- [x] Try to have a very simple webapp + text editor
- [x] No relative imports
- [x] Add tests (test your endpoint): pytest + fastapi documentation
- [x] Remove classes in tests
- [x] Run tests from Makefile with Docker
- [x] Run mypy / black --check / isort with make
- [x] Add flake8
- [x] Check docker volumes
- [x] Move your models to pdf_generation.models.py
- [ ] ImageFactory Refactor as a Context Manager
- [x] all paths should be pathlib.Path
- [x] Reorganize your files to put typst equivalent models in a single package
- [x] Create temporary directory for compiling the PDF
- [x] Make it a real API

## Sample JSON input

```json
    [
        {
            "type": "heading",
            "level": 1,
            "content": "This is my title"
        },
        {
            "type": "newline"
        },
        {
            "type": "text",
            "content": "Here is a sentence"
        },
        {
            "type": "table",
            "caption": "Whatever",
            "..."
        },
        {
            "type": "electoral-results-table",
        },
        {
            "type": "aligned-block",
            "alignement": "center",
            "content": [
                {
                    "type": "heading",
                    ...
                }
            ]
        }
    ]
```
