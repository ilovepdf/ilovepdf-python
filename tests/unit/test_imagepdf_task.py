"""Unit tests for the ImagePdfTask class in the ilovepdf module.

These tests verify correct behavior and parameter validation for image-to-PDF conversion
tasks using ImagePdfTask.
"""

import pytest

from ilovepdf import ImagePdfTask
from ilovepdf.exceptions import FileExtensionNotAllowed, InvalidChoiceError
from ilovepdf.exceptions.int_errors import IntOutOfRangeError, NotAnIntError
from tests.unit.base_test import AbstractUnitTaskTest


# pylint: disable=protected-access
class TestImagePdfTask(AbstractUnitTaskTest):
    """
    Unit tests for the ImagePdfTask class.
    """

    _task_class = ImagePdfTask
    _task_tool = "imagepdf"

    def test_initialization_sets_default_values(self, my_task):
        """
        Ensure ImagePdfTask is initialized with expected default values.
        """
        assert my_task.get_extension_list() == [
            "jpg",
            "jpeg",
            "png",
            "gif",
            "bmp",
            "tiff",
            "tif",
            "webp",
        ]
        assert my_task._DEFAULT_PAYLOAD == {
            "orientation": "portrait",
            "margin": 0,
            "rotate": 0,
            "pagesize": "fit",
            "merge_after": True,
        }
        assert my_task.orientation == "portrait"
        assert my_task.margin == 0
        assert my_task.rotate == 0
        assert my_task.pagesize == "fit"
        assert my_task.merge_after is True
        assert my_task.tool == "imagepdf"

    @pytest.mark.parametrize(
        "file_path",
        [
            "image.jpg",
            "photo.jpeg",
            "picture.png",
            "animation.gif",
            "bitmap.bmp",
            "scan.tiff",
            "document.tif",
            "graphic.webp",
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

    @pytest.mark.parametrize("orientation", ["portrait", "landscape"])
    def test_orientation_setter_valid(self, my_task, orientation):
        """Test setting a valid orientation."""
        my_task.orientation = orientation
        assert my_task.orientation == orientation

    @pytest.mark.parametrize("invalid_orientation", ["diagonal", "", None, 123])
    def test_orientation_setter_invalid(self, my_task, invalid_orientation):
        """Test setting an invalid orientation."""
        with pytest.raises(InvalidChoiceError):
            my_task.orientation = invalid_orientation

    @pytest.mark.parametrize("value", [0, 10, 100])
    def test_margin_setter_valid(self, my_task, value):
        """Test setting a valid margin."""
        my_task.margin = value
        assert my_task.margin == value

    @pytest.mark.parametrize("invalid_margin", [-1, -10])
    def test_margin_setter_negative(self, my_task, invalid_margin):
        """Test setting an invalid margin."""
        with pytest.raises(IntOutOfRangeError):
            my_task.margin = invalid_margin

    @pytest.mark.parametrize("invalid_margin", ["foo", None])
    def test_margin_setter_invalid(self, my_task, invalid_margin):
        """Test setting an invalid margin."""
        with pytest.raises(NotAnIntError):
            my_task.margin = invalid_margin

    @pytest.mark.parametrize("rotate", [0, 90, 180, 270])
    def test_rotate_setter_valid(self, my_task, rotate):
        """Test setting a valid rotation."""
        my_task.rotate = rotate
        assert my_task.rotate == rotate

    @pytest.mark.parametrize("invalid_rotate", [45, 360, "ninety", None])
    def test_rotate_setter_invalid(self, my_task, invalid_rotate):
        """Test setting an invalid rotation."""
        with pytest.raises(InvalidChoiceError):
            my_task.rotate = invalid_rotate

    @pytest.mark.parametrize("pagesize", ["fit", "A4", "letter"])
    def test_pagesize_setter_valid(self, my_task, pagesize):
        """Test setting a valid pagesize."""
        my_task.pagesize = pagesize
        assert my_task.pagesize == pagesize

    @pytest.mark.parametrize("invalid_pagesize", ["B5", "", None, 123])
    def test_pagesize_setter_invalid(self, my_task, invalid_pagesize):
        """Test setting an invalid pagesize."""
        with pytest.raises(InvalidChoiceError):
            my_task.pagesize = invalid_pagesize

    @pytest.mark.parametrize("merge_after", [True, False])
    def test_merge_after_setter(self, my_task, merge_after):
        """Test setting a valid merge_after."""
        my_task.merge_after = merge_after
        assert my_task.merge_after == merge_after

    def test_to_payload_includes_all_params(self, my_task):
        """Test that the payload includes all parameters."""
        my_task.orientation = "landscape"
        my_task.margin = 5
        my_task.rotate = 90
        my_task.pagesize = "letter"
        my_task.merge_after = False

        params = my_task._to_payload()
        assert params["orientation"] == "landscape"
        assert params["margin"] == 5
        assert params["rotate"] == 90
        assert params["pagesize"] == "letter"
        assert params["merge_after"] is False
