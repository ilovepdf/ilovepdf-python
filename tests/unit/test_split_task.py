"""Test the SplitTask class."""

import pytest

from ilovepdf import SplitTask


class TestSplitTask:
    """Test the SplitTask class."""

    @pytest.fixture
    def split_task(self):
        task = SplitTask("public_key", "secret_key", make_start=False)
        return task

    def test_set_ranges_valid(self, split_task):
        split_task.set_ranges("1,3,5-7", merge_after=True)
        task_dict = split_task._to_dict()  # pylint: disable=protected-access
        assert task_dict["split_mode"] == "ranges"
        assert task_dict["ranges"] == "1,3,5-7"
        assert task_dict["merge_after"] is True

    def test_set_ranges_invalid(self, split_task):
        with pytest.raises(ValueError):
            split_task.set_ranges("", merge_after=False)

    def test_set_fixed_range_default(self, split_task):
        split_task.set_fixed_range()
        task_dict = split_task._to_dict()  # pylint: disable=protected-access
        assert task_dict["split_mode"] == "fixed_range"
        assert task_dict["fixed_range"] == 1
        assert "merge_after" not in task_dict

    def test_set_fixed_range_custom(self, split_task):
        split_task.set_fixed_range(5)
        task_dict = split_task._to_dict()  # pylint: disable=protected-access
        assert task_dict["split_mode"] == "fixed_range"
        assert task_dict["fixed_range"] == 5
        assert "merge_after" not in task_dict

    def test_set_fixed_range_invalid(self, split_task):
        with pytest.raises(ValueError):
            split_task.set_fixed_range(0)

    def test_set_remove_pages_valid(self, split_task):
        split_task.set_remove_pages("2,4,6-8")
        task_dict = split_task._to_dict()  # pylint: disable=protected-access
        assert task_dict["split_mode"] == "remove_pages"
        assert task_dict["remove_pages"] == "2,4,6-8"

    def test_set_remove_pages_invalid(self, split_task):
        with pytest.raises(ValueError):
            split_task.set_remove_pages("")

    def test_set_filesize_valid(self, split_task):
        split_task.set_filesize(1048576)
        task_dict = split_task._to_dict()  # pylint: disable=protected-access
        assert task_dict["split_mode"] == "filesize"
        assert task_dict["filesize"] == 1048576

    def test_set_filesize_invalid(self, split_task):
        with pytest.raises(ValueError):
            split_task.set_filesize(0)
