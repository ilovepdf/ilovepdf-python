"""Integration tests for PdfMarkdownTask using the iLovePDF API.

Covers:
- Full workflow: add a PDF file, execute, and download the Markdown result.
"""

from ilovepdf import PdfMarkdownTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestPdfMarkdownTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for PdfMarkdownTask using the iLovePDF API.

    Covers:
    - Single PDF file conversion to Markdown.
    - Full workflow: add file, execute, and download result.
    """

    task_class = PdfMarkdownTask

    def test_pdfmarkdown_single_file(self):
        """Test the full flow: add file, execute, and download."""
        # Add the sample PDF file to the task
        self.add_sample_file("sample.pdf")

        # Execute the conversion task
        self.execute_task()

        # Download the Markdown result and verify
        self.download_result("result.md")
