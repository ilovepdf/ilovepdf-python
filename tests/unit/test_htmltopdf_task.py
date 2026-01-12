"""Unit tests for the HtmlToPdfTask class from ilovepdf.

This module contains tests to verify the correct behavior of HtmlToPdfTask,
including initialization, default values, and setter validation logic.
"""

import pytest

from ilovepdf import HtmlToPdfTask


class TestHtmlToPdfTask:
    """Unit tests for the HtmlToPdfTask class from ilovepdf."""

    @pytest.fixture
    def htmltopdf_task(self):
        """Fixture that creates an HtmlToPdfTask instance for testing."""
        return HtmlToPdfTask("public_key", "secret_key", make_start=False)

    def test_initialization_sets_tool_htmlpdf(self, htmltopdf_task):
        """
        Ensure HtmlToPdfTask is initialized with the correct tool value.
        """
        assert htmltopdf_task.tool == "htmlpdf", "Tool should be set to 'htmlpdf'"

    def test_default_values(self, htmltopdf_task):
        """
        Ensure HtmlToPdfTask is initialized with the correct default values.
        """
        assert htmltopdf_task.page_orientation == "portrait"
        assert htmltopdf_task.page_margin == 0
        assert htmltopdf_task.view_width == 1920
        assert htmltopdf_task.page_size == "A4"
        assert htmltopdf_task.single_page is False
        assert htmltopdf_task.block_ads is False
        assert htmltopdf_task.remove_popups is False

    @pytest.mark.parametrize("orientation", ["portrait", "landscape"])
    def test_page_orientation_setter_valid(self, htmltopdf_task, orientation):
        htmltopdf_task.page_orientation = orientation
        assert htmltopdf_task.page_orientation == orientation

    @pytest.mark.parametrize(
        "invalid_orientation", ["horizontal", "vertical", "", None, 123]
    )
    def test_page_orientation_setter_invalid(self, htmltopdf_task, invalid_orientation):
        with pytest.raises(ValueError):
            htmltopdf_task.page_orientation = invalid_orientation

    @pytest.mark.parametrize("margin", [0, 10, 50, 100])
    def test_page_margin_setter(self, htmltopdf_task, margin):
        htmltopdf_task.page_margin = margin
        assert htmltopdf_task.page_margin == margin

    @pytest.mark.parametrize("width", [800, 1200, 1920, 2560])
    def test_view_width_setter(self, htmltopdf_task, width):
        htmltopdf_task.view_width = width
        assert htmltopdf_task.view_width == width

    @pytest.mark.parametrize("page_size", ["A3", "A4", "A5", "A6", "Letter", "Auto"])
    def test_page_size_setter_valid(self, htmltopdf_task, page_size):
        htmltopdf_task.page_size = page_size
        assert htmltopdf_task.page_size == page_size

    @pytest.mark.parametrize("invalid_page_size", ["B5", "Legal", "", None, 123])
    def test_page_size_setter_invalid(self, htmltopdf_task, invalid_page_size):
        with pytest.raises(ValueError):
            htmltopdf_task.page_size = invalid_page_size

    @pytest.mark.parametrize("single_page", [True, False])
    def test_single_page_setter(self, htmltopdf_task, single_page):
        htmltopdf_task.single_page = single_page
        assert htmltopdf_task.single_page == single_page

    @pytest.mark.parametrize("block_ads", [True, False])
    def test_block_ads_setter(self, htmltopdf_task, block_ads):
        htmltopdf_task.block_ads = block_ads
        assert htmltopdf_task.block_ads == block_ads

    @pytest.mark.parametrize("remove_popups", [True, False])
    def test_remove_popups_setter(self, htmltopdf_task, remove_popups):
        htmltopdf_task.remove_popups = remove_popups
        assert htmltopdf_task.remove_popups == remove_popups
