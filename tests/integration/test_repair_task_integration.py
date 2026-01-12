"""Integration tests for RepairTask using the iLovePDF API.

Covers:
- Full workflow: add corrupted PDF file, execute repair, and download repaired PDF.
"""

import unittest

from ilovepdf import RepairTask

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestRepairTaskIntegration(BaseIlovePdfTaskTest):
    """
    Integration tests for RepairTask using the iLovePDF API.

    Covers:
    - Full workflow: add corrupted PDF file, execute repair, and download repaired PDF.
    """

    task_class = RepairTask
    sample_file_path = "sample_corrupted.pdf"

    def test_full_repair_flow(self):
        """
        Test the full flow: add corrupted file, execute repair, and download.
        """
        # Add the corrupted sample file to the task
        self.add_sample_file()

        # Execute the repair task and check status
        self.execute_task()

        # Download the repaired file and verify
        self.download_result("repaired_sample.pdf")


if __name__ == "__main__":
    unittest.main()
