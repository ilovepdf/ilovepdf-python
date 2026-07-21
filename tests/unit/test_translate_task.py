"""Unit tests for the TranslateTask class in the ilovepdf module.

These tests verify the correct behavior and parameter validation for PDF
translation tasks using TranslateTask.
"""

import pytest

from ilovepdf import TranslateTask
from ilovepdf.exceptions import InvalidChoiceError
from ilovepdf.exceptions.payload_field_errors import MissingPayloadFieldError
from ilovepdf.translate_task import (
    LANGUAGE_CODE_OPTIONS,
)

from .base_test import AbstractUnitTaskTest


class TestTranslateTask(AbstractUnitTaskTest):
    """
    Unit tests for TranslateTask.

    Covers initialization, valid and invalid language_input, language_output
    settings, and parameter validation.
    """

    _task_class = TranslateTask
    _task_tool = "translate"

    def test_initialization_sets_default_values(self, my_task):
        """Ensure TranslateTask starts with expected defaults."""
        assert my_task._DEFAULT_PAYLOAD == {
            "language_input": None,
            "language_output": None,
        }
        assert my_task.language_input is None
        assert my_task.language_output is None

    def test_setters_assign_values_correctly(self, my_task):
        """Confirm setters update and persist supported values."""
        for lang in LANGUAGE_CODE_OPTIONS:
            my_task.language_input = lang
            assert my_task.language_input == lang
            my_task.language_output = lang
            assert my_task.language_output == lang

    def test_invalid_language_input_raises(self, my_task):
        """Validate unsupported language_input values raise InvalidChoiceError."""
        with pytest.raises(InvalidChoiceError) as excinfo:
            my_task.language_input = "invalid_lang"
        assert "language_input" in str(excinfo.value)

    def test_invalid_language_output_raises(self, my_task):
        """Validate unsupported language_output values raise InvalidChoiceError."""
        with pytest.raises(InvalidChoiceError) as excinfo:
            my_task.language_output = "invalid_lang"
        assert "language_output" in str(excinfo.value)

    def test_to_payload_missing_required_fields(self, my_task):
        """Only fields that remain empty are reported as missing."""
        my_task._set_attr("language_input", "")
        with pytest.raises(MissingPayloadFieldError) as excinfo:
            my_task._to_payload()
        missing = excinfo.value.missing_fields
        assert "language_input" in missing
        assert "language_output" in missing
