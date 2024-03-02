from pathlib import Path
from shutil import copy2
from tempfile import NamedTemporaryFile
from typing import IO


class ImageFactory:
    def __init__(
        self,
        temp_dir_path: Path,
        image_dir_path: Path,
        temp_files: list[IO] | None = None,
    ):
        if temp_files is None:
            temp_files = []
        self.temp_files = temp_files
        self.temp_dir_path = temp_dir_path
        self.image_dir_path = image_dir_path

    def generate_image_path(self, id: str) -> Path:
        file = NamedTemporaryFile(
            delete=True, delete_on_close=True, dir=self.temp_dir_path
        )

        # Find the image file with the given id without knowing the file extension
        images: list[Path] = list(self.image_dir_path.rglob("*.jpeg")) + list(
            self.image_dir_path.glob("*.png")
        )
        for image in images:
            if image.stem == id:
                file_path = image
                break

        copy2(file_path, file.name)
        temp_file_relative_path = Path(file.name).relative_to(self.temp_dir_path)

        self.temp_files.append(file)

        return temp_file_relative_path

    def remove_temp_image_files(self):
        for file in self.temp_files:
            file.close()  # Delete on close is True, so this will delete the temp file
