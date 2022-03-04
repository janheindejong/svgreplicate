import io
import xml.etree.ElementTree as ET

import pytest

from svgreplicate.svghandler import ElementModification, SvgHandler


@pytest.fixture(scope="class")
def svg_file() -> io.StringIO:
    f = io.StringIO(
        """<svg
    width="210mm"
    height="297mm" 
    id="svg" 
    version="1.1"
    xmlns="http://www.w3.org/2000/svg" >
    <g id="group1">
        <ellipse
            style="opacity:1;fill:#009bff"
            id="ellipse1"
            cx="0.0"
            cy="0.0"
            rx="10.0"
            ry="10.0" />
        <g id="group2" />
    <text id="text1">
        <tspan>First text</tspan>
        <tspan>Second text 
            <tspan>Nested text</tspan> 
        </tspan>
    </text>
    </g>
</svg>
"""
    )
    return f


@pytest.fixture(scope="class")
def modifications():
    return [
        {"id": "ellipse1", "style": {"fill": "#000000", "display": "none"}},
        {"id": "group2", "style": {"display": "none"}},
        {"id": "text1", "text": "Hello, world!"},
    ]


@pytest.fixture(scope="class")
def svg_handler(svg_file: io.StringIO) -> SvgHandler:
    svg_handler = SvgHandler()
    svg_handler.read(svg_file)
    return svg_handler


class TestModifySuccessfully:
    @pytest.fixture(autouse=True, scope="class")
    def modify(self, svg_handler: SvgHandler, modifications: list[ElementModification]):
        svg_handler.modify(modifications)

    def test_elipse_modified_correctly(self, svg_handler: SvgHandler):
        element = ET.fromstring(svg_handler.get_element_string("ellipse1"))
        assert element.attrib["style"] == "opacity:1;fill:#000000;display:none"

    def test_group_modified_correctly(self, svg_handler: SvgHandler):
        element = ET.fromstring(svg_handler.get_element_string("group2"))
        assert element.attrib["style"] == "display:none"

    def test_text_modified_correctly(self, svg_handler: SvgHandler):
        element = ET.fromstring(svg_handler.get_element_string("text1"))
        assert element.text == "Hello, world!"
        assert len(element) == 0

    def test_file_written_correctly(self, svg_handler: SvgHandler):
        f = io.BytesIO()
        svg_handler.write(f)
        value = b" ".join(f.getvalue().split())
        expected = b"""<svg:svg xmlns:svg="http://www.w3.org/2000/svg" width="210mm" height="297mm" id="svg" version="1.1"> <svg:g id="group1"> <svg:ellipse style="opacity:1;fill:#000000;display:none" id="ellipse1" cx="0.0" cy="0.0" rx="10.0" ry="10.0" /> <svg:g id="group2" style="display:none" /> <svg:text id="text1">Hello, world!</svg:text> </svg:g> </svg:svg>"""
        assert value == expected
