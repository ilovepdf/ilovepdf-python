"""Unit tests for the SummarizeTask class in the ilovepdf module.

These tests verify the correct behavior and parameter validation for PDF
summarization tasks using SummarizeTask.
"""

import pytest

from ilovepdf import SummarizeTask
from ilovepdf.exceptions import InvalidChoiceError
from ilovepdf.summarize_task import LANGUAGE_OPTIONS, OUTPUT_FORMAT_OPTIONS

from .base_test import AbstractUnitTaskTest


# pylint: disable=protected-access
class TestSummarizeTask(AbstractUnitTaskTest):
    """
    Unit tests for SummarizeTask.

    Covers initialization, valid and invalid language and output_format
    settings, and parameter validation.
    """

    _task_class = SummarizeTask
    _task_tool = "summarize"

    def test_initialization_sets_default_values(self, my_task):
        """Ensure SummarizeTask starts with expected defaults."""
        assert my_task._DEFAULT_PAYLOAD == {
            "language": "en",
            "output_format": "pdf",
        }
        assert my_task.language == "en"
        assert my_task.output_format == "pdf"

    def test_setters_assign_values_correctly(self, my_task):
        """Confirm setters update and persist supported values."""
        for lang in LANGUAGE_OPTIONS:
            my_task.language = lang
            assert my_task.language == lang
        for fmt in OUTPUT_FORMAT_OPTIONS:
            my_task.output_format = fmt
            assert my_task.output_format == fmt

    def test_invalid_language_raises(self, my_task):
        """Validate unsupported language values raise InvalidChoiceError."""
        with pytest.raises(InvalidChoiceError) as excinfo:
            my_task.language = "invalid_lang"
        assert "language" in str(excinfo.value)

    def test_invalid_output_format_raises(self, my_task):
        """Validate unsupported output_format values raise InvalidChoiceError."""
        with pytest.raises(InvalidChoiceError) as excinfo:
            my_task.output_format = "docx"
        assert "output_format" in str(excinfo.value)
