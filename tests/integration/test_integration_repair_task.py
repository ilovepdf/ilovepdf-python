"""Integration tests for RepairTask using the iLovePDF API.

These tests verify the complete workflow for repairing corrupted PDF files,
including file upload, task execution, and result download.
"""

from ilovepdf import RepairTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestRepairTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for RepairTask using the iLovePDF API.

    Covers:
        - Single corrupted file repair.
        - Full workflow: add file, execute repair, and download result.
    """

    task_class = RepairTask

    def test_full_repair_flow(self):
        """
        Tests the complete workflow for repairing a corrupted PDF file.

        Steps:
            - Adds a corrupted sample PDF file to the task.
            - Executes the repair task.
            - Downloads the repaired PDF file.

        Asserts:
            - The workflow completes without errors.
            - The repaired file is downloaded successfully.
        """
        # Add the corrupted sample file to the task
        self.add_sample_file("sample_corrupted.pdf")

        # Execute the repair task and check status
        self.execute_task()

        # Download the repaired file and verify
        self.download_result("repaired_sample.pdf")
