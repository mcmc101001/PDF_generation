import re

typst_markup_char = [
    "\\",
    "*",
    "_",
    "`",
    "<",
    ">",
    "@",
    "=",
    "-",
    "+",
    "/",
    "$",
    "~",
    "#",
    '"',
    "'",
]


def escape_typst_code_iter(text: str) -> str:
    escaped_text = ""
    for char in text:
        if char in typst_markup_char:
            escaped_text += "\\" + char
        else:
            escaped_text += char
    return escaped_text


def escape_typst_code(text: str) -> str:
    escaped_text = text
    for char_to_escape in typst_markup_char:
        escaped_text = escaped_text.replace(char_to_escape, "\\" + char_to_escape)
    return escaped_text


def escape_typst_code_regex(text: str) -> str:
    regex_search_string = re.escape("".join(typst_markup_char))
    return re.sub(f"([{regex_search_string}])", r"\\\1", text)
