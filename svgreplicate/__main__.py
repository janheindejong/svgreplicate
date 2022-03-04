import argparse
import json
from typing import Protocol

from .svghandler import Replicas, SvgHandler


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
        "--replicas",
        type=str,
        help="JSON file with specification of replicas that will be created",
    )
    return parser.parse_args()


def main():
    args = get_args()

    with open(args.replications) as f:
        replicas: Replicas = json.load(f)

    for replica in replicas:
        svg_handler = SvgHandler()

        # Load template
        with open(args.filename) as f:
            svg_handler.read(f)

        # Modify stuff
        svg_handler.modify(replica["modifications"])

        # Save
        with open(replica["filename"], "wb") as f:
            svg_handler.write(f)


if __name__ == "__main__":
    main()
