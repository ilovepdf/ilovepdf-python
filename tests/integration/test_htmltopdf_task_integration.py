"""
Integration tests for the HtmlToPdfTask module.

This module contains integration tests for converting HTML files to PDF using the iLovePDF API.
"""

import unittest

from ilovepdf import HtmlToPdfTask

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestHtmlToPdfTaskIntegration(BaseIlovePdfTaskTest):
    """
    Integration tests for HtmlToPdfTask using the iLovePDF API.

    Covers:
    - Full workflow: add HTML file from URL, configure options, execute conversion, and download PDF.
    """

    task_class = HtmlToPdfTask

    def test_full_html_to_pdf_flow_from_url(self):
        """
        Test the full flow: add HTML file from URL, configure options, execute conversion, and download PDF.
        """
        # Use a public example URL
        self.task.add_file_from_url("https://www.ilovepdf.com")

        # Configure options for HTML to PDF conversion
        self.task.page_orientation = "landscape"
        self.task.page_margin = 15
        self.task.view_width = 1200
        self.task.page_size = "A4"
        self.task.single_page = False
        self.task.block_ads = True
        self.task.remove_popups = True

        # Execute the task and check the status
        self.execute_task()

        # Download the resulting PDF and verify that the file exists and is not empty
        self.download_result("sample_html_from_url_converted.pdf")


if __name__ == "__main__":
    unittest.main()
