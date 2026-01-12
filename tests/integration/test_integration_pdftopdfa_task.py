"""Integration tests for PdfToPdfATask using the iLovePDF API.

This module validates the end-to-end PDF to PDF/A conversion workflow,
including adding a file, configuring parameters, executing the task, and
retrieving the converted document.
"""

from ilovepdf import PdfToPdfATask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestPdfToPdfATaskIntegration(BaseTaskIntegrationTest[PdfToPdfATask]):
    """Integration tests for PdfToPdfATask using the iLovePDF API.

    Covers:
        - Add a PDF sample file to the task.
        - Configure PDF/A conformance parameters.
        - Execute the conversion workflow.
        - Download the converted PDF/A document.
    """

    task_class = PdfToPdfATask

    def test_full_pdfa_flow(self) -> None:
        """Runs the full PDF/A conversion flow from upload to download."""
        self.add_sample_file()

        self.task.conformance = "pdfa-1b"
        self.task.allow_downgrade = True

        self.execute_task()

        self.download_result("converted_pdfa.pdf")
