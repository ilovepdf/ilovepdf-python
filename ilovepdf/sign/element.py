"""
This module defines the SignElement class, which serves as a base class for
elements used in the ilovepdf sign feature. It provides methods for setting and
retrieving element properties such as type, position, size, content, and page range.
"""

import json
import re
from typing import Literal

from ilovepdf.abstract_task_element import AbstractTaskElement
from ilovepdf.validators import (
    ChoiceValidator,
    DateValidator,
    FloatValidator,
    IntValidator,
)

TypeXGravityPosition = Literal["left", "center", "right"]
X_GRAVITY_POSITION_OPTIONS = {"left", "center", "right"}

TypeYGravityPosition = Literal["top", "middle", "bottom"]
Y_GRAVITY_POSITION_OPTIONS = {"top", "middle", "bottom"}


ElementType = Literal["initials", "signature", "name", "date", "text", "input"]
ELEMENT_TYPE_OPTIONS = {"initials", "signature", "name", "date", "text", "input"}


# pylint: disable=too-many-instance-attributes
class Element(AbstractTaskElement):
    """Base class for sign elements.

    Handles element properties such as type, position, size, content, and page range.
    """

    _DEFAULT_PAYLOAD = {
        "position": "right bottom",
        "horizontal_position_adjustment": 0,
        "vertical_position_adjustment": 0,
        "pages": "-1",
        "content": None,
        "size": 18,
        "info": None,
        "type": "signature",
    }

    REQUIRED_FIELDS = ["position", "pages", "size"]

    @property
    def position(self):
        """Get the position attribute."""
        return self._get_attr("position")

    def _set_attr_position(self, pos_x, pos_y):
        """Set the position attribute as a string."""
        self._set_attr("position", f"{pos_x} {pos_y}".replace(".", ","))

    def set_gravity_position(
        self,
        position_x: TypeXGravityPosition,
        position_y: TypeYGravityPosition,
        horizontal_position_adjustment: int | None = None,
        vertical_position_adjustment: int | None = None,
    ):
        """
        Set position using gravity (named) positions.

        Args:
            position_x (str): 'left', 'center', or 'right'.
            position_y (str): 'top', 'middle', or 'bottom'.
            horizontal_position_adjustment (int, optional): Adjustment in points.
            vertical_position_adjustment (int, optional): Adjustment in points.
        """
        ChoiceValidator.validate(position_x, X_GRAVITY_POSITION_OPTIONS, "position_x")
        ChoiceValidator.validate(position_y, Y_GRAVITY_POSITION_OPTIONS, "position_y")
        if horizontal_position_adjustment is not None:
            self.horizontal_position_adjustment = horizontal_position_adjustment
        if vertical_position_adjustment is not None:
            self.vertical_position_adjustment = vertical_position_adjustment
        self._set_attr_position(position_x, position_y)

    def set_standard_position(self, position_x: float, position_y: float):
        """
        Set position using absolute coordinates.

        Args:
            position_x (float): X coordinate (0-99999).
            position_y (float): Y coordinate (-99999 to 0).
        """
        FloatValidator.validate_range(
            value=position_x,
            min_value=0,
            max_value=99999,
            param_name="standard_position:position_x",
        )
        FloatValidator.validate_range(
            value=position_y,
            min_value=-99999,
            max_value=0,
            param_name="standard_position:position_y",
        )
        self._set_attr_position(position_x, position_y)

    def _clean_horizontal_position_adjustment(self, value):
        """
        Clean horizontal adjustment based on gravity position.

        Args:
            value (int): Adjustment value.

        Returns:
            int: Cleaned value.
        """
        if self.position:
            pos_x, _ = self.position.split(" ")
            if pos_x == "left" and value < 0:
                value = 0

            elif pos_x == "right" and value > 0:
                value = 0
        return value

    def _clean_vertical_position_adjustment(self, value):
        """
        Clean vertical adjustment based on gravity position.

        Args:
            value (int): Adjustment value.

        Returns:
            int: Cleaned value.
        """
        if self.position:
            _, pos_y = self.position.split(" ")
            if pos_y == "top" and value > 0:
                value = 0

            elif pos_y == "bottom" and value < 0:
                value = 0
        return value

    @property
    def horizontal_position_adjustment(self) -> int:
        """Get the horizontal position adjustment."""
        value = self._get_attr("horizontal_position_adjustment")
        return self._clean_horizontal_position_adjustment(value)

    @horizontal_position_adjustment.setter
    def horizontal_position_adjustment(self, value: int):
        """
        Set the horizontal position adjustment.

        Args:
            value (int): Adjustment value.
        """
        IntValidator.validate_type(value, "horizontal_position_adjustment")
        value = self._clean_horizontal_position_adjustment(value)
        self._set_attr("horizontal_position_adjustment", value)

    @property
    def vertical_position_adjustment(self) -> int:
        """Get the vertical position adjustment."""
        value = self._get_attr("vertical_position_adjustment")
        return self._clean_vertical_position_adjustment(value)

    @vertical_position_adjustment.setter
    def vertical_position_adjustment(self, value: int):
        """
        Set the vertical position adjustment.

        Args:
            value (int): Adjustment value.
        """
        IntValidator.validate_type(value, "vertical_position_adjustment")
        value = self._clean_vertical_position_adjustment(value)
        self._set_attr("vertical_position_adjustment", value)

    @property
    def pages(self) -> str:
        """Get the pages where the element will be placed."""
        return self._get_attr("pages")

    @pages.setter
    def pages(self, pages: str | list[str]):
        """
        Set the pages where the element will be placed.

        Only single negative pages allowed (e.g. '-1'), not in ranges.

        Args:
            pages (str | list[str]): Comma-separated string or list. Must follow
                valid formats: positive int, negative single, or ranges (no
                negatives in ranges).

        Raises:
            ValueError: If format is not allowed or value is not string/list.
        """

        def parse_page(page):
            page = page.strip()
            if re.match(r"^-\d+$", page):
                return page
            if re.match(r"^[1-9]\d*$", page):
                return page
            m = re.match(r"^([1-9]\d*)-([1-9]\d*)$", page)
            if m:
                firstpage = int(m.group(1))
                lastpage = int(m.group(2))
                if lastpage < firstpage:
                    raise ValueError(f"Invalid page range '{page}'")
                return page
            raise ValueError(
                f"Invalid page or page range: '{page}' "
                f"(negatives not allowed in ranges, only as singles)"
            )

        if isinstance(pages, str):
            pages = [p.strip() for p in pages.split(",")]
        pages = list(map(parse_page, pages))
        self._set_attr("pages", ",".join(pages))

    @property
    def type(self) -> ElementType:
        """Get the type of the element. Default is 'signature'."""
        return self._get_attr("type")

    @type.setter
    def type(self, value: ElementType):
        """
        Set the type of the element.

        Args:
            value (ElementType): Must be one of ELEMENT_TYPE_OPTIONS.
                Uses ChoiceValidator for validation.

        Raises:
            ValueError: If value not allowed.
        """
        if value is None:
            value = "signature"
        ChoiceValidator.validate(value, ELEMENT_TYPE_OPTIONS, "type")
        self._set_attr("type", value)

    @property
    def content(self) -> str | None:
        """Get the content for type 'date' or 'text'."""
        if self.type not in ("date", "text"):
            raise TypeError(
                "This property can only be accessed for elements"
                " of type 'date' or 'text'"
            )
        return self._get_attr("content")

    @content.setter
    def content(self, value: str):
        """
        Set content (required if type is 'date' or 'text').

        Args:
            value (str): Content string. If type is 'date', must match allowed date
                format (see DateValidator).

        Raises:
            ValueError: If not str or, for dates, invalid format.
        """
        if self.type not in ("date", "text"):
            raise TypeError(
                "This property can only be set for elements of type 'date' or 'text'"
            )
        if self.type == "date":
            DateValidator.validate_format(value, "content")
        if not isinstance(value, str):
            raise TypeError("content must be a string.")
        self._set_attr("content", value)

    @property
    def size(self) -> int:
        """Get the size of the element (height in points)."""
        return self._get_attr("size")

    @size.setter
    def size(self, value: int):
        """
        Set the height size for the element.

        Args:
            value (int): Must be positive integer.

        Raises:
            ValueError: If negative or not int.
        """
        IntValidator.validate_positive(value, "size")
        self._set_attr("size", value)

    @property
    def info(self) -> str | None:
        """Get the info JSON string for type 'input'."""
        if self.type != "input":
            raise TypeError(
                "This property can only be accessed for elements of type 'input'."
            )
        return self._get_attr("info")

    @info.setter
    def info(self, value: str):
        """
        Set the info attribute for input elements; must be a JSON string.

        Args:
            value (str): Must be a valid JSON string. Only allowed for elements of type
                'input'.

        Raises:
            TypeError: If type is not 'input' or value is not a string.
            ValueError: If value is not a valid JSON string.
        """
        if self.type != "input":
            raise TypeError(
                "This property can only be set for elements of type 'input'."
            )
        if not isinstance(value, str):
            raise TypeError("info must be a string containing JSON.")
        try:
            json.loads(value)
        except Exception as exc:
            raise ValueError("info must be a valid JSON string.") from exc
        self._set_attr("info", value)
