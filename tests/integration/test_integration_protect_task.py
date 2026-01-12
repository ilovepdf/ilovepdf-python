"""Integration tests for ProtectTask using the iLovePDF API.

Covers:
    - Full workflow: add file, set password, execute, and download protected PDF.
"""

from ilovepdf import ProtectTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestProtectTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for ProtectTask using the iLovePDF API.

    Covers:
        - Single file protection with password.
        - Full workflow: add file, set password, execute, and download protected PDF.
    """

    task_class = ProtectTask

    def test_full_protect_flow(self):
        """
        Tests the complete ProtectTask workflow.

        Steps:
            - Add a sample file to the task.
            - Set a password for protection.
            - Execute the task.
            - Download the protected PDF.

        Asserts:
            - The protected file is downloaded successfully.
        """
        # Add the sample file for protection workflow
        self.add_sample_file()

        # Set password for PDF encryption
        self.task.password = "integrationTest123"

        # Execute the task and check status
        self.execute_task()

        # Download the protected file and verify
        self.download_result("protected_sample.pdf")
