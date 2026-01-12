"""Integration tests for SplitTask using the iLovePDF API.

Covers:
- Splitting by specific ranges
- Splitting by fixed range
- Removing specific pages
- Splitting by maximum filesize per part
"""

from ilovepdf import SplitTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestSplitTaskIntegration(BaseTaskIntegrationTest):
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

    def split_and_download(self, configure_task, output_file):
        """
        Helper to add sample file, configure task, execute, and download.
        """
        self.add_sample_file()
        configure_task()
        self.execute_task()
        self.download_result(output_file)

    def test_split_by_ranges(self):
        """
        Test splitting a PDF by specific ranges and downloading the result.
        """

        def configure():
            self.task.ranges = "1,2-3"
            self.task.merge_after = False

        self.split_and_download(configure, "split_range.pdf")

    def test_split_by_fixed_range(self):
        """
        Test splitting a PDF by fixed range and downloading the result.
        """

        def configure():
            self.task.fixed_range = 1  # Split every page into a separate file

        self.split_and_download(configure, "split_fixed.pdf")

    def test_remove_pages_and_split(self):
        """
        Test removing specific pages from a PDF and downloading the result.
        """

        def configure():
            self.task.remove_pages = "2"  # Remove page 2

        self.split_and_download(configure, "split_removed_pages.pdf")

    def test_split_by_filesize(self):
        """
        Test splitting a PDF by maximum filesize per part and downloading the result.
        """

        def configure():
            self.task.filesize = 50 * 1024  # 50 KB to force splitting

        self.split_and_download(configure, "split_filesize.pdf")
