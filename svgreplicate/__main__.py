import argparse
import json
from typing import Protocol

from .svghandler import Replications, SvgHandler


class Args(Protocol):

    filename: str
    replications: str


def get_args() -> Args:
    parser = argparse.ArgumentParser(
        description="Replicates and modifies SVG files in batch"
    )
    parser.add_argument(
        "--filename", type=str, help="SVG file that will be used as the basis"
    )
    parser.add_argument(
        "--replications",
        type=str,
        help="JSON file with specification of replications that will be created",
    )
    return parser.parse_args()


def main():
    args = get_args()

    with open(args.replications) as f:
        config: Replications = json.load(f)

    for replication in config:
        svg_handler = SvgHandler()

        # Load template
        with open(args.filename) as f:
            svg_handler.read_svg(f)

        # Modify stuff
        svg_handler.modify_svg(replication["modifications"])

        # Save
        with open(replication["filename"], "wb") as f:
            svg_handler.write_svg(f)


if __name__ == "__main__":
    main()
