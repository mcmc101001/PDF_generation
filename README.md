# PDF_generation

## Todo

- [x] python dependencies: poetry
- [x] use dataclasses
- [x] Clean code: isort + black
- [X] .dockerignore might me missing some stuff
- [ ] for env managment: environs
- [X] Check tempfiles (from the std)
- [X] check pathlib
- [X] How to escape typst code
- [X] Snake case methods
- [X] Makefile to start the project / build the docker image, etc.
- [X] Commit / push your code
- [ ] Try to have a very simple webapp + text editor
- [X] No relative imports
- [X] Add tests (test your endpoint): pytest + fastapi documentation

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
