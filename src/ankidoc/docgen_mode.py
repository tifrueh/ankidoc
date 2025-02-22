# Copyright (C) 2024-2025 Timo Früh
# See __main__.py for the full notice.

import logging

from ankidoc.converter import anote_to_adoc

# Run the program in docgen mode.
def run(front_paths, output_path, attributes, front_matter):

    if output_path == None:
        output_path = "out.adoc"

    logging.debug(f"operating in docgen mode on {front_paths}")

    if len(front_paths) > 1:
        logging.critical("cannot run in notegen mode when generating multiple files")
        exit(1)

    front_path = front_paths[0]

    anote_to_adoc(front_path, output_path, front_matter)
