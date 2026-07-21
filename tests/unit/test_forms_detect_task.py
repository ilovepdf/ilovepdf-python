"""Unit tests for the FormsDetectTask class in the ilovepdf module.

These tests verify the correct behavior and initialization for PDF form
detection tasks using FormsDetectTask.
"""

from ilovepdf import FormsDetectTask

from .base_test import AbstractUnitTaskTest


# pylint: disable=protected-access
class TestFormsDetectTask(AbstractUnitTaskTest):
    """
    Unit tests for FormsDetectTask.

    Covers initialization and default payload configuration.
    """

    _task_class = FormsDetectTask
    _task_tool = "formsdetect"

    def test_initialization_sets_default_values(self, my_task):
        """Ensure FormsDetectTask starts with expected defaults."""
        assert my_task._get_default_payload() == {
            "tool": None,
            "task": None,
            "files": [],
        }
        assert my_task.files == []
