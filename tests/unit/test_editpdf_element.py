"""
Unittest for the Element class in the editpdf task, validating field initialization,
type-setting, and payload structure based on element type.
"""

import pytest

from ilovepdf.editpdf_task import (
    FONT_FAMILY_OPTIONS,
    FONT_STYLE_OPTIONS,
    TEXT_ALIGN_OPTIONS,
    TYPE_OPTIONS,
    Element,
)
from ilovepdf.exceptions import IntOutOfRangeError, InvalidChoiceError, NotAnIntError

from .base_test import AbstractUnitTaskElementTest


class TestEditPdfElementTask(AbstractUnitTaskElementTest):
    """
    Unittest for validating the behavior and constraints of Element for the editpdf
    task, including field initialization, type-setting, and payload structure.
    """

    _task_class = Element

    def test_initialization(self, my_task):
        """
        Ensure Element initializes with correct default payload and no parent.
        """

        assert my_task._DEFAULT_PAYLOAD == {
            "type": None,
            "pages": None,
            "zindex": None,
            "dimensions": None,
            "coordinates": None,
            "rotation": 0,
            "opacity": 100,
            "text": None,
            "text_align": "left",
            "font_family": "Arial Unicode MS",
            "font_size": 14,
            "font_style": "Regular",
            "font_color": "#000000",
            "letter_spacing": 0,
            "underline_text": None,
            "server_filename": None,
        }
        assert my_task.parent is None
        assert TYPE_OPTIONS == {"bottom", "text", "image", "svg"}

    @pytest.mark.parametrize("value", TYPE_OPTIONS)
    def test_set_type_valid(self, my_task, value):
        """Test valid type assignment."""
        my_task.type = value
        assert my_task.type == value

    @pytest.mark.parametrize("value", ["invalid_type", "", None, 123])
    def test_set_type_invalid(self, my_task, value):
        """Test invalid type assignment raises error."""
        with pytest.raises(InvalidChoiceError):
            my_task.type = value

    @pytest.mark.parametrize("pages", ["1", "1-3", "1,3,5"])
    def test_set_pages_valid(self, my_task, pages):
        """Test valid pages assignment."""
        my_task.pages = pages
        assert my_task.pages == pages

    @pytest.mark.parametrize("pages", ["", None, 123])
    def test_set_pages_invalid(self, my_task, pages):
        """Test invalid pages assignment raises error."""
        with pytest.raises((TypeError, ValueError)):
            my_task.pages = pages

    @pytest.mark.parametrize("zindex", [-10, -1, 0, 1, 10])
    def test_set_zindex_valid(self, my_task, zindex):
        """Test valid zindex assignment."""
        my_task.zindex = zindex
        assert my_task.zindex == zindex

    @pytest.mark.parametrize("zindex", [None, 1.5, "invalid"])
    def test_set_zindex_invalid(self, my_task, zindex):
        """Test invalid zindex assignment raises error."""
        with pytest.raises(NotAnIntError):
            my_task.zindex = zindex

    @pytest.mark.parametrize("dimensions", [{"w": 100.0, "h": 50.0}])
    def test_set_dimensions_valid(self, my_task, dimensions):
        """Test valid dimensions assignment."""
        my_task.dimensions = dimensions
        assert my_task.dimensions == dimensions

    @pytest.mark.parametrize(
        "dimensions",
        [
            None,
            "invalid",
            123,
            {"width": 100, "height": 50},
            {},
            {"w": "100", "h": 50.0},
            {"w": 100.0, "h": "50"},
            {"w": 100.0},
            {"h": 50.0},
            {"w": 100.0, "h": 50.0, "extra": 1},
        ],
    )
    def test_set_dimensions_invalid(self, my_task, dimensions):
        """Test invalid dimensions assignment raises error."""
        with pytest.raises((TypeError, ValueError)):
            my_task.dimensions = dimensions

    @pytest.mark.parametrize("coordinates", [{"x": 100.0, "y": 50.0}])
    def test_set_coordinates_valid(self, my_task, coordinates):
        """Test valid coordinates assignment."""
        my_task.coordinates = coordinates
        assert my_task.coordinates == coordinates

    @pytest.mark.parametrize(
        "coordinates",
        [
            None,
            "invalid",
            123,
            {"width": 100, "height": 50},
            {},
            {"w": "100", "h": 50.0},
            {"w": 100.0, "h": "50"},
            {"w": 100.0},
            {"h": 50.0},
            {"w": 100.0, "h": 50.0, "extra": 1},
        ],
    )
    def test_set_coordinates_invalid(self, my_task, coordinates):
        """Test invalid coordinates assignment raises error."""
        with pytest.raises((TypeError, ValueError)):
            my_task.coordinates = coordinates

    @pytest.mark.parametrize("rotation", [0, 90, 360])
    def test_set_rotation_valid(self, my_task, rotation):
        """Test valid rotation assignment."""
        my_task.rotation = rotation
        assert my_task.rotation == rotation

    @pytest.mark.parametrize("rotation", [None, 1.5, "invalid"])
    def test_set_rotation_invalid(self, my_task, rotation):
        """Test invalid rotation assignment raises error."""
        with pytest.raises(NotAnIntError):
            my_task.rotation = rotation

    @pytest.mark.parametrize("rotation", [-361, 361])
    def test_set_rotation_out_range(self, my_task, rotation):
        """Test rotation assignment out of valid range raises error."""
        with pytest.raises(IntOutOfRangeError):
            my_task.rotation = rotation

    @pytest.mark.parametrize("opacity", [1, 50, 100])
    def test_set_opacity_valid(self, my_task, opacity):
        """Test valid opacity assignment."""
        my_task.opacity = opacity
        assert my_task.opacity == opacity

    @pytest.mark.parametrize("opacity", [None, 1.5, "invalid"])
    def test_set_opacity_invalid(self, my_task, opacity):
        """Test invalid opacity assignment raises error."""
        with pytest.raises(NotAnIntError):
            my_task.opacity = opacity

    @pytest.mark.parametrize("opacity", [0, 101])
    def test_set_opacity_out_range(self, my_task, opacity):
        """Test opacity assignment out of valid range raises error."""
        with pytest.raises(IntOutOfRangeError):
            my_task.opacity = opacity

    @pytest.mark.parametrize("text", ["Sample text", "Another example"])
    def test_set_text(self, my_task, text):
        """Test valid text assignment."""
        my_task.text = text
        assert my_task.text == text

    @pytest.mark.parametrize("text", [None, 123, ""])
    def test_set_text_invalid(self, my_task, text):
        """Test invalid text assignment raises error."""
        with pytest.raises((TypeError, ValueError)):
            my_task.text = text

    @pytest.mark.parametrize("text_align", TEXT_ALIGN_OPTIONS)
    def test_set_text_align_valid(self, my_task, text_align):
        """Test valid text_align assignment."""
        my_task.text_align = text_align
        assert my_task.text_align == text_align

    @pytest.mark.parametrize("text_align", [None, "invalid", 123])
    def test_set_text_align_invalid(self, my_task, text_align):
        """Test invalid text_align assignment raises error."""
        with pytest.raises(InvalidChoiceError):
            my_task.text_align = text_align

    @pytest.mark.parametrize("font_family", FONT_FAMILY_OPTIONS)
    def test_set_font_family_valid(self, my_task, font_family):
        """Test valid font_family assignment."""
        my_task.font_family = font_family
        assert my_task.font_family == font_family

    @pytest.mark.parametrize("font_family", [None, "invalid", 123])
    def test_set_font_family_invalid(self, my_task, font_family):
        """Test invalid font_family assignment raises error."""
        with pytest.raises(InvalidChoiceError):
            my_task.font_family = font_family

    @pytest.mark.parametrize("font_size", [1, 10, 100])
    def test_set_font_size_valid(self, my_task, font_size):
        """Test valid font_size assignment."""
        my_task.font_size = font_size
        assert my_task.font_size == font_size

    @pytest.mark.parametrize("font_size", [None, "invalid", -1, 0])
    def test_set_font_size_invalid(self, my_task, font_size):
        """Test invalid font_size assignment raises error."""
        with pytest.raises((NotAnIntError, IntOutOfRangeError)):
            my_task.font_size = font_size

    @pytest.mark.parametrize("font_style", FONT_STYLE_OPTIONS)
    def test_set_font_style_valid(self, my_task, font_style):
        """Test valid font_style assignment."""
        my_task.font_style = font_style
        assert my_task.font_style == font_style

    @pytest.mark.parametrize("font_style", [None, "invalid", 123])
    def test_set_font_style_invalid(self, my_task, font_style):
        """Test invalid font_style assignment raises error."""
        with pytest.raises(InvalidChoiceError):
            my_task.font_style = font_style

    @pytest.mark.parametrize("font_color", ["transparent", "#FF0000"])
    def test_set_font_color_valid(self, my_task, font_color):
        """Test valid font_color assignment."""
        my_task.font_color = font_color
        assert my_task.font_color == font_color

    @pytest.mark.parametrize("font_color", [None, 123, "invalid"])
    def test_set_font_color_invalid(self, my_task, font_color):
        """Test invalid font_color assignment raises error."""
        with pytest.raises((TypeError, ValueError)):
            my_task.font_color = font_color

    def set_generic_values(self, task, element_type="text"):
        """
        Helper to set typical values for an Element instance.
        Args:
            task (Element): The Element instance.
            element_type (str): Type for the element.
        """
        task.pages = "1-3"
        task.zindex = 1
        task.dimensions = {"w": 100.0, "h": 50.0}
        task.coordinates = {"x": 100.0, "y": 50.0}
        if element_type:
            task.type = element_type

    def check_has_keys(self, task, keys):
        """
        Assert that specified keys exist in the element's payload.
        Args:
            task (Element): The instance.
            keys (list): Keys to check.
        """
        payload_keys = task._to_payload().keys()
        for key in keys:
            assert key in payload_keys

    def check_not_has_keys(self, task, keys):
        """
        Assert that specified keys do NOT exist in the element's payload.
        Args:
            task (Element): The instance.
            keys (list): Keys that must not be present.
        """
        payload_keys = task._to_payload().keys()
        for key in keys:
            assert key not in payload_keys

    def test_set_type_botton(self, my_task):
        """Test payload keys for element type 'bottom'."""
        self.set_generic_values(my_task, element_type="bottom")
        assert my_task.type == "bottom"
        self.check_has_keys(
            my_task,
            keys=(
                "type",
                "pages",
                "zindex",
                "dimensions",
                "coordinates",
                "rotation",
                "opacity",
            ),
        )

        self.check_not_has_keys(
            my_task,
            keys=(
                "text",
                "text_align",
                "font_family",
                "font_size",
                "font_style",
                "font_color",
                "letter_spacing",
                "underline_text",
                "server_filename",
            ),
        )

    def test_set_type_text(self, my_task):
        """Test payload keys for element type 'text'."""
        my_task.text = "Sample text"
        self.set_generic_values(my_task, element_type="text")

        self.check_has_keys(
            my_task,
            keys=(
                "type",
                "pages",
                "zindex",
                "dimensions",
                "coordinates",
                "rotation",
                "opacity",
            ),
        )

        self.check_has_keys(
            my_task,
            keys=(
                "text",
                "text_align",
                "font_family",
                "font_size",
                "font_style",
                "font_color",
                "letter_spacing",
                "underline_text",
            ),
        )

        self.check_not_has_keys(my_task, keys=("server_filename",))

    @pytest.mark.parametrize("element_type", ["image", "svg"])
    def test_set_type_image_or_svg(self, my_task, element_type):
        """Test payload keys for element type 'image' or 'svg'."""
        my_task._set_attr("server_filename", "server_filename")
        self.set_generic_values(my_task, element_type=element_type)
        self.check_has_keys(
            my_task,
            keys=(
                "type",
                "pages",
                "zindex",
                "dimensions",
                "coordinates",
                "rotation",
                "opacity",
            ),
        )

        self.check_not_has_keys(
            my_task,
            keys=(
                "text",
                "text_align",
                "font_family",
                "font_size",
                "font_style",
                "font_color",
                "letter_spacing",
                "underline_text",
            ),
        )
        self.check_has_keys(my_task, keys=("server_filename",))
