"""Integration tests for RotateTask using the iLovePDF API.

Covers:
- Full workflow: add PDF file, set rotation, execute, and download rotated PDF.
"""

import unittest

from ilovepdf import RotateTask

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestRotateTaskIntegration(BaseIlovePdfTaskTest):
    """
    Integration tests for RotateTask using the iLovePDF API.

    Covers:
    - Full workflow: add PDF file, set rotation, execute, and download rotated PDF.
    """

    task_class = RotateTask
    sample_file_path = "sample.pdf"

    def test_full_rotate_flow(self):
        """
        Test the full flow: add file, set rotation, execute, and download.
        """
        # Add the sample file to the task and set rotation
        file = self.add_sample_file()
        file.set_rotation(90)

        # Execute the rotate task and check status
        self.execute_task()

        # Download the rotated file and verify
        self.download_result("rotated_sample.pdf")


if __name__ == "__main__":
    unittest.main()
