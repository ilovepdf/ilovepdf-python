"""
Integration tests for ImagePdfTask using the iLovePDF API.

Covers:
- Complete workflow: add image file(s), configure task options, execute conversion,
download and verify resulting PDF(s).
"""

from ilovepdf import ImagePdfTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestImagePdfTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for ImagePdfTask using the iLovePDF API.

    Covers:
    - Full workflow: add image file, set parameters, execute, and download result.
    """

    task_class = ImagePdfTask

    def test_full_image_to_pdf_flow(self):
        """
        Test full image to PDF workflow: add image, set parameters, execute, download
        and verify.
        """
        self.add_sample_file("sample-img-1.jpg")
        self.task.orientation = "landscape"
        self.task.margin = 5
        self.task.pagesize = "A4"
        self.task.merge_after = True
        self.execute_task()
        self.download_result("converted_image.pdf")

    def test_multiple_images_merged(self):
        """
        Test merging multiple images into a single PDF.
        """
        self.add_sample_file("sample-img-1.jpg")
        self.add_sample_file("sample-img-2.png")
        self.task.orientation = "portrait"
        self.task.margin = 0
        self.task.pagesize = "fit"
        self.task.merge_after = True
        self.execute_task()
        self.download_result("merged_images.pdf")
