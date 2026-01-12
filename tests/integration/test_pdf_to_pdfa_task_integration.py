"""Integration tests for PdfToPdfATask using the iLovePDF API.

Covers:
- Full workflow: add file, set PDF/A parameters, execute, and download converted PDF/A.
"""

import unittest

from ilovepdf import PdfToPdfATask

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestPdfToPdfATaskIntegration(BaseIlovePdfTaskTest):
    """
    Integration tests for PdfToPdfATask using the iLovePDF API.

    Covers:
    - Full workflow: add file, set PDF/A parameters, execute, and download converted PDF/A.
    """

    task_class = PdfToPdfATask
    sample_file_path = "sample.pdf"

    def test_full_pdfa_flow(self):
        """
        Test the full flow: add file, set PDF/A parameters, execute, and download.
        """
        # Add the sample file to the task
        self.add_sample_file()

        # Set PDF/A conversion parameters
        self.task.conformance = "pdfa-1b"
        self.task.allow_downgrade = True

        # Execute the task and check status
        self.execute_task()

        # Download the converted PDF/A file and verify
        self.download_result("converted_pdfa.pdf")


if __name__ == "__main__":
    unittest.main()
