# Copyright (C) 2024-2025 Timo Früh
# See __main__.py for the full notice.

import logging
import subprocess
import os

# Pass a stderr output of a subprocess to the logging system.
def pass_stderr(stderr):

    if stderr == None or stderr == b'':
        return

    stderr_string = stderr.decode("utf-8")
    stderr_lines = stderr_string.splitlines()

    for line in stderr_lines:
        logging.warning(line)

# Construct a asciidoctor command.
def get_adoc_cmd(input, output, embedded, attributes):
    cmd = ["asciidoctor"]

    if embedded:
        cmd.append("-e")

    if attributes:
        cmd.append("-a")
        cmd.append(attributes)

    cmd.append("-o")
    cmd.append(output)
    cmd.append(input)

    logging.debug(f"constructed command \"{cmd}\"");

    return cmd

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

# Generate front matter.
def get_front_matter(id, tags):

    front_matter = "+++\n"
    front_matter += f"title = '{id}'\n"

    if tags:

        front_matter += "tags = [ "

        for tag in tags[:-1]:
            front_matter += f"'{tag}', "

        front_matter += f"'{tags[-1]}' ]\n"

    front_matter += "+++\n"

    logging.debug(f"constructed front matter")

    return front_matter

# Read tags from a file.
def read_tags(input_path):

    logging.debug(f"reading tags from {input_path}")

    if not os.path.isfile(input_path):
        logging.warning(f"reading tags from {input_path} failed: not a file")
        return None

    with open(input_path, "r") as input_file:
        tags = []
        for line in input_file:
            tags.extend(line.split())
        return tags;

# Convert an adoc string to a html string.
def astr_to_hstr(input, embedded, attributes):

    input_bytes = input.encode("utf-8")

    cmd = get_adoc_cmd("-", "-", embedded, attributes)
    process = subprocess.run(cmd, input=input_bytes, capture_output=True)
    pass_stderr(process.stderr)

    return process.stdout.decode("utf-8")

# Convert an adoc string to a html file.
def astr_to_hfile(input, output_path, embedded, attributes):

    input_bytes = input.encode("utf-8")

    cmd = get_adoc_cmd("-", output_path, embedded, attributes)
    process = subprocess.run(cmd, input=input_bytes, capture_output=True)
    pass_stderr(process.stderr)

# Convert an adoc file to a html string.
def afile_to_hstr(input_path, embedded, attributes):

    cmd = get_adoc_cmd(input_path, "-", embedded, attributes)
    process = subprocess.run(cmd, capture_output=True)
    pass_stderr(process.stderr)

    return process.stdout.decode("utf-8")

# Convert an adoc file to a html file.
def afile_to_hfile(input_path, output_path, embedded, attributes):
    cmd = get_adoc_cmd(input_path, output_path, embedded, attributes)
    process = subprocess.run(cmd, capture_output=True)
    pass_stderr(process.stderr)

# Convert an anote directory to a note string.
def anote_to_hnstr(input_path, embedded, attributes):

    if not os.path.isdir(input_path):
        logging.warning(f"reading anote from {input_path} failed: not a directory")
        return None
    elif not os.path.splitext(input_path)[1] == ".anote":
        logging.warning(f"reading anote from {input_path} failed: not an anote directory")
        return None

    split_path = os.path.split(input_path)
    anote_name = split_path[0] if split_path[1] == '' else split_path[1]
    id = os.path.splitext(anote_name)[0]

    front_path = os.path.join(input_path, "front.adoc")
    back_path = os.path.join(input_path, "back.adoc")
    tags_path = os.path.join(input_path, "tags.txt")

    if not os.path.isfile(front_path):
        logging.warning(f"reading front from {front_path} failed: not a file")
        return None

    if not os.path.isfile(back_path):
        logging.warning(f"reading front from {back_path} failed: not a file")
        return None

    front_html = afile_to_hstr(front_path, embedded, attributes)
    back_html = afile_to_hstr(back_path, embedded, attributes)
    tags = read_tags(tags_path)

    if not tags:
        tags_string = ""
    else:
        tags_string = "" if len(tags) == 0 else " ".join(tags)

    front_html = front_html.replace("\"", "\"\"")
    back_html = back_html.replace("\"", "\"\"")

    return f"\"{id}\";\"{front_html}\";\"{back_html}\";\"{tags_string}\"\n"

# Convert an anote directory to a note file.
def anote_to_hnote(input_path, output_path, embedded, attributes):

    hnstr = anote_to_hnstr(input_path, embedded, attributes)

    if not hnstr:
        logging.warning(f"conversion to note file {output_path} failed")
        return

    with open(output_path, "w") as output_file:
        output_file.write(hnstr)

# Convert an anote directory to a asciidoc string.
def anote_to_astr(input_path, front_matter):

    if not os.path.isdir(input_path):
        logging.warning(f"reading anote from {input_path} failed: not a directory")
        return None
    elif not os.path.splitext(input_path)[1] == ".anote":
        logging.warning(f"reading anote from {input_path} failed: not an anote directory")
        return None

    split_path = os.path.split(input_path)
    anote_name = split_path[0] if split_path[1] == '' else split_path[1]
    id = os.path.splitext(anote_name)[0]

    front_path = os.path.join(input_path, "front.adoc")
    back_path = os.path.join(input_path, "back.adoc")
    tags_path = os.path.join(input_path, "tags.txt")

    if not os.path.isfile(front_path):
        logging.warning(f"reading front from {front_path} failed: not a file")
        return None

    if not os.path.isfile(back_path):
        logging.warning(f"reading front from {back_path} failed: not a file")
        return None

    with open(front_path, "r") as front_file:
        front_astr = front_file.read();

    with open(back_path, "r") as back_file:
        back_astr = back_file.read();

    tags = read_tags(tags_path)

    astr = ""

    if front_matter:
        astr += get_front_matter(id, tags)

    astr += f"{front_astr}\n'''\n\n{back_astr}"

    return astr

# Convert an anote directory to a adoc file.
def anote_to_adoc(input_path, output_path, front_matter):

    astr = anote_to_astr(input_path, front_matter)

    if not astr:
        logging.warning(f"conversion to adoc file {output_path} failed")
        return

    with open(output_path, "w") as output_file:
        output_file.write(astr)

# Convert an anote directory to a html string.
def anote_to_hstr(input_path, embedded, attributes):

    astr = anote_to_astr(input_path, False)
    
    if not astr:
        return None

    return astr_to_hstr(astr, embedded, attributes)

# Convert an anote directory to a html file.
def anote_to_html(input_path, output_path, embedded, attributes):

    hstr = anote_to_hstr(input_path, embedded, attributes)

    if not hstr:
        logging.warning(f"conversion to html file {output_path} failed")
        return

    with open(output_path, "w") as output_file:
        output_file.write(hstr)
