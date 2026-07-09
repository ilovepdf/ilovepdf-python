"""Integration tests for TranslateTask using the iLovePDF API.

Covers:
- Full workflow: add a PDF file, set parameters, execute, and download results.
"""

from ilovepdf import TranslateTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestTranslateTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for TranslateTask using the iLovePDF API.

    Covers:
    - Full workflow: add a PDF file, set parameters, execute, and download
      results.
    """

    task_class = TranslateTask

    def test_translate_single_file_pdf_output(self):
        """
        Test the full flow: add a single file, set input and output languages,
        execute, and download.
        """
        self.add_sample_file()

        self.task.language_input = "eng"
        self.task.language_output = "spa"

        self.execute_task()
        self.download_result("translate_spanish.pdf")
