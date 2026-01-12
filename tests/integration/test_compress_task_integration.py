"""Integration tests for CompressTask using the iLovePDF API.

Covers:
- Default compression level
- Setting valid and invalid compression levels
- Full compress workflow: add file, set level, execute, download
"""

import unittest

from ilovepdf import CompressTask

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestCompressTaskIntegration(BaseIlovePdfTaskTest):
    """
    Integration tests for CompressTask using the iLovePDF API.

    Covers:
    - Default compression level
    - Setting valid and invalid compression levels
    - Full compress workflow: add file, set level, execute, download
    """

    task_class = CompressTask
    sample_file_path = "sample_2MB.pdf"  # Use the larger sample for compression tests

    def test_default_compression_level(self):
        """Test that the default compression level is 'recommended'."""
        self.assertEqual(self.task.compression_level, "recommended")

    def test_set_compression_level_valid(self):
        """Test setting valid compression levels."""
        for level in ("low", "recommended", "extreme"):
            self.task.set_compression_level(level)
            self.assertEqual(self.task.compression_level, level)

    def test_set_compression_level_invalid(self):
        """Test that setting an invalid compression level raises ValueError."""
        with self.assertRaises(ValueError):
            self.task.set_compression_level("invalid_level")

    def test_full_compress_flow(self):
        """
        Test the full compress flow: add file, set compression level, execute, and download.
        """
        # Add the sample file to the task
        self.add_sample_file()

        # Set a valid compression level
        self.task.set_compression_level("extreme")
        self.assertEqual(self.task.compression_level, "extreme")

        # Execute the task and check status
        self.execute_task()

        # Download the compressed file and verify
        self.download_result("compressed_sample.pdf")


if __name__ == "__main__":
    unittest.main()
