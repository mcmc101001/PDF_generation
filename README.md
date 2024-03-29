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
- [X] Rework the dataclasses so that you don't have to do custom parsing
- [X] Use frozen & tuples as much as possible
- [X] Use docker engine over docker desktop to fix weird bug
- [X] Check fastapi depends with context manager to get a clean working directory
- [ ] Image Factory with symlicks -> Don't think this works as typst compiler requires the images to be in the same directory
- [ ] Generate qgis PNG maps with python script

## Questions
- [ ] How to inject imageFactory as dependency? into constructor makes more sense but have to recursively inject, else need to pass it as a parameter to every render_block method
- [ ] How does fastapi know what dataclass to use in request if typing is union of multiple dataclasses?