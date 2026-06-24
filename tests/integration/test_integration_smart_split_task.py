"""Integration tests for SmartSplitTask using the iLovePDF API.

Covers:
- Full workflow: add a PDF file, set the prompt, execute, and download results.
"""

from ilovepdf import SmartSplitTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestSmartSplitTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for SmartSplitTask using the iLovePDF API.

    Covers:
    - Single file processing with a custom prompt.
    - Full workflow: add file, execute, and download results.
    """

    task_class = SmartSplitTask

    def test_smart_split_single_file(self):
        """Test the full flow: add file, set prompt, execute, and download."""
        # Add the sample PDF file to the task
        self.add_sample_file()

        # Set the prompt to guide the AI split
        self.task.prompt = "Split at chapter boundaries"

        # Execute the task and check status
        self.execute_task()

        # Download the result (a ZIP with the split PDFs) and verify
        self.download_result("smart_split_output.zip")
