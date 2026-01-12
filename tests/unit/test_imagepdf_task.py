"""Unit tests for the ImagePdfTask class."""

import pytest

from ilovepdf import ImagePdfTask


class TestImagePdfTask:
    """Unit tests for the ImagePdfTask class."""

    @pytest.fixture
    def imagepdf_task(self):
        """Fixture that creates an ImagePdfTask instance for testing."""
        task = ImagePdfTask("public_key", "secret_key", make_start=False)
        return task

    def test_initialization_sets_default_values(self, imagepdf_task):
        """
        Ensure ImagePdfTask is initialized with default values.
        """
        assert imagepdf_task.orientation == "portrait"
        assert imagepdf_task.margin == 0
        assert imagepdf_task.pagesize == "fit"
        assert imagepdf_task.merge_after is True
        assert imagepdf_task.tool == "imagepdf"

    def test_setters_assign_values_correctly(self, imagepdf_task):
        """
        Ensure setters assign values correctly and validation works.
        """
        imagepdf_task.orientation = "landscape"
        assert imagepdf_task.orientation == "landscape"

        imagepdf_task.margin = 15
        assert imagepdf_task.margin == 15

        imagepdf_task.pagesize = "A4"
        assert imagepdf_task.pagesize == "A4"

        imagepdf_task.merge_after = False
        assert imagepdf_task.merge_after is False

    def test_invalid_values_raise(self, imagepdf_task):
        """
        Ensure invalid values raise ValueError.
        """
        with pytest.raises(ValueError):
            imagepdf_task.orientation = "diagonal"
        with pytest.raises(ValueError):
            imagepdf_task.margin = -5

        with pytest.raises(ValueError):
            imagepdf_task.pagesize = "B5"

    def test_to_dict_includes_all_params(self, imagepdf_task):
        """
        Ensure _to_dict includes all parameters.
        """
        imagepdf_task.orientation = "landscape"
        imagepdf_task.margin = 5
        imagepdf_task.pagesize = "letter"
        imagepdf_task.merge_after = False

        params = imagepdf_task._to_dict()  # pylint: disable=protected-access
        assert params["orientation"] == "landscape"
        assert params["margin"] == 5
        assert params["pagesize"] == "letter"
        assert params["merge_after"] is False
