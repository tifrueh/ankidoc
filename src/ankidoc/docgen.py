# Copyright (C) 2024-2025 Timo Früh
# See __main__.py for the full notice.

import logging

# Generate front matter.
def get_front_matter(id, tags_string):

    front_matter = "+++\n"
    front_matter += f"title = '{id}'\n"

    if tags_string != None:

        front_matter += "tags = [ "

        tags = tags_string.split()

        for tag in tags[:-1]:
            front_matter += f"'{tag}', "

        front_matter += f"'{tags[-1]}' ]\n"

    front_matter += "+++\n"

    logging.debug(f"constructed front matter")

    return front_matter
