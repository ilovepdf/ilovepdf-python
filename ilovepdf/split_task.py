"""
This module defines the SplitTask class for handling PDF split operations
with various modes such as ranges, fixed range, remove pages, and filesize.
"""

from typing import Any, Dict, Literal

from ilovepdf.validators import (
    BoolValidator,
    ChoiceValidator,
    IntValidator,
    StringValidator,
)

from .task import Task

SplitModeType = Literal["ranges", "fixed_range", "remove_pages", "filesize"]
SPLIT_MODE_OPTIONS = {"ranges", "fixed_range", "remove_pages", "filesize"}

# pylint: disable=abstract-method


class SplitTask(Task):
    """
    Handles PDF split tasks with flexible split modes and parameters.

    ## Split Extra Parameters

    split modes:
        - 'ranges': Define different ranges of pages.
        - 'fixed_range': Define a fixed range of pages to split the PDF.
        - 'remove_pages': Remove pages from a PDF.
        - 'filesize': Split PDF into multiple files with a maximum filesize per page
            range.
    """

    _tool = "split"

    _DEFAULT_PAYLOAD = {
        "split_mode": "ranges",
        "merge_after": False,
        "ranges": None,
        "fixed_range": None,
        "remove_pages": None,
        "filesize": None,
    }

    @property
    def split_mode(self) -> SplitModeType:
        """
        Returns the current split mode.
        """
        return self._get_attr("split_mode")

    @split_mode.setter
    def split_mode(self, value: SplitModeType):
        """
        Set the split mode.
        """
        ChoiceValidator.validate(value, SPLIT_MODE_OPTIONS)
        self._set_attr("split_mode", value)

    @property
    def merge_after(self) -> bool:
        """
        Returns True if ranges will be merged after splitting.
        Only available for split_mode 'ranges'.
        """
        self.ensure_split_mode("ranges")
        return self._get_attr("merge_after")

    @merge_after.setter
    def merge_after(self, merge_after: bool):
        """
        Set whether to merge ranges after splitting.
        Only available for split_mode 'ranges'.
        """
        self.ensure_split_mode("ranges")
        BoolValidator.validate(merge_after, "merge_after")
        self._set_attr("merge_after", merge_after)

    # Mode: Ranges
    @property
    def ranges(self) -> str:
        """
        Get the page ranges for splitting.
        Only available for split_mode 'ranges'.
        """
        self.ensure_split_mode("ranges")
        return self._get_attr("ranges")

    @ranges.setter
    def ranges(self, value: str):
        """
        Set the page ranges for splitting.
        Only available for split_mode 'ranges'.
        """
        StringValidator.validate(value, "ranges")
        self.split_mode = "ranges"
        self._set_attr("ranges", value)

    # Mode: Fixed range
    @property
    def fixed_range(self) -> int:
        """
        Get the fixed range for splitting.
        Only available for split_mode 'fixed_range'.
        """
        self.ensure_split_mode("fixed_range")
        return self._get_attr("fixed_range")

    @fixed_range.setter
    def fixed_range(self, value: int):
        """
        Set the fixed range for splitting.
        Only available for split_mode 'fixed_range'.
        """
        IntValidator.validate_positive(value, "fixed_range")
        self.split_mode = "fixed_range"
        self._set_attr("fixed_range", value)

    # Mode: Remove pages
    @property
    def remove_pages(self):
        """
        Get the pages to remove.
        Only available for split_mode 'remove_pages'.
        """
        self.ensure_split_mode("remove_pages")
        return self._get_attr("remove_pages")

    @remove_pages.setter
    def remove_pages(self, value: str):
        """
        Set the pages to remove.
        Only available for split_mode 'remove_pages'.
        """
        StringValidator.validate(value, "remove_pages")
        self.split_mode = "remove_pages"
        self._set_attr("remove_pages", value)

    # Mode: Filesize
    @property
    def filesize(self):
        """
        Get the maximum file size for each split file.
        Only available for split_mode 'filesize'.
        """
        self.ensure_split_mode("filesize")
        return self._get_attr("filesize")

    @filesize.setter
    def filesize(self, value: int):
        """
        Set the maximum file size for each split file.
        Only available for split_mode 'filesize'.
        """
        IntValidator.validate_positive(value, "filesize")
        self.split_mode = "filesize"
        self._set_attr("filesize", value)

    def ensure_split_mode(self, required_mode: SplitModeType):
        """
        Ensure that the split mode is set to the required mode.
        """
        if self.split_mode != required_mode:
            raise ValueError(
                f"The 'split_mode' must be set to '{required_mode}' "
                f"to perform this operation."
            )

    def _to_payload(self) -> Dict[str, Any]:
        """
        Convert the task to a payload dictionary.
        """
        payload = super()._to_payload()
        if self.split_mode == "ranges":
            del payload["fixed_range"]
            del payload["remove_pages"]
            del payload["filesize"]
        elif self.split_mode == "fixed_range":
            del payload["merge_after"]
            del payload["ranges"]
            del payload["remove_pages"]
            del payload["filesize"]
        elif self.split_mode == "remove_pages":
            del payload["merge_after"]
            del payload["ranges"]
            del payload["fixed_range"]
            del payload["filesize"]
        elif self.split_mode == "filesize":
            del payload["merge_after"]
            del payload["ranges"]
            del payload["fixed_range"]
            del payload["remove_pages"]
        return payload
