"""Integration tests for ProtectTask using the iLovePDF API.

Covers:
- Full workflow: add file, set password, execute, and download protected PDF.
"""

import unittest

from ilovepdf import ProtectTask

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestProtectTaskIntegration(BaseIlovePdfTaskTest):
    """
    Integration tests for ProtectTask using the iLovePDF API.

    Covers:
    - Full workflow: add file, set password, execute, and download protected PDF.
    """

    task_class = ProtectTask
    sample_file_path = "sample.pdf"

    def test_full_protect_flow(self):
        """
        Test the full flow: add file, set password, execute, and download.
        """
        # Add the sample file to the task
        self.add_sample_file()

        # Set a password for protection
        self.task.set_password("integrationTest123")

        # Execute the task and check status
        self.execute_task()

        # Download the protected file and verify
        self.download_result("protected_sample.pdf")


if __name__ == "__main__":
    unittest.main()
