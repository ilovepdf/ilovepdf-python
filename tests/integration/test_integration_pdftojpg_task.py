"""Integration tests for PdfToJpgTask using the iLovePDF API.

Covers:
- Full workflow: add PDF file, set conversion mode, execute, download, and verify
    results.
"""

from ilovepdf import PdfToJpgTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestPdfToJpgTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for PdfToJpgTask using the iLovePDF API.

    Covers:
    - Single PDF conversion in 'pages' mode.
    - Single PDF conversion in 'extract' mode.
    - Full workflow: add PDF file, set parameters, execute, download, and verify.
    """

    task_class = PdfToJpgTask

    def test_pdf_to_jpg_pages_mode(self):
        """
        Tests PDF to JPG conversion in 'pages' mode.

        Workflow:
        - Add sample PDF file.
        - Set conversion mode to 'pages' (each page becomes a JPG).
        - Execute the task.
        - Download the resulting ZIP file.
        """
        self.add_sample_file("sample.pdf")
        self.task.pdfjpg_mode = "pages"
        self.execute_task()
        self.download_result("pdftojpgtask_mode_pages.zip")

    def test_pdf_to_jpg_extract_mode(self):
        """
        Tests PDF to JPG conversion in 'extract' mode.

        Workflow:
        - Add sample PDF file.
        - Set conversion mode to 'extract' (extracts embedded images).
        - Execute the task.
        - Download the resulting ZIP file.
        """
        self.add_sample_file("sample.pdf")
        self.task.pdfjpg_mode = "extract"
        self.execute_task()
        self.download_result("pdftojpgtask_mode_extract.zip")
