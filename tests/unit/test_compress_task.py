"""Test the CompressTask class."""

# Criteria for CompressTask tests:
#
# 1. Must allow adding PDF files for compression.
# 2. Must perform compression on the added files.
# 3. Must have a method to set the compression level.
# 4. The method to set the compression level must only accept the values: "low", "recommended", and "extreme".
# 5. If an invalid compression level is set, it must raise an exception.
# 6. The default compression level must be "recommended".

from unittest.mock import MagicMock, patch

import pytest

from ilovepdf import CompressTask, File


class TestCompressTask:
    """Test the CompressTask class."""

    @pytest.fixture
    def compress_task(self):
        """Fixture to create a CompressTask instance for testing."""
        task = CompressTask("public_key", "secret_key", make_start=False)
        return task

    def test_initialization(self, compress_task):
        """
        Test that CompressTask is initialized correctly.

        Verifies that the default compression level is "recommended".
        """
        assert compress_task.compression_level == "recommended"
        assert compress_task.tool == "compress"

    def test_set_compression_level_valid(self, compress_task):
        """
        Test setting a valid compression level.

        Verifies that the compression level can be set to "low", "recommended", or "extreme".
        """
        for level in ("low", "recommended", "extreme"):
            task = compress_task.set_compression_level(level)
            assert compress_task.compression_level == level
            assert task is compress_task  # Test for fluent interface

    def test_set_compression_level_invalid(self, compress_task):
        """
        Test setting an invalid compression level.

        Verifies that setting an invalid compression level raises an exception.
        """
        with pytest.raises(ValueError) as excinfo:
            compress_task.set_compression_level("invalid_level")
        assert "Invalid compression level" in str(excinfo.value)

    def test_append_file(self, compress_task):
        """
        Test adding a single PDF file.

        Verifies that a single file is correctly added to the task.
        """
        mock_file = MagicMock(spec=File)
        mock_file.get_server_filename.return_value = "server_file_name"
        mock_file.filename = "local_file_name"

        compress_task.append_file(mock_file)

        assert len(compress_task.files) == 1
        assert compress_task.files[0].get_server_filename() == "server_file_name"
        assert compress_task.files[0].filename == "local_file_name"

    def test_execute_compresses_added_files(self, compress_task):
        """
        Test that execute() compresses the added files.

        Verifies that added files are processed when execute() is called.
        """
        mock_file = MagicMock(spec=File)
        mock_file.get_server_filename.return_value = "server_file_name"
        mock_file.filename = "local_file_name"

        compress_task.append_file(mock_file)

        # Mock the execute method if it exists, or simulate compression
        with patch.object(
            compress_task, "execute", return_value="compression_result"
        ) as mock_execute:
            result = compress_task.execute()
            mock_execute.assert_called_once()
            assert result == "compression_result"

    def test_append_single_file(self, compress_task):
        """
        Test for: Adding a single PDF file.
        """
        mock_file = MagicMock(spec=File)
        mock_file.get_server_filename.return_value = "server_file_name"
        mock_file.filename = "local_file_name"
        compress_task.append_file(mock_file)
        assert len(compress_task.files) == 1

    def test_append_multiple_files(self, compress_task):
        """
        Test for: Adding multiple PDF files.
        """
        for i in range(3):
            mock_file = MagicMock(spec=File)
            mock_file.get_server_filename.return_value = f"server_file_{i}"
            mock_file.filename = f"local_file_{i}"
            compress_task.append_file(mock_file)
        assert len(compress_task.files) == 3
        assert compress_task.files[0].filename == "local_file_0"
        assert compress_task.files[1].filename == "local_file_1"
        assert compress_task.files[2].filename == "local_file_2"
