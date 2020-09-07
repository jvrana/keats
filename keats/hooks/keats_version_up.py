import argparse
import logging
from typing import Optional
from typing import Sequence

from keats import Keats

logger = logging.getLogger("keats_version_up")


def version_up():
    keats = Keats()
    keats.version.up()


PYPROJECT = "pyproject.toml"


def run(filenames):
    retv = 0
    files = {PYPROJECT}
    logger.error(filenames)
    if files.intersection(set(filenames)):
        logger.error("Updating __version__.py")
        version_up()
    # else:
    #     keats = Keats()
    #     if not keats.version._exists():
    #         keats.version.up()
    return retv


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
        default=[],
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, -vvv)"
    )
    args = parser.parse_args(argv)
    return args


def main(argv: Optional[Sequence[str]] = None) -> int:
    logger.error("main: argv: {}".format(argv))
    args = parse_args(argv)
    if args.verbose == 3:
        logger.setLevel("DEBUG")
    elif args.verbose == 2:
        logger.setLevel("INFO")
    elif args.verbose == 1:
        logger.setLevel("WARNING")
    logger.debug("Args: {}".format(args))
    return run(args.filenames)


if __name__ == "__main__":
    exit(main())
