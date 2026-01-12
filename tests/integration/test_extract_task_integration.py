"""Integration tests for ExtractTask using the iLovePDF API.

Covers:
- Full workflow: add file, set extraction parameters, execute, and download extracted text.
"""

import unittest

from ilovepdf import ExtractTask

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestExtractTaskIntegration(BaseIlovePdfTaskTest):
    """
    Integration tests for ExtractTask using the iLovePDF API.

    Covers:
    - Full workflow: add file, set extraction parameters, execute, and download extracted text.
    """

    task_class = ExtractTask
    sample_file_path = "sample.pdf"

    def test_full_extract_flow(self):
        """
        Test the full flow: add file, set extraction parameters, execute, and download.
        """
        # Add the sample file to the task
        self.add_sample_file()

        # Set extraction parameters (e.g., detailed extraction)
        self.task.detailed = True

        # Execute the task and check status
        self.execute_task()

        # Download the extracted text file and verify
        self.download_result("extracted_text.txt")


if __name__ == "__main__":
    unittest.main()
