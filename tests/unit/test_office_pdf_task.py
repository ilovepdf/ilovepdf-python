"""Unit tests for the OfficePdfTask class."""

import pytest

from ilovepdf import OfficePdfTask
from ilovepdf.exceptions import FileExtensionNotAllowed, TooManyFilesError

from .base_test import AbstractUnitTaskTest


# pylint: disable=protected-access
class TestOfficePdfTask(AbstractUnitTaskTest):
    """Unit tests for the OfficePdfTask class."""

    _task_class = OfficePdfTask
    _task_tool = "officepdf"

    def test_initialization_sets_default_values(self, my_task):
        """
        Ensure OfficePdfTask is initialized with default values.
        """
        assert my_task.get_extension_list() == [
            "doc",
            "docx",
            "ppt",
            "pptx",
            "xls",
            "xlsx",
            "odt",
            "odp",
            "ods",
        ]

    @pytest.mark.parametrize(
        "file_path",
        [
            "document.doc",
            "presentation.pptx",
            "spreadsheet.xlsx",
            "notes.odt",
            "slides.odp",
            "data.ods",
            "report.DOCX",
            "summary.PPT",
            "table.XLS",
        ],
    )
    def test_validate_file_extension_accepts_valid_extensions(
        self,
        my_task,
        file_path,
        tmp_path,
    ):
        """
        Ensure valid Office and OpenDocument extensions are accepted.
        """
        # Create a simulated temporary file
        temp_file = tmp_path / file_path
        temp_file.write_text("dummy content")
        my_task._validate_file_extension(str(temp_file))

    @pytest.mark.parametrize(
        "file_path",
        [
            "image.jpg",
            "archive.zip",
            "script.py",
            "document.pdf",
            "audio.mp3",
            "video.mp4",
            "file.txt",
        ],
    )
    def test_validate_file_extension_rejects_invalid_extensions(
        self, my_task, file_path, tmp_path
    ):
        """
        Ensure invalid extensions are rejected.
        """
        temp_file = tmp_path / file_path
        temp_file.write_text("dummy content")
        with pytest.raises(FileExtensionNotAllowed):
            my_task._validate_file_extension(str(temp_file))

    def test_add_file_allows_only_one_file(self, my_task, tmp_path):
        """
        Ensure that only one file can be added to OfficePdfTask.
        """
        valid_file = tmp_path / "document.docx"
        valid_file.write_text("dummy content")
        my_task.append_file(str(valid_file))

        another_file = tmp_path / "presentation.pptx"
        another_file.write_text("dummy content")

        with pytest.raises(TooManyFilesError):
            my_task.append_file(str(another_file))
