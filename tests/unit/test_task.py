"""Unit tests for the Task class in the ilovepdf module.

Covers file extension validation logic, including edge cases and custom extension lists.
"""

import pytest

from ilovepdf import File
from ilovepdf.exceptions import FileExtensionNotAllowed
from ilovepdf.task import Task

from .base_test import AbstractUnitTaskTest

# pylint: disable=protected-access


class DummyTask(Task):
    """Generic task class for testing."""

    _tool = "nametool"
    _task_status = "some_status"


class TestDummyTask(AbstractUnitTaskTest):
    """Test class for DummyTask."""

    _task_class = DummyTask
    _task_tool = "nametool"

    def test_initialization_sets_expected_values(self, my_task):
        """
        Should initialize with correct default payload and properties.
        """
        expected_default_payload = {"tool": None, "task": None, "files": []}
        expected_payload = {"tool": "nametool", "task": None, "files": []}
        assert my_task._DEFAULT_PAYLOAD == expected_default_payload
        assert my_task._to_payload() == expected_payload
        assert my_task.tool == "nametool"
        assert my_task._task_status == "some_status"
        assert my_task.files == []

    @pytest.mark.parametrize("tool_name", ["othertool", "anothertool"])
    def test_tool_setter_updates_payload(self, my_task, tool_name):
        """
        Should update tool property and payload when set.
        """
        my_task.tool = tool_name
        assert my_task.tool == my_task._to_payload()["tool"] == tool_name

    @pytest.mark.parametrize("task_value", ["task_123", "task_abc"])
    def test_set_task_updates_payload(self, my_task, task_value):
        """
        Should update task property and payload when set_task is called.
        """
        my_task.set_task(task_value)
        assert my_task.task == my_task._to_payload()["task"] == task_value

    # Tests for validate extensions
    def test_accepts_valid_image_extensions(self, my_task):
        """Should accept standard image extensions."""
        for ext in [".pdf"]:
            my_task._validate_file_extension(f"file{ext}")

    def test_accepts_uppercase_image_extensions(self, my_task):
        """Should accept uppercase image extensions."""
        for ext in [".PDF"]:
            my_task._validate_file_extension(f"file{ext}")

    def test_rejects_invalid_extension(self, my_task):
        """Should raise ValueError for non-image extensions."""
        with pytest.raises(FileExtensionNotAllowed):
            my_task._validate_file_extension("file.txt")

    def test_rejects_file_without_extension(self, my_task):
        """Should raise ValueError for files without extension."""
        with pytest.raises(ValueError):
            my_task._validate_file_extension("file")

    def test_rejects_file_with_double_extension(self, my_task):
        """Should reject files with valid extension followed by invalid one."""
        with pytest.raises(ValueError):
            my_task._validate_file_extension("file.jpg.txt")

    def test_accepts_custom_extension_list(self, my_task):
        """Should accept only extensions in a custom list."""
        # Only .abc is allowed
        my_task._validate_file_extension("file.abc", extension_list=["abc"])
        with pytest.raises(ValueError):
            my_task._validate_file_extension("file.jpg", extension_list=["abc"])

    def test_error_message_lists_allowed_extensions(self, my_task):
        """Error message should list allowed extensions."""
        allowed = ["jpg", "png"]
        with pytest.raises(ValueError) as excinfo:
            my_task._validate_file_extension("file.txt", extension_list=allowed)
        for ext in allowed:
            assert f".{ext}" in str(excinfo.value)

    def test_append_file(self, my_task):
        """Should append a file to the task."""
        file1 = File(server_filename="srv1", filename="file1.pdf")
        file2 = File(server_filename="srv2", filename="file2.pdf")
        file3 = File(server_filename="srv3", filename="file3.pdf")
        res_file1 = my_task.append_file(file1)
        res_file2 = my_task.append_file(file2)
        res_file3 = my_task.append_file(file3)
        assert file1 is res_file1
        assert file2 is res_file2
        assert file3 is res_file3

        assert my_task._to_payload()["files"] == [
            file1._to_payload(),
            file2._to_payload(),
            file3._to_payload(),
        ]
