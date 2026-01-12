"""Unit tests for the RotateTask class in the ilovepdf module."""

from unittest.mock import patch

import pytest

from ilovepdf import File, RotateTask


class TestRotateTask:
    """Unit tests for the RotateTask class."""

    @pytest.fixture
    def rotate_task(self):
        """Fixture that creates a RotateTask instance for testing."""
        task = RotateTask("public_key", "secret_key", make_start=False)
        return task

    def test_initialization_sets_default_values(self, rotate_task):
        """
        Ensure RotateTask is initialized with default values.
        Checks that the default rotation is None and the tool is set to 'rotate'.
        """
        assert rotate_task.tool == "rotate", "Tool should be set to 'rotate'"

    def test_add_file_returns_file_with_set_rotation(self, rotate_task):
        dummy_file = File("server_filename.pdf", "sample.pdf")
        rotate_task.task = "dummy_task_id"
        with patch.object(rotate_task, "upload_file", return_value=dummy_file):
            file = rotate_task.add_file("sample.pdf")
            assert hasattr(file, "set_rotation")
            file.set_rotation(90)
            assert file.rotate == 90

    @pytest.mark.parametrize("angle", [90, 180, 270])
    def test_set_rotation_valid_angles(self, rotate_task, angle):
        dummy_file = File("server_filename.pdf", "sample.pdf")
        rotate_task.task = "dummy_task_id"
        with patch.object(rotate_task, "upload_file", return_value=dummy_file):
            file = rotate_task.add_file("sample.pdf")
            file.set_rotation(angle)
            assert file.rotate == angle

    @pytest.mark.parametrize("invalid_angle", [-90, 45, 100, 360, None, "90"])
    def test_set_rotation_invalid_angles(self, rotate_task, invalid_angle):
        dummy_file = File("server_filename.pdf", "sample.pdf")
        rotate_task.task = "dummy_task_id"
        with patch.object(rotate_task, "upload_file", return_value=dummy_file):
            file = rotate_task.add_file("sample.pdf")
            with pytest.raises(ValueError):
                file.set_rotation(invalid_angle)

    def test_execute_and_download_are_called(self, rotate_task):
        dummy_file = File("server_filename.pdf", "sample.pdf")
        rotate_task.task = "dummy_task_id"
        with (
            patch.object(rotate_task, "upload_file", return_value=dummy_file),
            patch.object(rotate_task, "execute", return_value=None) as mock_execute,
            patch.object(
                rotate_task, "set_output_filename", return_value=None
            ) as mock_set_output,
            patch.object(rotate_task, "download", return_value=None) as mock_download,
        ):
            file = rotate_task.add_file("sample.pdf")
            file.set_rotation(180)
            rotate_task.execute()
            rotate_task.set_output_filename("document_rotated.pdf")
            rotate_task.download()
            mock_execute.assert_called_once()
            mock_set_output.assert_called_once_with("document_rotated.pdf")
            mock_download.assert_called_once()
            assert file.rotate == 180
