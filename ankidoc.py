#!/usr/bin/env python3

import argparse
import logging
import subprocess
import os
import sys

anki_header = """#separator:semicolon
#html:true
#columns:id;question;answer

"""

# Construct a asciidoctor command.
def get_adoc_cmd(embedded, input, output):
    cmd = ["asciidoctor"]

    if embedded:
        cmd.append("-e")

    cmd.append("-o")
    cmd.append(output)
    cmd.append(input)

    return cmd

# Pass a stderr output of a subprocess to the logging system.
def pass_stderr(stderr):

    if stderr == None or stderr == b'':
        return

    stderr_string = stderr.decode("utf-8")
    stderr_lines = stderr_string.splitlines()

    for line in stderr_lines:
        logging.warning(line)

# Generate a note from a front file.
def notegen(front_path, build_directory):
    logging.info(f"running notegen on {front_path}")

    id_path, ext = os.path.splitext(front_path)

    if ext != ".front":
        logging.warning(f"{front_path} is not a front file, skipping")
        return None

    if not os.path.isdir(build_directory):
        logging.warning(f"{directory} is not a directory")
        return None

    id = os.path.basename(id_path)
    back_path = id_path + ".back"
    note_path = build_directory + "/" + id + ".note"

    front = subprocess.run(get_adoc_cmd(True, front_path, "-"), capture_output=True)
    pass_stderr(front.stderr)

    back = subprocess.run(get_adoc_cmd(True, back_path, "-"), capture_output=True)
    pass_stderr(back.stderr)

    if front.stdout == None or front.stdout == b'' or back.stdout == None or back.stdout == b'':
        return None

    front_contents = front.stdout.decode("utf-8").replace("\"", "\"\"")
    back_contents = back.stdout.decode("utf-8").replace("\"", "\"\"")

    with open(note_path, "w") as note_file:
        note_file.write(f"\"{id}\";\"{front_contents}\";\"{back_contents}\"\n")
        return note_path

# Link notes into one output file.
def link(note_paths, output_path):
    logging.info("running linker")
    logging.debug(f"notes to link: {note_paths}")

    output_contents = anki_header

    for note_path in note_paths:

        if not os.path.exists(note_path):
            logging.warning(f"{note_path} doesn't exist, not linked")
            continue
        elif not os.path.splitext(note_path)[1] == ".note":
            logging.warning(f"{note_path} not a note file, not linked")
            continue

        logging.info(f"linking {note_path}")

        with open(note_path, "r") as note_file:
            output_contents += note_file.read()

    with open(output_path, "w") as output:
        output.write(output_contents)

# Run the program in default mode on 'front_paths'.
def default_mode(front_paths, output_path, build_directory):

    logging.debug(f"operating on {front_paths}")

    note_paths = []

    for front_path in front_paths:

        note_path = notegen(front_path, build_directory)

        if note_path != None:
            note_paths.append(note_path)

    link(note_paths, output_path)

# Run the program in asciigen mode on 'front_paths'.
def asciigen_mode(front_paths, output_path):

    logging.debug(f"operating on {front_paths}")

    asciidoc_output = ""

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

        asciidoc_output += f"\n{front_contents}\n\n_{id}_\n\n{back_contents}\n"

    asciidoc_bytes = asciidoc_output.encode("utf-8")

    asciidoctor = subprocess.run(get_adoc_cmd(False, "-", output_path), input=asciidoc_bytes, capture_output=True)
    pass_stderr(asciidoctor.stderr)

# Run the program in notegen mode on 'front_paths'.
def notegen_mode(front_paths, build_directory):

    logging.debug(f"operating on {front_paths}")

    for front_path in front_paths:

        notegen(front_path, build_directory)

# Run the program in link mode on 'front_paths'.
def link_mode(front_paths, output_path):

    logging.debug(f"operating on {front_paths}")

    link(front_paths, output_path)

def main():

    # Initialise the argument parser and all arguments.
    parser = argparse.ArgumentParser(description="convert asciidoc notes to anki notes")

    parser.add_argument(
        "-a", "--asciigen",
        action="store_true",
        help="concatenate the front/back files passed into one asciidoc document"
    )

    parser.add_argument(
        "-n", "--notegen",
        action="store_true",
        help="compile the front/back files passed into note files"
    )

    parser.add_argument(
        "-l", "--link",
        action="store_true",
        help="link the note files passed into one anki import file"
    )

    parser.add_argument(
        "-o", "--output",
        default="out",
        metavar="OUT",
        help="the desired output filename (does not apply in notegen mode)"
    )

    parser.add_argument(
        "-d", "--dir",
        default=".",
        metavar="DIR",
        help="generate note files in DIR"
    )

    parser.add_argument(
        "-L", "--loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        metavar="LV",
        help="select a logging level"
    )

    parser.add_argument(
        "files",
        nargs="*",
        help="the files to operate on"
    )

    args = parser.parse_args()

    # Configure the logging mechanism.
    loglevel = logging.WARNING

    if args.loglevel == "DEBUG":
        loglevel = logging.DEBUG
    elif args.loglevel == "INFO":
        loglevel = logging.INFO
    elif args.loglevel == "WARNING":
        loglevel = logging.WARNING
    elif args.loglevel == "ERROR":
        loglevel = logging.ERROR
    elif args.loglevel == "CRITICAL":
        loglevel = logging.CRITICAL

    logging.basicConfig(format=f"{parser.prog}: %(levelname)s: %(message)s", level=loglevel)

    # Rule out common errors.
    if (args.asciigen and args.notegen) or (args.asciigen and args.link) or (args.notegen and args.link):
        logging.critical("incompatible modes")
        exit(1)

    if args.files == []:
        logging.critical("no files provided")
        exit(1)

    # Run the program in the mode requested by the user.
    if args.asciigen:
        asciigen_mode(args.files, args.output)
    elif args.notegen:
        notegen_mode(args.files, args.dir)
    elif args.link:
        link_mode(args.files, args.output)
    else:
        default_mode(args.files, args.output, args.dir)

    exit(0)

if __name__ == "__main__":
    main()
