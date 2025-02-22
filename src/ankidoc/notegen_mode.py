# Copyright (C) 2024-2025 Timo Früh
# See __main__.py for the full notice.

import logging
import os

from ankidoc.converter import anote_to_hnote

# Run the program in notegen mode.
def run(front_paths, output_path, attributes):

    if output_path == None:
        output_path = "out.note"

    logging.debug(f"operating in notegen_mode on {front_paths}")

    if len(front_paths) > 1:
        logging.critical("cannot run in notegen mode when generating multiple files")
        exit(1)

    note = anote_to_hnote(front_paths[0], output_path, True, attributes)
