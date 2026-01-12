"""Integration tests for ImagePdfTask using the iLovePDF API.

Covers:
- Full workflow: add image file, set parameters, execute, and download PDF.
"""

import unittest

from ilovepdf import ImagePdfTask

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestImagePdfTaskIntegration(BaseIlovePdfTaskTest):
    """
    Integration tests for ImagePdfTask using the iLovePDF API.

    Covers:
    - Full workflow: add image file, set parameters, execute, and download PDF.
    """

    task_class = ImagePdfTask
    sample_file_path = "sample.jpg"

    def test_full_imagepdf_flow(self):
        """
        Test the full flow: add image, set parameters, execute, and download.
        """
        # Add the sample image file to the task
        self.add_sample_file()

        # Set parameters for PDF conversion
        self.task.orientation = "portrait"
        self.task.margin = 10
        self.task.pagesize = "A4"
        self.task.merge_after = True

        # Execute the task and check status
        self.execute_task()

        # Download the converted PDF and verify
        self.download_result("converted_image.pdf")


if __name__ == "__main__":
    unittest.main()
