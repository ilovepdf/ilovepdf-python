"""
This module defines the SplitTask class for handling PDF split operations
with various modes such as ranges, fixed range, remove pages, and filesize.
"""

# pylint: disable=abstract-method

from .task import ProcessTask


class SplitTask(ProcessTask):
    """
    Handles PDF split tasks with flexible split modes and parameters.

    ## Split Extra Parameters

    split modes:
        - 'ranges': Define different ranges of pages.
        - 'fixed_range': Define a fixed range of pages to split the PDF.
        - 'remove_pages': Remove pages from a PDF.
        - 'filesize': Split PDF into multiple files with a maximum filesize per page range.
    """

    def __init__(self, public_key=None, secret_key=None, make_start=True):
        super().__init__(public_key, secret_key, make_start, tool="split")
        self.__extra_params: dict = {}

    def set_ranges(self, ranges: str, merge_after: bool = False):
        """
        Set the page ranges to split the files. Every range will be saved as a different PDF file.

        Parameters
        ----------
        ranges : str
            Example: '1,5,10-14'

        merge_after : bool OPTIONAL
            Merge all ranges after being split.
            Default: False
        """
        if not ranges:
            raise ValueError("split_mode 'ranges' requires the 'ranges' parameter.")

        self.__extra_params = {
            "split_mode": "ranges",
            "ranges": ranges,
            "merge_after": merge_after,
        }
        return self

    def set_fixed_range(self, fixed_range: int = 1):
        """
        Set the page ranges to split the files. Every range will be saved as a different PDF file.

        Parameters
        ----------
        fixed_range : int
            Default: 1
        """

        if not fixed_range:
            raise ValueError(
                "split_mode 'fixed_range' requires the 'fixed_range' parameter."
            )

        self.__extra_params = {
            "split_mode": "fixed_range",
            "fixed_range": fixed_range,
        }
        return self

    def set_remove_pages(self, remove_pages: str):
        """
        Set the pages to remove from a PDF.

        Parameters
        ----------
        remove_pages : str
            Accepted format: '1,4,8-12,16'
        """
        if not remove_pages:
            raise ValueError(
                "split_mode 'remove_pages' requires the 'remove_pages' parameter."
            )

        self.__extra_params = {
            "split_mode": "remove_pages",
            "remove_pages": remove_pages,
        }
        return self

    def set_filesize(self, filesize: int):
        """
        Split PDF into multiple files with a maximum filesize per page range.

        Parameters
        ----------
        filesize : int
            Maximum filesize per split (in bytes).
        """
        if not filesize:
            raise ValueError("split_mode 'filesize' requires the 'filesize' parameter.")
        self.__extra_params = {
            "split_mode": "filesize",
            "filesize": filesize,
        }
        return self

    def set_merge_after(self, merge_after: bool):
        """
        Merge the resulting files after splitting.

        Parameters
        ----------
        merge_after : bool
            Whether to merge the resulting files after splitting.
        """
        self.__extra_params["merge_after"] = merge_after
        return self

    def _to_dict(self):
        """
        Convert the task to a dictionary for use in a request.
        """

        data = dict(super()._to_dict(), **self.__extra_params)
        return data
