"""Unit tests for the OfficePdfTask class."""

from unittest.mock import patch

import pytest

from ilovepdf import OfficePdfTask
from ilovepdf.task import ProcessTask


class TestOfficePdfTask:
    """Unit tests for the OfficePdfTask class."""

    @pytest.fixture
    def office_pdf_task(self):
        """Fixture that creates an OfficePdfTask instance for testing."""
        task = OfficePdfTask("public_key", "secret_key", make_start=False)
        return task

    def test_initialization_sets_default_values(self, office_pdf_task):
        """
        Ensure OfficePdfTask is initialized with default values.
        """
        assert office_pdf_task.tool == "officepdf", "Tool should be set to 'officepdf'"

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
        self, office_pdf_task, file_path, tmp_path
    ):
        """
        Ensure valid Office and OpenDocument extensions are accepted.
        """
        # Create a simulated temporary file
        temp_file = tmp_path / file_path
        temp_file.write_text("dummy content")
        # Should not raise exception
        # pylint: disable=protected-access
        office_pdf_task._validate_file_extension(str(temp_file))
        # pylint: enable=protected-access

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
        self, office_pdf_task, file_path, tmp_path
    ):
        """
        Ensure invalid extensions are rejected.
        """
        temp_file = tmp_path / file_path
        temp_file.write_text("dummy content")
        with pytest.raises(
            ValueError, match="Only Office and OpenDocument files are supported"
        ):
            # pylint: disable=protected-access
            office_pdf_task._validate_file_extension(str(temp_file))
            # pylint: enable=protected-access

    def test_add_file_allows_only_one_file(self, office_pdf_task, tmp_path):
        """
        Ensure that only one file can be added to OfficePdfTask.
        """
        valid_file = tmp_path / "document.docx"
        valid_file.write_text("dummy content")
        office_pdf_task.files = [str(valid_file)]
        another_file = tmp_path / "presentation.pptx"
        another_file.write_text("dummy content")
        with patch.object(ProcessTask, "add_file", return_value=None):
            with pytest.raises(
                ValueError, match="OfficePdfTask can only handle one file at a time."
            ):
                office_pdf_task.add_file(str(another_file))
