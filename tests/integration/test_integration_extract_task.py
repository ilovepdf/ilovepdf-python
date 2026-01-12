"""Integration tests for ExtractTask using the iLovePDF API.

Covers:
- Full workflow: add file, set extraction parameters, execute, and download extracted
    text.
"""

from ilovepdf import ExtractTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestExtractTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for ExtractTask using the iLovePDF API.

    Covers:
    - Full workflow: add file, set extraction parameters, execute, and download
        extracted text.
    """

    task_class = ExtractTask

    def test_full_extract_flow(self):
        """
        Test the full flow: add file, set extraction parameters, execute, and download.
        """
        # Add the sample file to the task
        self.add_sample_file()

        # Execute the task and check status
        self.execute_task()

        # Download the extracted text file and verify
        self.download_result("extracted_text.txt")

    def test_full_extract_detailed_flow(self):
        """
        Test the full flow: add file, set extraction parameters, execute, and download.
        """
        # Add the sample file to the task
        self.add_sample_file()

        # Set extraction parameters (e.g., detailed extraction)
        self.task.detailed = True

        # Execute the task and check status
        self.execute_task()

        # Download the extracted text file and verify
        self.download_result("extracted_text_detailed.txt")
