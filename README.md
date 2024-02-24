# PDF_generation

## Todo

- [x] python dependencies: poetry
- [x] use dataclasses
- [x] Clean code: isort + black
- [X] .dockerignore might me missing some stuff
- [ ] for env managment: environs
- [X] Check tempfile (from the std)
- [X] check pathlib
- [X] How to escape typst code
- [ ] Check the performance (replace / regex)
- [X] Snake case methods
- [X] Makefile to start the project / build the docker image, etc.
- [X] Commit / push your code
- [ ] Try to have a very simple webapp + text editor
- [X] No relative imports
- [X] Add tests (test your endpoint): pytest + fastapi documentation
- [X] Remove classes in tests
- [X] Run tests from Makefile with Docker
- [X] Run mypy / black --check / isort with make
- [X] Add flake8
- [X] Check docker volumes
- [X] Move your models to pdf_generation.models.py
- [ ] ImageFactory Refactor as a Context Manager
- [X] all paths should be pathlib.Path
- [X] Reorganize your files to put typst equivalent models in a single package
- [ ] Create temporary directory for compiling the PDF
- [X] Make it a real API


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
