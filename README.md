# PDF_generation

## Todo

- [x] python dependencies: poetry
- [x] use dataclasses
- [x] Clean code: isort + black
- [ ] .dockerignore might me missing some stuff
- [ ] for env managment: environs
- [ ] Check tempfiles (from the std)
- [ ] check pathlib
- [ ] How to escape typst code
- [ ] Snake case methods
- [ ] Makefile to start the project / build the docker image, etc.
- [ ] Commit / push you code
- [ ] Try to have a very simple webapp + text editor
- [ ] No relative imports
- [ ] Add tests (test your endpoint): pytest + fastapi documentation

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
