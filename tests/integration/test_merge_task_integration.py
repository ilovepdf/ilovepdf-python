"""
Integration tests for the MergeTask functionality using the iLovePDF API.

This module contains tests that verify the full workflow of merging PDF files,
including adding files, executing the merge, and downloading the merged result.
"""

import os
import unittest

from ilovepdf import MergeTask

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestMergeTaskIntegration(BaseIlovePdfTaskTest):
    """
    Integration tests for MergeTask using the iLovePDF API.

    Covers:
    - Full workflow: add multiple PDF files, execute merge, and download merged PDF.
    """

    task_class = MergeTask

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Define two sample files for merging
        cls.sample_file_path_1 = "sample.pdf"
        cls.sample_file_path_2 = "sample-1-2.pdf"
        # Ensure both files exist in the sample folder
        cls.sample_file_path_1 = os.path.join(
            cls.folder_sample_path, cls.sample_file_path_1
        )
        cls.sample_file_path_2 = os.path.join(
            cls.folder_sample_path, cls.sample_file_path_2
        )
        if not (
            os.path.exists(cls.sample_file_path_1)
            and os.path.exists(cls.sample_file_path_2)
        ):
            raise unittest.SkipTest(
                f"Sample files not found at {cls.sample_file_path_1} and/or {cls.sample_file_path_2}"
            )

    def test_full_merge_flow(self):
        """
        Test the full flow: add files, execute merge, and download the result.
        """
        # Add both sample files to the merge task
        self.task.add_file(self.sample_file_path_1)
        self.task.add_file(self.sample_file_path_2)

        # Execute the merge task and check status
        self.execute_task()

        # Download the merged file and verify
        output_filename = "merged_sample.pdf"
        self.download_result(output_filename)


if __name__ == "__main__":
    unittest.main()
