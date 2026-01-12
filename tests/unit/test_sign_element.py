"""Unit tests for the Element class in ilovepdf.sign.element."""

import json

import pytest

from ilovepdf.exceptions import (
    IntOutOfRangeError,
    InvalidChoiceError,
    MissingPayloadFieldError,
)
from ilovepdf.sign import Element

from .base_test import AbstractUnitTaskElementTest


# pylint: disable=protected-access,too-many-public-methods
class TestSignElement(AbstractUnitTaskElementTest):
    """Unit tests for the SignElement class."""

    _task_class = Element

    @classmethod
    def setup_sample_elements(cls):
        """Set up sample Element instances for use in tests."""
        cls.element1 = cls._task_class()
        cls.element2 = cls._task_class()
        cls.element3 = cls._task_class()
        cls.element4 = cls._task_class()

    def test_sample_elements_payload(self):
        """Test that sample elements can be converted to payloads without error."""
        self.setup_sample_elements()
        self.element1._to_payload()
        self.element2._to_payload()
        self.element3._to_payload()
        self.element4._to_payload()

    def test_initialization(self):
        """Test initialization of Element class default payload and required fields."""
        assert Element._DEFAULT_PAYLOAD == {
            "position": "right bottom",
            "horizontal_position_adjustment": 0,
            "vertical_position_adjustment": 0,
            "pages": "-1",
            "content": None,
            "size": 18,
            "info": None,
            "type": "signature",
        }
        assert Element.REQUIRED_FIELDS == ["position", "pages", "size"]

    def test_valid_gravity_element_minimal(self, my_task):
        """Test minimal gravity position element with default values."""
        my_task.set_gravity_position("left", "top")
        my_task.size = 15
        my_task.pages = "1"
        assert my_task.type == "signature"
        assert my_task.size == 15
        assert my_task.pages == "1"
        assert my_task.position == "left top"
        assert my_task.horizontal_position_adjustment == 0
        assert my_task.vertical_position_adjustment == 0

    def test_standard_position(self, my_task):
        """Test setting standard position with coordinates."""
        my_task.set_standard_position(10, -100)
        assert my_task.position == "10 -100"
        assert my_task.horizontal_position_adjustment == 0
        assert my_task.vertical_position_adjustment == 0

        my_task.set_standard_position(254.98, -700.232)
        assert my_task.position == "254,98 -700,232"

    def test_valid_standard_element(self, my_task):
        """Test valid standard element with position, size, pages, and type."""
        # my_task._set_attr("position", "10 -100")
        my_task.set_standard_position(10, -100)

        my_task.size = 22
        my_task.pages = "3,5"
        my_task.type = "name"
        assert my_task.position == "10 -100"
        assert my_task.type == "name"
        assert my_task.horizontal_position_adjustment == 0
        assert my_task.vertical_position_adjustment == 0

    def test_type_default_signature(self, my_task):
        """Test that default type is 'signature'."""
        my_task.set_gravity_position("left", "top")
        my_task.size = 5
        my_task.pages = "2"
        assert my_task.type == "signature"

    def test_invalid_position_gravity(self, my_task):
        """Test invalid gravity positions raise exceptions."""
        # Gravity invalid (invalid X or Y anchor)
        with pytest.raises(InvalidChoiceError):
            my_task.set_gravity_position("north", "top")
        with pytest.raises(InvalidChoiceError):
            my_task.set_gravity_position("left", "toppp")

    def test_invalid_position_standard(self, my_task):
        """Test invalid standard positions using _set_attr."""
        # _set_attr does NOT validate; gravity_position method does
        # If needed, can check if _get_attr reflects what was set
        my_task._set_attr("position", "-2 -4")
        assert my_task._get_attr("position") == "-2 -4"
        my_task._set_attr("position", "nonsense")
        assert my_task._get_attr("position") == "nonsense"
        # The real validation is in the public API usage, not _set_attr

    def test_adjustments_gravity_ignored(self, my_task):
        """Test that adjustments are ignored for gravity positions."""
        my_task.set_gravity_position(
            "left",
            "top",
            horizontal_position_adjustment=-5,
            vertical_position_adjustment=10,
        )
        assert my_task.horizontal_position_adjustment == 0
        assert my_task.vertical_position_adjustment == 0
        my_task.set_gravity_position(
            "right",
            "bottom",
            horizontal_position_adjustment=6,
            vertical_position_adjustment=-7,
        )
        assert my_task.horizontal_position_adjustment == 0
        assert my_task.vertical_position_adjustment == 0
        # If bypassing with _set_attr, the business logic is not applied
        my_task._set_attr("horizontal_position_adjustment", -5)
        assert my_task.horizontal_position_adjustment == -5

    def test_invalid_size(self, my_task):
        """Test that invalid sizes raise exceptions."""
        my_task.set_gravity_position("left", "top")
        with pytest.raises(IntOutOfRangeError):
            my_task.size = -1
        with pytest.raises(IntOutOfRangeError):
            my_task.size = 0

    def test_missing_pages_or_size(self, my_task):
        """Test default values for missing pages or size."""
        my_task.set_gravity_position("left", "top")
        assert my_task.size == 18  # class default if never assigned
        assert my_task.pages == "-1"

    def test_invalid_pages_negative_range(self, my_task):
        """Test that negative page ranges raise exceptions."""
        my_task.set_gravity_position("left", "top")
        my_task.size = 8
        with pytest.raises(ValueError, match="Invalid page or page range"):
            my_task.pages = "-2--1"
        # with pytest.raises(ValueError, match="Invalid page range"):
        #     my_task.pages = "3,-2--1"

    def test_valid_pages_negatives_individuals(self, my_task):
        """Test valid negative individual page numbers."""
        my_task.set_gravity_position("left", "top")
        my_task.size = 7
        my_task.pages = "-1,-2,5"
        pages = my_task.pages.split(",")
        assert "-1" in pages and "-2" in pages

    def test_type_and_content_logic(self, my_task):
        """Test logic for type and content fields."""
        my_task.set_gravity_position("left", "top")
        my_task.size = 8
        my_task.pages = "1"
        my_task.type = "date"
        my_task.content = "01/02/2024"
        assert my_task.content == "01/02/2024"
        my_task2 = Element()
        my_task2.set_gravity_position("left", "top")
        my_task2.size = 8
        my_task2.pages = "1"
        my_task2.type = "text"
        my_task2.content = "mytext"
        assert my_task2.content == "mytext"
        my_task3 = Element()
        my_task3.set_gravity_position("left", "top")
        my_task3.size = 8
        my_task3.pages = "1"
        my_task3.type = "text"
        # .content raises error if type is wrong, not if not set
        assert my_task3._get_attr("content") is None
        my_task4 = Element()
        my_task4.set_gravity_position("left", "top")
        my_task4.size = 8
        my_task4.pages = "1"
        my_task4.type = "date"
        with pytest.raises(ValueError):
            my_task4.content = "notadate"

    def test_info_input_type(self, my_task):
        """Test info field for input type elements."""
        my_task.set_gravity_position("left", "top")
        my_task.size = 5
        my_task.pages = "2"
        my_task.type = "input"
        jval = json.dumps({"label": "Test", "description": "desc"})
        my_task.info = jval
        assert my_task.info is not None
        assert json.loads(my_task.info)["label"] == "Test"
        my_task2 = Element()
        my_task2.set_gravity_position("left", "top")
        my_task2.size = 5
        my_task2.pages = "2"
        my_task2.type = "input"
        # .info getter raises error if type != 'input' or
        # if never assigned, verify is None
        assert my_task2._get_attr("info") is None
        my_task3 = Element()
        my_task3.set_gravity_position("left", "top")
        my_task3.size = 5
        my_task3.pages = "2"
        my_task3.type = "input"
        with pytest.raises(ValueError):
            my_task3.info = '{"bad": True}'

    def test_type_invalid(self, my_task):
        """Test that invalid types raise exceptions."""
        my_task.set_gravity_position("left", "top")
        my_task.size = 3
        my_task.pages = "8"
        with pytest.raises(ValueError):
            my_task.type = "nonexistent-type"

    def test__set_attr_position_direct(self, my_task):
        """Direct test for _set_attr_position (private)."""
        my_task._set_attr_position(12.5, -8.3)
        assert my_task.position == "12,5 -8,3"

    def test__clean_horizontal_position_adjustment_direct(self, my_task):
        """Direct test for _clean_horizontal_position_adjustment (private)."""
        # Case with gravity position (should return 0)
        my_task.set_gravity_position("left", "top")
        result = my_task._clean_horizontal_position_adjustment(-5)
        assert result == 0
        # Case with standard position (should return the original value)
        my_task.set_standard_position(10, -10)
        result = my_task._clean_horizontal_position_adjustment(7)
        assert result == 7

    def test___clean_vertical_position_adjustment_direct(self, my_task):
        """Direct test for __clean_vertical_position_adjustment (private)."""
        # Case with gravity position (should return 0)
        my_task.set_gravity_position("left", "top")
        result = my_task._clean_vertical_position_adjustment(9)
        assert result == 0
        # Case with standard position (should return the original value)
        my_task.set_standard_position(10, -10)
        result = my_task._clean_vertical_position_adjustment(-3)
        assert result == -3

    def test_missing_required_fields_raises(self, my_task):
        """Test that MissingPayloadFieldError is raised when required fields are
        missing."""
        my_task._payload.update({"position": None, "pages": None, "size": None})

        with pytest.raises(MissingPayloadFieldError) as excinfo:
            my_task._to_payload()
        missing = excinfo.value.missing_fields
        assert missing == ["position", "pages", "size"]
