"""Unit tests for the RepairTask class in the ilovepdf module.

These tests verify correct initialization, file addition constraints,
and error handling for RepairTask.
"""

from ilovepdf import RepairTask

from .base_test import AbstractUnitTaskTest


# pylint: disable=protected-access
class TestRepairTask(AbstractUnitTaskTest):
    """
    Unit tests for RepairTask.

    Covers initialization, file addition constraints, and error handling.
    """

    _task_class = RepairTask
    _task_tool = "repair"

    def test_initialization_sets_default_values(self, my_task):
        """
        Ensures RepairTask is initialized with default values.

        Asserts:
            - The files list is empty upon initialization.
        """
        assert my_task.files == [], "Files list should be empty"

    def test_add_file_allows_only_one_file(self, my_task, tmp_path):
        """
        Ensures only one file can be added to the RepairTask.

        Raises:
            ValueError: When attempting to add more than one file.
        """
        # Create a dummy PDF file
        pdf_file = tmp_path / "file.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%EOF")
        my_task.append_file(str(pdf_file))

        # Create another dummy PDF file
        other_pdf_file = tmp_path / "file2.pdf"
        other_pdf_file.write_bytes(b"%PDF-1.4\n%EOF")
