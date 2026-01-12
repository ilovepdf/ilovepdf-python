"""Unit tests for the MergeTask class in the ilovepdf package."""

from unittest.mock import MagicMock

import pytest

from ilovepdf import File, MergeTask


class TestMergeTask:
    """Unit tests for the MergeTask class in the ilovepdf package."""

    @pytest.fixture
    def merge_task(self):
        """Fixture that creates a MergeTask instance for unit testing."""
        task = MergeTask("public_key", "secret_key", make_start=False)
        return task

    def test_initialization_sets_default_values(self, merge_task):
        """
        Ensure MergeTask is initialized with default values.
        The 'tool' attribute should be 'merge'.
        """
        assert merge_task.tool == "merge", "The 'tool' attribute should be 'merge'"

    def test_append_file(self, merge_task):
        """
        Test adding a single PDF file using _append_file.

        Verifies that a single file is correctly added to the task.
        """
        mock_file = MagicMock(spec=File)
        mock_file.get_server_filename.return_value = "server_file_name"
        mock_file.filename = "local_file_name"

        merge_task.append_file(mock_file)

        assert len(merge_task.files) == 1
        assert merge_task.files[0].get_server_filename() == "server_file_name"
        assert merge_task.files[0].filename == "local_file_name"

    def test_append_multiple_files(self, merge_task):
        """
        Test for: Adding multiple PDF files using _append_file.
        """
        for i in range(3):
            mock_file = MagicMock(spec=File)
            mock_file.get_server_filename.return_value = f"server_file_{i}"
            mock_file.filename = f"local_file_{i}"
            merge_task.append_file(mock_file)
        assert len(merge_task.files) == 3
        assert merge_task.files[0].filename == "local_file_0"
        assert merge_task.files[1].filename == "local_file_1"
        assert merge_task.files[2].filename == "local_file_2"
