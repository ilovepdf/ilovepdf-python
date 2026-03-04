"""Unit tests for the PageNumbersTask class in the ilovepdf module.

These tests verify the correct behavior, parameter validation, and error handling
for page numbering tasks using PageNumbersTask.
"""

import pytest

from ilovepdf import PageNumbersTask
from ilovepdf.exceptions import (
    IntOutOfRangeError,
    InvalidChoiceError,
)
from ilovepdf.pagenumbers_task import (
    FONT_FAMILY_OPTIONS,
    FONT_STYLE_OPTIONS,
    LAYER_OPTIONS,
    PAGE_NUMBER_POSITION_OPTIONS,
)

from .base_test import AbstractUnitTaskTest


class TestPageNumbersTask(AbstractUnitTaskTest):
    """
    Unit tests for PageNumbersTask.

    Covers initialization, valid and invalid property settings, and parameter
        validation.
    """

    _task_class = PageNumbersTask
    _task_tool = "pagenumber"

    def test_initialization_sets_default_values(self, my_task):
        """Test that default values are set correctly upon initialization."""
        assert my_task.position == "bottom_center"
        assert my_task.format == "{page_number}"
        assert my_task.start_number == 1
        assert my_task.font_family == "Arial Unicode MS"
        assert my_task.font_style is None
        assert my_task.font_size == 12
        assert my_task.font_color == "#000000"
        assert my_task.transparency == 100
        assert my_task.layer == "above"
        assert my_task.pages == "all"
        assert my_task.show_on_cover is False

        assert my_task._DEFAULT_PAYLOAD == {
            "position": "bottom_center",
            "format": "{page_number}",
            "start_number": 1,
            "font_family": "Arial Unicode MS",
            "font_style": None,
            "font_size": 12,
            "font_color": "#000000",
            "transparency": 100,
            "layer": "above",
            "pages": "all",
            "show_on_cover": False,
        }

    @pytest.mark.parametrize("position", list(PAGE_NUMBER_POSITION_OPTIONS))
    def test_position_setter_accepts_valid_values(self, my_task, position):
        my_task.position = position
        assert my_task.position == position

    def test_position_setter_rejects_invalid_value(self, my_task):
        with pytest.raises(InvalidChoiceError):
            my_task.position = "middle_left"

    def test_format_setter_accepts_valid_string(self, my_task):
        my_task.format = "Page {page_number} of {total_pages}"
        assert my_task.format == "Page {page_number} of {total_pages}"

    @pytest.mark.parametrize("invalid", [None, "", 123])
    def test_format_setter_rejects_invalid(self, my_task, invalid):
        with pytest.raises((TypeError, ValueError)):
            my_task.format = invalid

    def test_start_number_setter_accepts_positive_int(self, my_task):
        my_task.start_number = 5
        assert my_task.start_number == 5

    @pytest.mark.parametrize("invalid", [0, -1, -100])
    def test_start_number_setter_rejects_non_positive(self, my_task, invalid):
        with pytest.raises(IntOutOfRangeError):
            my_task.start_number = invalid

    @pytest.mark.parametrize("font_family", list(FONT_FAMILY_OPTIONS))
    def test_font_family_setter_accepts_valid(self, my_task, font_family):
        my_task.font_family = font_family
        assert my_task.font_family == font_family

    def test_font_family_setter_rejects_invalid(self, my_task):
        with pytest.raises(InvalidChoiceError):
            my_task.font_family = "Papyrus"

    @pytest.mark.parametrize("font_style", list(FONT_STYLE_OPTIONS))
    def test_font_style_setter_accepts_valid(self, my_task, font_style):
        my_task.font_style = font_style
        assert my_task.font_style == font_style

    def test_font_style_setter_rejects_invalid(self, my_task):
        with pytest.raises(InvalidChoiceError):
            my_task.font_style = "Underline"

    @pytest.mark.parametrize("size", [6, 12, 72])
    def test_font_size_setter_accepts_valid_range(self, my_task, size):
        my_task.font_size = size
        assert my_task.font_size == size

    @pytest.mark.parametrize("invalid", [5, 0, 73, 100])
    def test_font_size_setter_rejects_out_of_range(self, my_task, invalid):
        with pytest.raises(IntOutOfRangeError):
            my_task.font_size = invalid

    def test_font_color_setter_accepts_valid_string(self, my_task):
        my_task.font_color = "#FF00FF"
        assert my_task.font_color == "#FF00FF"

    @pytest.mark.parametrize("invalid", [None, "", 123])
    def test_font_color_setter_rejects_invalid(self, my_task, invalid):
        with pytest.raises((TypeError, ValueError)):
            my_task.font_color = invalid

    @pytest.mark.parametrize("transparency", [1, 50, 100])
    def test_transparency_setter_accepts_valid_range(self, my_task, transparency):
        my_task.transparency = transparency
        assert my_task.transparency == transparency

    @pytest.mark.parametrize("invalid", [0, 101, -1])
    def test_transparency_setter_rejects_out_of_range(self, my_task, invalid):
        with pytest.raises(IntOutOfRangeError):
            my_task.transparency = invalid

    @pytest.mark.parametrize("layer", list(LAYER_OPTIONS))
    def test_layer_setter_accepts_valid(self, my_task, layer):
        my_task.layer = layer
        assert my_task.layer == layer

    def test_layer_setter_rejects_invalid(self, my_task):
        with pytest.raises(InvalidChoiceError):
            my_task.layer = "underneath"

    def test_pages_setter_accepts_valid_string(self, my_task):
        my_task.pages = "1,2,3"
        assert my_task.pages == "1,2,3"

    @pytest.mark.parametrize("invalid", [None, "", 123])
    def test_pages_setter_rejects_invalid(self, my_task, invalid):
        with pytest.raises((TypeError, ValueError)):
            my_task.pages = invalid

    @pytest.mark.parametrize("flag", [True, False])
    def test_show_on_cover_setter_accepts_bool(self, my_task, flag):
        my_task.show_on_cover = flag
        assert my_task.show_on_cover == flag

    @pytest.mark.parametrize("invalid", [None, 1, "true", [], {}])
    def test_show_on_cover_setter_rejects_non_bool(self, my_task, invalid):
        # with pytest.raises(Exception):
        #     my_task.show_on_cover = invalid
        with pytest.raises(InvalidChoiceError):
            my_task.show_on_cover = invalid
