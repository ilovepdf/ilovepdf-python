"""Integration tests for SplitTask using the iLovePDF API.

Covers:
- Splitting by specific ranges
- Splitting by fixed range
- Removing specific pages
- Splitting by maximum filesize per part
"""

import unittest

from ilovepdf import SplitTask

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestSplitTaskIntegration(BaseIlovePdfTaskTest):
    """
    Integration tests for SplitTask using the iLovePDF API.

    Covers:
    - Splitting by specific ranges
    - Splitting by fixed range
    - Removing specific pages
    - Splitting by maximum filesize per part
    """

    task_class = SplitTask
    sample_file_path = "sample.pdf"

    def split_and_download(self, set_split_method, output_file, *args, **kwargs):
        """
        Helper to add sample file, set split method, execute, and download.
        """
        self.add_sample_file()
        set_split_method(*args, **kwargs)
        self.execute_task()
        self.download_result(output_file)

    def test_set_ranges_and_split(self):
        """
        Test splitting a PDF by specific ranges and downloading the result.
        """
        self.split_and_download(
            self.task.set_ranges, "split_range.pdf", "1,2-3", merge_after=False
        )

    def test_set_fixed_range_and_split(self):
        """
        Test splitting a PDF by fixed range and downloading the result.
        """
        self.split_and_download(
            self.task.set_fixed_range,
            "split_fixed.pdf",
            1,  # Split every page into a separate file
        )

    def test_set_remove_pages_and_split(self):
        """
        Test removing specific pages from a PDF and downloading the result.
        """
        self.split_and_download(
            self.task.set_remove_pages, "split_removed_pages.pdf", "2"  # Remove page 2
        )

    def test_set_filesize_and_split(self):
        """
        Test splitting a PDF by maximum filesize per part and downloading the result.
        """
        self.split_and_download(
            self.task.set_filesize,
            "split_filesize.pdf",
            50 * 1024,  # 50 KB to force splitting
        )


if __name__ == "__main__":
    unittest.main()
