# Copyright (C) 2024-2025 Timo Früh
# See __main__.py for the full notice.

import logging
import os

from ankidoc.converter import get_anki_header

# Link notes into one output file.
def run(note_paths, output_path, notetype, deck):
    logging.info("running linker")
    logging.debug(f"notes to link: {note_paths}")

    if output_path == None:
        output_path = "out.txt"

    with open(output_path, "w") as output:
        output.write(get_anki_header(notetype, deck))

    with open(output_path, "a") as output:
        for note_path in note_paths:
            link_note(note_path, output)

# Link a note into an output file.
def link_note(note_path, output):

    if not os.path.isfile(note_path):
        logging.warning(f"{note_path} is not a file, not linked")
        return
    elif not os.path.splitext(note_path)[1] == ".note":
        logging.warning(f"{note_path} not a note file, not linked")
        return

    logging.info(f"linking {note_path}")

    with open(note_path, "r") as note_file:
        output.write(note_file.read())
