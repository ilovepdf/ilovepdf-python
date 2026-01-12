"""Integration tests for CompressTask using the iLovePDF API.

Covers:
- Full workflow: add PDF files, set parameters, execute, and download results.
"""

from ilovepdf import CompressTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestCompressTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for CompressTask using the iLovePDF API.

    Covers:
    - Full workflow: add PDF files, set parameters, execute, and download
      results.
    """

    task_class = CompressTask

    def test_compress_single_file_flow(self):
        """
        Test the full flow: add a single file, set low compression level, execute,
        and download.
        """
        # Add sample PDF file to the task
        self.add_sample_file()

        # Set compression level
        self.task.compression_level = "low"

        # Execute the task and check status
        self.execute_task()

        # Download the compressed file and verify
        self.download_result("compressed_low.pdf")

    def test_compress_multiple_files_extreme(self):
        """
        Test the full flow: add multiple files, set extreme compression level, execute,
        and download.
        """
        # Add sample PDF files to the task
        self.add_sample_file()
        self.add_sample_file()

        # Set compression level
        self.task.compression_level = "extreme"

        # Execute the task and check status
        self.execute_task()

        # Download the compressed files and verify
        self.download_result("compressed_extreme.zip")
