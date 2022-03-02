import xml.etree.ElementTree as ET
from typing import TextIO, TypedDict
from xml.etree.ElementTree import Element


# Define types and interfaces
class Object(TypedDict):
    id: str
    style: dict[str, str]


class RequestedOutputFile(TypedDict):

    filename: str
    objects: list[Object]


Config = list[RequestedOutputFile]


# Namespace
ns = {
    # "inkscape": "http://www.inkscape.org/namespaces/inkscape",
    "svg": "http://www.w3.org/2000/svg"
}


class SvgHandler:

    _tree: ET.ElementTree

    def modify_svg(self, objects: list[Object]):
        for object in objects:
            self._modify_element_style(object["id"], object["style"])

    def read_svg(self, file: TextIO) -> None:
        """Reads SVG from TextIO"""
        self._tree = ET.parse(file)

    def write_svg(self, file: TextIO) -> None:
        """Writes SVG to StringIO"""
        self._tree.write(file)

    def _get_root(self) -> ET.Element:
        try:
            return self._tree.getroot()
        except AttributeError:
            raise Exception("You need to read and SVG first")

    # All this stuff could be taken to a separate class that handles the elements
    def _modify_element_style(self, id: str, style: dict[str, str]) -> None:
        element = self._get_element(id)
        try:
            current_style = self._marshal_style(element.attrib["style"])
        except KeyError:
            current_style = {}
        style = {**current_style, **style}
        element.set("style", self._unmarshal_style(style))

    def _get_element(self, id: str) -> Element:
        if (element := self._get_root().find(f".//*[@id='{id}']", ns)) is not None:
            return element
        else:
            raise Exception(f'Element "{id}" not found')

    @staticmethod
    def _marshal_style(style: str) -> dict[str, str]:
        marshaled_style = {}
        for attrib in style.split(";"):
            key, value = tuple(attrib.split(":"))
            marshaled_style[key] = value
        return marshaled_style

    @staticmethod
    def _unmarshal_style(style: dict) -> str:
        return ";".join([f"{key}:{val}" for key, val in style.items()])
