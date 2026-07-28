"""Integration tests for SummarizeTask using the iLovePDF API.

Covers:
- Full workflow: add PDF files, set parameters, execute, and download results.
"""

from ilovepdf import SummarizeTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestSummarizeTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for SummarizeTask using the iLovePDF API.

    Covers:
    - Full workflow: add a PDF file, set parameters, execute, and download
      results.
    """

    task_class = SummarizeTask

    def test_summarize_single_file_pdf_output(self):
        """
        Test the full flow: add a single file, set PDF output format, execute,
        and download.
        """
        # Add sample PDF file to the task
        self.add_sample_file()

        # Set output format to PDF (default)
        self.task.output_format = "pdf"

        # Execute the task and check status
        self.execute_task()

        # Download the summarized file and verify
        self.download_result("summary_pdf.pdf")

    def test_summarize_single_file_md_output(self):
        """
        Test the full flow: add a single file, set Markdown output format, execute,
        and download.
        """
        # Add sample PDF file to the task
        self.add_sample_file()

        # Set output format to Markdown
        self.task.output_format = "md"
        self.task.language = "en"

        # Execute the task and check status
        self.execute_task()

        # Download the summarized file and verify
        self.download_result("summary_md.md")

    def test_summarize_with_language(self):
        """
        Test the full flow: add a single file, set Spanish language, execute,
        and download.
        """
        # Add sample PDF file to the task
        self.add_sample_file()

        # Set language to Spanish
        self.task.language = "es"

        # Execute the task and check status
        self.execute_task()

        # Download the summarized file and verify
        self.download_result("summary_spanish.pdf")
