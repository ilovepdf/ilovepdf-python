"""Unit tests for the MergeTask class in the ilovepdf package."""

from ilovepdf import MergeTask

from .base_test import AbstractUnitTaskTest


class TestMergeTask(AbstractUnitTaskTest):
    """Unit tests for the MergeTask class in the ilovepdf package."""

    _task_class = MergeTask
    _task_tool = "merge"

    def test_dummy(self, my_task):
        """
        Verifies that a MergeTask instance can be created for test infrastructure
        compliance.

        This test exists to satisfy AbstractUnitTaskTest's requirement for at least one
        unit test method in each task-specific test class.
        """
