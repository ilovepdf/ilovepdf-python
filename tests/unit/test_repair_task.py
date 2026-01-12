"""Unit tests for the RepairTask class from the ilovepdf package.

This module contains pytest-based unit tests for the RepairTask class,
which is part of the ilovepdf package. The tests verify correct
initialization, file addition constraints, dictionary conversion, and
error handling for task state.
"""

import pytest

from ilovepdf import RepairTask


class TestRepairTask:
    """Unit tests for the RepairTask class from the ilovepdf package."""

    @pytest.fixture
    def repair_task(self):
        """Fixture that creates a RepairTask instance for testing."""
        task = RepairTask("public_key", "secret_key", make_start=False)
        # Simulate that the task has already been started
        task.task = "dummy_task_id"
        return task

    def test_initialization_sets_default_values(self, repair_task):
        """
        Ensure RepairTask is initialized with default values.
        """
        assert repair_task.tool == "repair", "Tool should be 'repair'"
        assert repair_task.files == [], "Files list should be empty"

    def test_add_file_allows_only_one_file(self, repair_task, tmp_path):
        """
        Ensure only one file can be added.
        """
        # Create a dummy PDF file
        pdf_file = tmp_path / "file.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%EOF")
        # Patch methods to avoid real operations
        # pylint: disable=protected-access
        repair_task._validate_task_started = lambda: None
        # pylint: enable=protected-access
        repair_task.upload_file = lambda task, file_path, extra_params=None: type(
            "DummyFile",
            (),
            {
                "get_server_filename": lambda self: "server.pdf",
                "filename": "file.pdf",
                "get_file_options": lambda self: {
                    "server_filename": "server.pdf",
                    "filename": "file.pdf",
                },
            },
        )()
        repair_task.add_file(str(pdf_file))
        assert (
            len(repair_task.files) == 1
        ), "There should be one file after adding the first"
        # Trying to add another file should raise ValueError
        with pytest.raises(ValueError):
            repair_task.add_file(str(pdf_file))

    def test_to_dict_includes_files(self, repair_task, tmp_path):
        """
        Ensure that _to_dict includes the files when they are added.
        """
        pdf_file = tmp_path / "file.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%EOF")
        # pylint: disable=protected-access
        repair_task._validate_task_started()
        # pylint: disable=protected-access
        repair_task.upload_file = lambda task, file_path, extra_params=None: type(
            "DummyFile",
            (),
            {
                "get_server_filename": lambda self: "server.pdf",
                "filename": "file.pdf",
                "get_file_options": lambda self: {
                    "server_filename": "server.pdf",
                    "filename": "file.pdf",
                },
            },
        )()
        repair_task.add_file(str(pdf_file))
        task_dict = repair_task._to_dict()  # pylint: disable=protected-access
        assert "files" in task_dict, "The dictionary should include 'files'"
        assert isinstance(task_dict["files"], list), "'files' should be a list"
        assert task_dict["files"][0]["filename"] == "file.pdf"

    def test_add_file_raises_if_task_not_started(self, tmp_path):
        """
        Ensure add_file raises an exception if the task is not started.
        """
        task = RepairTask("public_key", "secret_key", make_start=False)
        pdf_file = tmp_path / "file.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%EOF")
        # task.task is not set, so it should raise an exception
        with pytest.raises(
            Exception, match="Current task does not exist. You must start your task"
        ):
            task.add_file(str(pdf_file))
