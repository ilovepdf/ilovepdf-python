"""Integration tests for OfficePdfTask using the iLovePDF API.

Covers:
- Full workflow: add Office file, execute conversion, and download resulting PDF.
"""

from ilovepdf import OfficePdfTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestOfficePdfTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for OfficePdfTask using the iLovePDF API.

    Covers:
    - Full workflow: add Office file, execute conversion, and download resulting PDF.
    """

    task_class = OfficePdfTask

    def test_full_office_to_pdf_flow(self):
        """
        Test the full flow: add Office file, execute conversion, and download PDF.
        """
        # Add the Office file to the task
        self.add_sample_file("sample_word.docx")

        # Execute the conversion task and check status
        self.execute_task()

        # Download the converted PDF and verify
        self.download_result("converted_sample.pdf")
