"""Integration tests for FormsDetectTask using the iLovePDF API.

Covers:
- Full workflow: add PDF files, execute, and download results.
"""

from ilovepdf import FormsDetectTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestFormsDetectTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for FormsDetectTask using the iLovePDF API.

    Covers:
    - Full workflow: add a PDF file, execute, and download results.
    """

    task_class = FormsDetectTask

    def test_forms_detect_single_file(self):
        """
        Test the full flow: add a single file, execute, and download.
        """
        # Add sample PDF file to the task
        self.add_sample_file("sample-form.pdf")

        # Execute the task and check status
        self.execute_task()

        # Download the result and verify
        self.download_result("forms_detect_result.pdf")
