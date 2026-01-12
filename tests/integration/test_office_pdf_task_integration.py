"""Integration tests for OfficePdfTask using the iLovePDF API.

Covers:
- Full workflow: add Office file, execute conversion, and download resulting PDF.
"""

import unittest

from ilovepdf import OfficePdfTask

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestOfficePdfTaskIntegration(BaseIlovePdfTaskTest):
    """
    Integration tests for OfficePdfTask using the iLovePDF API.

    Covers:
    - Full workflow: add Office file, execute conversion, and download resulting PDF.
    """

    task_class = OfficePdfTask
    sample_file_path = "sample_word.docx"

    def test_full_office_to_pdf_flow(self):
        """
        Test the full flow: add Office file, execute conversion, and download PDF.
        """
        # Add the Office file to the task
        self.add_sample_file()

        # Execute the conversion task and check status
        self.execute_task()

        # Download the converted PDF and verify
        output_file = "converted_sample.pdf"
        self.download_result(output_file)


if __name__ == "__main__":
    unittest.main()
