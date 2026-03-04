"""Integration tests for PageNumbersTask using the iLovePDF API.

Covers:
- Full workflow: add PDF file, set page numbering parameters, execute, and download
    results.
"""

from ilovepdf import PageNumbersTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestPageNumbersTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for PageNumbersTask using the iLovePDF API.

    Covers:
    - Single file page numbering with various positions and formats.
    - Custom font, color, and transparency options.
    - Full workflow: add PDF file, set parameters, execute, and download results.
    """

    task_class = PageNumbersTask

    def test_add_page_numbers_basic(self):
        """
        Test full flow: add PDF file, set default page numbers, execute, and download.
        """
        self.add_sample_file("sample.pdf")
        self.task.execute()
        self.download_result("sample_pagenumbers_basic.pdf")

    def test_add_page_numbers_custom_format_and_position(self):
        """
        Test adding page numbers with custom format and position.
        """
        self.add_sample_file("sample.pdf")
        self.task.position = "top_right"
        self.task.format = "Page {page_number} of {total_pages}"
        self.task.font_size = 16
        self.task.font_color = "#3366FF"
        self.task.transparency = 80
        self.task.layer = "below"
        self.task.show_on_cover = True
        self.task.execute()
        self.download_result("sample_pagenumbers_custom.pdf")

    def test_add_page_numbers_with_font_and_style(self):
        """
        Test adding page numbers with custom font family and style.
        """
        self.add_sample_file("sample.pdf")
        self.task.font_family = "Verdana"
        self.task.font_style = "Bold"
        self.task.position = "bottom_left"
        self.task.start_number = 5
        self.task.execute()
        self.download_result("sample_pagenumbers_fontstyle.pdf")
