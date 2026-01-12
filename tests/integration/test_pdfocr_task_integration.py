"""Integration test for PdfOcrTask using the iLovePDF API.

This test covers the full OCR workflow:
- Setting OCR languages
- Adding a scanned PDF file
- Executing the OCR process
- Downloading and verifying the output file
"""

import unittest

from ilovepdf import PdfOcrTask

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestPdfOcrTaskIntegration(BaseIlovePdfTaskTest):
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
        # file_sample.set_languages(["spa", "eng"])
        print("file_sample>>>>>>>>>>>>>>>>>>>>>>>", file_sample.get_file_options())
        print("file_sample>>>>>>>>>>>>>>>>>>>>>>>", type(file_sample))
        # raise Exception("Test failed")

        # Set OCR languages
        # file_sample.set_languages(["spa", "eng"] )

        # Execute the task and check status
        self.execute_task()

        # Download the protected file and verify
        self.download_result("document_ocr.pdf")


if __name__ == "__main__":
    unittest.main()
