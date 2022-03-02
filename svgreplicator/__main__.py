import argparse
import json
from typing import Protocol

from .svgreplicator import Config, SvgHandler


class Args(Protocol):

    filename: str
    config: str


def get_args() -> Args:
    parser = argparse.ArgumentParser(description="Modify SVG files")
    parser.add_argument("--filename", type=str, help="SVG file")
    parser.add_argument("--config", type=str, help="Configuration file")
    return parser.parse_args()


def main():
    args = get_args()

    with open(args.config) as f:
        config: Config = json.load(f)

    for requested_output_file in config:
        svg_handler = SvgHandler()

        # Load template
        with open(args.filename) as f:
            svg_handler.read_svg(f)

        # Modify stuff
        svg_handler.modify_svg(requested_output_file["objects"])

        # Save
        with open(requested_output_file["filename"], "wb") as f:
            svg_handler.write_svg(f)


if __name__ == "__main__":
    main()
