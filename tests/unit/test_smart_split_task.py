"""Unit tests for the SmartSplitTask class in the ilovepdf module.

These tests verify the correct behavior and parameter validation for smart
split PDF tasks using SmartSplitTask.
"""

import pytest

from ilovepdf import SmartSplitTask

from .base_test import AbstractUnitTaskTest


# pylint: disable=protected-access
class TestSmartSplitTask(AbstractUnitTaskTest):
    """
    Unit tests for SmartSplitTask.

    Covers initialization, prompt validation, and required-field enforcement.
    """

    _task_class = SmartSplitTask
    _task_tool = "splitsmart"

    def test_initialization_sets_default_values(self, my_task):
        """Ensure SmartSplitTask starts with expected defaults."""
        assert my_task._DEFAULT_PAYLOAD == {"prompt": None}
        assert my_task.prompt is None

    def test_setters_assign_values_correctly(self, my_task):
        """Confirm the prompt setter updates and persists supported values."""
        my_task.prompt = "Split at chapter boundaries"
        assert my_task.prompt == "Split at chapter boundaries"

        my_task.prompt = "Separate each section"
        assert my_task.prompt == "Separate each section"

    def test_invalid_empty_prompt_raises(self, my_task):
        """Validate that an empty prompt raises ValueError."""
        with pytest.raises(ValueError):
            my_task.prompt = ""

    def test_invalid_prompt_type_raises(self, my_task):
        """Validate that non-string prompt values raise TypeError."""
        for invalid in [None, 123, 3.14, [], {}]:
            with pytest.raises(TypeError):
                my_task.prompt = invalid

    def test_missing_required_fields_raises(self, my_task):
        """Validate that a missing prompt raises MissingPayloadFieldError."""
        self.assert_missing_required_fields_raise(my_task, ["prompt"])
