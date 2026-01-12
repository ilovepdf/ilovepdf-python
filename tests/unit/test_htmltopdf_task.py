"""Unit tests for the HtmlToPdfTask class in the ilovepdf module.

These tests verify the correct behavior and parameter validation for HTML to PDF
conversion tasks using HtmlToPdfTask.
"""

import pytest

from ilovepdf.htmltopdf_task import HtmlToPdfTask
from tests.unit.base_test import AbstractUnitTaskTest


# pylint: disable=protected-access
class TestHtmlToPdfTask(AbstractUnitTaskTest):
    """Unit tests for the HtmlToPdfTask class."""

    _task_class = HtmlToPdfTask
    _task_tool = "htmlpdf"

    def test_initialization_sets_default_values(self, my_task):
        """
        Ensure HtmlToPdfTask is initialized with correct default values.
        Checks that the default settings reflect intended HTML-to-PDF parameters.
        """
        assert my_task._DEFAULT_PAYLOAD == {
            "page_orientation": "portrait",
            "page_margin": 0,
            "view_width": 1920,
            "page_size": "A4",
            "single_page": False,
            "block_ads": False,
            "remove_popups": False,
        }
        assert my_task.tool == "htmlpdf"
        assert my_task.page_orientation == "portrait"
        assert my_task.page_margin == 0
        assert my_task.view_width == 1920
        assert my_task.page_size == "A4"
        assert my_task.single_page is False
        assert my_task.block_ads is False
        assert my_task.remove_popups is False

    @pytest.mark.parametrize("orientation", ["portrait", "landscape"])
    def test_page_orientation_setter_valid(self, my_task, orientation):
        """
        Test setting valid values for page_orientation property.
        """
        my_task.page_orientation = orientation
        assert my_task.page_orientation == orientation

    @pytest.mark.parametrize(
        "invalid_orientation", ["horizontal", "vertical", "", None, 123]
    )
    def test_page_orientation_setter_invalid(self, my_task, invalid_orientation):
        """
        Test setting invalid values for page_orientation raises ValueError.
        """
        with pytest.raises(ValueError):
            my_task.page_orientation = invalid_orientation

    @pytest.mark.parametrize("margin", [0, 10, 50, 100])
    def test_page_margin_setter(self, my_task, margin):
        """
        Test setting valid values for page_margin property.
        """
        my_task.page_margin = margin
        assert my_task.page_margin == margin

    @pytest.mark.parametrize("width", [800, 1200, 1920, 2560])
    def test_view_width_setter(self, my_task, width):
        """
        Test setting valid values for view_width property.
        """
        my_task.view_width = width
        assert my_task.view_width == width

    @pytest.mark.parametrize("page_size", ["A3", "A4", "A5", "A6", "Letter", "Auto"])
    def test_page_size_setter_valid(self, my_task, page_size):
        """
        Test setting valid values for page_size property.
        """
        my_task.page_size = page_size
        assert my_task.page_size == page_size

    @pytest.mark.parametrize("invalid_page_size", ["B5", "Legal", "", None, 123])
    def test_page_size_setter_invalid(self, my_task, invalid_page_size):
        """
        Test setting invalid values for page_size raises ValueError.
        """
        with pytest.raises(ValueError):
            my_task.page_size = invalid_page_size

    @pytest.mark.parametrize("single_page", [True, False])
    def test_single_page_setter(self, my_task, single_page):
        """
        Test setting valid booleans for single_page property.
        """
        my_task.single_page = single_page
        assert my_task.single_page == single_page

    @pytest.mark.parametrize("block_ads", [True, False])
    def test_block_ads_setter(self, my_task, block_ads):
        """
        Test setting valid booleans for block_ads property.
        """
        my_task.block_ads = block_ads
        assert my_task.block_ads == block_ads

    @pytest.mark.parametrize("remove_popups", [True, False])
    def test_remove_popups_setter(self, my_task, remove_popups):
        """
        Test setting valid booleans for remove_popups property.
        """
        my_task.remove_popups = remove_popups
        assert my_task.remove_popups == remove_popups
