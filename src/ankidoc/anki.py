# Construct an anki import file header.
def get_anki_header(notetype, deck):
    header = ""

    header += "#separator:semicolon\n"
    header += "#html:true\n"
    header += "#columns:id;front;back\n"

    if not notetype == None:
        header += f"#notetype:{notetype}\n"

    if not deck == None:
        header += f"#deck:{deck}\n"

    header += "\n"

    return header
