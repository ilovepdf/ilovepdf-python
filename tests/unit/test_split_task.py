"""Test the SplitTask class."""

import pytest

from ilovepdf import SplitTask
from ilovepdf.exceptions import InvalidChoiceError
from ilovepdf.split_task import SPLIT_MODE_OPTIONS

from .base_test import AbstractUnitTaskTest


# pylint: disable=protected-access
class TestSplitTask(AbstractUnitTaskTest):
    """Test the SplitTask class."""

    _task_class = SplitTask
    _task_tool = "split"

    def test_initialization(self, my_task):
        """
        Test that SplitTask is initialized correctly.

        Verifies that the default split_mode is "ranges".
        """
        assert SPLIT_MODE_OPTIONS == {
            "ranges",
            "fixed_range",
            "remove_pages",
            "filesize",
        }
        assert my_task.split_mode == "ranges"

    @pytest.mark.parametrize("value", SPLIT_MODE_OPTIONS)
    def test_set_split_mode_level_valid(self, my_task, value):
        """
        Test that setting a valid split_mode level works as expected.

        Verifies that the split_mode is updated correctly.
        """
        my_task.split_mode = value
        assert my_task.split_mode == value

    @pytest.mark.parametrize("value", ["invalid_mode", None, ""])
    def test_set_split_mode_level_invalid(self, my_task, value):
        """
        Test that setting an invalid split_mode level raises an error.

        Verifies that the split_mode is not updated and an error is raised.
        """
        with pytest.raises(ValueError):
            my_task.split_mode = value

    @pytest.mark.parametrize("value", [True, False])
    def test_set_merge_after_valid(self, my_task, value):
        """
        Test that setting a valid merge_after value works as expected.

        Verifies that the merge_after is updated correctly.
        """
        my_task.split_mode = "ranges"
        my_task.merge_after = value
        assert my_task.merge_after == value

    @pytest.mark.parametrize("value", ["True", "False", None, "", 0, 1])
    def test_set_merge_after_invalid(self, my_task, value):
        """
        Test that setting an invalid merge_after value raises an error.

        Verifies that the merge_after is not updated and an error is raised.
        """
        my_task.split_mode = "ranges"
        with pytest.raises(InvalidChoiceError):
            my_task.merge_after = value

        my_task.split_mode = "ranges"
        with pytest.raises(InvalidChoiceError):
            my_task.merge_after = value

    def test_split_mode_updates_on_attr_set(self, my_task):
        """Test split_mode changes when setting related attributes."""
        my_task._set_attr("split_mode", "other_mode")

        # Ranges mode
        my_task.ranges = "1-10"
        assert my_task.split_mode == "ranges"
        assert my_task.ranges == "1-10"
        payload = my_task._to_payload()

        assert "ranges" in payload
        assert "merge_after" in payload
        assert "fixed_range" not in payload
        assert "remove_pages" not in payload
        assert "filesize" not in payload

        # Fixed range mode
        my_task._set_attr("split_mode", "other_mode")
        my_task.fixed_range = 1
        assert my_task.split_mode == "fixed_range"
        assert my_task.fixed_range == 1
        payload = my_task._to_payload()
        assert "fixed_range" in payload
        assert "ranges" not in payload
        assert "merge_after" not in payload
        assert "remove_pages" not in payload
        assert "filesize" not in payload

        # Remove pages mode
        my_task._set_attr("split_mode", "other_mode")
        my_task.remove_pages = "1,2,3"
        assert my_task.split_mode == "remove_pages"
        assert my_task.remove_pages == "1,2,3"
        payload = my_task._to_payload()

        assert "remove_pages" in payload
        assert "ranges" not in payload
        assert "merge_after" not in payload
        assert "fixed_range" not in payload
        assert "filesize" not in payload

        # Filesize mode
        my_task._set_attr("split_mode", "other_mode")
        my_task.filesize = 1024
        assert my_task.split_mode == "filesize"
        assert my_task.filesize == 1024
        payload = my_task._to_payload()
        assert "filesize" in payload
        assert "ranges" not in payload
        assert "merge_after" not in payload
        assert "fixed_range" not in payload
        assert "remove_pages" not in payload

    def test_accessors_require_correct_split_mode(self, my_task):
        """Ensure attributes raise ValueError if split_mode is not correct."""
        my_task._set_attr("split_mode", "other_mode")

        with pytest.raises(ValueError, match="must be set to 'ranges'"):
            _ = my_task.merge_after
        with pytest.raises(ValueError, match="must be set to 'ranges'"):
            my_task.merge_after = "some_value"

        with pytest.raises(ValueError, match="must be set to 'ranges'"):
            _ = my_task.ranges

        with pytest.raises(ValueError, match="must be set to 'fixed_range'"):
            _ = my_task.fixed_range

        with pytest.raises(ValueError, match="must be set to 'remove_pages'"):
            _ = my_task.remove_pages

        with pytest.raises(ValueError, match="must be set to 'filesize'"):
            _ = my_task.filesize

    def test_ranges_setter_invalid(self, my_task):
        """Test that ranges setter rejects invalid values."""
        my_task.split_mode = "ranges"
        with pytest.raises(ValueError):
            my_task.ranges = ""
        for invalid in [None, 123, 3.14, [], {}]:
            with pytest.raises(TypeError):
                my_task.ranges = invalid

    def test_remove_pages_setter_invalid(self, my_task):
        """Test that remove_pages setter rejects invalid values."""
        my_task.split_mode = "remove_pages"
        with pytest.raises(ValueError):
            my_task.remove_pages = ""
        for invalid in [None, 123, 3.14, [], {}]:
            with pytest.raises(TypeError):
                my_task.remove_pages = invalid

    def test_fixed_range_setter_invalid(self, my_task):
        """Test that fixed_range setter rejects invalid values."""
        my_task.split_mode = "fixed_range"
        for invalid in [0, -1, -10]:
            with pytest.raises(ValueError):
                my_task.fixed_range = invalid
        for invalid in [None, "10", 3.14, [], {}]:
            with pytest.raises(TypeError):
                my_task.fixed_range = invalid

    def test_filesize_setter_invalid(self, my_task):
        """Test that filesize setter rejects invalid values."""
        my_task.split_mode = "filesize"
        for invalid in [0, -1, -100]:
            with pytest.raises(ValueError):
                my_task.filesize = invalid
        for invalid in [None, "2048", 3.14, [], {}]:
            with pytest.raises(TypeError):
                my_task.filesize = invalid
