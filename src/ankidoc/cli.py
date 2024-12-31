import argparse
import logging

from ankidoc.modes import default_mode
from ankidoc.modes import notegen_mode
from ankidoc.modes import link_mode
from ankidoc.modes import docgen_mode
from ankidoc import __version__

def main():

    # Initialise the argument parser and all arguments.
    parser = argparse.ArgumentParser(
        description="convert asciidoc notes to anki notes",
        usage="%(prog)s [ -d | -n | -l ] files ..."
    )

    parser.add_argument(
        "-a", "--attributes",
        metavar="ATTR",
        help="any asciidoctor attributes to set"
    )

    parser.add_argument(
        "-d", "--docgen",
        action="store_true",
        help="generate a single html document from the front files passed"
    )

    parser.add_argument(
        "-D", "--deck",
        help="preset an anki deck for the import"
    )

    parser.add_argument(
        "-l", "--link",
        action="store_true",
        help="link the note files passed into one anki import file"
    )

    parser.add_argument(
        "-L", "--loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        metavar="LV",
        help="select a logging level"
    )

    parser.add_argument(
        "-n", "--notegen",
        action="store_true",
        help="compile the front/back files passed into note files"
    )

    parser.add_argument(
        "-N", "--notetype",
        default="Ankidoc",
        metavar="TYPE",
        help="preset a note type for the import"
    )

    parser.add_argument(
        "-o", "--output",
        metavar="OUT",
        help="the desired output filename"
    )

    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="display version information"
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

    if args.version:
        print(__version__)
        exit(0)

    # Rule out common errors.
    if (args.docgen and args.notegen) or (args.docgen and args.link) or (args.notegen and args.link):
        logging.critical("incompatible modes")
        exit(1)

    if args.files == []:
        logging.critical("no files provided")
        exit(1)

    # Run the program in the mode requested by the user.
    if args.docgen:
        docgen_mode(args.files, args.output, args.attributes)
    elif args.notegen:
        notegen_mode(args.files, args.output, args.attributes)
    elif args.link:
        link_mode(args.files, args.output, args.notetype, args.deck)
    else:
        default_mode(args.files, args.output, args.attributes, args.notetype, args.deck)

    exit(0)

if __name__ == "__main__":
    main()
