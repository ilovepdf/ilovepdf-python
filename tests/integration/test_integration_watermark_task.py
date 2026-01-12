"""Integration tests for WatermarkTask using the iLovePDF API.

Covers:
- Full workflow: add PDF files, configure watermark options, execute, and download.
- Scenarios for both text and image watermarks.
"""

from ilovepdf import WatermarkTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestWatermarkTaskIntegration(BaseTaskIntegrationTest):
    """Integration tests for WatermarkTask covering text and image use cases."""

    task_class = WatermarkTask

    def test_watermark_single_file_with_text(self):
        """Apply a text watermark to a single PDF file."""

        self.add_sample_file()
        self.task.mode = "text"
        self.task.text = "Confidential"
        self.task.font_size = 24
        self.task.rotation = 45
        self.task.transparency = 60

        self.execute_task()
        self.download_result("sample_watermarked_text.pdf")

    def test_watermark_single_file_with_image(self):
        """Apply an image watermark to a single PDF file."""

        self.add_sample_file()

        img_filename = self.resolve_sample_file_path("sample-img-1.jpg")

        self.task.mode = "image"
        self.task.set_watermark_image(img_filename)
        # self.task.image = image_file["server_filename"]
        self.task.horizontal_position = "right"
        self.task.vertical_position = "top"
        self.task.rotation = 0
        self.task.transparency = 50

        self.execute_task()
        self.download_result("sample_watermarked_image.pdf")
