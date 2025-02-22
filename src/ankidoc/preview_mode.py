# Copyright (C) 2024-2025 Timo Früh
# See __main__.py for the full notice.

import logging

from ankidoc.converter import anote_to_html

# Run the program in preview mode.
def run(front_paths, output_path, attributes):

    if output_path == None:
        output_path = "out.html"

    logging.debug(f"operating in preview mode on {front_paths}")

    if len(front_paths) > 1:
        logging.critical("cannot run in preview mode when generating multiple files")
        exit(1)

    front_path = front_paths[0]

    anote_to_html(front_path, output_path, False, attributes)
