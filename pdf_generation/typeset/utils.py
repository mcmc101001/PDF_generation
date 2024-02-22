typst_markup_char = [
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
    "\\",
    "~",
    "-",
    "#",
    '"',
    "'",
]


def escape_typst_code(text: str) -> str:
    escape_text = ""
    for char in text:
        if char in typst_markup_char:
            escape_text += "\\" + char
        else:
            escape_text += char
    return escape_text
