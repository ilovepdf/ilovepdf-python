"""
Integration tests for HtmlToPdfTask using the iLovePDF API.

Covers:
- Complete workflow: add HTML from a public URL, configure task options, execute
conversion, download and verify the resulting PDF.
"""

from ilovepdf import HtmlToPdfTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestHtmlToPdfTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for HtmlToPdfTask using the iLovePDF API.

    Covers:
    - Full workflow: adding HTML from URL, setting options, executing
        conversion, and downloading result.
    """

    task_class = HtmlToPdfTask

    def test_full_html_to_pdf_flow_from_url(self):
        """
        Test the full workflow: add HTML file from public URL, set conversion options,
            execute, and download result.
        """
        self.task.add_file_from_url("https://www.ilovepdf.com")

        # Configure HTML to PDF options
        self.task.page_orientation = "landscape"
        self.task.page_margin = 15
        self.task.view_width = 1200
        self.task.page_size = "A4"
        self.task.single_page = False
        self.task.block_ads = True
        self.task.remove_popups = True

        # Execute conversion and download
        self.execute_task()
        self.download_result("sample_html_from_url_converted.pdf")
