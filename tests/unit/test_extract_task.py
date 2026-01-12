"""Unit tests for the ExtractTask class in the ilovepdf module.

These tests verify the correct behavior and parameter validation for PDF extraction
tasks using ExtractTask.
"""

import pytest

from ilovepdf import ExtractTask
from ilovepdf.exceptions import InvalidChoiceError

from .base_test import AbstractUnitTaskTest


# pylint: disable=protected-access
class TestExtractTask(AbstractUnitTaskTest):
    """Unit tests for the ExtractTask class in the ilovepdf module."""

    _task_class = ExtractTask
    _task_tool = "extract"

    def test_initialization(self, my_task):
        """
        Test that ExtractTask is initialized correctly.

        Verifies that the default detailed is False.
        """

        assert my_task._DEFAULT_PAYLOAD == {"detailed": False}
        assert my_task.detailed is False

    def test_set_detailed_valid(self, my_task):
        """
        Test that detailed can be set to True or False.

        Verifies that detailed is set correctly.
        """
        my_task.detailed = True
        assert my_task.detailed is True

        my_task.detailed = False
        assert my_task.detailed is False

    def test_set_detailed_invalid(self, my_task):
        """
        Test that detailed can only be set to True or False.

        Verifies that detailed is set correctly.
        """
        with pytest.raises(InvalidChoiceError) as excinfo:
            my_task.detailed = "invalid_level"
        assert "detailed" in str(excinfo.value)
        with pytest.raises(InvalidChoiceError) as excinfo:
            my_task.detailed = None
        assert "detailed" in str(excinfo.value)
