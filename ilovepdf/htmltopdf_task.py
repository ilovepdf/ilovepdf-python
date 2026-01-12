"""Handles HTML to PDF conversion tasks using the iLovePDF API.

Provides the HtmlToPdfTask class to configure and execute HTML to PDF
conversion.
Allows setting options such as page orientation, margin, view width, page size,
and more.
"""

from typing import Literal

from ilovepdf.exceptions.int_errors import IntOutOfRangeError
from ilovepdf.task import Task
from ilovepdf.validators import BoolValidator, ChoiceValidator, IntValidator

PageOrientationType = Literal["portrait", "landscape"]
PAGE_ORIENTATION_OPTIONS = {"portrait", "landscape"}

PageSizeType = Literal["A3", "A4", "A5", "A6", "Letter", "Auto"]
PAGE_SIZE_OPTIONS = {"A3", "A4", "A5", "A6", "Letter", "Auto"}


class HtmlToPdfTask(Task):
    """
    Handles HTML to PDF conversion tasks using the iLovePDF API.

    Args:
        public_key (str, optional): API public key.
            Uses ILOVEPDF_PUBLIC_KEY env variable if not provided.
        secret_key (str, optional): API secret key.
            Uses ILOVEPDF_SECRET_KEY env variable if not provided.
        make_start (bool, optional): Start the task immediately. Default is False.

    Example:
        task = HtmlToPdfTask(public_key="your_public_key", secret_key="your_secret_key")
    """

    _tool = "htmlpdf"

    _DEFAULT_PAYLOAD = {
        "page_orientation": "portrait",
        "page_margin": 0,
        "view_width": 1920,
        "page_size": "A4",
        "single_page": False,
        "block_ads": False,
        "remove_popups": False,
    }

    @property
    def page_orientation(self) -> PageOrientationType:
        """
        Gets the current page orientation. Default is 'portrait'.

        Returns:
            PageOrientationType: The current orientation.
        """
        return self._get_attr("page_orientation")

    @page_orientation.setter
    def page_orientation(self, value: PageOrientationType):
        """
        Sets the page orientation.

        Args:
            value (PageOrientationType): Must be one of PAGE_ORIENTATION_OPTIONS.

        Raises:
            InvalidChoiceError: If the provided value is not valid.
        """
        ChoiceValidator.validate(value, PAGE_ORIENTATION_OPTIONS, "page_orientation")
        self._set_attr("page_orientation", value)

    @property
    def page_margin(self) -> int:
        """
        Gets the current page margin in points. Default is 0.

        Returns:
            int: The current page margin.
        """
        return self._get_attr("page_margin")

    @page_margin.setter
    def page_margin(self, value: int):
        """
        Sets the page margin in points.

        Args:
            value (int): Must be a non-negative integer.

        Raises:
            IntOutOfRangeError: If the value is negative.
        """
        IntValidator.validate_type(value, "page_margin")
        if value < 0:
            raise IntOutOfRangeError("Invalid page_margin: value must be >= 0.")
        self._set_attr("page_margin", value)

    @property
    def view_width(self) -> int:
        """
        Gets the current view width in pixels. Default is 1920.

        Returns:
            int: The current view width.
        """
        return self._get_attr("view_width")

    @view_width.setter
    def view_width(self, value: int):
        """
        Sets the view width in pixels.

        Args:
            value (int): Must be a positive integer.

        Raises:
            IntOutOfRangeError: If the value is not positive.
        """
        IntValidator.validate_positive(value, "view_width")
        self._set_attr("view_width", value)

    @property
    def page_size(self) -> PageSizeType:
        """
        Gets the current page size. Default is 'A4'.

        Returns:
            PageSizeType: The current page size.
        """
        return self._get_attr("page_size")

    @page_size.setter
    def page_size(self, value: PageSizeType):
        """
        Sets the page size.

        Args:
            value (PageSizeType): Must be one of PAGE_SIZE_OPTIONS.

        Raises:
            InvalidChoiceError: If the provided value is not valid.
        """
        ChoiceValidator.validate(value, PAGE_SIZE_OPTIONS, "page_size")
        self._set_attr("page_size", value)

    @property
    def single_page(self) -> bool:
        """
        Gets the single page option. Default is False.

        Returns:
            bool: True if single page mode is enabled.
        """
        return self._get_attr("single_page")

    @single_page.setter
    def single_page(self, value: bool):
        """
        Sets the single page option.

        Args:
            value (bool): Enable or disable single page mode.
        """
        BoolValidator.validate(value)
        self._set_attr("single_page", value)

    @property
    def block_ads(self) -> bool:
        """
        Gets the block ads option. Default is False.

        Returns:
            bool: True if ads are blocked.
        """
        return self._get_attr("block_ads")

    @block_ads.setter
    def block_ads(self, value: bool):
        """
        Sets the block ads option.

        Args:
            value (bool): Enable or disable ad blocking.
        """
        BoolValidator.validate(value)
        self._set_attr("block_ads", value)

    @property
    def remove_popups(self) -> bool:
        """
        Gets the remove popups option. Default is False.

        Returns:
            bool: True if popups are removed.
        """
        return self._get_attr("remove_popups")

    @remove_popups.setter
    def remove_popups(self, value: bool):
        """
        Sets the remove popups option.

        Args:
            value (bool): Enable or disable popup removal.
        """
        BoolValidator.validate(value)
        self._set_attr("remove_popups", value)
