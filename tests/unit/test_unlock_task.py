"""Unit tests for the UnlockTask class from ilovepdf.

This module contains tests to verify the correct behavior of UnlockTask,
including initialization and file validation logic.
"""

from ilovepdf import UnlockTask

from .base_test import AbstractUnitTaskTest


# pylint: disable=protected-access
class TestUnlockTask(AbstractUnitTaskTest):
    """Unit tests for the UnlockTask class from ilovepdf."""

    _task_class = UnlockTask
    _task_tool = "unlock"

    def test_dummy(self, my_task):
        """
        Verifies that a UnlockTask instance can be created for test infrastructure
        compliance.

        This test exists to satisfy AbstractUnitTaskTest's requirement for at least one
        unit test method in each task-specific test class.
        """
