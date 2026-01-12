"""
Integration tests for the MergeTask functionality using the iLovePDF API.

This module contains tests that verify the full workflow of merging PDF files,
including adding files, executing the merge, and downloading the merged result.
"""

from ilovepdf import MergeTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestMergeTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for MergeTask using the iLovePDF API.

    Covers:
    - Full workflow: add multiple PDF files, execute merge, and download
        merged PDF.
    """

    task_class = MergeTask

    def test_full_merge_flow(self):
        """
        Test the full flow: add files, execute merge, and download the result.
        """
        # Add two sample PDFs to test merging functionality
        self.add_sample_file("sample.pdf")
        self.add_sample_file("sample-1-2.pdf")

        # Execute the merge task and check status
        self.execute_task()

        # Download the merged file and verify
        self.download_result("merged_sample.pdf")
