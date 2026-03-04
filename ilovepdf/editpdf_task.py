"""
Edit PDF Task module for iLovePDF Python SDK.
Provides classes for editing PDF elements (text, image, svg, bottom),
validation, and task management.
"""

from typing import Any, Literal

from .abstract_task_element import AbstractTaskElement
from .file import File
from .helpers import FONT_FAMILY_OPTIONS
from .task import Task
from .validators import ChoiceValidator, FloatValidator, IntValidator, StringValidator

TypeType = Literal["bottom", "text", "image", "svg"]
TYPE_OPTIONS = {"bottom", "text", "image", "svg"}

TextAlignType = Literal["left", "center", "right"]
TEXT_ALIGN_OPTIONS = {"left", "center", "right"}

FontStyleType = Literal["Regular", "Bold", "Italic", "Bold italic"]
FONT_STYLE_OPTIONS = {"Regular", "Bold", "Italic", "Bold italic"}


class Element(AbstractTaskElement):
    """
    Represents an editable PDF element (text, image, svg, or bottom) for the editpdf
    task.

    Attributes:
        type (str): Element type ('bottom', 'text', 'image', 'svg')
        pages (str): Target pages in the PDF (e.g., '1', '1-3', '1,3,5')
        zindex (int): Stack order of the element
        dimensions (dict): Element width and height (keys: 'w', 'h')
        coordinates (dict): Element position (keys: 'x', 'y')
        rotation (int): Element rotation in degrees
        opacity (int): Element opacity (1-100)
        text (str): Text content if type is 'text'
        text_align (str): Alignment for text ('left', 'center', 'right')
        font_family (str): Font family for text
        font_size (int): Size of font for text
        font_style (str): Font style for text
        font_color (str): Font color (hex or 'transparent')
        letter_spacing (int): Space between letters
        underline_text (float): Whether text is underlined
        server_filename (str): Filename (for image/svg)
    """

    _DEFAULT_PAYLOAD = {
        "type": None,
        "pages": None,
        "zindex": None,
        "dimensions": None,
        "coordinates": None,
        "rotation": 0,
        "opacity": 100,
        # Text-specific attributes (only for type "text")
        "text": None,
        "text_align": "left",
        "font_family": "Arial Unicode MS",
        "font_size": 14,
        "font_style": "Regular",
        "font_color": "#000000",
        "letter_spacing": 0,
        "underline_text": None,
        # Attributes specific to type "image" or "svg"
        "server_filename": None,
    }

    REQUIRED_FIELDS = ["type", "pages", "zindex", "dimensions", "coordinates"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.parent: EditPdfTask | None = None
        self.image: File | None = None
        self.svg: File | None = None
        # The parent attribute tracks the EditPdfTask instance containing this element.
        super().__init__(*args, **kwargs)

    @property
    def type(self) -> str | None:
        """
        Element type.
        Returns:
            str: Either 'bottom', 'text', 'image', or 'svg'.
        Raises:
            InvalidChoiceError: If an invalid type is set (see setter).
        """

        return self._get_attr("type")

    @type.setter
    def type(self, value: str) -> None:
        """
        Set the element type.
        Args:
            value (str): Must be one of TYPE_OPTIONS.
        Raises:
            InvalidChoiceError: If value is not a valid option.
        """
        ChoiceValidator.validate(value, TYPE_OPTIONS, "type")
        self._set_attr("type", value)

    @property
    def pages(self) -> str | None:
        """
        Pages where the element will be applied.
        Returns:
            str: Format examples: '1', '1-3', '1,3,5'. Can return None if unset.
        """
        return self._get_attr("pages")

    @pages.setter
    def pages(self, value: str) -> None:
        """
        Assigns the pages where the element will be applied.
        Args:
            value (str): Format examples: '1', '1-3', '1,3,5'.
        Raises:
            TypeError, ValueError: If the value is not a valid string.
        """
        StringValidator.validate(value, "pages")
        self._set_attr("pages", value)

    @property
    def zindex(self) -> int | None:
        """
        Element stacking index (z-index).
        Returns:
            int: Z-index position, can be None if unset.
        """
        return self._get_attr("zindex")

    @zindex.setter
    def zindex(self, value: int) -> None:
        """
        Set stacking index (z-index).
        Args:
            value (int): Z-index position.
        Raises:
            NotAnIntError: If value is not an integer.
        """
        IntValidator.validate_type(value, "zindex")
        self._set_attr("zindex", value)

    @property
    def dimensions(self) -> dict | None:
        """
        Element dimensions.
        Returns:
            dict: Keys 'w' (width, float), 'h' (height, float).
        """
        return self._get_attr("dimensions")

    @dimensions.setter
    def dimensions(self, value: dict) -> None:
        """
        Set element dimensions.
        Args:
            value (dict): {'w': float, 'h': float}
        Raises:
            TypeError, ValueError: If dict is not valid.
        """
        self.validate_object("dimensions", value, key_x="w", key_y="h")
        self._set_attr("dimensions", value)

    @property
    def coordinates(self) -> dict | None:
        """
        Element coordinates (position).
        Returns:
            dict: Keys 'x' (float), 'y' (float).
        """
        return self._get_attr("coordinates")

    @coordinates.setter
    def coordinates(self, value: dict) -> None:
        """
        Set element coordinates (position).
        Args:
            value (dict): {'x': float, 'y': float}
        Raises:
            TypeError, ValueError: If dict is not valid.
        """
        self.validate_object("coordinates", value, key_x="x", key_y="y")
        self._set_attr("coordinates", value)

    @staticmethod
    def validate_object(attr_name: str, value: dict, key_x="x", key_y="y") -> None:
        """
        Validates an object's structure and types for element coordinates or dimensions.
        Args:
            attr_name (str): The attribute name being validated.
            value (dict): Dict containing required keys.
            key_x (str): First required key.
            key_y (str): Second required key.
        Raises:
            TypeError: If value is not a dict or values are not floats.
            ValueError: If required keys are missing.
        """
        if not isinstance(value, dict):
            raise TypeError(f"{attr_name} must be a dictionary.")
        if set(value.keys()) != {key_x, key_y}:
            raise ValueError(f"{attr_name} must have keys '{key_x}' and '{key_y}'.")
        if not isinstance(value[key_x], float) or not isinstance(value[key_y], float):
            raise TypeError(f"{attr_name} values must be floats.")

    @property
    def rotation(self) -> int | None:
        """
        Get the rotation angle of the element in degrees.
        Returns:
            int: Angle between 0 and 360, or None.
        """
        return self._get_attr("rotation")

    @rotation.setter
    def rotation(self, value: int) -> None:
        IntValidator.validate_range(
            value,
            min_value=0,
            max_value=360,
            param_name="rotation",
        )
        self._set_attr("rotation", value)

    @property
    def opacity(self) -> int | None:
        """
        Get the opacity percentage of the element.
        Returns:
            int: Value between 1 and 100, or None.
        """
        return self._get_attr("opacity")

    @opacity.setter
    def opacity(self, value: int) -> None:
        IntValidator.validate_range(
            value,
            min_value=1,
            max_value=100,
            param_name="opacity",
        )
        self._set_attr("opacity", value)

    @property
    def text(self) -> str | None:
        """
        Get the text content of the element.
        Returns:
            str: Text applied if the element type is 'text', or None.
        """
        return self._get_attr("text")

    @text.setter
    def text(self, value: str) -> None:
        StringValidator.validate(value, "text")
        self._set_attr("text", value)

    @property
    def text_align(self) -> str | None:
        """
        Get the text alignment of the element ('left', 'center', 'right').
        Returns:
            str: Alignment if set, or None.
        """
        return self._get_attr("text_align")

    @text_align.setter
    def text_align(self, value: str) -> None:
        ChoiceValidator.validate(value, TEXT_ALIGN_OPTIONS, "text_align")
        self._set_attr("text_align", value)

    @property
    def font_family(self) -> str | None:
        """Get the font family of the text element."""
        return self._get_attr("font_family")

    @font_family.setter
    def font_family(self, value: str) -> None:
        ChoiceValidator.validate(value, FONT_FAMILY_OPTIONS, "font_family")
        self._set_attr("font_family", value)

    @property
    def font_size(self) -> int | None:
        """Get the font size of the text element."""
        return self._get_attr("font_size")

    @font_size.setter
    def font_size(self, value: int) -> None:
        IntValidator.validate_positive(value, "font_size")
        self._set_attr("font_size", value)

    @property
    def font_style(self) -> str | None:
        """Get the font style of the text element."""
        return self._get_attr("font_style")

    @font_style.setter
    def font_style(self, value: str) -> None:
        ChoiceValidator.validate(value, FONT_STYLE_OPTIONS, "font_style")
        self._set_attr("font_style", value)

    @property
    def font_color(self) -> str | None:
        """Get the font color of the text element."""
        return self._get_attr("font_color")

    @font_color.setter
    def font_color(self, value: str) -> None:
        StringValidator.validate(value, "font_color")
        if value != "transparent" and not value.startswith("#"):
            raise ValueError(
                "font_color must be a hexadecimal string or 'transparent'."
            )
        self._set_attr("font_color", value)

    @property
    def letter_spacing(self) -> int | None:
        """Get the letter spacing of the text element."""
        return self._get_attr("letter_spacing")

    @letter_spacing.setter
    def letter_spacing(self, value: int) -> None:
        if value is not None:
            IntValidator.validate_type(value, "letter_spacing")
            if value < 0:
                raise ValueError("letter_spacing must be 0 or greater.")
        self._set_attr("letter_spacing", value)

    @property
    def underline_text(self) -> float | None:
        """
        Get the underline_text value.

        Returns:
            float or None: The underline_text value, which should be a float or None.
        """
        return self._get_attr("underline_text")

    @underline_text.setter
    def underline_text(self, value: Any) -> None:
        """
        Set the underline_text value.

        Args:
            value (float or None): The underline_text value, must be a float between 0.0
                and 1.0, or None.

        Raises:
            TypeError: If value is not a float or None.
            ValueError: If value is not between 0.0 and 1.0.
        """
        FloatValidator.validate_range(
            value, min_value=0.0, max_value=1.0, param_name="underline_text"
        )
        self._set_attr("underline_text", value)

    @property
    def server_filename(self) -> str | None:
        """
        Get the server filename for image or svg elements.
        Returns:
            str: The filename as returned by the API, or None.
        """
        return self._get_attr("server_filename")

    def _to_payload(self):
        """
        Generate API-ready payload for this element.
        Keys irrelevant for each type are omitted based on element type.
        Returns:
            dict: Element payload for API call.
        """
        payload = super()._to_payload()
        # Define keys to exclude based on element type
        text_keys = [
            "text",
            "text_align",
            "font_family",
            "font_size",
            "font_style",
            "font_color",
            "letter_spacing",
            "underline_text",
        ]
        image_keys = ["server_filename"]
        keys_delete = []
        if self.type == "bottom":
            keys_delete = text_keys + image_keys
        elif self.type == "text":
            keys_delete = image_keys
            # StringValidator.validate(payload.get("text"), "text")

            if not payload.get("text"):
                raise ValueError(f"text is required for element type '{self.type}'.")

        elif self.type in ("image", "svg"):
            keys_delete = text_keys
            if not payload.get("server_filename"):
                raise ValueError(
                    f"server_filename is required for element type '{self.type}'."
                )
        for key in keys_delete:
            payload.pop(key, None)
        return payload

    def _upload_image(
        self, file_path: str, extension_list: list[str], **kwargs: Any
    ) -> File:
        """
        Helper method to validate and upload an image file for the element.
        Args:
            file_path (str): Local path to the image file.
            extension_list (list[str]): Allowed file extensions for validation.
            **kwargs: Additional options for validation/upload.
        Returns:
            File: The uploaded file object.
        Raises:
            RuntimeError: If the element has no parent assigned for file upload.
        """
        # IMAGE_FILE_EXTENSIONS
        if self.parent is not None:
            file = self.parent._validate_and_upload_file(
                file_path, extension_list=extension_list, **kwargs
            )
        else:
            raise RuntimeError("Element has no parent assigned.")

        return file

    def set_image(self, file_path: str, **kwargs: Any) -> File:
        """Set the image for this element by uploading a file and assigning it to the
            element.
        Args:
            file_path (str): Local path to the image file.
            **kwargs: Additional options for validation/upload.
        Returns:
            File: The uploaded file object assigned to this element.
        """
        extension_list = ["png", "jpg", "jpeg", "jfif", "gif"]
        if self.type == "svg":
            extension_list = ["svg"]
        file = self._upload_image(file_path, extension_list=extension_list, **kwargs)
        self._set_attr("server_filename", file.server_filename)
        self.image = file
        return file

    def set_svg(self, file_path: str, **kwargs: Any) -> File:
        """Set the SVG for this element by uploading a file and assigning it to the
            element.
        Args:
            file_path (str): Local path to the SVG file.
            **kwargs: Additional options for validation/upload.
        Returns:
            File: The uploaded file object assigned to this element.
        """
        extension_list = ["svg"]
        file = self._upload_image(file_path, extension_list=extension_list, **kwargs)

        self.svg = file
        return file


class EditPdfTask(Task):
    """
    Task that enables detailed editing of PDF files by adding, customizing, or removing
    elements such as text, images, SVGs, and bottom elements.

    Attributes:
        elements (List[Element]): Elements applied to the PDF in this task.
    """

    _tool = "editpdf"

    _DEFAULT_PAYLOAD = {
        "elements": [],
    }
    REQUIRED_FIELDS = ["elements"]

    @property
    def elements(self) -> list[Element]:
        """
        Retrieve the list of Element objects applied to the PDF.
        Returns:
            list[Element]: Current elements.
        """
        return self._get_attr("elements")

    def add_element(self, element: Element | None = None) -> Element:
        """
        Add a new Element to the EditPdfTask.
        Args:
            element (Element | None): Existing Element to add. If None, creates a new
                Element instance.
        Returns:
            Element: The added or newly created element.
        Raises:
            TypeError: If the argument is not an Element.
        """
        element = element or Element()
        if not isinstance(element, Element):
            raise TypeError("element must be an Element object.")
        self.elements.append(element)
        element.parent = self
        return element
