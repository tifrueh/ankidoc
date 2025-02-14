# Copyright (C) 2024-2025 Timo Früh
# See __main__.py for the full notice.

# Construct an anki import file header.
def get_anki_header(notetype, deck):
    header = ""

    header += "#separator:semicolon\n"
    header += "#html:true\n"
    header += "#columns:id;front;back;tags\n"
    header += "#tags column:4\n"

    if not notetype == None:
        header += f"#notetype:{notetype}\n"

    if not deck == None:
        header += f"#deck:{deck}\n"

    header += "\n"

    return header
