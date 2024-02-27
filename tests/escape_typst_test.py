from pdf_generation.typeset.utils import (
    escape_typst_code,
    escape_typst_code_regex,
    escape_typst_code_iter,
)

from random import choice
from string import ascii_letters, digits, punctuation

from time import time

STRING_LENGTH = 10000000

random_string = "".join(
    choice(ascii_letters + digits + punctuation) for _ in range(STRING_LENGTH)
)

str_to_escape = "This is - a *test* string with _some_ `special` characters"
expected_output = (
    "This is \\- a \\*test\\* string with \\_some\\_ \\`special\\` characters"
)


def test_escape_typst_code():
    assert escape_typst_code(str_to_escape) == expected_output


def test_escape_typst_code_iter():
    assert escape_typst_code_iter(str_to_escape) == expected_output


def test_escape_typst_code_regex():
    assert escape_typst_code_regex(str_to_escape) == expected_output


def test_all_escapes():
    assert (
        escape_typst_code(random_string)
        == escape_typst_code_iter(random_string)
        == escape_typst_code_regex(random_string)
    )


def compare_timing():
    start = time()
    escape_typst_code(random_string)
    print(f"escape_typst_code_replace: {time() - start}")

    start = time()
    escape_typst_code_iter(random_string)
    print(f"escape_typst_code_iter: {time() - start}")

    start = time()
    escape_typst_code_regex(random_string)
    print(f"escape_typst_code_regex: {time() - start}")


if __name__ == "__main__":
    compare_timing()
