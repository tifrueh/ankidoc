# Copyright (C) 2024-2025 Timo Früh
# See __main__.py for the full notice.

import logging

from ankidoc.converter import get_anki_header
from ankidoc.converter import anote_to_hnstr

# Run the program in default mode.
def run(front_paths, output_path, attributes, notetype, deck):

    if output_path == None:
        output_path = "out.txt"

    logging.debug(f"operating in default mode on {front_paths}")

    with open(output_path, "w") as output:
        output.write(get_anki_header(notetype, deck))

    with open(output_path, "a") as output:
        for front_path in front_paths:
            hnstr = anote_to_hnstr(front_path, True, attributes)
            if not hnstr: continue
            output.write(hnstr)
