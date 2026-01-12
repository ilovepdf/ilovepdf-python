"""
Module for handling HTML to PDF conversion tasks using the iLovePDF API.

This module defines the HtmlToPdfTask class, which provides methods and properties
to configure and execute the conversion of HTML content to PDF files. Options such as
page orientation, margin, view width, page size, and more can be set for the conversion task.
"""

from .task import ProcessTask

ORIENTATION_VALUES = ("portrait", "landscape")
PAGESIZE_VALUES = ("A3", "A4", "A5", "A6", "Letter", "Auto")


class HtmlToPdfTask(ProcessTask):
    """
    Class to handle the HTML to PDF conversion task using the iLovePDF API.

    This class allows you to configure and execute the conversion of HTML content to PDF files.
    You can set options such as page orientation, margin, view width, page size, and more.
    """

    def __init__(self, public_key=None, secret_key=None, make_start=True):
        """
        Initialize the HtmlToPdfTask.

        Args:
            public_key (Optional[str]): The public API key.
            secret_key (Optional[str]): The secret API key.
            make_start (bool): Whether to start the task immediately.
        """
        super().__init__(public_key, secret_key, make_start, tool="htmlpdf")

    DEFAULTS_VALUES = {
        "page_orientation": "portrait",
        "page_margin": 0,
        "view_width": 1920,
        "page_size": "A4",
        "single_page": False,
        "block_ads": False,
        "remove_popups": False,
    }

    @property
    def page_orientation(self) -> str:
        """
        Get the current page orientation.

        Returns:
            str: The page orientation ("portrait" or "landscape").
        """
        return self._params.get("page_orientation", False)

    @page_orientation.setter
    def page_orientation(self, orientation: str):
        """
        Set the page orientation for the task.

        Args:
            orientation (str): "portrait" or "landscape".

        Raises:
            ValueError: If orientation is not valid.
        """
        if orientation not in ORIENTATION_VALUES:
            raise ValueError("Invalid orientation")
        self._params["page_orientation"] = orientation

    @property
    def page_margin(self) -> int:
        """
        Get the current page margin.

        Returns:
            int: The page margin in points.
        """
        return self._params.get("page_margin", 0)

    @page_margin.setter
    def page_margin(self, margin: int):
        """
        Set the page margin for the task.

        Args:
            margin (int): The page margin in points.
        """
        self._params["page_margin"] = margin

    @property
    def view_width(self) -> int:
        """
        Get the current view width.

        Returns:
            int: The view width in pixels.
        """
        return self._params.get("view_width", self.DEFAULTS_VALUES["view_width"])

    @view_width.setter
    def view_width(self, width: int):
        """
        Set the view width for the task.

        Args:
            width (int): The view width in pixels.
        """
        self._params["view_width"] = width

    @property
    def page_size(self) -> str:
        """
        Get the current page size.

        Returns:
            str: The page size (e.g., "A4").
        """
        return self._params.get("page_size", self.DEFAULTS_VALUES["page_size"])

    @page_size.setter
    def page_size(self, page_size: str):
        """
        Set the page size for the task.

        Args:
            page_size (str): The page size (e.g., "A4").
        """
        if page_size not in PAGESIZE_VALUES:
            raise ValueError("Invalid page size")
        self._params["page_size"] = page_size

    @property
    def single_page(self) -> bool:
        """
        Get the single page option.

        Returns:
            bool: True if single page mode is enabled, False otherwise.
        """
        return self._params.get("single_page", self.DEFAULTS_VALUES["single_page"])

    @single_page.setter
    def single_page(self, single_page: bool):
        """
        Set the single page option.

        Args:
            single_page (bool): Enable or disable single page mode.
        """
        self._params["single_page"] = single_page

    @property
    def block_ads(self) -> bool:
        """
        Get the block ads option.

        Returns:
            bool: True if ads are blocked, False otherwise.
        """
        return self._params.get("block_ads", self.DEFAULTS_VALUES["block_ads"])

    @block_ads.setter
    def block_ads(self, block_ads: bool):
        """
        Set the block ads option.

        Args:
            block_ads (bool): Enable or disable ad blocking.
        """
        self._params["block_ads"] = block_ads

    @property
    def remove_popups(self) -> bool:
        """
        Get the remove popups option.

        Returns:
            bool: True if popups are removed, False otherwise.
        """
        return self._params.get("remove_popups", self.DEFAULTS_VALUES["remove_popups"])

    @remove_popups.setter
    def remove_popups(self, remove_popups: bool):
        """
        Set the remove popups option.

        Args:
            remove_popups (bool): Enable or disable popup removal.
        """
        self._params["remove_popups"] = remove_popups
