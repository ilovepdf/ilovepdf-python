"""Unit tests for the PdfMarkdownTask class in the ilovepdf module.

These tests verify the correct behavior and initialization for PDF to Markdown
conversion tasks using PdfMarkdownTask.
"""

from ilovepdf import PdfMarkdownTask

from .base_test import AbstractUnitTaskTest


class TestPdfMarkdownTask(AbstractUnitTaskTest):
    """
    Unit tests for PdfMarkdownTask.

    Covers initialization and default payload configuration.
    """

    _task_class = PdfMarkdownTask
    _task_tool = "pdfmarkdown"

    def test_dummy(self, my_task):
        """
        Verifies that a PdfMarkdownTask instance can be created for test infrastructure
        compliance.

        This test exists to satisfy AbstractUnitTaskTest's requirement for at least one
        unit test method in each task-specific test class.
        """
