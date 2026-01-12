"""Integration tests for RotateTask using the iLovePDF API.

Covers:
- Full workflow: add image file, set rotation, execute, and download rotated image.
"""

from ilovepdf.rotate_task import RotateTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestRotateTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for RotateTask using the iLovePDF API.

    Covers:
    - Full workflow: add image file, set rotation, execute, and download rotated image.
    """

    task_class: type[RotateTask] = RotateTask

    def test_rotate_single_file_flow(self):
        """
        Test the full flow: add file, set rotation, execute, and download.
        """
        # Add the sample file and set rotation to 90 degrees for landscape output
        file = self.add_sample_file()
        file.rotate = 90

        # Execute the rotate task and check status
        self.execute_task()

        # Download the rotated file and verify
        self.download_result("rotated_sample.pdf")

    def test_rotate_multiple_files_flow(self):
        """
        Test the full flow: add multiple files, set rotation, execute, and download.
        """
        # Add two sample files and set different rotations to verify batch processing
        file1 = self.add_sample_file()
        file1.rotate = 90
        file2 = self.add_sample_file()
        file2.rotate = 180

        # Execute the rotate task and check status
        self.execute_task()

        # Download the rotated file and verify
        self.download_result("rotated_sample.zip")
