import logging
import os

from ankidoc.adoc import file_to_str

# Generate a note from a front file.
def notegen(front_path, attributes):
    logging.info(f"running notegen on {front_path}")

    id_path, ext = os.path.splitext(front_path)

    if ext != ".front":
        logging.warning(f"{front_path} is not a front file, skipping")
        return None

    id = os.path.basename(id_path)
    back_path = id_path + ".back"

    front = file_to_str(front_path, True, attributes)
    back = file_to_str(back_path, True, attributes)

    if front == None or back == None:
        return None

    front = front.replace("\"", "\"\"")
    back = back.replace("\"", "\"\"")

    return f"\"{id}\";\"{front}\";\"{back}\"\n"
