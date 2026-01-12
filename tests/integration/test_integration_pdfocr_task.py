"""Integration test for PdfOcrTask using the iLovePDF API.

This test covers the full OCR workflow:
- Setting OCR languages
- Adding a scanned PDF file
- Executing the OCR process
- Downloading and verifying the output file
"""

from ilovepdf import PdfOcrTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestPdfOcrTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration test for PdfOcrTask using the iLovePDF API.

    This test covers the full OCR workflow:
    - Setting OCR languages
    - Adding a scanned PDF file
    - Executing the OCR process
    - Downloading and verifying the output file
    """

    task_class = PdfOcrTask
    sample_file_path = "pdf_sample_scanned.pdf"

    def test_full_pdfocr_flow(self):
        """
        Test the full flow: set languages, add file, process, and download OCR result.
        """
        # Add the sample file to the task
        file_sample = self.add_sample_file()

        # Set OCR languages
        file_sample.ocr_languages = ["spa", "eng"]

        # Execute the task and check status
        self.execute_task()

        # Download the OCR result
        self.download_result("pdf_sample_scanned_ocr.pdf")
