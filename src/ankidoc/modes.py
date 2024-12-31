import logging
import os

from ankidoc.anki import get_anki_header
from ankidoc.adoc import str_to_file
from ankidoc.notegen import notegen

# Convert and add a note to an output file.
def convert_note(front_path, output, attributes):
    note = notegen(front_path, attributes)

    if not note == None:
        output.write(note)

# Run the program in default mode.
def default_mode(front_paths, output_path, attributes, notetype, deck):

    if output_path == None:
        output_path = "out.txt"

    logging.debug(f"operating in default mode on {front_paths}")

    with open(output_path, "w") as output:
        output.write(get_anki_header(notetype, deck))

    with open(output_path, "a") as output:
        for front_path in front_paths:
            convert_note(front_path, output, attributes)

# Run the program in notegen mode.
def notegen_mode(front_paths, output_path, attributes):

    if output_path == None:
        output_path = "out.note"

    logging.debug(f"operating in notegen_mode on {front_paths}")

    if len(front_paths) > 1:
        logging.critical("cannot run in notegen mode when generating multiple files")
        exit(1)

    note = notegen(front_paths[0], attributes)

    if note == None:
        return

    with open(output_path, "w") as note_file:
        note_file.write(note)

# Link a note into an output file.
def link_note(note_path, output):

    if not os.path.exists(note_path):
        logging.warning(f"{note_path} doesn't exist, not linked")
        return
    elif not os.path.splitext(note_path)[1] == ".note":
        logging.warning(f"{note_path} not a note file, not linked")
        return

    logging.info(f"linking {note_path}")

    with open(note_path, "r") as note_file:
        output.write(note_file.read())

# Link notes into one output file.
def link_mode(note_paths, output_path, notetype, deck):
    logging.info("running linker")
    logging.debug(f"notes to link: {note_paths}")

    if output_path == None:
        output_path = "out.txt"

    with open(output_path, "w") as output:
        output.write(get_anki_header(notetype, deck))

    with open(output_path, "a") as output:
        for note_path in note_paths:
            link_note(note_path, output)

# Run the program in docgen mode.
def docgen_mode(front_paths, output_path, attributes):

    if output_path == None:
        output_path = "out.html"

    logging.debug(f"operating in docgen mode on {front_paths}")

    adoc = ""

    for front_path in front_paths:

        id_path, ext = os.path.splitext(front_path)

        if ext != ".front":
            logging.warning(f"{front_path} is not a front file, skipping")
            continue

        id = os.path.basename(id_path)
        back_path = id_path + ".back"

        if not os.path.isfile(front_path):
            logging.warning(f"{front_path} is not a file, skipping")
            continue
        elif not os.path.isfile(back_path):
            logging.warning(f"{back_path} is not a file, skipping")
            continue

        front_contents = ""
        back_contents = ""

        with open(front_path, "r") as front_file:
            front_contents = front_file.read()

        with open(back_path, "r") as back_file:
            back_contents = back_file.read()

        adoc += f"\n{front_contents}\n\n_{id}_\n\n{back_contents}\n"

    str_to_file(adoc, output_path, False, attributes)
