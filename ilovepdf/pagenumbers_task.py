"""Handles adding page numbers to PDF files using the iLovePDF API.

Provides the PageNumbersTask class to configure and execute page numbering,
including position, format, typography, and appearance options.
"""

from typing import Literal

from ilovepdf.task import Task
from ilovepdf.validators import (
    BoolValidator,
    ChoiceValidator,
    IntValidator,
    StringValidator,
)

from .helpers import (
    FONT_FAMILY_OPTIONS,
    FONT_STYLE_OPTIONS,
    LAYER_OPTIONS,
    FontFamilyType,
    FontStyleType,
    LayerType,
)

# Type aliases and allowed value sets
PageNumberPositionType = Literal[
    "top_left",
    "top_center",
    "top_right",
    "bottom_left",
    "bottom_center",
    "bottom_right",
]
PAGE_NUMBER_POSITION_OPTIONS = {
    "top_left",
    "top_center",
    "top_right",
    "bottom_left",
    "bottom_center",
    "bottom_right",
}


class PageNumbersTask(Task):
    """Configure and execute page numbering tasks using the iLovePDF API.

    PageNumbersTask allows adding page numbers to PDF files with customizable
    position, format, typography, color, and appearance.

    Args:
        public_key (str | None): API public key. Uses ``ILOVEPDF_PUBLIC_KEY`` when
            omitted.
        secret_key (str | None): API secret key. Uses ``ILOVEPDF_SECRET_KEY`` when
            omitted.
        make_start (bool): Whether to start the task immediately. Default is False.

    Example:
        task = PageNumbersTask(public_key="your_public_key",
            secret_key="your_secret_key")
        task.add_file("/path/to/document.pdf")
        task.position = "bottom_center"
        task.format = "Page {page_number} of {total_pages}"
        task.font_size = 12
        task.font_color = "#FF0000"
        task.execute()
        task.download("/path/to/output.pdf")
    """

    _tool = "pagenumber"

    _DEFAULT_PAYLOAD = {
        "position": "bottom_center",
        "format": "{page_number}",
        "start_number": 1,
        "font_family": "Arial Unicode MS",
        "font_style": None,
        "font_size": 12,
        "font_color": "#000000",
        "transparency": 100,
        "layer": "above",
        "pages": "all",
        "show_on_cover": False,
    }

    allowed_extensions = ["pdf"]

    @property
    def position(self) -> PageNumberPositionType:
        """
        Gets the position of the page number. Default is "bottom_center".

        Returns:
            PageNumberPositionType: The current position.
        """
        return self._get_attr("position")

    @position.setter
    def position(self, value: PageNumberPositionType) -> None:
        """
        Sets the position of the page number.

        Args:
            value (PageNumberPositionType): Must be one of PAGE_NUMBER_POSITION_OPTIONS.

        Raises:
            ValueError: If the provided value is not valid.
        """
        ChoiceValidator.validate(value, PAGE_NUMBER_POSITION_OPTIONS, "position")
        self._set_attr("position", value)

    @property
    def format(self) -> str:
        """
        Gets the format string for page numbers. Default is "{page_number}".

        Returns:
            str: The current format string.
        """
        return self._get_attr("format")

    @format.setter
    def format(self, value: str) -> None:
        """
        Sets the format string for page numbers.

        Args:
            value (str): Must be a non-empty string. Supports placeholders:
                {page_number}, {total_pages}.

        Raises:
            TypeError: If value is not a string.
            ValueError: If value is an empty string.
        """
        StringValidator.validate(value, "format")
        self._set_attr("format", value)

    @property
    def start_number(self) -> int:
        """
        Gets the starting page number. Default is 1.

        Returns:
            int: The starting page number.
        """
        return self._get_attr("start_number")

    @start_number.setter
    def start_number(self, value: int) -> None:
        """
        Sets the starting page number.

        Args:
            value (int): Must be a positive integer.

        Raises:
            IntOutOfRangeError: If the provided value is not a positive integer.
        """
        IntValidator.validate_positive(value, "start_number")
        self._set_attr("start_number", value)

    @property
    def font_family(self) -> FontFamilyType:
        """
        Gets the font family. Default is "Arial Unicode MS".

        Returns:
            FontFamilyType: The current font family.
        """
        return self._get_attr("font_family")

    @font_family.setter
    def font_family(self, value: FontFamilyType) -> None:
        """
        Sets the font family.

        Args:
            value (FontFamilyType): Must be one of FONT_FAMILY_OPTIONS.

        Raises:
            InvalidChoiceError: If the provided value is not valid.
        """
        ChoiceValidator.validate(value, FONT_FAMILY_OPTIONS, "font_family")
        self._set_attr("font_family", value)

    @property
    def font_style(self) -> FontStyleType:
        """
        Gets the font style. Default is None.

        Returns:
            FontStyleType: The current font style.
        """
        return self._get_attr("font_style")

    @font_style.setter
    def font_style(self, value: FontStyleType) -> None:
        """
        Sets the font style.

        Args:
            value (FontStyleType): Must be one of FONT_STYLE_OPTIONS.

        Raises:
            InvalidChoiceError: If the provided value is not valid.
        """
        ChoiceValidator.validate(value, FONT_STYLE_OPTIONS, "font_style")
        self._set_attr("font_style", value)

    @property
    def font_size(self) -> int:
        """
        Gets the font size in points. Default is 12.

        Returns:
            int: The font size.
        """
        return self._get_attr("font_size")

    @font_size.setter
    def font_size(self, value: int) -> None:
        """
        Sets the font size in points.

        Args:
            value (int): Must be between 6 and 72 inclusive.

        Raises:
            IntOutOfRangeError: If the provided value is not in range.
        """
        IntValidator.validate_range(value, 6, 72, "font_size")
        self._set_attr("font_size", value)

    @property
    def font_color(self) -> str:
        """
        Gets the font color in hexadecimal format. Default is "#000000".

        Returns:
            str: The font color.
        """
        return self._get_attr("font_color")

    @font_color.setter
    def font_color(self, value: str) -> None:
        """
        Sets the font color in hexadecimal format.

        Args:
            value (str): Must be a valid non-empty string.

        Raises:
            TypeError: If value is not a string.
            ValueError: If value is an empty string.
        """
        StringValidator.validate(value, "font_color")
        self._set_attr("font_color", value)

    @property
    def transparency(self) -> int:
        """
        Gets the transparency percentage. Default is 100.

        Returns:
            int: The transparency percentage.
        """
        return self._get_attr("transparency")

    @transparency.setter
    def transparency(self, value: int) -> None:
        """
        Sets the transparency percentage.

        Args:
            value (int): Must be between 1 and 100 inclusive.

        Raises:
            IntOutOfRangeError: If the provided value is not in range.
        """
        IntValidator.validate_range(value, 1, 100, "transparency")
        self._set_attr("transparency", value)

    @property
    def layer(self) -> LayerType:
        """
        Gets the layer setting. Default is "above".

        Returns:
            LayerType: The current layer setting.
        """
        return self._get_attr("layer")

    @layer.setter
    def layer(self, value: LayerType) -> None:
        """
        Sets the layer setting.

        Args:
            value (LayerType): Must be one of LAYER_OPTIONS.

        Raises:
            InvalidChoiceError: If the provided value is not valid.
        """
        ChoiceValidator.validate(value, LAYER_OPTIONS, "layer")
        self._set_attr("layer", value)

    @property
    def pages(self) -> str:
        """
        Gets the page selection string. Default is "all".

        Returns:
            str: The page selection string.
        """
        return self._get_attr("pages")

    @pages.setter
    def pages(self, value: str) -> None:
        """
        Sets the page selection string.

        Args:
            value (str): Page selection expression (e.g., "all", "1,3,5", "2-4").

        Raises:
            TypeError: If value is not a string.
            ValueError: If value is an empty string.
        """
        StringValidator.validate(value, "pages")
        self._set_attr("pages", value)

    @property
    def show_on_cover(self) -> bool:
        """
        Gets the flag for showing page numbers on the cover page. Default is False.

        Returns:
            bool: Whether to show page numbers on the cover page.
        """
        return self._get_attr("show_on_cover")

    @show_on_cover.setter
    def show_on_cover(self, value: bool) -> None:
        """
        Sets the flag for showing page numbers on the cover page.

        Args:
            value (bool): Must be a boolean.

        Raises:
            TypeError: If value is not a boolean.
        """
        BoolValidator.validate(value, "show_on_cover")
        self._set_attr("show_on_cover", value)
